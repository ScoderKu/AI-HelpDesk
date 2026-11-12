# Security and deployment considerations

## 1. Purpose and scope

This document describes the security posture and deployment boundaries of the AI HelpDesk student project. It distinguishes controls present in the repository from recommendations for a future LAN or WAN deployment. It is not a penetration-test report, security certification, or claim of full OWASP compliance.

The school-project scope remains a self-service helpdesk: user registration and login, profile management, personal conversations, AI-assisted support, and user-owned tickets. No administrator, support-agent, or role-based privileged access model is introduced here.

## 2. Deployment profiles

| Profile | Intended use | Security position |
|---|---|---|
| Local development/demo | Developer machine and classroom demonstration | Current Compose configuration is intended for local development. Frontend uses the Vite development server. HTTP requires `AUTH_COOKIE_SECURE=false`; do not reuse that setting for HTTPS. |
| Private LAN | Future access from trusted devices on a private network | Not a supported production deployment yet. Requires a production frontend build, HTTPS reverse proxy, trusted-proxy validation, firewall rules, and device/network controls. |
| Public WAN | Internet-accessible deployment | Not supported or security-validated. Requires a separate production deployment review, hardened edge infrastructure, monitoring, backup/restore, incident response, and ongoing patching. |

Do not expose the development server or management interfaces directly to the Internet.

## 3. Existing application controls

The following controls are implemented in the application source on the security-hardening branch; they must still pass the project's automated and manual regression tests before being described as verified at runtime.

- Server-side sessions are stored in MySQL. The browser receives an HMAC-signed session cookie with an eight-hour absolute lifetime, `HttpOnly`, `SameSite=Lax`, and configurable `Secure`.
- Passwords are stored using scrypt with per-password random salts. Existing parameters are retained to preserve compatibility with current password hashes.
- Login attempts are limited by client IP and normalized account identifier through Redis.
- Registration attempts are limited by client IP through Redis; Redis failure rejects registration rather than silently disabling the control.
- Unsafe API requests carrying the session cookie are checked against the exact configured frontend-origin allowlist. Login and registration are excluded because they do not use an authenticated session cookie.
- AI generation is serialized through a Redis-backed global lease shared by chat and ticket-draft generation. When capacity is occupied, the API returns a retryable response rather than allowing concurrent requests to overload the local model.
- Private versioned API responses receive `Cache-Control: no-store`.
- API responses receive baseline browser security headers: `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and a restrictive `Permissions-Policy`.
- CORS is restricted to the configured frontend origins and the methods/headers used by the application.
- Ticket and conversation access is scoped to the authenticated owner in database queries. Automated two-account IDOR regression coverage should be maintained for every resource route.

## 4. Local Compose network boundaries

The current Compose file binds frontend, backend, phpMyAdmin, and Ollama host ports to loopback (127.0.0.1). MySQL and Redis do not publish host ports. This is appropriate for a single-machine local demo, not a substitute for a LAN/WAN edge architecture.

Keep MySQL, Redis, and Ollama on internal Docker networks. Do not publish their ports to a LAN or WAN interface. phpMyAdmin is a database-management surface: keep it disabled outside local development or restrict it to a dedicated management host/network with HTTPS and strong access controls.

The backend trusts forwarded client-IP information only from explicitly configured proxy addresses/CIDRs. Never add a broad or user-controlled network range to `TRUSTED_PROXY_IPS`. Ensure the actual reverse-proxy source address matches the configured value and that the proxy overwrites, rather than blindly appends to, forwarded headers.

## 5. Requirements before LAN deployment

Before enabling access from other devices:

1. Build and serve the frontend as static production assets; do not run the Vite development server.
2. Put a maintained reverse proxy in front of the application and enforce HTTPS with a valid certificate.
3. Set `AUTH_COOKIE_SECURE=true` and configure `FRONTEND_ORIGINS` with the exact HTTPS origin(s), including scheme and port where applicable.
4. Set `TRUSTED_PROXY_IPS` to the exact proxy address/CIDR and verify client-IP forwarding from a second LAN device.
5. Bind the public-facing listener only to the intended LAN interface; firewall all other inbound ports.
6. Keep MySQL, Redis, Ollama, and phpMyAdmin inaccessible from client devices.
7. Use unique high-entropy secrets and database credentials; keep `.env` out of version control and rotate any credentials that may have been exposed.
8. Test login, logout, registration throttling, cross-origin requests, session expiry, password changes, ticket ownership, conversation ownership, and AI overload behavior from separate devices.

These are deployment requirements, not claims that LAN deployment has already been tested.

## 6. Additional requirements before WAN deployment

WAN exposure requires a separate threat model and deployment review. At minimum:

- Use a production-grade reverse proxy/WAF where appropriate, TLS configuration, request-size and connection limits, and strict inbound firewall rules.
- Expose only the HTTPS application entry point. Never expose MySQL, Redis, Ollama, phpMyAdmin, Docker socket, or internal service ports.
- Disable interactive API documentation and schema endpoints in production unless there is a documented operational need and access restriction.
- Run containers with least privilege, non-root users where supported, read-only filesystems where practical, dropped Linux capabilities, and resource limits.
- Pin production image versions/digests and lock Python/JavaScript dependencies; establish a patch/update process.
- Add centralized log collection, security-event monitoring, alerting, privacy-aware retention, and an incident-response procedure. Do not log passwords, session cookies, authorization headers, or full private conversations unnecessarily.
- Back up MySQL securely, encrypt backups, restrict access, and regularly test restoration.
- Define account abuse controls, availability targets, recovery objectives, and an operational owner.
- Perform an independent security assessment and verify all authorization/IDOR paths, CSRF behavior, rate limits, denial-of-service controls, and secret handling.

## 7. Known limitations and verification backlog

The following are not established as complete merely because the controls above exist:

- End-to-end LAN testing with two physical devices and the intended reverse proxy.
- A full two-user IDOR test matrix for every ticket, conversation, message, and retry endpoint.
- Production container non-root execution, read-only filesystem, capability dropping, and resource limits.
- Fully pinned images and reproducible dependency lockfiles.
- Production disablement of OpenAPI/Redoc/schema endpoints.
- A complete Content Security Policy compatible with the final production frontend.
- Request-body limits at both reverse proxy and ASGI layers.
- Load testing of the AI lease, queue/overload response, client disconnect behavior, and Ollama timeout behavior.
- Security log review, backup restoration drill, and incident-response exercise.
- Formal penetration testing or independent verification.

## 8. Security reference

Use OWASP ASVS 5.0.0 as a verification checklist when the project is expanded or deployed beyond a classroom demo: https://owasp.org/www-project-application-security-verification-standard/ and https://asvs.owasp.org/.

ASVS is a reference framework here, not a certification claim. Select applicable requirements based on the actual deployment threat model; do not claim Level 2 compliance without completing and evidencing the relevant verification activities.
