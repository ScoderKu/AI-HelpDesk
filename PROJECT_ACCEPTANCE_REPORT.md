# AI HelpDesk – Projektin loppuraportti ja kokonaisarviointi

**Raportin päiväys:** 12.11.2026  
**Tarkastelun kohde:** kouluprojektin toiminnallinen kokonaisuus ja dokumentoitu hyväksyntä  
**Tietoturvamuutokset:** erillinen haara `security/hardening-demo`; ei vielä hyväksytty osaksi päähaaraa

## 1. Projektin tavoite ja toteutunut laajuus

AI HelpDesk on React/TypeScript-, FastAPI- ja MySQL-pohjainen verkkosovellus, jossa käyttäjä voi hallita omaa profiiliaan ja tukipyyntöjään sekä keskustella paikallisesti ajettavan Ollama-tekoälyn kanssa. Keskustelut ja viestit tallennetaan tietokantaan. Sovellukseen kuuluu myös rajattu dokumenttihakuun perustuva RAG-toiminto, suomen- ja englanninkielinen käyttöliittymä sekä Docker Compose -kehitys- ja esittely-ympäristö.

Projektinhallinnan ja hyväksyntäpäivitysten mukaan toteuttaja on vahvistanut kaikkien käyttäjätarinoiden US-01–US-17 käytännön hyväksymisen 05.11.2026. Tämä on toteuttajan dokumentoima hyväksyntä, ei ulkopuolisen auditoijan tekemä riippumaton varmennus.

## 2. Keskeiset toteutetut ominaisuudet

- Käyttäjän rekisteröityminen, kirjautuminen, uloskirjautuminen ja profiilin hallinta.
- Omien tukipyyntöjen luominen, tarkastelu, priorisointi ja sulkeminen.
- AI-chat, tallennettu keskusteluhistoria ja epäonnistuneen AI-vastauksen uudelleenyritys.
- Tukipyynnön luominen keskustelusta vasta käyttäjän tarkistuksen ja vahvistuksen jälkeen (US-09).
- Etusivun omien tukipyyntöjen yhteenveto: kokonaismäärä sekä OPEN- ja CLOSED-määrät (US-14).
- Suomen- ja englanninkielinen käyttöliittymä.
- RAG-haku rajatusta Markdown/TXT-dokumenttikokoelmasta avainsanoilla; lähdetiedot näytetään löydösten yhteydessä.
- Docker Compose -käynnistys frontendille, backendille, MySQL:lle, Redisille ja Ollamalle sekä valitulle paikalliselle mallille.

## 3. Testaus ja hyväksynnän näyttö

Projektidokumentaatioon kirjattu 05.11.2026 tilanne:

- Toteuttaja vahvisti kaikkien käyttäjätarinoiden US-01–US-17 hyväksymiskriteerien käytännön hyväksynnän.
- Koko Docker Compose -kokonaisuus käynnistettiin tyhjillä MySQL- ja Ollama-volyymeilla.
- Rekisteröitymisen ja kahdeksan rinnakkaisen kirjautumisen integraatiotesti läpäisi paikallisessa Compose/MySQL-ympäristössä.
- README:n mukaan backendin 86 testistä 85 läpäisi ja yksi valinnainen MySQL-integraatiotesti ohitettiin normaalissa ajossa; erikseen ajettu integraatiotesti läpäisi.
- Frontendin lint, TypeScript-tarkistus ja tuotantobuild onnistuivat.

Testitulokset kuvaavat dokumentoitua testaushetkeä. Ne eivät takaa virheettömyyttä kaikissa laite-, käyttöjärjestelmä- tai verkkoympäristöissä. AI-mallin vastausten laatu ja RAG-haun kattavuus ovat rajallisia ja riippuvat mallista, kysymyksen muotoilusta sekä käytettävissä olevista dokumenteista.

## 4. Tietoturvan yhteenveto

### Toteutettu projektissa

