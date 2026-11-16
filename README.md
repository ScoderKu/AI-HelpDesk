# AI HelpDesk
## Suomeksi

AI HelpDesk on suomen- ja englanninkielinen teknisen tuen verkkosovellus. Käyttäjä voi kysyä tekoälyltä IT- ja ohjelmistokehitysongelmista, hallita omia tukipyyntöjään ja tarkastella tallennettuja keskustelujaan.

### Ominaisuudet

- Käyttäjätilin rekisteröinti, kirjautuminen, uloskirjautuminen ja profiilin hallinta.
- AI-chat, tallennettu keskusteluhistoria, vastaamattoman viestin uudelleenyritys ja generoinnin pysäytys.
- Itsenäiset keskustelut ja lapsikeskustelut, joiden otsikon ja kontekstiyhteenvedon käyttäjä tarkistaa ennen luontia.
- Tukipyyntöjen luonti, listaus, avoimen pyynnön muokkaus ja sulkeminen.
- Tukipyynnön luonti keskustelusta vasta käyttäjän tarkistuksen ja vahvistuksen jälkeen.
- Kirjautuneen käyttäjän tukipyyntöjen kokonaismäärä sekä OPEN- ja CLOSED-määrät.
- Suomen- ja englanninkielinen käyttöliittymä.
- Projektikohtainen RAG rajatusta paikallisesta Markdown/TXT-tietopohjasta.
- Docker Compose -kehitys- ja esittely-ympäristö MySQL:llä, Redisillä ja Ollamalla.

### Teknologiat

| Osa | Teknologia |
|---|---|
| Frontend | React 19, TypeScript, Vite |
| Backend | Python, FastAPI, Uvicorn |
| Tietokanta ja migraatiot | MySQL 8.4, SQLAlchemy, Alembic |
| Jaettu koordinointi ja käyttörajoitukset | Redis |
| Paikallinen tekoälyajoympäristö | Ollama |
| Kehitysympäristö | Docker Compose |

### Dokumentaatio

- [Dokumentaation hakemisto (EN/FI)](docs/README.md)
- [Projektin hyväksyntä- ja testausraportti](reports/PROJECT_ACCEPTANCE_REPORT.md)
- [Järjestelmän suunnittelu (FI)](docs/fi/03-järjestelmän%20suunnittelu.md) · [System Design (EN)](docs/en/03-System%20Design.md)
- [Tietoturva ja käyttöönotto (FI)](docs/fi/08-tietoturva-ja-kayttoonotto.md) · [Security and Deployment (EN)](docs/en/08-security-deployment-considerations.md)

Dokumentaatiohakemisto kertoo, mikä dokumentti on ensisijainen vaatimuksille, käyttäjätarinoille, suunnittelulle, suunnitelmille, lisensseille ja testausnäytölle. Lähdekoodi, asetukset ja tietokantamigraatiot määrittävät toteutetun toiminnan.

### Edellytykset

- Docker Engine/Desktop ja Docker Compose.
- Nykyinen Compose-kokoonpano käyttää NVIDIA GPU -tukea. Muita GPU-tyyppejä ei ole varmennettu.
- Riittävästi levytilaa Ollama-mallille ja Docker-kuville.

### Paikallinen käyttöönotto

1. Kloonaa repositorio ja siirry sen juurihakemistoon.
2. Luo paikallinen ympäristötiedosto:

   ```powershell
   Copy-Item .env.example .env
   ```

3. Aseta yksilölliset tietokantasalasanat ja luo ympäristölle oma 64-merkkinen JWT_SECRET_KEY:

   ```powershell
   [Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
   ```

   Kopioi luotu arvo .env-tiedostoon. Älä lisää .env-tiedostoa versionhallintaan tai käytä samoja salaisuuksia tuotannossa.

4. Säilytä oletusmalliasetukset, ellet ole valinnut ja testannut muuta Ollama-yhteensopivaa mallia:

   ```dotenv
   OLLAMA_MODEL=poro
   OLLAMA_MODEL_SOURCE=modelfile
   ```

   Oletus-Modelfile edellyttää tiedostoa ollama/models/Llama-Poro-2-8B-Instruct.Q4_K_M.gguf. Tarkista mallin lisenssi ja laitteistovaatimukset. Jos vaihdat mallia, pidä OLLAMA_MODEL yhtenäisenä backendille ja mallin alustuspalvelulle.

5. Rakenna ja käynnistä palvelut:

   ```powershell
   docker compose up --build
   ```

