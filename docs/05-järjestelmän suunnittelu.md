# AI HelpDesk – Järjestelmän suunnittelu

## 1. Johdanto

### 1.1 Dokumentin tarkoitus

Tämä dokumentti kuvaa AI HelpDesk -sovelluksen teknisen suunnittelun. Se määrittelee järjestelmän arkkitehtuurin, tietokannan rakenteen, tietokannan entiteettien väliset suhteet, REST-rajapinnan sekä käyttöliittymän keskeiset näkymät.

Suunnittelun tavoitteena on luoda selkeä ja ylläpidettävä rakenne, joka tukee sovelluksen keskeisiä toimintoja:

- Käyttäjien rekisteröityminen ja kirjautuminen.
- Käyttäjäprofiilin hallinta.
- Tukipyyntöjen luominen ja hallinta.
- Tekoälypohjainen keskustelu.
- Keskusteluviestien pysyvä tallentaminen.
- Tukipyynnön luominen keskustelun perusteella.
- Tietopohjainen tekoälyneuvonta, jossa Knowledge Service hakee keskusteluun liittyvää teknistä dokumentaatiota.
- Suomen- ja englanninkielinen käyttöliittymä.
- Frontendin, backendin, MySQL-tietokannan, Redisin ja Ollama-tekoälypalvelun käynnistäminen Docker Composella yhdellä komennolla.
- Tukipyynnön luominen keskustelusta vasta käyttäjän tarkistuksen ja vahvistuksen jälkeen sekä omien tukipyyntöjen rajattu yhteenveto.

### 1.2 Järjestelmän tavoitteet

AI HelpDesk -sovelluksen tavoitteena on tarjota käyttäjälle yksi palvelu, jossa teknisiä ongelmia voidaan ratkaista tekoälyn avulla ja tarvittaessa siirtää ratkaisemattomat ongelmat tukipyyntöjen käsittelyyn.

Järjestelmän tulee olla:

- **Turvallinen:** käyttäjä voi käsitellä vain tietoja, joihin hänellä on oikeus.
- **Ylläpidettävä:** käyttöliittymä, backend, tietokanta ja tekoälyintegraatio ovat selkeästi erotettuja.
- **Laajennettava:** uusia toimintoja voidaan lisätä ilman koko järjestelmän uudelleensuunnittelua.
- **Luotettava:** virhetilanteet käsitellään hallitusti ja käyttäjälle annetaan ymmärrettävä palaute.
- **Testattava:** keskeisille toiminnoille voidaan toteuttaa yksikkö- ja integraatiotestit.

### 1.3 Käyttäjäroolit

| Rooli | Kuvaus |
|---------|---------|
| Rekisteröitynyt käyttäjä | Hallitsee profiiliaan, keskustelee tekoälyn kanssa ja hallitsee omia tukipyyntöjään. |
| Sovelluksen kehittäjä | Toteuttaa, testaa, ylläpitää ja dokumentoi järjestelmää. |

Kehittäjärooli kuvaa projektin teknistä vastuuta eikä automaattisesti tarkoita erillistä sovelluksen ylläpitäjäroolia.

---

## 2. Järjestelmän arkkitehtuuri

### 2.1 Arkkitehtuurin yleiskuvaus

AI HelpDesk toteutetaan kerroksittaisena web-sovelluksena. Frontend vastaa käyttöliittymästä, backend liiketoimintalogiikasta ja tietoturvatarkistuksista sekä tietokanta pysyvästä tallennuksesta. Tekoälypalvelua käytetään teknisten ongelmien analysointiin ja ratkaisuehdotusten tuottamiseen.

![Järjestelmän looginen arkkitehtuuri: frontend, backend, tietokanta, tekoälypalvelu ja dokumentaatiohaku](../photos/system%20architecture.png)

Arkkitehtuurikuva säilyy rakenteeltaan ennallaan. Valitut lisäominaisuudet näkyvät siinä ja toteutuksen rajauksessa seuraavasti:

