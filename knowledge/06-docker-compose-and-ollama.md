# Docker Compose and Ollama — AI HelpDesk Operations

- **Document ID:** KB-OPS-06
- **Status:** project setup verified from README and Modelfile; exact service names must be checked in current Compose configuration
- **RAG Scope:** project-specific
- **Applies to:** Windows 11 Docker development environment, Compose services, Ollama
- **Keywords:** Docker, Docker Compose, container, image, volume, network, healthcheck, Ollama, GGUF, Modelfile, GPU, kontti, käyttöönotto, mallin lataus

## Container fundamentals

A Docker image is a packaged template; a container is a running instance of an image. A volume persists data beyond the lifetime of an individual container. A Compose service defines how a container is built/run and connected to other services.

Container-local `localhost` refers to the same container. To reach MySQL or Ollama from the backend container, use the Compose service hostname or network alias configured for that environment.

## Project startup

The README documents this startup sequence from the repository root:
```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
docker compose up --build
```
Set database credentials and a random `JWT_SECRET_KEY` of at least 32 characters in the local `.env`. Do not commit `.env`.

The README describes the frontend, backend, MySQL, Redis and Ollama services. It also describes a one-time `ollama-model-init` service that waits for Ollama health, checks for `poro-helpdesk`, and creates it from the Modelfile if absent.

## Ollama model

The model artifact is:
`ollama/models/Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`

The Modelfile uses:
```
FROM /models/models/Llama-Poro-2-8B-Instruct.Q4_K_M.gguf
PARAMETER num_ctx 4096
PARAMETER temperature 0.2
```
The Ollama model name used by the backend defaults to `poro-helpdesk`. The model is stored in a persistent Ollama data volume. The README says the backend preloads the model at startup and asks Ollama to keep it loaded for 24 hours while idle.

Useful checks:
```powershell
docker compose ps
docker compose logs --tail=100 ollama
docker compose logs --tail=100 backend
docker compose exec ollama ollama list
docker compose exec ollama ollama ps
```
Use service names from the current Compose file if they differ.

## Health versus readiness

A container may be running while its service is not ready. Check health checks and application-level behavior. Ollama being reachable does not prove the intended model exists; `ollama list` checks available models and `ollama ps` checks models currently loaded.

## Common failure patterns

### Model file not found
Check the host path, bind mount, container path and file name. The Modelfile's `FROM` path must exist inside the Ollama container, not merely on Windows.

### Model initialization exits non-zero
Inspect the init service logs and its entrypoint/command. If a container image has its own entrypoint, a shell command may be interpreted as an argument to that entrypoint. Confirm the effective entrypoint and command rather than repeatedly changing YAML at random.

### Backend cannot reach Ollama
From inside the backend container, verify the configured Ollama base URL uses the Compose service hostname and port. Do not use `localhost:11434` unless Ollama runs in the same container or host networking is intentionally configured.

### Slow inference or memory pressure
Model inference depends on model size/quantization, context length, prompt size, GPU/VRAM, system RAM, CPU, GPU offload and concurrent requests. 100% GPU utilization alone does not prove that every model layer is resident in VRAM or that the bottleneck is GPU compute. Inspect Ollama logs/metrics and model residency before changing quantization or hardware assumptions.

### Data loss warning
`docker compose down -v` removes named volumes. It can delete MySQL and Ollama persistent data. Do not use it as a casual troubleshooting step. Prefer `docker compose down` and targeted rebuild/restart commands unless a full data reset is explicitly intended and backed up.


## Tiivistelmä suomeksi

Docker-kuva on sovelluksen paketoitu malli ja kontti sen käynnissä oleva instanssi. Compose määrittelee palvelut, verkot, volyymit ja käynnistysriippuvuudet. Kontin localhost tarkoittaa kyseistä konttia, ei toista palvelua. Palveluiden välisessä yhteydessä käytetään Compose-palvelun DNS-nimeä. Ollaman mallidata tarvitsee pysyvän volyymin. Terveystarkistus kertoo palvelun tilasta, mutta sovellustason yhteys pitää testata erillisellä pyynnöllä.
