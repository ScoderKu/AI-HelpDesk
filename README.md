# AI HelpDesk

## Suomeksi

AI HelpDesk on kehitteillä oleva verkkopohjainen tukipalvelusovellus. Käyttäjä voi keskustella tekoälyn kanssa tietotekniikkaan ja ohjelmistokehitykseen liittyvistä ongelmista sekä hallita omia tukipyyntöjään.

> **Projektin tila 05.11.2026:** Projektin toteuttaja on vahvistanut käyttäjätarinoiden US-01–US-17 käytännön hyväksymiskriteerit suoritetuiksi. US-07:n ja US-15:n testauksessa havaittuja tekoälymallin ja RAG:n laatuhavaintoja on kirjattu projektinhallintadokumenttiin. Automaattisten testien ja buildin viimeisin kirjattu tulos on 04.11.2026; tarkempi tilanne on [projektinhallintadokumentissa](docs.suomi/00-projektinhallinta.md).

### Keskeiset ominaisuudet

- Käyttäjätilin luominen, kirjautuminen ja uloskirjautuminen; profiilissa etu- ja sukunimi sekä sähköpostiosoite ovat vain luettavia, käyttäjänimi on muokattavissa.
- Ollama-pohjainen tekoälychat, tallennettu keskusteluhistoria ja epäonnistuneen AI-vastauksen erillinen uudelleenyritys.
- Tukipyyntöjen luominen, tarkastelu ja sulkeminen.
- Tukipyyntöjen prioriteetit LOW, MEDIUM ja HIGH erotetaan visuaalisesti toisistaan.
- Etusivun rajattu yhteenveto käyttäjän omista tukipyynnöistä: kokonaismäärä sekä `OPEN`- ja `CLOSED`-määrät.
- Suomen- ja englanninkielinen käyttöliittymä.
- RAG hakee avainsanoilla rajatusta Markdown- ja TXT-dokumenttikokoelmasta ja on integroitu AI-keskusteluun; US-15 on hyväksytty käytännössä, ja hakujen sekä generatiivisten vastausten tunnetut rajoitteet on kirjattu.
- Kehitys- ja esittely-ympäristön käynnistäminen Docker Composella, mukaan lukien Ollama ja valittu tekoälymalli.

### Teknologiapino

- Frontend: React ja TypeScript
- Backend: Python ja FastAPI
- Tietokanta: MySQL
- Kirjautumisen käyttörajoitukset: Redis
- Tekoälypalvelu: Ollama Docker Compose -ympäristössä
- Tekoälymalli: `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`
- Kontitus: Docker Compose

Työkalujen ja kirjastojen tulee olla maksuttomia. Niiden sekä tekoälymallin lisenssit ja käyttöehdot tarkistetaan ennen toimitusta.

Ollama-ympäristö testataan projektissa NVIDIA-GPU:lla. Muiden GPU-valmistajien tai -tyyppien yhteensopivuutta ei varmenneta tässä projektissa; niiden käyttöä haluava käyttäjä testaa yhteensopivuuden itse.

### Arkkitehtuurin yleiskuva

Frontend käyttää backendin REST-rajapintaa. Backend käsittelee liiketoimintalogiikan ja tietokantayhteyden sekä kutsuu Ollamaa Docker Compose -verkon kautta. MySQL tallentaa käyttäjät ja palvelinpuolen kirjautumisistunnot. Redis jakaa kirjautumisyritysten käyttörajat backend-pyyntöjen välillä. RAG-haku käsittelee sovittua Markdown- ja TXT-lähdekokoelmaa avainsanoilla.

```mermaid
flowchart LR
    U[Kayttaja] --> F[React-frontend]
    F --> B[FastAPI-backend]
    B --> DB[(MySQL)]
    B --> R[(Redis)]
    B --> K[Knowledge Service<br/>Markdown/TXT-avainsanahaku]
    K --> D[Dokumenttikokoelma]
    B --> O[Ollama]
    O --> M[Llama-Poro 2 8B]
```