- **RAG:** Chat Service hyödyntää Knowledge Serviceä, joka hakee avainsanoilla rajatusta Markdown- ja TXT-dokumenttikokoelmasta. Löydetty sisältö ja todelliset lähdetiedot välitetään AI Servicelle ja näytetään vastauksen yhteydessä. Jos sopivaa sisältöä ei löydy, vastausta ei esitetä dokumentaation vahvistamana. Semanttinen haku ei kuulu MVP:hen, ja sitä harkitaan vain testinäytön perusteella.
- **Monikielisyys:** Frontendin käyttöliittymätekstit ovat saatavilla suomeksi ja englanniksi. Kielivalinta säilytetään selaimessa; tekoälyn vastauskieli määräytyy keskustelun kielen ja agentin kieliohjeiden mukaan.
- **Docker Compose:** frontend, backend, MySQL ja Ollama käynnistetään README:ssä dokumentoidulla yhdellä komennolla. Ollama käyttää valittua GGUF-mallia Docker-ympäristössä, eikä AI-palvelun suorittaminen riipu host-koneelle asennetusta Ollamasta.
- **Autentikointi:** rekisteröityminen sekä kirjautuminen ja uloskirjautuminen ovat käytössä. Kirjautumisistunnot tallennetaan MySQL:ään ja kirjautumisyritysten käyttörajat Redisissä.
- **Proxy ja IP-käyttöraja:** kehityksen Compose-ympäristössä frontend käyttää vain erillistä proxy-verkkoa, jonka IP on `172.30.0.2`, ja välittää `/api`-pyynnöt backendille verkkoaliaksella `backend-proxy`. Backend lukee `X-Forwarded-For`-otsakkeen vain, kun suora yhteyden peer-osoite kuuluu `TRUSTED_PROXY_IPS`-asetuksella määritettyyn luotettuun IP-verkkoon. Ketjua käsitellään oikealta vasemmalle; luotetut proxy-hopit ohitetaan ja ensimmäistä luottamatonta osoitetta käytetään asiakkaan IP-osoitteena. Muiden peerien välittämää otsaketta ei käytetä.
- **Toimituslaajuus:** US-09 ja US-14 ovat virallisia käyttäjätarinoita. Tukipyyntö luodaan keskustelusta vain käyttäjän tarkistuksen ja vahvistuksen jälkeen; yhteenveto näyttää vain käyttäjän omat kokonais-, `OPEN`- ja `CLOSED`-määrät.

### 2.2 Frontend

Frontend tarjoaa käyttäjälle visuaalisen käyttöliittymän ja välittää käyttäjän toiminnot backendille REST-rajapinnan kautta.

#### Frontendin vastuut

- Rekisteröitymis- ja kirjautumisnäkymät.
- Käyttäjäprofiilin tarkastelu ja päivittäminen.
- Tukipyyntöjen luominen, tarkastelu ja sulkeminen.
- Tekoälykeskustelun näyttäminen.
- Keskusteluhistorian näyttäminen.
- Lomakkeiden syötteiden alustava validointi.
- Onnistumis- ja virheilmoitusten näyttäminen.
- Suomen- ja englanninkielisen käyttöliittymän tukeminen.

Frontend ei vastaa käyttöoikeuksien lopullisesta tarkistamisesta. Kaikki suojattujen tietojen käsittelyä koskevat tarkistukset tehdään backendissä.

### 2.3 Backend

Backend tarjoaa REST-rajapinnan ja toteuttaa sovelluksen liiketoimintalogiikan.

#### Backendin vastuut

- Käyttäjien rekisteröityminen ja kirjautuminen.
- Autentikointi ja käyttöoikeuksien tarkistaminen.
- Pyyntöjen validointi.
- Tukipyyntöjen ja keskusteluviestien käsittely.
- Tietojen lukeminen ja tallentaminen tietokantaan.
- Tekoälypalvelun kutsuminen ja vastausten käsittely.
- Virhetilanteiden hallinta.
- Rajapinnan yhtenäisten HTTP-vastausten palauttaminen.

#### Backendin loogiset komponentit

| Komponentti | Vastuu |
|------------|---------|
| Auth Service | Käyttäjän tunnistaminen ja käyttöoikeudet |
| User Service | Profiilitietojen hallinta |
| Ticket Service | Tukipyyntöjen luominen ja päivittäminen |
| Chat Service | Keskustelujen ja viestien käsittely |
| AI Service | Tekoälypalvelun integraatio |
| Knowledge Service | Teknisen dokumentaation haku RAG-vastauksia varten |

Nämä ovat loogisia komponentteja, eivät välttämättä erillisiä palvelimia tai mikropalveluita.

### 2.4 Tietokanta

Järjestelmän ensisijaisena relaatiotietokantana käytetään MySQL-tietokantaa.

Tietokanta tallentaa:

- Käyttäjien tiedot.
- Aktiiviset kirjautumisistunnot ja niiden voimassaoloajat.
- Tukipyynnöt ja niiden tilat.
- Keskustelut.
- Keskusteluviestit.
- Tarvittavat luonti- ja päivitysajat.

Tietokannan viite-eheys varmistetaan pää- ja viiteavaimilla. Käyttäjäkohtaisissa hauissa käytetään tunnistetun käyttäjän omistajuuteen perustuvia suodatuksia.

### 2.5 Tekoälyintegraatio

AI Service välittää käyttäjän viestin Compose-ympäristössä toimivalle Ollama-palvelulle ja käsittelee saadun vastauksen. Käytettävä malli on `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`, jonka konfiguraatio on [Modelfile](../agents/Modelfile)-tiedostossa. Mallin kontekstipituus on 4096 ja lämpötila 0.2.

