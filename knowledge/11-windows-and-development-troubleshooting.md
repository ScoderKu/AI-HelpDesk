# Windows 11 and Local Development Troubleshooting

- **Document ID:** KB-OPS-11
- **Status:** general Windows/PowerShell guidance; project-specific commands are identified separately
- **Applies to:** Windows 11 development workstation, PowerShell, Docker Desktop, Node.js
- **Keywords:** Windows 11, PowerShell, PATH, environment variable, port, process, Docker Desktop, terminal, troubleshooting, Windows-ongelma, komentokehote

## PowerShell versus Command Prompt

PowerShell and cmd.exe have different syntax. A command copied from Bash/Linux may not work unchanged in PowerShell. Use PowerShell syntax when the user's prompt is PowerShell.

Examples:
```powershell
Get-Location
Get-ChildItem
Test-Path .env
Copy-Item .env.example .env
$env:NAME = "value"
```

## PATH and executable not found

If PowerShell reports that a command is not recognized:
1. Check whether the program is installed.
2. Run `Get-Command node` or `where.exe node`.
3. Inspect PATH with `$env:Path -split ';'`.
4. Reopen the terminal after installation or PATH changes.
5. Confirm the expected version with `node --version` or the relevant version command.

Do not assume that installing a VS Code extension installs a system-wide runtime. The executable used by a terminal depends on the environment and PATH.

## Port already in use

To identify a process listening on a port:
```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen |
  Select-Object LocalAddress, LocalPort, OwningProcess
Get-Process -Id <PID>
```
Do not terminate a process until its purpose is understood. A port can be used by another development server or Docker port mapping.

## Docker Desktop

If Compose cannot connect to the Docker daemon:
- confirm Docker Desktop is running;
- check that the intended Linux container engine is active;
- run `docker version` and `docker compose version`;
- inspect `docker compose ps` from the project directory.

## Environment files

The repository uses a local `.env` file for secrets and configuration. The README documents copying `.env.example` when `.env` does not exist. Do not paste the contents of `.env` into a chat, issue, screenshot or commit. Share variable names and redacted values only.

## Project startup checks

From the repository root:
```powershell
docker compose ps
docker compose logs --tail=100 backend
docker compose logs --tail=100 mysql
docker compose logs --tail=100 redis
docker compose logs --tail=100 ollama
```
If a Compose service name differs, inspect the current Compose file and use the exact service key.

## Safe troubleshooting sequence

Start with read-only inspection. Avoid destructive commands such as removing Docker volumes, deleting database files, resetting Git history or reinstalling all dependencies until the cause is understood and important data is backed up.


## Tiivistelmä suomeksi

PowerShell ja komentokehote eivät käytä kaikilta osin samaa syntaksia kuin Bash. Tarkista ensin nykyinen hakemisto, PATH, ympäristömuuttujat, prosessit ja portit. Jos komentoa ei löydy, selvitä onko ohjelma asennettu ja PATH päivitetty; älä muuta järjestelmäasetuksia summittaisesti. Docker Desktopin, Node.js:n ja muiden kehitystyökalujen ongelmat kannattaa rajata komentoon, palveluun ja käyttöjärjestelmään.