### Projektidokumentaatio

- [Projektinhallinta](docs.suomi/00-projektinhallinta.md)
- [Vaatimusmäärittely](docs.suomi/01-vaatimusmaarittely.md)
- [Käyttäjätarinat ja hyväksymiskriteerit](<docs.suomi/02-k%C3%A4ytt%C3%A4j%C3%A4tarinat%20ja%20hyv%C3%A4ksymiskriteerit.md>)
- [Product Backlog](<docs.suomi/03-product%20backlog.md>)
- [Sprint-suunnitelma](<docs.suomi/04-sprintin%20suunnitelma.md>)
- [Järjestelmän suunnittelu](<docs.suomi/05-j%C3%A4rjestelm%C3%A4n%20suunnittelu.md>)
- [UX/UI-suunnittelu](docs.suomi/06-ux-ui-suunnittelu.md)
- [Ollama-mallin Modelfile](ollama/Modelfile)

### Edellytykset

Käynnistys edellyttää Dockeria ja Docker Composea. Luo paikallinen `.env` kopioimalla esimerkkitiedosto ja aseta tietokantatunnukset sekä vähintään 32-merkkinen satunnainen `JWT_SECRET_KEY`.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

### Asennus ja käynnistäminen

Käynnistä frontend, backend, MySQL, Redis ja Ollama yhdellä komennolla:

```powershell
docker compose up --build
```

Ollama-malli luodaan automaattisesti ensimmäisellä käynnistyskerralla: `ollama-model-init` odottaa Ollaman terveystarkistusta, tarkistaa löytyykö `poro-helpdesk` ja luo sen komennolla `ollama create poro-helpdesk -f /models/Modelfile`, jos mallia ei vielä ole. Kun backend käynnistyy, se lataa mallin valmiiksi ja pyytää Ollamaa pitämään sen muistissa 24 tuntia käyttämättömänä; tämä tapahtuu uudelleen myös backendin/Dockerin käynnistyessä uudelleen. Backend ei aloita palvelua ennen kuin preload onnistuu. Modelfile käyttää tiedostoa `ollama/models/Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`; varmista, että tiedosto on paikallisesti tässä polussa ennen käynnistystä. Luotu malli tallentuu pysyvään `ollama_data`-volyymiin. Seuraavilla käynnistyskerroilla mallia ei luoda uudelleen, jos se on jo olemassa. Tarkista asennus komennolla `docker compose exec ollama ollama list` ja muistissa oleva malli komennolla `docker compose exec ollama ollama ps`.

Paikalliseen HTTP-kehitykseen aseta `.env`-tiedostossa `AUTH_COOKIE_SECURE=false`. Tämä Compose-asetus rajaa frontendin ja backendin `127.0.0.1`-osoitteeseen; sovellus ei tällä asetuksella ole muiden lähiverkon laitteiden käytettävissä. Frontend välittää `/api`-pyynnöt samalle alkuperälle. Compose-ympäristössä frontend käyttää vain erillistä proxy-verkkoa osoitteella `172.30.0.2` ja ottaa backend-yhteyden verkkoaliaksella `backend-proxy`, joten yhteys käyttää sitä verkkorajapintaa, jonka backend tunnistaa luotetuksi. `TRUSTED_PROXY_IPS`-asetuksen oletusarvo rajaa luottamuksen frontendin IP-osoitteeseen. Backend käyttää asiakkaan IP:nä luotetulta proxylta välitetyn ketjun ensimmäistä luottamatonta osoitetta. Jos muutat Compose-verkon tai proxyn osoitetta, päivitä myös `TRUSTED_PROXY_IPS`. Vanhentuneet kirjautumisistunnot siivotaan erillisessä taustatehtävässä tunnin välein, ei kirjautumisen yhteydessä. Nykyistä IP-välitystä ei ole vielä varmennettu kahdella oikealla LAN-laitteella. HTTPS-käyttöönotossa käytä `AUTH_COOKIE_SECURE=true`, aseta `FRONTEND_ORIGINS` sisältämään sovelluksen tarkka HTTPS-alkuperä ja käytä HTTPS:ää tarjoavaa reverse proxyä; määritä myös kyseisen proxyn luottamus erikseen. Aseta `VITE_API_BASE_URL` vain, jos backendin API on eri alkuperässä; arvon tulee olla backendin alkuperäosoite ilman `/api`-polkua.