#### Tekoälyintegraation tulee

- Kutsua Ollamaa backendistä Compose-verkon sisäisellä palvelunimellä ja rajapinnalla; selain ei kutsu Ollamaa suoraan.
- Käynnistää Ollama Compose-palveluna ja varmistaa terveystarkistuksella, että palvelu sekä valittu malli ovat käytettävissä.
- Tuoda mallin GGUF-tiedosto Ollama-kontin saataville dokumentoidulla tavalla. Nykyinen suunnitteluratkaisu liittää `agents`-hakemiston mallitiedoston konttiin vain luku -tilassa; `Modelfile` käyttää kontissa polkua `/models/Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`.
- Luoda valitun mallin Ollamaan automaattisesti Compose-käynnistyksen yhteydessä `Modelfile`-tiedoston perusteella, jos mallia ei vielä ole Ollaman mallivarastossa.
- Säilyttää Ollaman mallivaraston pysyvässä Docker-volyymissa, jotta palvelun uudelleenkäynnistys ei edellytä mallin uutta manuaalista tuontia.
- Käsitellä aikakatkaisut, palveluvirheet ja käyttörajoitukset.
- Rajoittaa tekoälylle lähetettävän keskustelukontekstin määrää.
- Tallentaa keskusteluviestit sovelluksen määrittelemien tallennuskäytäntöjen mukaisesti.
- Välttää tarpeettomien henkilötietojen lähettämistä mallille.

Tekoälyn tuottamat vastaukset ovat ehdotuksia. Niiden oikeellisuutta ei voida taata kaikissa tilanteissa.

### 2.6 RAG MVP ja tietolähteet

Knowledge Service käsittelee ennen toteutusta ryhmän rajaamaa, käyttöön hyväksyttyä Markdown- ja TXT-dokumenttikokoelmaa. Tarkka lähdekokoelma ja sen ylläpitopaikka vahvistetaan ennen toteutusta; dokumentteja ei haeta ennalta määrittelemättömistä tai ulkoisista lähteistä.

MVP:n hakutapa on avainsanahaku. Palvelu hakee kysymykseen sopivia dokumenttikohtia, välittää löydetyt tekstikatkelmat ja lähdetiedot Chat Servicen kautta AI Servicelle sekä palauttaa lähdetiedot käyttöliittymän näytettäväksi. Hakutuloksen lähdetieto perustuu todelliseen tiedostoon ja löydettyyn kohtaan. Jos sopivaa kohtaa ei löydy, mallille ei anneta keksittyä lähdettä eikä vastausta esitetä dokumentaation vahvistamana.

Avainsanahaun laatua arvioidaan ennen toteutusta määritellyillä kysymyksillä ja dokumenteilla, mukaan lukien relevantin osuman ja osumattoman kyselyn testit. Semanttinen haku tai vektoritietokanta lisätään vasta, jos testitulokset osoittavat avainsanahaun riittämättömäksi ja muutos hyväksytään. RAG MVP:n dokumenttikokoelma ja hakutapa eivät edellytä ER-kaavion tai MySQL-skeeman muuttamista. Jos myöhemmin syntyy todellinen pysyvän uuden datan tarve, tietomalli ja ER-kaavio päivitetään erikseen muutoksenhallinnassa.

Malli, Ollama, Docker-kuvat ja muut työkalut sekä kirjastot tarkistetaan maksuttomuuden, lisenssien ja käyttöehtojen osalta ennen toimitusta. Mahdollisia lisenssiehtoja ei oleteta täytetyiksi ilman tarkistusta.

---

## 3. ER-diagrammi

### 3.1 Entiteetit ja niiden suhteet

Järjestelmän keskeiset entiteetit ovat User, Ticket, Conversation ja Message.

![DB construction](../photos/ER_AIHD.svg)

Kaavio on ylläpidetty muuttamattomana yleiskuvana tietokantatauluista ja niiden suhteista. Alla olevat taulukot täsmentävät kenttien nimet ja rajoitteet. Ne sisältävät myös `tickets.created_at`- ja `tickets.updated_at`-kentät, `conversations.created_at`- ja `conversations.updated_at`-kentät sekä `messages.created_at`-kentän, joita ei ole merkitty kaavioon. Tukipyynnön luontiaika vaaditaan FR-05:n täyttämiseksi; muut aikaleimat tukevat historian näyttämistä ja tietojen ylläpitoa.

### 3.2 Entiteettien kuvaukset

#### User

Sisältää käyttäjän tunnistamiseen ja profiiliin liittyvät tiedot. Sähköpostiosoite on yksilöllinen, ja salasana tallennetaan vain turvallisesti tiivistettynä.

