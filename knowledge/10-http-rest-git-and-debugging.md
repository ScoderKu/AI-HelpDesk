# HTTP, REST, Git and Technical Debugging

- **Document ID:** KB-TECH-10
- **Status:** general technical guidance; API examples align with AI HelpDesk conventions
- **Applies to:** browser-to-backend communication and repository workflow
- **Keywords:** HTTP, REST, JSON, status code, cookie, CORS, Origin, Git, GitHub, branch, commit, pull request, debugging, virhekoodi, versionhallinta

## HTTP basics

HTTP is a request/response protocol. A request includes a method, target URL, headers and sometimes a body. A response includes a status code, headers and sometimes a body.

Common methods:
- GET reads a resource.
- POST submits data or requests an operation, often creating a resource.
- PATCH partially updates a resource.
- PUT replaces a resource representation.
- DELETE requests resource deletion.

Common status codes:
- 200 OK — request succeeded.
- 201 Created — resource created.
- 204 No Content — succeeded with no response body.
- 400 Bad Request — request cannot be processed as submitted.
- 401 Unauthorized — authentication is missing or invalid.
- 403 Forbidden — request is understood but not permitted.
- 404 Not Found — resource is absent or intentionally hidden.
- 409 Conflict — state conflict, duplicate or concurrency conflict.
- 422 Unprocessable Content — validation failed.
- 429 Too Many Requests — rate limit exceeded.
- 500 Internal Server Error — unexpected server failure.
- 503 Service Unavailable — dependency/service temporarily unavailable.

## REST and JSON

REST-style APIs expose resources through URLs and use HTTP methods to describe operations. JSON is a common data representation. A client must not assume a successful HTTP status unless it checks `response.ok` or the status code.

A request with cookies may need `credentials: 'include'` in browser fetch. The server must set appropriate cookie, CORS and Origin policies. CORS errors are enforced by browsers; they do not mean the backend route itself is necessarily unavailable.

## Debugging a failed API call

1. Open browser developer tools → Network.
2. Select the failed request.
3. Inspect request URL, method, status, Origin, cookie presence and payload shape.
4. Inspect response body for a safe validation/error detail.
5. Check backend logs for the same request time.
6. Check the relevant dependency (MySQL, Redis or Ollama).
7. Reproduce with a minimal request using Swagger or an HTTP client.
8. Change one cause at a time and retest.

Never share session cookies, Authorization headers, passwords or tokens in screenshots or logs.

## Git workflow

Git tracks source history. A branch isolates a change. A commit records a coherent snapshot. A pull request (PR) presents changes for review and merging.

A safe feature workflow:
```powershell
git status
git switch main
git pull
git switch -c feature/short-description
# edit and test
git diff
git status
git add <specific-files>
git commit -m "feat: describe the change"
git push -u origin feature/short-description
```
Do not commit `.env`, credentials, local databases, model weights or generated secrets. Review `git diff` before committing.

Do not force-push shared branches unless explicitly coordinated. Do not merge a PR without the project owner's approval when approval is required.

## Useful Git diagnostics

- `git status` — working tree and branch state.
- `git log --oneline --decorate -10` — recent commit history.
- `git diff` — unstaged changes.
- `git diff --cached` — staged changes.
- `git branch --show-current` — current branch.
- `git remote -v` — configured remotes.

## Root-cause discipline

Distinguish symptom, cause, fix and verification. A command that exits zero is evidence only for that command; it does not prove the entire application works. Record exact error text, affected service, reproduction steps, change made and the test that confirms the fix.