Jos frontend ajetaan Composen sijasta suoraan Viten kehityspalvelimella (oletusportti 5173), lisää `http://localhost:5173` ja `http://127.0.0.1:5173` `FRONTEND_ORIGINS`-asetukseen. Asetuksen on sisällettävä frontendin tarkka alkuperä, jotta kirjautumisen ulos Origin-tarkistus hyväksyy pyynnön.

Backend ajaa `alembic upgrade head` -migraatiot automaattisesti ennen käynnistymistä. Ensimmäinen baseline-migraatio luo `users`- ja `auth_sessions`-taulut uuteen tietokantaan tai ottaa aiemman käynnistystavan luomat taulut käyttöön niitä muuttamatta. Varmista aiemman version tietokannan skeema ja ota MySQL-volyymista varmuuskopio ennen päivitystä. Alembicin automaattisesti generoima migraatio on ehdotus: tarkista migraatiotiedosto ennen sen yhdistämistä.

LAN-käytössä lisää `FRONTEND_ORIGINS`-asetukseen sovelluksen tarkka alkuperä, esimerkiksi `http://helpdesk.lan:8088`, ja pidä logoutin `Origin`-tarkistus käytössä. Suosi HTTPS:ää ja `AUTH_COOKIE_SECURE=true`-asetusta istuntokeksin suojaamiseksi.

### Sovelluksen käyttö

1. Avaa Compose-käynnistyksen jälkeen `http://localhost:8088` ja luo käyttäjätili tai kirjaudu sisään.
2. Tukipyynnöt-näkymässä voit luoda pyynnön, valita prioriteetin, muokata avointa pyyntöä ja sulkea sen. Suljetun pyynnön tietoja ei voi enää muokata.
3. AI-keskustelu-näkymässä voit luoda keskustelun, lähettää viestejä ja palata aiempiin keskusteluihin. Jos AI-palvelu ei vastaa, jo tallennettu käyttäjän viesti säilyy historiassa; käytä kyseisen viestin **Yritä uudelleen** -toimintoa sen sijaan, että lähettäisit saman viestin uudestaan uutena viestinä.
4. AI-keskustelusta voi luoda tukipyynnön: järjestelmä ehdottaa otsikon ja kuvauksen, käyttäjä voi tarkastaa ja vahvistaa luomisen ennen tallennusta. Peruutus tai hylkäys ei luo pyyntöä.
5. Profiilissa voit vaihtaa käyttäjänimen. Etunimi, sukunimi ja sähköpostiosoite näkyvät vain luettavina tietoina.
6. Vaihda käyttöliittymän kieltä FI/EN-valinnalla. Valinta tallentuu samaan selaimeen.
7. Etusivulla näytetään kirjautuneen käyttäjän omien tukipyyntöjen kokonaismäärä sekä `OPEN`- ja `CLOSED`-määrät.

**Tietojen säilytys:** taustatehtävä suoritetaan päivittäin ja poistaa pysyvästi yli kolme kalenterikuukautta suljettuina olleet tukipyynnöt (`closed_at`) sekä yli kolme kalenterikuukautta käyttämättöminä olleet keskustelut (`updated_at`). Keskustelu säilytetään, jos siihen liittyy avoin tukipyyntö tai tukipyyntö, jonka oma säilytysaika ei ole vielä täyttynyt. Keskustelun viestit poistuvat keskustelun mukana. Poistoa ei voi peruuttaa; ota tarvittavat varmuuskopiot ja noudata organisaation tietojen säilytyskäytäntöjä.