#### Ticket

Sisältää tukipyynnön otsikon, kuvauksen, tilan, prioriteetin ja omistajan. Jokainen tukipyyntö kuuluu yhdelle käyttäjälle.

#### Conversation

Edustaa yhtä käyttäjän keskustelukokonaisuutta. Keskustelu kuuluu yhdelle käyttäjälle ja voi sisältää useita viestejä.

#### Message

Sisältää keskusteluun liittyvän yksittäisen viestin. Viestin rooli kertoo, onko kyse käyttäjän viestistä vai tekoälyn vastauksesta.

### 3.3 Kardinaliteetit

| Suhde | Kardinaliteetti | Kuvaus |
|---------|---------|---------|
| User – Ticket | User 1 → 0..N Ticket; Ticket 1 → 1 User | Käyttäjällä voi olla nolla tai useita tukipyyntöjä; jokaisella tukipyynnöllä on yksi omistaja. |
| User – Conversation | User 1 → 0..N Conversation; Conversation 1 → 1 User | Käyttäjällä voi olla nolla tai useita keskusteluja; jokainen keskustelu kuuluu yhdelle käyttäjälle. |
| Conversation – Ticket | Conversation 1 → 0..N Ticket; Ticket 0..1 → 1 Conversation | Keskustelusta voidaan luoda useita tukipyyntöjä; tukipyyntö voi olla itsenäinen tai liittyä yhteen keskusteluun. |
| Conversation – Message | Conversation 1 → 0..N Message; Message 1 → 1 Conversation | Keskustelussa voi olla nolla tai useita viestejä; jokainen viesti kuuluu yhteen keskusteluun. |

ER-diagrammi kuvaa MVP-version tietomallin ja pidetään ennallaan. RAG MVP käyttää tiedostopohjaista Markdown- ja TXT-dokumenttikokoelmaa avainsanahakuun eikä lisää tietokantaan dokumentti- tai hakutauluja. ER-skeemaa muutetaan vain, jos toteutuksessa syntyy erikseen perusteltu pysyvän uuden datan tarve.

---

## 4. Tietokannan suunnittelu

## 4.1 Yleiset tietokantaperiaatteet

1. Taulujen ensisijaiset avaimet ovat yksilöllisiä.
2. Viiteavaimet varmistavat taulujen väliset suhteet.
3. Sähköpostiosoitteelle asetetaan yksilöllisyysrajoite.
4. Pakolliset kentät määritellään `NOT NULL` -rajoitteilla.
5. Aikaleimat tallennetaan yhdenmukaisesti sovitulla aikavyöhykekäytännöllä, esimerkiksi UTC-ajassa.
6. Käyttäjien salasanat tallennetaan vahvalla salasanatiivisteellä.
7. Käyttäjän tiedot voidaan hakea sähköpostiosoitteen ja pääavaimen avulla.
8. Tukipyynnöt ja keskustelut haetaan käyttäjäkohtaisesti.
9. Tietokantayhteydet käyttävät parametrisoituja kyselyitä.

## 4.2 Taulu: users

| Sarake | Tietotyyppi | Rajoitteet | Kuvaus |
|----------|------------|------------|---------|
| id | BIGINT | PK, AUTO_INCREMENT | Käyttäjän tunniste |
| first_name | VARCHAR(100) | NOT NULL | Käyttäjän etunimi |
| last_name | VARCHAR(100) | NOT NULL | Käyttäjän sukunimi |
| username | VARCHAR(100) | NOT NULL, UNIQUE | Käyttäjänimi |
| email | VARCHAR(255) | NOT NULL, UNIQUE | Sähköpostiosoite |
| password_hash | VARCHAR(255) | NOT NULL | Salasanan tiiviste |
| created_at | DATETIME | NOT NULL | Luontiaika |
| updated_at | DATETIME | NOT NULL | Viimeisin päivitysaika |

Kirjautumisistunnot tallennetaan lisäksi tekniseen `auth_sessions`-tauluun. Taulussa on istunnon satunnainen tunniste, käyttäjän viiteavain sekä luonti- ja vanhenemisajat. Uloskirjautuminen poistaa kyseisen istunnon, jolloin myös kopioitu istuntoeväste lakkaa toimimasta. Tämä tekninen taulu ei kuulu nykyiseen käsitteelliseen ER-kaavioon.

## 4.3 Taulu: tickets

