import base64
import binascii
import hmac
import hashlib
import os


SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_DKLEN = 64


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    derived_key = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=SCRYPT_DKLEN,
        maxmem=64 * 1024 * 1024,
    )
    encoded_salt = base64.urlsafe_b64encode(salt).decode("ascii").rstrip("=")
    encoded_key = base64.urlsafe_b64encode(derived_key).decode("ascii").rstrip("=")
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${encoded_salt}${encoded_key}"


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        algorithm, n, r, p, encoded_salt, encoded_key = encoded_hash.split("$")
        if (
            algorithm != "scrypt"
            or int(n) != SCRYPT_N
            or int(r) != SCRYPT_R
            or int(p) != SCRYPT_P
        ):
            return False

        salt = base64.urlsafe_b64decode(
            encoded_salt + "=" * (-len(encoded_salt) % 4)
        )
        expected_key = base64.urlsafe_b64decode(
            encoded_key + "=" * (-len(encoded_key) % 4)
        )
        if len(salt) != 16 or len(expected_key) != SCRYPT_DKLEN:
            return False

        derived_key = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=SCRYPT_N,
            r=SCRYPT_R,
            p=SCRYPT_P,
            dklen=SCRYPT_DKLEN,
            maxmem=64 * 1024 * 1024,
        )
    except (ValueError, TypeError, binascii.Error):
        return False

    return hmac.compare_digest(derived_key, expected_key)