### Ylläpitäjän ohje: unohtuneen salasanan palautus (US-17)

US-17:n salasanan palautus tehdään vain backendin ylläpitokomennolla. Sovelluksessa ei ole julkista salasanan palautusrajapintaa, käyttäjän palautusnäkymää, sähköpostipalautusta tai ADMIN-käyttöliittymää.

**Ennen palautusta**
1. Varmista käyttäjän henkilöllisyys sovelluksen ulkopuolella organisaation käytännön mukaisesti.
2. Varmista, että sinulla on oikeus käyttää suojattua backend-/Docker-ympäristöä. Docker- ja palvelinympäristön käyttöoikeus antaa mahdollisuuden suorittaa ylläpitotoimintoja.
3. Varmista, että backend ja tietokanta ovat käynnissä.

**Palauta salasana**

Suorita projektin juurihakemistossa PowerShellissä seuraava komento ja korvaa sähköpostiosoite kohdekäyttäjän osoitteella:

```powershell
docker compose exec backend python -m app.admin reset-password --email user@example.com
```

Onnistuneessa palautuksessa komento tulostaa uuden väliaikaisen salasanan kerran. Kopioi se heti ja toimita käyttäjälle varmennetun, turvallisen erillisen kanavan kautta. Käyttäjän on kirjauduttava sisään väliaikaisella salasanalla ja vaihdettava se ennen muiden suojattujen toimintojen käyttöä. Salasanan vaihdon jälkeen käyttäjän on kirjauduttava uudelleen uudella salasanalla.

**Tietoturvaohjeet**
- Älä suorita komentoa jaetussa tai tallentavassa terminaalissa. Suojaa terminaalin tuloste ja tyhjennä/poista mahdolliset tallenteet organisaation käytäntöjen mukaisesti.
- Älä kirjoita väliaikaista salasanaa tikettiin, sähköpostiin, chattiin, komentoriviparametriksi, tiedostoon tai lokiin.
- Älä suorita komentoa uudelleen vain siksi, että salasana jäi kopioimatta. Uusi suoritus luo uuden väliaikaisen salasanan ja mitätöi aiemman; suorita palautus uudelleen hallitusti ja toimita viimeisin salasana turvallisesti.
- Jos käyttäjää ei löydy tai tietokantatoiminto epäonnistuu, komento palauttaa virheen eikä tulosta salasanaa. Tarkista backendin ja tietokannan tila; älä yritä muuttaa salasanaa suoraan tietokannasta.
- Palautus mitätöi käyttäjän kaikki olemassa olevat kirjautumisistunnot.
- Komento ei luo ylläpitäjäroolia eikä tarkista sovelluksen käyttäjäroolia: sen käyttöoikeus perustuu suojatun backend-ympäristön käyttöoikeuksiin.

### Testaus

Frontendin tyypitys, tuotantobuild ja lint-tarkistukset voi suorittaa näin:

```powershell
cd frontend
npm run build
npm run lint
```

Backendin koko `unittest`-testisarjan voi ajaa projektin juuresta Dockerilla:

```powershell
docker compose exec backend python -m unittest discover -s tests -v
```

Testit kattavat proxy-IP:n poiminnan, kirjautumisen rate limiting -laskurit ja Redis-virheet, vanhentuneiden istuntojen siivouskyselyn, kolmen kalenterikuukauden tietojen säilytyssäännöt sekä Ticket API:n validoinnin, omistajuusrajauksen ja keskeiset toiminnot. Testit eivät korvaa rekisteröitymisen ja kirjautumisen API-integraatiotestejä, rinnakkaisten kirjautumisten testiä MySQL:llä tai oikeassa LAN-verkossa tehtävää IP-välitystestiä. Frontendin build ja lint ajetaan erikseen frontend-kansiossa.