| Sarake | Tietotyyppi | Rajoitteet | Kuvaus |
|----------|------------|------------|---------|
| id | BIGINT | PK, AUTO_INCREMENT | Tukipyynnön tunniste |
| user_id | BIGINT | FK, NOT NULL | Tukipyynnön omistaja |
| conversation_id | BIGINT | FK, NULL | Tukipyynnön lähdekeskustelu, jos pyyntö luotiin keskustelusta |
| title | VARCHAR(200) | NOT NULL | Tukipyynnön otsikko |
| description | TEXT | NOT NULL | Ongelman kuvaus |
| status | VARCHAR(20) | NOT NULL | Tukipyynnön tila |
| priority | VARCHAR(20) | NOT NULL | Tukipyynnön prioriteetti |
| created_at | DATETIME | NOT NULL | Luontiaika |
| updated_at | DATETIME | NOT NULL | Viimeisin päivitysaika |
| closed_at | DATETIME | NULL | Sulkemisaika |

MVP:n tukipyynnön tilat ovat:

- `OPEN`
- `CLOSED`

`IN_PROGRESS` voidaan ottaa käyttöön myöhemmin, kun tukipalvelun käsittelyrooli ja tilan muutossäännöt määritellään.

Prioriteetit voivat olla:

- `LOW`
- `MEDIUM`
- `HIGH`

Sallitut arvot validoidaan backendissä ja tarvittaessa tietokannan rajoitteilla.

## 4.4 Taulu: conversations

| Sarake | Tietotyyppi | Rajoitteet | Kuvaus |
|----------|------------|------------|---------|
| id | BIGINT | PK, AUTO_INCREMENT | Keskustelun tunniste |
| user_id | BIGINT | FK, NOT NULL | Keskustelun omistaja |
| title | VARCHAR(200) | NULL | Keskustelun otsikko |
| created_at | DATETIME | NOT NULL | Luontiaika |
| updated_at | DATETIME | NOT NULL | Viimeisin päivitysaika |

Keskustelun otsikko voidaan määritellä käyttäjän ensimmäisen viestin perusteella tai antaa käyttäjän muokattavaksi myöhemmässä versiossa.

## 4.5 Taulu: messages

| Sarake | Tietotyyppi | Rajoitteet | Kuvaus |
|----------|------------|------------|---------|
| id | BIGINT | PK, AUTO_INCREMENT | Viestin tunniste |
| conversation_id | BIGINT | FK, NOT NULL | Viestin keskustelu |
| role | VARCHAR(20) | NOT NULL | Viestin lähettäjän rooli |
| content | TEXT | NOT NULL | Viestin sisältö |
| created_at | DATETIME | NOT NULL | Viestin luontiaika |

Viestin `role` voi olla esimerkiksi:

- `USER`
- `ASSISTANT`

Järjestelmän sisäisiä ohjeita tai työkaluviestejä varten tarvitaan erillinen, tarkemmin määritelty käsittely, jos sellaisia tallennetaan.

## 4.6 Indeksit ja viite-eheys

### Suositellut indeksit

| Taulu | Indeksi | Tarkoitus |
|---------|---------|---------|
| users | UNIQUE(email) | Nopeuttaa kirjautumista ja estää päällekkäiset sähköpostiosoitteet |
| tickets | INDEX(user_id, created_at) | Käyttäjän tukipyyntöjen hakeminen |
| tickets | INDEX(user_id, status) | Tukipyyntöjen haku tilan perusteella |
| tickets | INDEX(conversation_id) | Keskusteluun liittyvien tukipyyntöjen hakeminen |
| conversations | INDEX(user_id, updated_at) | Käyttäjän keskusteluhistorian hakeminen |
| messages | INDEX(conversation_id, created_at, id) | Keskusteluviestien hakeminen järjestyksessä |

Viiteavaimille määritellään tietojen poistamiseen ja päivittämiseen sopivat säännöt. Esimerkiksi käyttäjän poistamista ei tule toteuttaa siten, että siihen liittyvät tiedot jäävät tietokantaan hallitsemattomasti.

Käyttäjän poistaminen ja keskusteluhistorian säilyttäminen tulee määritellä erikseen tietosuojan ja sovelluksen vaatimusten perusteella.

Kun tukipyyntö luodaan keskustelusta, `tickets.conversation_id` viittaa lähdekeskusteluun. Backend varmistaa, että keskustelu kuuluu samalle kirjautuneelle käyttäjälle kuin tukipyyntö. Itsenäisesti luodun tukipyynnön `conversation_id` on `NULL`.

## 4.7 Tietojen tallennuksen transaktiot

Tietokantaan liittyvät toiminnot toteutetaan tarvittaessa transaktioina.

Esimerkiksi tukipyynnön luomisessa järjestelmä:

1. Validoi käyttäjän lähettämät tiedot.
2. Tarkistaa käyttäjän tunnistamisen ja oikeudet.
3. Tallentaa tukipyynnön tietokantaan.
4. Palauttaa luodun tukipyynnön tunnisteen ja tiedot.

