# MySQL, Redis and Data Lifecycle

- **Document ID:** KB-TECH-09
- **Status:** general guidance plus verified AI HelpDesk backend behavior
- **Applies to:** MySQL, SQLAlchemy models, Alembic, Redis
- **Keywords:** MySQL, SQL, relational database, foreign key, index, transaction, Redis, TTL, cache, lock, retention, tietokanta, välimuisti, istunnon vanheneminen

## MySQL as the system of record

MySQL stores durable application records. A relational database organizes data into tables, rows and columns. Primary keys identify rows; foreign keys enforce relationships between tables; unique constraints prevent duplicate values; indexes improve lookup performance but add write/storage cost.

Use parameterized SQL or SQLAlchemy expressions. Never build SQL by concatenating untrusted user input.

## Transactions

A transaction groups database operations into an atomic unit. Commit makes changes durable; rollback discards uncommitted changes. Keep transactions short and avoid holding row locks while waiting for a slow AI response or network request.

Deadlocks can occur when concurrent transactions acquire locks in incompatible orders. Investigate the involved SQL statements and transaction boundaries; do not treat retrying blindly as a complete fix.

## SQLAlchemy and migrations

The project maps database tables through SQLAlchemy ORM models. Alembic migration files are the versioned history of schema changes. The database schema is defined by both model code and migrations; review both before documenting a column or relationship.

A backup is required before risky schema/data changes. Do not delete volumes or tables to fix a connection error.

## Redis in this application

Redis is used for ephemeral coordination, not durable business records:
- login rate-limit counters with expiry;
- per-conversation AI generation locks with expiry and token-checked renewal/release.

A Redis TTL is a time-to-live: the key expires automatically after its configured lifetime. Expiry is useful for cleanup if a process crashes, but a lock should also verify ownership before renewal or release. The project's chat lock uses a random token and Lua scripts to ensure only the holder with the matching token can renew or release it.

Redis failure has functional consequences: login rate limiting or chat lock verification may fail and the backend can return a service-unavailable response. Do not silently bypass security controls when Redis is down.

## Data retention

The reviewed backend runs a daily retention task. It permanently deletes tickets that are CLOSED and whose `closed_at` is at least three calendar months old. It also deletes conversations inactive for at least three calendar months based on `updated_at`, except when linked to a ticket that must still be retained (for example, an OPEN ticket or a ticket not yet past its retention cutoff).

This is permanent deletion, not soft delete or archive. Conversation messages are removed with their conversation according to the schema's delete relationship. Make a backup if data must be preserved.

## Useful SQL diagnostics

Use read-only queries first:
```sql
SELECT DATABASE();
SELECT 1;
SHOW TABLES;
SHOW CREATE TABLE users;
```
Do not paste real user data, password hashes, session tokens or personal information into AI chat or Knowledge Base documents.