03.11.2026 tehdyssä tarkistuksessa backendin kaikki 57 `unittest`-testiä läpäisivät, frontendin lint oli puhdas ja TypeScript-tarkistus sekä tuotantobuild onnistuivat. Testit ajettiin päivitetyllä lähdekoodilla Docker-kontissa. Tämä ei korvaa käyttöönotetun tietokannan migraation, tyhjistä Docker-volyymeista käynnistyksen, todellisen LAN-välityksen eikä manuaalisen toiminnallisen hyväksymistestauksen tarkistusta; ajantasainen projektitilanne on projektinhallintadokumentissa.

### Kuvat

Arkkitehtuuri- ja käyttöliittymäsuunnitelmat löytyvät [järjestelmän suunnittelusta](<docs/05-j%C3%A4rjestelm%C3%A4n%20suunnittelu.md>) ja [UX/UI-suunnittelusta](docs/06-ux-ui-suunnittelu.md>). Kuvakaappauksia ei tällä hetkellä ylläpidetä projektissa.

### Lisenssi

Projektin lisenssiä ei ole vielä määritelty. Myös kolmannen osapuolen mallien, työkalujen ja kirjastojen lisenssit sekä käyttöehdot tarkistetaan ennen julkaisua.

---

## English

AI HelpDesk is a web-based support application under development. Users can discuss IT and software development issues with an AI assistant and manage their own support tickets.

> **Project status on 05.11.2026:** The project implementer has confirmed practical acceptance for US-01 through US-17. AI model and RAG quality limitations observed while testing US-07 and US-15 are recorded in the project management document. The latest recorded automated test/build results are dated 04.11.2026; see the [project management document](docs.eng/docs/00-Project%20Management.md) for details.

### Main features

- User registration, sign-in, and sign-out; first name, last name, and email are read-only on the profile, while username can be changed.
- Ollama-backed AI chat, saved conversation history, and a separate retry for a failed AI response.
- Creating, viewing, and closing support tickets.
- Support-ticket priorities LOW, MEDIUM, and HIGH are visually distinguished.
- A limited dashboard for the signed-in user's tickets: total count and `OPEN`/`CLOSED` counts.
- Finnish and English user interface.
- RAG keyword search over a selected Markdown and TXT collection is integrated into AI chat and US-15 has passed practical acceptance; known retrieval and generative-answer limitations are documented.
- Starting the development and demo environment with Docker Compose, including Ollama and the selected AI model.

### Technology stack

- Frontend: React and TypeScript
- Backend: Python and FastAPI
- Database: MySQL
- Login rate limiting: Redis
- AI service: Ollama in the Docker Compose environment
- AI model: `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`
- Containerization: Docker Compose

Tools and libraries must be free of charge. Their licenses and terms of use, as well as those of the AI model, will be checked before delivery.

The Ollama environment is tested on NVIDIA GPUs. Compatibility with GPUs from other vendors or of other types is not verified by this project; users who want to use them are responsible for testing compatibility.

### Architecture overview

The frontend uses the backend REST API. The backend handles application logic and database access, and calls Ollama over the Docker Compose network. MySQL stores users and server-side login sessions. Redis shares login-attempt limits across backend requests. RAG searches the agreed Markdown and TXT document collection using keywords.

```mermaid
flowchart LR
    U[User] --> F[React frontend]
    F --> B[FastAPI backend]
    B --> DB[(MySQL)]
    B --> R[(Redis)]
    B --> K[Knowledge Service<br/>Markdown/TXT keyword search]
    K --> D[Document collection]
    B --> O[Ollama]
    O --> M[Llama-Poro 2 8B]
```

### Project documentation

