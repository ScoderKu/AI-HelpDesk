# JavaScript, TypeScript and Node.js — Practical Technical Guide

- **Document ID:** KB-TECH-06
- **Status:** general technical guidance; examples are applicable to the AI HelpDesk React/Vite frontend
- **Applies to:** browser JavaScript, TypeScript, Node.js, npm, Vite
- **Keywords:** JavaScript, JS, TypeScript, TS, Node.js, Node, npm, package.json, promise, async await, event loop, module, ESM, JSON, callback, JavaScript perusteet, TypeScript perusteet

## JavaScript and TypeScript

JavaScript (JS) is the language executed by browsers and by Node.js. TypeScript (TS) adds a static type system and is normally transpiled/compiled into JavaScript before execution. Types are erased at runtime: TypeScript types do not automatically validate data received from an API.

Example:
```ts
type TicketStatus = 'OPEN' | 'CLOSED'

function isClosed(status: TicketStatus): boolean {
  return status === 'CLOSED'
}
```
The compiler catches invalid values in typed code, but JSON received over HTTP still needs runtime validation at the trusted backend boundary.

## Variables and scope

- `const` prevents reassignment of the binding; it does not deeply freeze an object.
- `let` allows reassignment and is block-scoped.
- Avoid `var` in modern code because its function-scoping and hoisting behavior can be surprising.
- Prefer narrow scopes and immutable updates for React state.

## Values and equality

JavaScript has primitive values (string, number, boolean, bigint, symbol, null, undefined) and objects. Use strict equality (`===`) unless coercion is intentional. An object/array variable holds a reference; copying with spread syntax is shallow.

## Functions and closures

Functions are first-class values. A closure retains access to variables from its lexical scope. React event handlers and effects often close over values from a render; stale closure bugs occur when asynchronous work uses outdated values. Use correct hook dependencies and refs only when mutable cross-render identity is required.

## Promises and async/await

A Promise represents an eventual result or failure. `async` functions always return a Promise. `await` pauses that async function until the Promise settles; it does not block the entire JavaScript event loop.

```ts
async function loadProfile(): Promise<User> {
  const response = await fetch('/api/v1/users/me', {
    credentials: 'include',
  })
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return await response.json() as User
}
```
The type assertion above helps TypeScript but does not verify the JSON shape at runtime.

Always handle rejected Promises. A `try/catch` around an awaited call catches its rejection. Use `Promise.all` only when operations can safely run concurrently; use sequential awaits when later work depends on an earlier result.

## Event loop and streaming

JavaScript runs user code on an event loop. Network I/O is asynchronous. A streamed HTTP response can deliver arbitrary byte chunks: a chunk may contain half a JSON record or several records. Decode bytes with `TextDecoder`, append to a buffer, split at protocol record boundaries, and keep the incomplete remainder for the next read.

Do not assume one `reader.read()` call equals one server event.

## Modules: ESM and CommonJS

Modern Vite projects use ES modules:
```ts
import { createRoot } from 'react-dom/client'
export const answer = 42
```
The AI HelpDesk frontend `package.json` declares `"type": "module"`. Node.js also supports CommonJS in appropriate contexts, but do not mix module systems without understanding package configuration and file extensions.

## Node.js and npm

Node.js is a JavaScript runtime outside the browser. npm is the package manager and registry client commonly used with Node.js. In a Vite frontend:
- Node/npm run development, lint and build scripts.
- Vite serves the frontend during development and bundles browser assets for production.
- The browser, not Node.js, runs the built React application in production.

`package.json` declares scripts and dependency ranges. `package-lock.json` records the resolved dependency tree for reproducible installs. `npm ci` requires a lock file and installs exactly from it; if the lock file is absent or inconsistent, it fails. `npm install` can create/update the lock file. Commit the lock file for reproducible CI/container builds.

## Useful commands

```powershell
node --version
npm --version
npm install
npm ci
npm run dev
npm run lint
npm run build
npm ls --depth=0
```

Run these in the frontend directory unless the project scripts explicitly say otherwise.

## Common errors

- `npm is not recognized`: Node.js/npm is not installed or PATH is stale; reopen terminal after installation and verify `where.exe node` and `where.exe npm`.
- `npm ci` fails because lock file is missing: generate and commit a lock file with the project's chosen npm version, then rerun `npm ci`.
- `Cannot find module`: verify working directory, dependency installation and import path/case.
- ESM/CommonJS error: inspect `type` in package.json, file extension and dependency module format.
- TypeScript says a property does not exist: inspect the declared type and actual API response; do not silence the error without checking the data contract.


## Tiivistelmä suomeksi

JavaScript suoritetaan selaimessa ja Node.js-ympäristössä. TypeScript lisää staattisen tyyppijärjestelmän, mutta kääntyy JavaScriptiksi. Node.js on palvelinpuolen JavaScript-ajoympäristö, npm hallitsee paketteja ja package-lock.json lukitsee riippuvuuksien ratkaisut. Promise ja async/await helpottavat asynkronista toimintaa. Muista, että TypeScript-tyyppi ei tarkista API:n ajonaikaista dataa; käytä tarvittaessa skeemavalidointia.