Keskusteluviestin tallennuksessa käyttäjän viesti ja tekoälyn vastaus käsitellään erillisinä tallennettavina tapahtumina. Tekoälypalvelun virhe ei saa aiheuttaa virheellistä tai keksittyä vastausta keskusteluhistoriaan.

---

## 5. REST API -suunnittelu

## 5.1 Yleiset periaatteet

REST API toimii frontendin ja backendin välisenä rajapintana.

### Rajapinnan periaatteet

1. Käytetään HTTP-protokollaa ja JSON-muotoista tiedonsiirtoa.
2. Käytetään resurssipohjaisia URL-osoitteita.
3. Suojatut endpointit edellyttävät autentikointia.
4. Backend validoi kaikki asiakkaalta tulevat tiedot.
5. Käyttäjän omistajuus ja käyttöoikeudet tarkistetaan jokaisessa suojatussa resurssipyynnössä.
6. Virhetilanteissa palautetaan tarkoituksenmukainen HTTP-statuskoodi.
7. Rajapinnan versio voidaan sisällyttää osoitteeseen, esimerkiksi `/api/v1`.
8. Istuntoevästeitä käyttävä selain lähettää pyyntöihin tunnistetiedot; backend sallii tunnistetiedot sisältävän CORS-pyynnön vain määritellystä frontend-alkuperästä eikä käytä tunnistetietojen kanssa yleistä `*`-alkuperää.

## 5.2 Endpointit

Alla olevista autentikointireiteistä rekisteröityminen, kirjautuminen, uloskirjautuminen ja nykyisen käyttäjän haku on toteutettu. Tukipyyntö-, keskustelu-, haku- ja profiilireitit kuvaavat suunniteltua rajapintaa eivätkä ole vielä toteutettuja.

### Autentikointi ja käyttäjätili

| HTTP-metodi | Endpoint | Kuvaus | Autentikointi |
|------------|----------|---------|--------------|
| POST | `/api/v1/auth/register` | Luo käyttäjätilin | Ei |
| POST | `/api/v1/auth/login` | Kirjaa käyttäjän sisään | Ei |
| POST | `/api/v1/auth/logout` | Kirjaa käyttäjän ulos ja mitätöi nykyisen istunnon, jos eväste on voimassa | Istuntoeväste |
| GET | `/api/v1/auth/me` | Palauttaa nykyisen kirjautuneen käyttäjän | Kyllä |
| GET | `/api/v1/users/me` | Hakee kirjautuneen käyttäjän profiilin | Suunniteltu |
| PATCH | `/api/v1/users/me` | Päivittää käyttäjän profiilin | Suunniteltu |

Autentikointi käyttää MySQL:ään tallennettua palvelinpuolen istuntoa. Sovelluksen käynnistyksessä SQLAlchemy luo puuttuvat mallien taulut riippuvuusjärjestyksessä, joten `users` luodaan ennen sitä viittaavaa `auth_sessions`-taulua. Eväste sisältää HMAC-allekirjoitetun käyttäjä-, vanhenemis- ja istuntotunnisteen; eväste on `HttpOnly` ja `SameSite=Lax`, ja sen voimassaolo on kahdeksan tuntia. `AUTH_COOKIE_SECURE` määrittää `Secure`-attribuutin: Compose käyttää oletuksena arvoa `true`; vain paikallisessa HTTP-kehityksessä `.env`-tiedostossa asetetaan `AUTH_COOKIE_SECURE=false`. HTTPS-tuotannossa asetus pidetään arvossa `true`. Uloskirjautuminen poistaa istunnon MySQL:stä ja evästeen selaimesta. Lisäksi uloskirjautumispyynnön `Origin`-otsakkeen on vastattava täsmälleen jotakin `FRONTEND_ORIGINS`-asetuksen alkuperää; puuttuva tai tuntematon alkuperä hylätään. Erillistä CSRF-tokenia ei käytetä.

Frontend käyttää oletuksena suhteellista `/api`-polkua. Viten kehityspalvelin proxyaa pyynnöt backendille, ja tuotanto-Nginx proxyaa saman polun backendille. Jos backend tarjotaan eri alkuperästä, `VITE_API_BASE_URL` voidaan asettaa build-vaiheessa backendin alkuperäosoitteeksi ilman `/api`-polkua.