- [Project management](docs.eng/docs/00-projektinhallinta.md)
- [Requirements specification](docs.eng/docs/01-vaatimusmaarittely.md)
- [User stories and acceptance criteria](<docs.eng/docs/02-k%C3%A4ytt%C3%A4j%C3%A4tarinat%20ja%20hyv%C3%A4ksymiskriteerit.md>)
- [Product Backlog](<docs.eng/docs/03-product%20backlog.md>)
- [Sprint plan](<docs.eng/docs/04-sprintin%20suunnitelma.md>)
- [System design](<docs.eng/docs/05-j%C3%A4rjestelm%C3%A4n%20suunnittelu.md>)
- [UX/UI design](docs.eng/docs/06-ux-ui-suunnittelu.md)
- [Ollama model Modelfile](ollama/Modelfile)

### Prerequisites

The setup requires Docker and Docker Compose. Create a local `.env` from the example file and set the database credentials and a random `JWT_SECRET_KEY` of at least 32 characters.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

### Installation and running

Start the frontend, backend, MySQL, Redis, and Ollama with:

```powershell
docker compose up --build
```

The Ollama model is created automatically on first startup: `ollama-model-init` waits for Ollama's health check, checks whether `poro-helpdesk` exists, and runs `ollama create poro-helpdesk -f /models/Modelfile` when it does not. When the backend starts, it preloads the model and asks Ollama to keep it in memory for 24 hours while idle; this runs again after backend/Docker restarts. The backend does not start serving until preload succeeds. The Modelfile uses `ollama/models/Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`; make sure this file exists locally at that path before startup. The created model is stored in the persistent `ollama_data` volume and is not recreated on later starts if it already exists. Check installation with `docker compose exec ollama ollama list` and the loaded model with `docker compose exec ollama ollama ps`.

For local HTTP development, set `AUTH_COOKIE_SECURE=false` in `.env`. Compose binds the frontend and backend to `127.0.0.1`, so this setup is not accessible from other devices on the LAN. The frontend sends `/api` requests through the same-origin proxy. In Compose, the frontend uses only the dedicated proxy network at `172.30.0.2` and connects to the backend through the `backend-proxy` network alias, ensuring the connection uses the interface trusted by the backend. The default `TRUSTED_PROXY_IPS` value trusts only the frontend IP. The backend uses the first untrusted address in the chain forwarded by a trusted proxy as the client IP. If you change the Compose network or proxy address, update `TRUSTED_PROXY_IPS` as well. Expired login sessions are cleaned by an hourly background task. A separate daily task permanently deletes closed tickets after three calendar months and inactive conversations after three calendar months without activity. Conversations linked to an open ticket or a ticket that has not yet reached its retention date are preserved. Forwarding has not yet been verified using two real LAN devices. For an HTTPS deployment, use `AUTH_COOKIE_SECURE=true`, set `FRONTEND_ORIGINS` to include the exact HTTPS application origin, and use an HTTPS reverse proxy; configure trust for that proxy separately. Set frontend `VITE_API_BASE_URL` only when the backend API uses a different origin; its value must be the backend origin without an `/api` path.

If you run the frontend directly with the Vite development server instead of Compose (default port 5173), add `http://localhost:5173` and `http://127.0.0.1:5173` to `FRONTEND_ORIGINS`. The setting must include the exact frontend origin so the logout Origin check accepts the request.

Before startup, the backend automatically runs `alembic upgrade head`. The initial baseline migration creates the `users` and `auth_sessions` tables in a new database or adopts tables created by the previous startup path without changing them. Verify the schema of a database created by an earlier version and back up the MySQL volume before upgrading. Alembic autogeneration produces a candidate migration; review each migration file before merging it.

For LAN access, add the exact application origin to `FRONTEND_ORIGINS`, for example `http://helpdesk.lan:8088`, and keep the logout `Origin` check enabled. Prefer HTTPS with `AUTH_COOKIE_SECURE=true` to protect the session cookie.

### Using the application

