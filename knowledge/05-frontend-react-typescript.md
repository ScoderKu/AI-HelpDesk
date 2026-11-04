# Frontend — React and TypeScript in AI HelpDesk

- **Document ID:** KB-TECH-05
- **Status:** project-specific facts verified from current frontend source; general React guidance
- **RAG Scope:** project-specific
- **Applies to:** `frontend/src`
- **Keywords:** React, TypeScript, TSX, JSX, hooks, useState, useEffect, fetch, Vite, component, frontend, käyttöliittymä, komponentti, tila

## Frontend stack

The frontend uses React 19 and TypeScript, with Vite as the development server and production build tool. The package scripts include:
- `npm run dev` — Vite development server.
- `npm run build` — TypeScript project build followed by Vite production build.
- `npm run lint` — Oxlint.
- `npm run preview` — preview the production build locally.

The root React entry is `frontend/src/main.tsx`, which mounts `App` into the HTML element with ID `root` under React StrictMode.

## Main application structure

The reviewed source includes:
- `App.tsx`: top-level application state, language selection, session check, authentication and page composition.
- `api.ts`: API base URL configuration.
- `types.ts`: shared TypeScript types for language, user, ticket and profile data.
- `i18n/copy.ts`: Finnish and English UI text.
- `pages/`: page-level components such as authentication, home, chat and forced password change.
- `main.tsx`: React root creation.

Check the current tree before assuming the file inventory is complete.

## React state concepts used in the project

- `useState` stores state that affects rendering, such as current user, language, messages, loading and error state.
- `useEffect` synchronizes with external systems, such as checking the current session or updating the document language.
- `useRef` stores mutable values between renders without triggering a render; the chat page uses refs to track the active conversation/request and draft-related state.
- A state setter schedules a React update; it does not mutate the state variable in place.

Effects that perform asynchronous requests should guard against stale updates after a component is no longer active or after the user switches to another conversation.

## TypeScript in the UI

Shared types define the expected shape of API data. Examples in the repository:
- `Language = 'fi' | 'en'`
- `TicketStatus = 'OPEN' | 'CLOSED'`
- `TicketPriority = 'LOW' | 'MEDIUM' | 'HIGH'`

A union of string literals narrows allowed values at compile time. It does not validate untrusted JSON at runtime. The backend remains responsible for request validation.

TypeScript's `as SomeType` is a compile-time assertion, not a runtime conversion or validation. Treat API responses as external data even when a TypeScript type annotation is used.

## API calls and credentials

The frontend's API base URL is read from `import.meta.env.VITE_API_BASE_URL`, defaulting to an empty string. In same-origin deployments this allows requests such as `/api/v1/...`.

Authenticated fetch calls use `credentials: 'include'` so the browser sends the session cookie. Do not move session secrets into localStorage or JavaScript-readable storage.

## Chat rendering

The chat page renders assistant Markdown through a React renderer implemented in the frontend. It supports common structures such as headings, paragraphs, lists, emphasis and code blocks. Code is rendered as text, not arbitrary HTML. This is important: do not replace safe text rendering with unsanitized `dangerouslySetInnerHTML`.

The chat UI handles streamed response chunks, optimistic messages, persisted message IDs, retry state and conversation switching. Async callbacks must check that the active conversation/request is still the one they started for; otherwise a late response could update the wrong conversation.

## Localization

The current language type is `fi | en`. UI copy is stored centrally in `i18n/copy.ts`. The selected language is stored in browser localStorage under `ai-helpdesk-language`; the default is Finnish if the stored value is absent or invalid. The application also updates the root HTML `lang` attribute.

The UI language is not the same as the AI model's response-language classification.

## Common frontend debugging

- A blank page: inspect browser console, failed JS chunks and Vite/build errors.
- API 401: session cookie may be absent, expired or invalid.
- API 403 on logout: verify exact Origin against `FRONTEND_ORIGINS`.
- CORS error: inspect browser origin, backend allowlist and credential settings; do not solve by allowing every origin with credentials.
- Stale chat content: inspect conversation/request identity guards and asynchronous state updates.
- Stream parse error: verify buffering of partial newline-delimited JSON records.
- TypeScript build error: run `npm run build` and fix type errors rather than suppressing them with broad `any`.


## Tiivistelmä suomeksi

React rakentaa käyttöliittymän komponenteista. TypeScript tuo staattiset tyypit kehitysaikaiseen tarkistukseen, mutta tyypit poistuvat ajonaikana eivätkä validoi automaattisesti palvelimelta tulevaa JSON-dataa. React-tilan päivitykset tehdään setterien kautta; sivuvaikutukset kuuluvat tarkoituksenmukaisiin hookeihin. API-kutsujen virhetilanteet, lataustila ja käyttäjälle näkyvät virheilmoitukset on käsiteltävä erikseen.