Kirjautumista rajoitetaan Redisissä yhteisillä, atomisilla laskureilla: enintään viisi yritystä sähköpostiosoitetta kohti 15 minuutissa ja 20 yritystä IP-osoitetta kohti minuutissa. Rajan ylitys palauttaa `429 Too Many Requests`-vastauksen ja `Retry-After`-otsakkeen. Rajat tarkistetaan ennen salasanatiivisteen laskentaa; Redis-yhteyden virheessä kirjautuminen estetään ja palautetaan `503`. `X-Forwarded-For`-otsaketta käytetään IP:n tunnistamiseen vain, kun yhteys tulee `TRUSTED_PROXY_IPS`-asetuksessa määritetystä luotetusta proxysta. Ketjua luetaan oikealta vasemmalle luotetut proxy-hopit ohittaen; ensimmäinen luottamaton osoite toimii asiakkaan IP:nä. Vanhentuneet kirjautumisistunnot poistetaan erillisessä taustatehtävässä kerran tunnissa. Siivous hakee vanhentuneiden rivien tunnisteet ja poistaa ne erissä ensisijaisavaimen perusteella; kirjautumisen transaktiossa ei tehdä `expires_at`-aluepoistoa.

### Tukipyynnöt

| HTTP-metodi | Endpoint | Kuvaus | Autentikointi |
|------------|----------|---------|--------------|
| GET | `/api/v1/tickets` | Hakee kirjautuneen käyttäjän tukipyynnöt | Kyllä |
| POST | `/api/v1/tickets` | Luo uuden tukipyynnön | Kyllä |
| GET | `/api/v1/tickets/summary` | Hakee käyttäjän tukipyyntöjen yhteenvedon | Kyllä |
| GET | `/api/v1/tickets/{id}` | Hakee yksittäisen tukipyynnön | Kyllä |
| PATCH | `/api/v1/tickets/{id}` | Päivittää avoimen tukipyynnön otsikon, kuvauksen tai prioriteetin | Kyllä |
| POST | `/api/v1/tickets/{id}/close` | Sulkee tukipyynnön | Kyllä |

Staattinen `/summary`-reitti määritellään ennen dynaamista `{id}`-reittiä, jotta reititin ei tulkitse sanaa `summary` tukipyynnön tunnisteeksi.

### Keskustelut ja viestit

| HTTP-metodi | Endpoint | Kuvaus | Autentikointi |
|------------|----------|---------|--------------|
| GET | `/api/v1/conversations` | Hakee käyttäjän keskustelut | Kyllä |
| POST | `/api/v1/conversations` | Luo uuden keskustelun | Kyllä |
| GET | `/api/v1/conversations/{id}` | Hakee keskustelun tiedot | Kyllä |
| GET | `/api/v1/conversations/{id}/messages` | Hakee keskustelun viestit | Kyllä |
| POST | `/api/v1/conversations/{id}/messages` | Lähettää viestin tekoälykeskusteluun | Kyllä |
| POST | `/api/v1/conversations/{id}/tickets` | Luo tukipyynnön keskustelun perusteella | Kyllä |

### Tietopohjainen tekoälyneuvonta

| HTTP-metodi | Endpoint | Kuvaus | Autentikointi |
|------------|----------|---------|--------------|
| POST | `/api/v1/knowledge/search` | Hakee avainsanoilla Markdown- ja TXT-dokumenteista ja palauttaa osuman lähdetiedot | Kyllä |

### Rekisteröityminen

```http
POST /api/v1/auth/register
```

```json
{
  "first_name": "Example",
  "last_name": "User",
  "username": "exampleuser",
  "email": "user@example.com",
  "password": "example-password"
}
```

Onnistunut rekisteröityminen palauttaa HTTP 201 -vastauksen. Vastaus ei sisällä salasanaa eikä sen tiivistettä.

```json
{
  "user": {
    "id": 12,
    "first_name": "Example",
    "last_name": "User",
    "username": "exampleuser",
    "email": "user@example.com"
  }
}
```

## 5.3 Esimerkkipyyntö: kirjautuminen

### Request

```http
POST /api/v1/auth/login
```

```json
{
  "email": "user@example.com",
  "password": "example-password"
}
```

### Response

```json
{
  "id": 12,
  "first_name": "Example",
  "last_name": "User",
  "username": "exampleuser",
  "email": "user@example.com"
}
```

Onnistunut kirjautuminen palauttaa HTTP 200 -vastauksen ja `Set-Cookie`-otsakkeen. Virheelliset tunnukset palauttavat yleisen HTTP 401 -vastauksen; käyttörajan ylitys palauttaa HTTP 429 -vastauksen. `GET /api/v1/auth/me` palauttaa saman käyttäjäobjektin vain voimassa olevalle istunnolle.

## 5.4 Esimerkkipyyntö: tukipyynnön luominen

### Request

```http
POST /api/v1/tickets
```

```json
{
  "title": "Cannot connect to the network",
  "description": "The computer cannot connect to the office network."
}
```

### Response

```json
{
  "id": 101,
  "title": "Cannot connect to the network",
  "description": "The computer cannot connect to the office network.",
  "status": "OPEN",
  "priority": "MEDIUM",
  "created_at": "2026-10-22T14:00:00Z"
}
```