1. After starting Compose, open `http://localhost:8088` and create an account or sign in.
2. In **Support tickets**, create a ticket, select a priority, edit an open ticket, or close it. Closed tickets cannot be edited.
3. In **AI chat**, create a conversation, send messages, and return to saved conversations. If the AI service fails, the user message remains in history; use **Retry** for that message rather than sending the same text as a new message.
4. From an AI conversation, generate a support-ticket draft, review or edit its title and description, and confirm to save it. Cancelling does not create a ticket.
5. In **Profile**, change the username. First name, last name, and email are read-only.
6. Switch the interface language with the FI/EN control. The selection is stored in the same browser.
7. The homepage shows the signed-in user's total, `OPEN`, and `CLOSED` ticket counts.

**Data retention:** a daily background task permanently deletes closed support tickets after three calendar months based on `closed_at`, and conversations inactive for three calendar months based on `updated_at`. A conversation is retained while it is linked to an open ticket or a ticket that has not yet reached its own retention date. Messages are deleted with their conversation. Deletion cannot be undone; keep any required backups and follow the organization's data-retention policies.

### Administrator guide: forgotten password reset (US-17)

US-17 password resets are performed only through a backend maintenance command. The application does not provide a public password-reset API, a user-facing reset page, email-based recovery, or an ADMIN user interface.

**Before resetting a password**
1. Verify the user's identity outside the application according to your organization's procedure.
2. Ensure that you are authorized to access the protected backend/Docker environment. Access to the Docker and server environment allows maintenance commands to be run.
3. Ensure that the backend and database are running.

**Reset the password**

From the project root, run the following command in PowerShell. Replace the email address with the target user's email:

```powershell
docker compose exec backend python -m app.admin reset-password --email user@example.com
```

When the reset succeeds, the command prints the new temporary password once. Copy it immediately and deliver it to the user through a verified, secure out-of-band channel. The user must sign in with the temporary password and change it before accessing any other protected feature. After changing the password, the user must sign in again with the new password.

**Security instructions**
- Do not run the command in a shared or recorded terminal. Protect terminal output and remove any recordings according to your organization's policy.
- Never put the temporary password in a ticket, email, chat, command-line argument, file, or log.
- Do not rerun the command merely because the password was not copied. A new run generates a new temporary password and invalidates the previous one; if a reset must be repeated, perform it deliberately and securely deliver the latest password.
- If the target user does not exist or a database operation fails, the command returns an error and does not print a password. Check backend/database health; do not change the password directly in the database.
- The reset invalidates all existing login sessions belonging to the user.
- The command does not create an administrator role or check an application-level user role. Authorization is based on access to the protected backend environment.

### Testing

Run the frontend type-check/production build and lint checks with:

```powershell
cd frontend
npm run build
npm run lint
```

Run the complete backend `unittest` suite from the project root using Docker:

```powershell
docker compose exec backend python -m unittest discover -s tests -v
```

The tests cover proxy client-IP resolution, login rate-limit counters and Redis failures, expired-session cleanup, three-calendar-month data-retention rules, and Ticket API validation, ownership checks, and core actions. They do not replace registration/sign-in API integration tests, a concurrent sign-in test against MySQL, or an IP-forwarding test on a real LAN. Run the frontend build and lint separately from the frontend directory.

In the 04.11.2026 check, all 65 backend `unittest` tests passed; frontend lint, TypeScript checks, and the production build also succeeded. Tests ran against the updated source in a Docker container. This does not replace verifying migration application to the active database, startup from empty Docker volumes, actual LAN forwarding, or full manual acceptance testing; see project management for the current status.

### Screenshots

Architecture and interface design materials are available in the [system design](<docs.eng/docs/05-j%C3%A4rjestelm%C3%A4n%20suunnittelu.md>) and [UX/UI design](docs.eng/docs/06-ux-ui-suunnittelu.md) documents. Screenshots are not currently maintained in the project.

### License

The project license has not yet been defined. Licenses and terms of use for third-party models, tools, and libraries will also be checked before release.
