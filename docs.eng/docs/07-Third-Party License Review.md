# AI HelpDesk — Third-Party License Review

**Review date:** 05.11.2026  
**Status:** Preliminary inventory completed; release compliance actions remain open.  
**Scope:** Repository manifests, current local Compose image versions, the locally present GGUF file, and upstream license information. This is a technical inventory, not a legal opinion.

## Findings

| Component | Observed license / terms | Review result |
|---|---|---|
| AI model `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf` | The LumiOpen Poro 2 8B Instruct model card and the matching mradermacher GGUF repository identify the Llama 3.3 Community License. The model file exists locally (4,920,739,552 bytes) but is ignored by Git, so its exact download revision and checksum are not recorded. | The license is conditional, not an unrestricted OSI license. If distributing Llama materials or a product containing them, the agreement requires providing the license, displaying “Built with Llama”, retaining the required attribution notice, and following the Acceptable Use Policy. The agreement also has a separate-license threshold above 700 million monthly active users. Record the exact GGUF source/revision and checksum, include required notices for the delivery form, and have the project owner confirm intended use. See the [Poro model card](https://huggingface.co/LumiOpen/Llama-Poro-2-8B-Instruct), [GGUF repository](https://huggingface.co/mradermacher/Llama-Poro-2-8B-Instruct-GGUF), [Meta license](https://dev.meta.ai/llama/llama3_3/license), and [Acceptable Use Policy](https://dev.meta.ai/llama/llama3_3/use-policy). |
| Ollama | Upstream repository license is MIT. | Keep the copyright and permission notice when redistributing Ollama software. The Compose image uses the mutable `ollama/ollama:latest` tag; its exact image digest and bundled third-party notices were not inventoried. See [Ollama LICENSE](https://github.com/ollama/ollama/blob/main/LICENSE). |
| Redis server | Running image reports Redis 7.4.12 (`redis:7-alpine`). Redis 7.4.x is dual licensed under RSALv2 or SSPLv1, not the BSD license used by Redis 7.2 and earlier. | Select and document the applicable license and confirm that the intended deployment model fits its terms. The floating `7-alpine` tag may move to another 7.x release. See [Redis license overview](https://redis.io/legal/licenses/). |
| Python direct dependencies | `requirements.txt` declares seven dependencies with version ranges but no lockfile. The running backend resolves FastAPI 0.162.0, Uvicorn 0.54.0, SQLAlchemy 2.1.6, Alembic 1.20.1, PyMySQL 1.2.3, pydantic-settings 2.16.2, and redis-py 6.4.0. Their upstream project licenses are permissive MIT/BSD-family licenses. | The dependency ranges can resolve to different versions later. Transitive dependencies are not fully pinned or represented in a project lock/SBOM; preserve notices and generate a versioned inventory for the release. |
| Frontend npm dependencies | `package-lock.json` contains 90 package entries and records a license for every entry: 54 MIT, 22 Apache-2.0, 12 MPL-2.0, one ISC, and one BSD-3-Clause. The MPL-2.0 entries are Lightning CSS and its platform packages. | Keep the lockfile and applicable notices. Review MPL-2.0 notice/source obligations if those files are modified or redistributed as part of the frontend build. |
| Container images and system packages | The current Compose stack uses MySQL 8.4.13 (Community Server, GPL), phpMyAdmin `5`, `python:3.12-slim`, `node:22-alpine`, and `nginx:alpine`. The application base-image tags are not pinned by digest. | The image-level and OS-package-level notices were not exhaustively inventoried. Record image digests and generate an SBOM/license report for the exact release images. |
| AI HelpDesk project | The README says the project license has not been defined; no root `LICENSE` file was found. | Choose a project license before distribution and ensure it does not claim rights over third-party model materials. |

## Actions before distribution

1. Decide and document the AI HelpDesk project license.
2. Record the GGUF download URL/revision and SHA-256; include the applicable Llama 3.3 agreement/attribution and “Built with Llama” notice for the chosen delivery form, and review the Acceptable Use Policy.
3. Confirm whether Redis 7.4.12 under RSALv2 or SSPLv1 fits the project’s intended use; document the selected terms and pin the Redis image version/digest.
4. Add a Python dependency lockfile and generate an SBOM/license inventory for the Python environment and all final container images.
5. Retain third-party notices for npm packages and container images; pin image digests so the reviewed set does not silently change.

## Evidence gathered

- `frontend/package-lock.json` was parsed: all 90 package records declare a license.
- The running Compose stack reported MySQL 8.4.13, Redis 7.4.12, and `ollama/ollama:latest`.
- The GGUF is present in the local `ollama/models/` directory but ignored by Git; repository history does not establish its exact source revision or checksum.
- Backend auth integration was separately exercised against the local Compose MySQL database; this is recorded in the project management log and does not certify the target-site environment.
