# AI HelpDesk — kolmansien osapuolten lisenssiselvitys

**Tarkistuspäivä:** 05.11.2026  
**Tila:** Alustava inventointi on tehty; julkaisuun liittyviä toimia on vielä avoinna.  
**Rajaus:** Projektin manifestit, käynnissä olevien paikallisten Compose-kuvien versiot, paikallinen GGUF-tiedosto sekä alkupään lisenssitiedot. Tämä on tekninen inventointi, ei oikeudellinen lausunto.

## Havainnot

| Komponentti | Havaittu lisenssi / ehdot | Tulos |
|---|---|---|
| Oletusmalli `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf` | LumiOpenin Poro 2 8B Instruct -mallikortti ja vastaava mradermacherin GGUF-repositorio ilmoittavat Llama 3.3 Community License -lisenssin. Mallitiedosto on paikallisesti olemassa (4 920 739 552 tavua), mutta Git ohittaa sen, joten tarkkaa latausrevisiota ja tarkistussummaa ei ole kirjattu. | Lisenssi on ehdollinen eikä rajoittamaton OSI-lisenssi. Jos Llama-materiaalia tai sitä sisältävä tuote jaetaan, sopimus edellyttää lisenssin toimittamista, “Built with Llama” -mainintaa, vaaditun attribuution säilyttämistä ja Acceptable Use Policy -käytännön noudattamista. Sopimuksessa on myös erillinen lisenssikynnys yli 700 miljoonalle kuukausittaiselle käyttäjälle. Kirjaa GGUF-tiedoston tarkka lähde/revisio ja SHA-256, lisää jakelumuotoa koskevat ilmoitukset ja pyydä projektin omistajalta vahvistus suunnitellulle käytölle. Selvitys koskee vain projektin oletusmallia; asiakkaan valitseman Ollama-mallin lisenssi ja käyttöehdot on tarkistettava erikseen. Katso [Poro-mallikortti](https://huggingface.co/LumiOpen/Llama-Poro-2-8B-Instruct), [GGUF-repositorio](https://huggingface.co/mradermacher/Llama-Poro-2-8B-Instruct-GGUF), [Metan lisenssi](https://dev.meta.ai/llama/llama3_3/license) ja [Acceptable Use Policy](https://dev.meta.ai/llama/llama3_3/use-policy). |
| Ollama | Alkupään repositorion lisenssi on MIT. | Säilytä tekijänoikeus- ja lupailmoitus, jos Ollama-ohjelmistoa jaetaan edelleen. Compose käyttää muuttuvaa `ollama/ollama:latest`-tagia; tarkan kuvan digestiä ja mukana tulevien kolmannen osapuolen ilmoituksia ei ole inventoitu. Katso [Ollaman LICENSE](https://github.com/ollama/ollama/blob/main/LICENSE). |
| Redis-palvelin | Käynnissä olevan kuvan versio on Redis 7.4.12 (`redis:7-alpine`). Redis 7.4.x käyttää kaksoislisenssiä RSALv2 tai SSPLv1; Redis 7.2:ssa ja vanhemmissa käytettiin BSD-lisenssiä. | Valitse ja dokumentoi sovellettava lisenssi sekä varmista, että suunniteltu käyttötapa sopii sen ehtoihin. Muuttuva `7-alpine`-tagi voi päivittyä toiseen 7.x-versioon. Katso [Redisin lisenssikatsaus](https://redis.io/legal/licenses/). |
| Pythonin suorat riippuvuudet | `requirements.txt` ilmoittaa seitsemän versioväleillä rajattua riippuvuutta, mutta ei lukitustiedostoa. Käynnissä oleva backend käyttää FastAPI 0.162.0, Uvicorn 0.54.0, SQLAlchemy 2.1.6, Alembic 1.20.1, PyMySQL 1.2.3, pydantic-settings 2.16.2 ja redis-py 6.4.0. Niiden alkupään lisenssit ovat sallivia MIT-/BSD-perheen lisenssejä. | Riippuvuusvälit voivat myöhemmin ratkaista eri versioihin. Transitiivisia riippuvuuksia ei ole lukittu kattavasti eikä koottu projektin SBOMiin; säilytä ilmoitukset ja luo julkaisukohtainen versioitu inventointi. |
| Frontendin npm-riippuvuudet | `package-lock.json` sisältää 90 pakettimerkintää, joista jokaiselle on ilmoitettu lisenssi: 54 MIT, 22 Apache-2.0, 12 MPL-2.0, yksi ISC ja yksi BSD-3-Clause. MPL-2.0-merkinnät koskevat Lightning CSS:ää ja sen alustapaketteja. | Säilytä lukitustiedosto ja soveltuvat ilmoitukset. Tarkista MPL-2.0:n ilmoitus- ja lähdekoodivelvoitteet, jos näitä tiedostoja muutetaan tai jaetaan osana frontend-koontia. |
| Konttikuvat ja järjestelmäpaketit | Nykyinen Compose-pino käyttää MySQL 8.4.13 -versiota (Community Server, GPL), phpMyAdmin `5` -tagia sekä kuvia `python:3.12-slim`, `node:22-alpine` ja `nginx:alpine`. Sovelluksen pohjakuvien digestejä ei ole lukittu. | Kuvakohtaisia ja käyttöjärjestelmäpakettien ilmoituksia ei ole inventoitu kattavasti. Kirjaa kuvadigestit ja muodosta SBOM/lisenssiraportti täsmällisille julkaisukuville. |
| AI HelpDesk -projekti | README kertoo, ettei projektin omaa lisenssiä ole määritelty; juuren `LICENSE`-tiedostoa ei löytynyt. | Valitse projektin lisenssi ennen jakelua ja varmista, ettei sillä väitetä oikeuksia kolmannen osapuolen mallimateriaaliin. |

## Ennen jakelua tehtävät toimet

1. Päätä AI HelpDesk -projektin oma lisenssi ja dokumentoi se.
2. Kirjaa GGUF-latausosoite/revisio ja SHA-256; lisää valitun jakelumuodon edellyttämä Llama 3.3 -lisenssi/attribuutio ja “Built with Llama” -maininta sekä tarkista Acceptable Use Policy.
3. Varmista, sopiiko Redis 7.4.12:n RSALv2- tai SSPLv1-lisenssi projektin suunniteltuun käyttöön; dokumentoi valitut ehdot ja lukitse Redis-kuvan versio/digesti.
4. Lisää Python-riippuvuuksien lukitustiedosto ja muodosta SBOM/lisenssi-inventointi Python-ympäristölle ja kaikille lopullisille konttikuville.
5. Säilytä npm-pakettien ja konttikuvien kolmannen osapuolen ilmoitukset; lukitse kuvadigestit, jotta tarkistettu sisältö ei muutu huomaamatta.

## Kerätty näyttö

- `frontend/package-lock.json` analysoitiin: kaikki 90 pakettimerkintää ilmoittavat lisenssin.
- Käynnissä oleva Compose-pino ilmoitti MySQL 8.4.13:n, Redis 7.4.12:n ja `ollama/ollama:latest`-kuvan.
- GGUF on paikallisessa `ollama/models/`-hakemistossa, mutta Git ohittaa sen; repositorion historia ei osoita tarkkaa lähderevisiota tai tarkistussummaa.
- Backendin autentikoinnin integraatiotesti ajettiin paikallisella Compose/MySQL-tietokannalla. Tulos on projektinhallintalokiin kirjattu, eikä se varmista kohdeympäristöä.
