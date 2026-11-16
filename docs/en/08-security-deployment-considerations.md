# Security and deployment considerations

## 1. Purpose and scope

This document summarizes the AI HelpDesk student project's security posture and deployment boundaries. It separates controls present in the source from recommendations for future LAN/WAN deployment. It is not a penetration-test report, security certification, or claim of full OWASP compliance.

The project remains a self-service helpdesk: user accounts, login, profile management, personal conversations, AI-assisted guidance, and user-owned tickets. No administrator, support-agent, or role-based privileged access model is added.

## 2. Deployment profiles

| Environment | Intended use | Security status |
|---|---|---|
| Local development/demo | Developer machine and classroom demonstration | The current Compose setup is for development. The frontend uses Vite's development server. Local HTTP requires `AUTH_COOKIE_SECURE=false`; never reuse this setting for HTTPS. |
| Private LAN | Future access from trusted local devices | Not yet a supported or validated production deployment. Requires a production frontend build, HTTPS reverse proxy, trusted-proxy validation, firewall rules, and device/network controls. |
| Public WAN | Internet-facing service | Not supported or security-validated. Requires a separate production review, hardened edge infrastructure, monitoring, backups, recovery procedures, and ongoing patching. |

Do not expose the development server or management interfaces directly to the Internet.

## 3. Application security controls

- Server-side sessions are stored in MySQL. The browser session cookie is HMAC-signed, has an eight-hour absolute lifetime, and uses `HttpOnly` and `SameSite=Lax`; `Secure` is configurable.
- Passwords are stored as scrypt hashes with per-password random salts. Existing parameters are retained to preserve compatibility with existing hashes.
- Redis-based login throttling uses the client IP and normalized account identifier.
- Registration attempts are limited by client IP (5 attempts per hour). If Redis fails, registration is rejected rather than allowing the limit to be bypassed.
- Unsafe API requests carrying the session cookie are checked against the exact frontend-origin allowlist. Login and registration are excluded from this session-based check.
- AI generation is serialized through a Redis-backed global lock shared by chat and ticket-draft generation. When capacity is occupied, the API returns a retryable response instead of allowing concurrent model generations.
- Private versioned API responses receive `Cache-Control: no-store`.
- API responses receive baseline browser security headers: `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and a restrictive `Permissions-Policy`.
- CORS is restricted to configured frontend origins and the methods and headers required by the application.
- Ticket and conversation database queries are scoped to the authenticated owner. Two-user IDOR regression tests should be maintained for every resource endpoint.

## 4. Local Docker Compose network boundaries

The current Compose configuration binds the frontend, backend, phpMyAdmin, and Ollama host ports to loopback (127.0.0.1). MySQL and Redis do not publish host ports. This is suitable for a single-machine local demo, but it is not by itself a LAN/WAN production architecture.

Keep MySQL, Redis, and Ollama on internal Docker networks. Do not publish their ports to the LAN or Internet. phpMyAdmin is a database-management interface: keep it disabled outside local development or restrict it to a separate management network/host behind HTTPS and strong access controls.

The backend trusts forwarded client IP addresses only from explicitly configured proxy addresses or networks. Do not add a broad or user-controlled network range to `TRUSTED_PROXY_IPS`. Ensure the actual reverse proxy uses the configured source address and overwrites forwarded headers instead of blindly trusting client-supplied values.

## 5. Requirements before LAN deployment

Before making the application available to other devices:

1. Build the frontend for production and serve static assets; do not use Vite's development server.
2. Place a maintained reverse proxy in front of the application and enforce HTTPS with a valid certificate.
3. Set `AUTH_COOKIE_SECURE=true` and configure `FRONTEND_ORIGINS` with the exact HTTPS origins, including scheme and port.
4. Set `TRUSTED_PROXY_IPS` to the exact proxy address/network and verify client-IP forwarding from a second LAN device.
5. Bind the public listener only to the intended LAN interface and firewall all other inbound ports.
6. Keep MySQL, Redis, Ollama, and phpMyAdmin inaccessible to client devices.
7. Use unique, strong secrets and database credentials; keep `.env` out of version control and rotate any credentials that may have been exposed.
8. Test login, logout, registration throttling, cross-origin requests, session expiry, password changes, ticket and conversation ownership, and AI overload behavior from separate devices.

These are LAN deployment requirements, not claims that LAN testing has already been completed.

## 6. Requirements before WAN deployment

Internet exposure requires a separate threat model and deployment security review. At minimum:

- Use a production-grade reverse proxy and, where appropriate, a WAF; configure TLS, request-size and connection limits, and strict firewall rules.
- Expose only the HTTPS application entry point. Never expose MySQL, Redis, Ollama, phpMyAdmin, the Docker socket, or internal service ports.
- Disable interactive API documentation and schema endpoints in production unless there is a documented need and separate access restriction.
- Run containers with least privilege; use non-root users, read-only filesystems, dropped Linux capabilities, and resource limits where practical.
- Pin production images to versions or digests and lock Python/JavaScript dependencies. Establish a patching process.
- Add centralized logging, security-event monitoring, alerts, privacy-aware retention, and an incident-response procedure. Do not log passwords, session cookies, Authorization headers, or private conversations unnecessarily.
- Protect and encrypt MySQL backups, restrict access, and test restoration regularly.
- Define abuse controls, availability and recovery objectives, and an operational owner.
- Perform an independent security assessment and verify authorization/IDOR paths, CSRF protection, rate limits, denial-of-service controls, and secret handling.

## 7. Known limitations and items requiring verification

The following are not considered complete merely because the controls above exist in source:

- End-to-end LAN testing with two physical devices and the intended reverse proxy.
- A complete two-user IDOR test matrix for all ticket, conversation, message, and retry endpoints.
- Non-root production containers, read-only filesystems, capability restrictions, and resource limits.
- Fully locked dependencies and pinned container images.
- Disabling OpenAPI/Redoc/schema endpoints in production.
- A complete Content Security Policy compatible with the final production frontend.
- Request-body limits at both the reverse proxy and ASGI layers.
- Load testing of the AI lock, overload response, client disconnect handling, and Ollama timeouts.
- Security-log review, backup restoration exercise, and incident-response exercise.
- Formal penetration testing or independent verification.

## 8. Security reference

OWASP ASVS 5.0.0 can be used as a checklist when the project is expanded or deployed beyond a classroom demo: https://owasp.org/www-project-application-security-verification-standard/ and https://asvs.owasp.org/.

ASVS is a reference framework here, not a certification claim. Select applicable requirements based on the actual deployment threat model. Do not claim Level 2 compliance without systematically verifying the requirements and retaining evidence.