Backend johtaa omistajan kirjautuneesta istunnosta, asettaa uuden pyynnön tilaksi `OPEN` ja käyttää puuttuvalle prioriteetille oletusta `MEDIUM`. Asiakas ei voi asettaa omistajaa, alkuperäistä tilaa tai aikaleimoja. Jos pyyntö luodaan keskustelusta, backend tarkistaa keskustelun omistajuuden ja tallentaa sen tunnisteen `conversation_id`-kenttään.

MVP-versiossa käyttäjä voi sulkea oman avoimen tukipyyntönsä erillisellä `/close`-toiminnolla. Tällöin backend asettaa tilaksi `CLOSED` sekä päivittää `closed_at`- ja `updated_at`-aikaleimat. `PATCH` sallii vain otsikon, kuvauksen ja prioriteetin päivittämisen avoimessa pyynnössä; se ei salli tilan, omistajan, tunnisteiden tai aikaleimojen muuttamista. `IN_PROGRESS` varataan myöhempään laajennukseen, jossa tukipalvelurooli tai muu määritelty käsittelyprosessi muuttaa tilaa.

## 5.5 Esimerkkipyyntö: keskusteluviestin lähettäminen

### Request

```http
POST /api/v1/conversations/25/messages
```

```json
{
  "content": "My application crashes when I open it."
}
```

### Response

```json
{
  "message": {
    "id": 501,
    "role": "USER",
    "content": "My application crashes when I open it."
  },
  "assistant_message": {
    "id": 502,
    "role": "ASSISTANT",
    "content": "Which operating system and application version are you using?"
  }
}
```

## 5.6 HTTP-statuskoodit

| Statuskoodi | Merkitys | Käyttötapaus |
|-------------|-----------|-------------|
| 200 OK | Pyyntö onnistui | Tietojen haku tai päivitys |
| 201 Created | Resurssi luotiin | Käyttäjä, tukipyyntö tai keskustelu |
| 204 No Content | Toiminto onnistui ilman vastaussisältöä | Uloskirjautuminen |
| 400 Bad Request | Pyyntö on virheellinen | Virheellinen pyyntörakenne |
| 401 Unauthorized | Käyttäjä ei ole tunnistautunut | Puuttuva tai virheellinen autentikointi |
| 403 Forbidden | Toiminto ei ole sallittu | Käyttäjällä ei ole tarvittavia oikeuksia |
| 404 Not Found | Resurssia ei löydy | Tuntematon resurssi |
| 409 Conflict | Tietojen välillä on ristiriita | Käytössä oleva sähköpostiosoite |
| 422 Unprocessable Content | Validointi epäonnistui | Virheelliset kenttäarvot |
| 429 Too Many Requests | Pyyntöjä on liikaa | Rate limiting |
| 500 Internal Server Error | Odottamaton palvelinvirhe | Käsittelemätön virhe |
| 502 Bad Gateway | Ulkoisen palvelun virhe | Tekoälypalvelun virhe |

## 5.7 Rajapinnan tietoturva

1. Salasanat tiivistetään turvallisella salasanatiivistealgoritmilla.
2. Autentikointi toteutetaan turvallisella istunto- tai token-mekanismilla.
3. HTTPS on pakollinen tuotantoympäristössä.
4. Backend tarkistaa käyttäjän oikeudet ennen resurssien palauttamista tai muuttamista.
5. Syötteet validoidaan palvelinpuolella.
6. Tietokantakyselyissä käytetään parametrisoituja kyselyitä.
7. Kirjautumisyrityksiä rajoitetaan Redisissä asiakkaan IP-osoitteen ja normalisoidun sähköpostiosoitteen perusteella; raja palauttaa HTTP 429 -vastauksen ja `Retry-After`-otsakkeen. IP-osoite otetaan välitetystä otsakkeesta vain suoraan yhdistetyn, erikseen luotetuksi määritetyn proxyn tapauksessa. Luotetut proxy-verkot määritetään `TRUSTED_PROXY_IPS`-ympäristömuuttujassa pilkuin eroteltuina IP-osoitteina tai CIDR-verkkoina. Proxy-ketjussa luotetut hopit ohitetaan oikealta vasemmalle, ja ensimmäistä luottamatonta osoitetta käytetään asiakkaana. Proxyn on lisättävä tai korvattava välitystieto turvallisesti; luottamattoman yhteyden lähettämää `X-Forwarded-For`-otsaketta ei pidä hyväksyä asiakkaan IP:nä.
8. API-avaimia ja muita salaisuuksia ei tallenneta lähdekoodiin.
9. Virhelokeihin ei tallenneta salasanoja, autentikointitunnuksia tai tarpeettomia henkilötietoja.
10. Tekoälypalvelulle lähetetään vain pyynnön käsittelyn kannalta tarpeelliset tiedot.