6. Avaa sovellus osoitteessa [http://localhost:8088](http://localhost:8088). phpMyAdmin on paikallisesti osoitteessa [http://localhost:8080](http://localhost:8080).

Ensimmäinen käynnistys lataa konttikuvat ja alustaa valitun Ollama-mallin. Malli tallennetaan pysyvään ollama_data-volyymiin. Backendin käynnistys odottaa tarvittavien palvelujen ja mallin latauksen valmistumista.

### Kehityksen tarkistukset

Suorita frontendin tarkistukset frontend/-hakemistossa:

```powershell
npm run lint
npm run build
```

Suorita backendin yksikkötestit projektin juurihakemistosta:

```powershell
docker compose exec backend python -m unittest discover -s tests -v
```

Hyväksyntäraportti kokoaa aiemmin raportoidut testitulokset ja erittelee vielä varmentamattomat asiat. Historiallisia tuloksia ei pidä tulkita nykyisen commitin uudeksi testiajaksi.

### Käyttöönoton rajaus

Toimitettu Compose-kokoonpano sitoo julkaistut palveluportit loopback-osoitteeseen paikallista kehitys- ja esittelykäyttöä varten. Se ei ole tuotantokäyttöönoton määritys. Älä julkaise sovellusta suoraan julkiseen Internetiin. Tutustu kaksikieliseen tietoturva- ja käyttöönotto-ohjeeseen ja tee erillinen käyttöönoton/tietoturvan arviointi ennen LAN- tai WAN-käyttöä.

### Lisenssi

Projektin omaa lisenssiä ei ole vielä valittu. Kolmansien osapuolten riippuvuuksien ja mallien lisenssit ovat tarkastelussa; katso dokumentti 07 dokumentaatiohakemistosta.

---

## English

AI HelpDesk is a bilingual (Finnish/English) technical-support web application. Users can ask an AI assistant about IT and software-development issues, manage their own support tickets, and review saved conversations.

### Features

- User registration, sign-in, sign-out and profile management.
- AI chat with saved conversation history, retry for unanswered messages and Stop Generation.
- Independent conversations and child conversations with a user-reviewed title and context summary.
- Ticket creation, listing, editing of open tickets, and closing.
- Ticket creation from a conversation only after the user reviews and confirms the proposed title and description.
- A dashboard showing the signed-in user's total, OPEN and CLOSED ticket counts.
- Finnish and English interface.
- Project-specific RAG over an approved local Markdown/TXT knowledge corpus.
- Docker Compose development/demo environment with MySQL, Redis and Ollama.

### Technology

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript, Vite |
| Backend | Python, FastAPI, Uvicorn |
| Database and migrations | MySQL 8.4, SQLAlchemy, Alembic |
| Shared coordination and rate limiting | Redis |
| Local AI runtime | Ollama |
| Development environment | Docker Compose |

### Documentation

- [Documentation index (English and Finnish)](docs/README.md)
- [Project acceptance and verification report](reports/PROJECT_ACCEPTANCE_REPORT.md)
- [System design (EN)](docs/en/03-System%20Design.md) · [Järjestelmän suunnittelu (FI)](docs/fi/03-järjestelmän%20suunnittelu.md)
- [Security and deployment (EN)](docs/en/08-security-deployment-considerations.md) · [Tietoturva ja käyttöönotto (FI)](docs/fi/08-tietoturva-ja-kayttoonotto.md)

The documentation index explains which document is authoritative for requirements, user stories, design, planning, licensing and verification. Source code, configuration and database migrations define the implemented behavior.

### Prerequisites

- Docker Engine/Desktop with Docker Compose.
- NVIDIA GPU support is used by the current Compose configuration. Other GPU types have not been validated.
- Sufficient disk space for the Ollama model and Docker images.

### Local setup

1. Clone the repository and open its root directory.
2. Create a local environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

3. Set unique database passwords and generate a unique 64-character JWT_SECRET_KEY for this environment:

   ```powershell
   [Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
   ```

   Paste the generated value into .env. Do not commit .env or reuse production secrets.

4. Keep the default model settings in .env unless you have selected and tested another Ollama-compatible model:

   ```dotenv
   OLLAMA_MODEL=poro
   OLLAMA_MODEL_SOURCE=modelfile
   ```

   The default Modelfile expects ollama/models/Llama-Poro-2-8B-Instruct.Q4_K_M.gguf. Check model licensing and hardware requirements before use. If you change the model, keep OLLAMA_MODEL consistent for backend and model initialization.

5. Build and start the services:

   ```powershell
   docker compose up --build
   ```

6. Open the application at [http://localhost:8088](http://localhost:8088). phpMyAdmin is available locally at [http://localhost:8080](http://localhost:8080).

The first startup downloads the container images and initializes the configured Ollama model. The model is stored in the persistent ollama_data volume. Backend startup waits for required services and model preload.

### Development checks

Run frontend checks from the frontend/ directory:

```powershell
npm run lint
npm run build
```

Run backend unit tests from the project root:

```powershell
docker compose exec backend python -m unittest discover -s tests -v
```

The acceptance report records historical test evidence and explicitly lists checks that remain unverified. These results must not be interpreted as a fresh test run for the current commit.

### Deployment boundary

The supplied Compose configuration binds published service ports to loopback for local development/demo use. It is not a production deployment configuration. Do not expose the application directly to the public Internet. Review the bilingual Security and Deployment documentation and complete a separate deployment/security review before LAN or WAN exposure.

### License

The project's own license has not yet been selected. Third-party dependency and model licensing is under review; see document 07 in the documentation index.
