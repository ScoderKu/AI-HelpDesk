# AI HelpDesk — Known Troubleshooting Cases and Investigation History

- **Document ID:** KB-PROJECT-08
- **Status:** historical cases from implementation sessions; current state must be rechecked before applying a fix
- **RAG Scope:** project-specific
- **Applies to:** Docker, MySQL, FastAPI, Ollama, frontend build and local inference
- **Keywords:** troubleshooting, incident, root cause, SQLAlchemy URL, password hash symbol, MySQL connection, npm ci, package-lock, Ollama model init, GPU slow inference, virhe, korjaus, debuggaus

## How to use this document

These are cases encountered while developing this project. A historical fix is not automatically the correct fix for a new failure. Compare the current error, configuration and source code before repeating a change.

## Case 1 — MySQL password contained a reserved URL character

**Symptom:** the backend could not establish its SQLAlchemy MySQL connection when the configured database password contained a `#` character.

**Cause:** manually composing a database URL as a string can misinterpret reserved URL characters in credentials.

**Fix used:** `backend/app/database.py` was changed to construct the URL with SQLAlchemy `URL.create()`, passing driver, username, password, host, port and database as separate values.

**Verification reported during the session:** direct `SELECT 1` returned `1`; the backend database health endpoint `GET /api/health/db` returned an OK status.

**General lesson:** use a structured URL builder rather than manually concatenating credentials. Do not log the full connection URL because it may contain a password.

## Case 2 — Frontend Docker build failed at `npm ci`

**Symptom:** the frontend image build failed because the Dockerfile ran `npm ci` while the expected `package-lock.json` was absent.

**Cause:** `npm ci` requires a lock file and does not create one.

**Correct workflow:** from the frontend directory, run `npm install` using the intended Node/npm toolchain to generate or update `package-lock.json`; inspect and commit the lock file; then run `npm ci` in the clean build.

**Important:** this records the historical failure and the npm behavior. It does not assert that the current repository still lacks a lock file. Check the current branch and Dockerfile before changing anything.

## Case 3 — Ollama model initialization container exited with code 1

**Symptom:** the `ollama-model-init` service initially exited with a non-zero code during Compose startup.

**Outcome:** the project owner later confirmed that model initialization completed successfully and the init service exited with code 0.

**Investigation guidance:** inspect the exact init service command, container entrypoint, health dependency, mounted Modelfile and GGUF path. A container image's own entrypoint may interpret a supplied command as arguments rather than as a shell command. Do not assume this was the root cause of the historical failure unless logs prove it.

**Verification:** use the current Compose service name, inspect its logs and exit code, then check `ollama list` inside the Ollama service.

## Case 4 — Backend database creation/connection confusion

**Symptom:** during early container testing, running only the backend led to a report that the database had not been created.

**Resolution path:** the project was moved toward running the complete Compose environment, then the SQLAlchemy URL construction issue was fixed as described in Case 1.

**Lesson:** distinguish among (a) MySQL server not running, (b) database/schema not initialized, (c) tables absent, and (d) backend credentials/network connection failing. These are different failure classes. Check MySQL health, database name, migrations, tables and backend connection separately.

## Case 5 — Ollama inference slow while GPU utilization is high

**Observation:** the project owner reported that the selected 8B Q4 model/API could show 100% GPU utilization while generating slowly on the development PC.

**Status:** unresolved performance investigation in the historical session. High GPU utilization alone does not identify the bottleneck and does not prove all model layers are resident in VRAM.

**Investigate before changing the model:**
1. Record prompt length and generated token count.
2. Measure time to first token and steady-state tokens per second separately.
3. Inspect Ollama model/process information and GPU memory usage.
4. Check whether model layers are offloaded to system RAM/CPU.
5. Check context length, concurrency and other GPU processes.
6. Compare a short prompt with a long conversation context.
7. Change one variable at a time and preserve the known-good configuration.

Do not claim this issue is fixed or recommend a model replacement without measurements.

## Reporting format for future incidents

Record:
- exact error text and timestamp;
- affected service/container and current branch/commit;
- reproduction steps;
- relevant redacted configuration (never secrets);
- root cause, if proven;
- code/configuration change;
- verification command and observed result;
- whether the fix is confirmed, provisional or unresolved.

## Tiivistelmä suomeksi

Tämä dokumentti kokoaa kehityksen aikana havaittuja historiallisia ongelmia. Esimerkkejä ovat MySQL-yhteysosoitteen erikoismerkki salasanassa, puuttuva package-lock.json npm ci -asennuksessa ja Ollaman mallin alustus. Historiallinen korjaus ei ole automaattisesti oikea uuteen tilanteeseen. Vertaa aina tarkkaa virheilmoitusta, nykyistä asetusta ja ohjelmistoversiota ennen muutosta. GPU:n suuri käyttöaste ei yksin todista hidastumisen syytä.