- Palvelinpuolen istunnot MySQL:ssä; allekirjoitettu eväste, HttpOnly, SameSite=Lax ja konfiguroitava Secure.
- Salasanojen scrypt-tiivistys ja satunnaiset suolat.
- Kirjautumisen Redis-pohjainen käyttörajoitus.
- Backendin omistajuustarkistukset tukipyynnöille ja keskusteluille.
- CORS- ja luotetun Originin tarkistukset osassa tilaa muuttavista pyynnöistä.
- Docker Compose -ympäristössä tietokanta ja Redis eivät julkaise host-portteja; palveluiden portit on rajattu paikalliseen loopback-käyttöön.

### Tietoturvahaaraan lisätty, mutta vielä testaamatta

Erillisessä haarassa `security/hardening-demo` on lisätty keskitetty Origin-tarkistus istuntoevästeen sisältäville tilaa muuttaville API-pyynnöille, rekisteröinnin IP-kohtainen käyttörajoitus, globaali AI-generoinnin lukko, yksityisten API-vastausten `no-store`-välimuistiasetus ja perustason tietoturvaotsakkeet. Muutoksia ei ole vielä varmennettu ajamalla testejä todellisessa Compose/MySQL/Redis-ympäristössä, eikä niitä pidä merkitä tuotannossa testatuiksi ennen tätä.

### Puutteet ja riskit LAN/WAN-käytössä

- Todellista kahden laitteen LAN-käyttöä, reverse proxyn IP-välitystä ja HTTPS-käyttöönottoa ei ole varmennettu.
- Nykyinen Compose on kehitys-/demoympäristö, ei valmis tuotantoratkaisu.
- WAN-käyttö edellyttäisi tuotantofrontendia, HTTPS-reverse proxya, palomuuria, sisäisten palveluiden eristystä ja tuotantokäyttöönoton erillistä tietoturvakatsausta.
- Tuotantokonttien vähimmät käyttöoikeudet, riippuvuuksien ja kuvien lukitus, pyyntökokojen rajat, kattava CSP, tuotannon API-dokumentaation sulkeminen, lokien valvonta ja palautusharjoitukset vaativat lisätyötä.
- Täydellistä kahden käyttäjän IDOR-testimatriisia ja riippumatonta penetraatiotestausta ei ole osoitettu.
- AI:n vastaukset voivat olla virheellisiä; paikallinen malli ja RAG eivät takaa ongelman ratkeamista.

Yksityiskohtaiset kontrollit, LAN/WAN-vaatimukset ja varmennettavat asiat on kuvattu erillisissä suomen- ja englanninkielisissä tietoturvadokumenteissa.

## 5. Avoimet toimitus- ja ylläpitoasiat

- Kolmansien osapuolten lisensseistä on tehty alustava inventointi, mutta projektin oman lisenssin valinta ja mahdolliset jakelukohtaiset toimet ovat avoinna.
- Todellinen LAN-verkkotestaus on tehtävä siinä ympäristössä, jossa sovellusta aiotaan käyttää.
- WAN-julkaisu ei kuulu kouluprojektin hyväksyttyyn toimituslaajuuteen.
- Tietoturvahaara on testattava ja arvioitava erikseen ennen mahdollista yhdistämistä päähaaraan.

## 6. Kokonaisarvio

Projektin dokumentoidun hyväksyntätilanteen perusteella kouluprojektin sovittu toiminnallinen laajuus US-01–US-17 on toteuttajan mukaan hyväksytty. Sovellus sisältää keskeisen tukipyyntöprosessin, AI-keskustelun, dokumenttihakuun perustuvan RAG-toiminnon, kaksikielisen käyttöliittymän ja toistettavan Docker Compose -kehitys-/demoympäristön.

**Hyväksyntä koskee kouluprojektin sovittua toiminnallista laajuutta ja dokumentoitua paikallista testausympäristöä. Se ei tarkoita, että sovellus olisi valmis tuotantokäyttöön LAN- tai WAN-verkossa tai että se olisi riippumattomasti tietoturva-auditoitu.**

