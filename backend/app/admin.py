"""Protected maintenance commands for AI HelpDesk administration.

Run from the backend environment:
    python -m app.admin reset-password --email user@example.com

The temporary password is printed only after the database transaction commits.
Protect terminal output and deliver the password to the verified user out of band.
"""
import argparse
import secrets
import sys
from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal
from app.models import AuthSession, User
from app.security import hash_password


def reset_password(email: str) -> str:
    normalized_email = email.strip().lower()
    if not normalized_email or "@" not in normalized_email:
        raise ValueError("A valid target email address is required.")

    temporary_password = secrets.token_urlsafe(18)
    db = SessionLocal()
    try:
        user = db.scalar(
            select(User)
            .where(User.email == normalized_email)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        if user is None:
            raise LookupError("No user account matches the supplied email address.")

        user.password_hash = hash_password(temporary_password)
        user.must_change_password = True
        user.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.execute(delete(AuthSession).where(AuthSession.user_id == user.id))
        db.commit()
        return temporary_password
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="AI HelpDesk backend maintenance")
    subparsers = parser.add_subparsers(dest="command", required=True)
    reset_parser = subparsers.add_parser(
        "reset-password",
        help="Reset a user's password and require a change at next sign-in",
    )
    reset_parser.add_argument("--email", required=True, help="Target user's email")
    args = parser.parse_args()

    try:
        temporary_password = reset_password(args.email)
    except LookupError as error:
        print(str(error), file=sys.stderr)
        return 1
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    except SQLAlchemyError:
        # Deliberately do not print exception details: database diagnostics may
        # contain sensitive connection or query information.
        print("Password reset failed because of a database error.", file=sys.stderr)
        return 1
    except Exception:
        print("Password reset failed.", file=sys.stderr)
        return 1

    print("Password reset completed. Deliver this temporary password securely:")
    print(temporary_password)
    print("The user must change it immediately after signing in.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
