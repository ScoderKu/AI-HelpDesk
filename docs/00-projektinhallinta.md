# AI HelpDesk – Projektinhallinta

> **Dokumentin tarkoitus:** toimia projektin yhteisenä ohjausdokumenttina. Tämä dokumentti kuvaa projektin tavoitteet, rajauksen, aikataulun, vastuut, riskit, riippuvuudet, seurannan ja muutostenhallinnan. Yksityiskohtaiset vaatimukset, käyttäjätarinat ja toteutustehtävät määritellään niille tarkoitetuissa dokumenteissa.

## 1. Projektin perustiedot

| Tieto | Kuvaus |
|---|---|
| Projektin nimi | AI HelpDesk |
| Projektin tyyppi | Opiskelijaprojekti |
| Projektin tavoitekesto | 5 viikkoa |
| Suunniteltu työmäärä | Vähintään 20 tuntia viikossa, yhteensä noin 100 tuntia |
| Kehitysmalli | Scrumista sovellettu iteratiivinen työskentely |
| Versionhallinta | Git ja GitHub |
| Projektin vastuuhenkilö | **Khoi Nguyen** |
| Keskeiset sidosryhmät | Projektin toteuttaja, opettaja ja sovelluksen loppukäyttäjät |
| Dokumentin tila | Elävä dokumentti; päivitetään projektin edetessä |

**Nykytilanne 26.10.2026:** vaatimusmäärittely, käyttäjätarinat hyväksymiskriteereineen, Product Backlog, Sprint-suunnitelma, järjestelmän suunnittelu ja UX/UI-suunnittelu on yhtenäistetty ennen toteutuksen aloittamista. `backend`- ja `frontend`-hakemistoissa ei vielä ole sovelluksen lähdekooditiedostoja. Toteutuksen edistyminen päivitetään jatkossa seurantaan ja GitHub-tehtäviin, ei tämän tilannekuvauksen kautta.

## 2. Projektin tarkoitus ja tavoitteet

AI HelpDesk on verkkosovellus, jonka avulla käyttäjä voi pyytää apua tietotekniikkaan ja ohjelmistokehitykseen liittyvissä ongelmissa. Käyttäjä voi keskustella tekoälyn kanssa, saada ongelmanratkaisuehdotuksia ja tallentaa ratkaisemattoman ongelman tukipyynnöksi.

Projektin tavoitteet ovat:

1. Toteuttaa toimiva verkkosovellus, jossa on käyttöliittymä, backend, REST-rajapinta ja relaatiotietokanta.
2. Mahdollistaa käyttäjän rekisteröityminen, kirjautuminen ja omien profiilitietojen hallinta.
3. Mahdollistaa tukipyyntöjen luominen, tarkastelu ja sulkeminen sekä tietojen tallentaminen tietokantaan.
4. Tarjota tekoälypohjainen keskustelu, jossa käyttäjä voi kuvata ongelmansa ja saada ehdotuksia sen ratkaisemiseksi.
5. Tallentaa keskusteluviestit ja mahdollistaa tukipyynnön luominen keskustelun perusteella käyttäjän tarkistuksen ja vahvistuksen jälkeen.
6. Toteuttaa kirjautuneelle käyttäjälle tukipyyntöjen rajatun yhteenvedon: kokonaismäärä sekä `OPEN`- ja `CLOSED`-tilojen määrät.
7. Toteuttaa lopulliseen julkaisuun kolme valittua lisäominaisuutta:
   - tietopohjainen tekoälyneuvonta (RAG)
   - suomen- ja englanninkielinen käyttöliittymä
   - sovelluksen ja Ollama-tekoälypalvelun käynnistäminen Docker Composella yhdellä dokumentoidulla komennolla.
8. Toteuttaa projekti GitHub-versionhallintaa ja soveltuvin osin Scrum-käytäntöjä hyödyntäen.
9. Tuottaa tekninen dokumentaatio, testitulokset ja sovelluksen esittely.

Projektin onnistumista arvioidaan toimivan ohjelmiston ja hyväksymiskriteerien lisäksi dokumentaation, testauksen, versionhallinnan ja projektin esittelyn perusteella.

## 3. Projektin laajuus

### 3.1 Projektin sisältö

Projektin suunniteltuun laajuuteen kuuluvat:

- käyttäjän rekisteröityminen ja kirjautuminen
- käyttäjäprofiilin tarkastelu ja muokkaaminen
- tukipyyntöjen luominen, tarkastelu ja sulkeminen
- tukipyyntöjen tilan ja prioriteetin tallentaminen
- tekoälypohjainen chat ja tarkentavat kysymykset
- keskusteluviestien tallentaminen
- REST-rajapinta
- MySQL-tietokanta nykyisen järjestelmäsuunnitelman mukaisesti
- RAG-pohjainen neuvonta rajatusta Markdown- ja TXT-dokumenttikokoelmasta avainsanahaulla; semanttinen haku voidaan lisätä vain, jos testinäyttö osoittaa avainsanahaun riittämättömäksi
- käyttöliittymän suomen- ja englanninkieliset tekstit
- Docker Compose -käyttöönotto frontendille, backendille, MySQL-tietokannalle ja Ollama-tekoälypalvelulle
- paikallisen `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`-mallin käyttö Ollama-kontissa
- automaattiset tai toistettavat testit keskeisille toiminnoille
- README, API-dokumentaatio, tietokantakuvaus/ER-kaavio, kuvakaappaukset ja esittely.
- maksuttomien työkalujen ja kirjastojen käyttö sekä niiden lisenssien ja käyttöehtojen tarkistaminen ennen valintaa ja toimitusta.

### 3.2 Rajauksen ulkopuolelle jäävät asiat

Seuraavat ominaisuudet eivät kuulu sovittuun ydinsisältöön, ellei niitä hyväksytä erikseen muutoksenhallinnan kautta:

- äänen syöttö tai puhevastaukset
- PDF-raporttien luominen
- laaja yritystason IT-palvelunhallinta
- yliopiston keskitettyyn tunnistautumiseen integrointi
- käyttäjän tietokoneella suoritettavien komentojen automaattinen suorittaminen
- täysin itsenäinen ongelmanratkaisu ilman käyttäjän osallistumista
- laajat organisaatioiden väliset käyttöoikeudet ja integraatiot.

`US-09` ja `US-14` kuuluvat viralliseen toimituslaajuuteen. US-09 mahdollistaa tukipyynnön luomisen AI-keskustelusta vasta sen jälkeen, kun käyttäjä on tarkistanut ja vahvistanut ehdotetut tiedot. US-14 näyttää vain kirjautuneen käyttäjän tukipyyntöjen kokonaismäärän sekä `OPEN`- ja `CLOSED`-tilojen lukumäärät; siihen eivät kuulu kaaviot, suodatukset, aikavertailut tai muiden käyttäjien tiedot. Nämä ovat virallisia käyttäjätarinoita eivätkä valinnaisia lisäominaisuuksia.

`US-16`-tarinan 5 Story Pointin arvio kattaa frontendin, backendin, MySQL:n ja Ollaman Compose-palvelut, valitun mallin käyttöönoton Ollama-kontissa, esimerkkikonfiguraation, pysyvän tallennuksen, valmiustarkistukset sekä dokumentoinnin ja käynnistyksen testauksen. Tuotantoympäristön käyttöönotto ja orkestrointi eivät kuulu tähän rajaukseen. Sprint 1:n sisältö ja 33 SP:n suunnitelma säilyvät ennallaan.

### 3.3 Laajuuden hallinnan periaate

Viiden viikon aikaraja ja sovittu toimituslaajuus muodostavat projektin lähtökohdan. Jos aikataulu tai työmäärä uhkaa ylittyä, poikkeama kirjataan ja sen vaikutukset arvioidaan yhdessä projektin tavoitteiden ja hyväksymiskriteerien kanssa. US-09, US-14 ja kolme valittua lisäominaisuutta ovat virallisia toimitussitoumuksia; niitä ei poisteta tai rajata hiljaisesti. Mahdollinen muutos edellyttää muutostenhallinnan mukaista nimenomaista päätöstä. Sprint 1:n sisältöä ja suunnitelmaa ei muuteta.

## 4. Roolit ja vastuut

Projekti toteutetaan opiskelijaprojektina. Minä hoidan useita rooleja; roolien nimeäminen auttaa kuitenkin pitämään vastuut selkeinä.

| Rooli | Vastuu |
|---|---|
| Projektin toteuttaja / Developer | Suunnittelee, toteuttaa, testaa ja dokumentoi sovelluksen sekä ylläpitää GitHub-repositorya. |
| Product Owner -vastuu | Priorisoi Product Backlogin ja tekee ehdotukset laajuuden muutoksista projektin tavoitteiden perusteella. Opiskelija hoitaa tämän vastuun, ellei opettaja määrää muuta. |
| Scrum Master -vastuu | Suunnittelee viikoittaisen työskentelyn, seuraa esteitä ja arvioi Sprintin lopputulosta. Opiskelija soveltaa käytäntöjä omaan työskentelyynsä. |
| Testausvastuu | Laatii testit, suorittaa ne ja kirjaa havaitut virheet sekä testitulokset. |
| Opettaja | Arvioi työn tehtävänannon ja sovittujen arviointikriteerien perusteella sekä antaa tarvittaessa palautetta. Ei oleteta päivittäiseksi projektin päätöksentekijäksi. |
| Loppukäyttäjä | Antaa näkökulman sovelluksen käytettävyyteen ja tarpeisiin; käyttäjärooli kuvataan vaatimuksissa ja käyttäjätarinoissa. |

Git-haaroja ja Pull Requesteja käytetään mahdollisuuksien mukaan versionhallinnan ja tarkasteluprosessin harjoitteluun; käytännöt pidetään projektin kokoon nähden kevyinä.

## 5. Aikataulu ja välitavoitteet

Projektin tavoitekesto on viisi viikkoa. Alla olevat M1–M5-välitavoitteet ovat viikkokohtaisia tavoitetuloksia. Product Backlogin ja Sprint-suunnitelman viiden Sprintin jako pidetään sovitun mukaisena; Sprinttien tarkka kesto ja viikkotavoitteiden suhde Sprintteihin vahvistetaan Sprint Planningissa. Viralliseen toimituslaajuuteen kuuluvia käyttäjätarinoita ei poisteta hiljaisesti kapasiteettiriskin perusteella.

| Välitavoite | Ajankohta | Keskeinen työ | Valmistumisen näyttö |
|---|---|---|---|
| M1 – Suunnittelu ja tekninen perusta | Viikko 1 | Vaatimusten ja backlogiin tutustuminen, arkkitehtuuri- ja tietomalliratkaisujen tarkentaminen, repositoryn käytännöt, Docker Composen perusrakenne Ollamalle ja valitulle mallille | Dokumentoidut arkkitehtuuriratkaisut ja käynnistettävä kehitysympäristö palveluineen tai selkeästi kirjattu tekninen este |
| M2 – Backend, tietokanta ja käyttäjähallinta | Viikko 2 | Tietokantamalli, yhteys tietokantaan, REST-rajapinnan perusrakenne, rekisteröityminen ja kirjautuminen | Tietokanta toimii ja käyttäjähallinnan keskeiset testit läpäistään |
| M3 – Tukipyyntöjen ydinkulku | Viikko 3 | Tukipyyntöjen luonti, omien pyyntöjen tarkastelu ja sulkeminen, käyttöoikeuksien tarkistukset, keskustelun tekninen perusta | Käyttäjä pystyy kirjautuneena hallitsemaan omia tukipyyntöjään |
| M4 – AI-chat ja käyttöliittymän kielet | Viikko 4 | Ollama-integraation käyttö sovelluksesta, keskusteluviestien tallennus, tarkentavat kysymykset, suomen- ja englanninkielinen käyttöliittymä; RAG:n tekninen kokeilu | AI-chat toimii hallitusti ja kielivalinta on testattu; RAG:n rajattu Markdown/TXT-lähdekokoelma on vahvistettu |
| M5 – RAG, integrointi ja toimitusvalmius | Viikko 5 | Avainsanahaku rajatusta dokumenttikokoelmasta, Docker Compose -kokonaisuuden tarkistus, regressiotestaus, dokumentaatio ja demo | RAG, monikielisyys ja Docker Compose Ollamineen on todennettu sovitussa laajuudessa; US-09 ja US-14 sekä README, API-dokumentaatio, ER-kaavio ja demo ovat valmiit |

**Aikataulun tarkennus:** sovitussa jaossa `US-16` (Docker Compose, mukaan lukien Ollama ja valittu malli) on Sprint 1:ssä, `US-09`, `US-13` ja `US-14` Sprint 4:ssä sekä `US-15` (RAG avainsanahaulla) Sprint 5:ssä. RAG:n lähdekokoelmaa ja testikysymyksiä voidaan valmistella aiemmin. Tämä Sprint-jako ei yksinään määritä Sprinttien kestoa.

Sprintin tavoite on suunnitelma, ei lupaus siitä, että jokainen tehtävä valmistuu hinnalla millä hyvänsä. Jos työmääräarviot tai tekniset esteet muuttuvat, Product Backlog ja jäljellä olevat tavoitteet tarkistetaan.

## 6. Keskeiset riippuvuudet

| Kohde | Riippuvuus | Hallintatapa |
|---|---|---|
| Käyttäjähallinta | Tietomalli, tietokantayhteys, salasanan turvallinen käsittely ja autentikointi | Toteutetaan ja testataan ennen suojattujen toimintojen laajentamista |
| Tukipyyntöjen hallinta | REST-rajapinta, tietokanta ja kirjautuneen käyttäjän tunnistaminen | Testataan sekä omistajan oikeudet että luvattoman käytön estäminen |
| Keskusteluhistorian tallennus | Keskustelun ja viestien tietomalli sekä tietokantayhteys | Määritellään viestien ja keskustelujen väliset suhteet arkkitehtuurivaiheessa |
| AI-chat | Backendin yhteys Docker Compose -ympäristössä toimivaan Ollamaan ja valittuun GGUF-malliin | Tehdään integraatiokoe varhaisessa vaiheessa; testataan mallin lataus, valmis-tila ja palveluvirheet |
| RAG | AI-chat, ennen toteutusta rajattu Markdown/TXT-lähdekokoelma ja avainsanahaku | Määritellään testikysymykset; testataan relevantti osuma, lähdetiedot ja osumaton kysely |
| Monikielinen käyttöliittymä | Käyttöliittymän tekstien erottaminen kieliresursseihin | Sovitaan kielivalinnan tallennustapa ja testataan tärkeimmät näkymät molemmilla kielillä |
| Docker Compose | Frontendin, backendin, MySQL:n, Ollaman ja mallin käynnistysasetukset, ympäristömuuttujat, pysyvä tallennus ja verkkoyhteydet | Testataan palvelut ja backendin sisäinen Ollama-yhteys yhdessä; kirjataan yksi toistettava käynnistyskomento |
| Lopullinen toimitus | Testitulokset, dokumentaatio ja käynnistysprosessin toimivuus | Varaa viimeiseen Sprintiin aikaa koko sovelluksen läpikäyntiin ja puuttuvien kohtien korjaamiseen |

Riippuvuus ei aina tarkoita, että koko edeltävän toiminnon pitää olla valmis ennen seuraavan aloittamista. Esimerkiksi RAG:n lähdedokumentteja ja Dockerin rakennetta voidaan valmistella rinnakkain, kunhan integraatiot testataan kokonaisuutena.

## 7. Riskienhallinta

Riskit arvioidaan laadullisesti vaikutuksen ja todennäköisyyden perusteella. Rekisteriä päivitetään vähintään jokaisen Sprintin lopussa sekä silloin, kun uusi merkittävä este ilmenee.

| ID | Riski | Todennäköisyys | Vaikutus | Ehkäisevä toimenpide / varasuunnitelma | Seuranta |
|---|---|---|---|---|---|
| R1 | AI-mallin tai -palvelun integrointi vie odotettua enemmän aikaa | Keskitaso | Korkea | Testataan yhteys ja yksi kysymys-vastaus-kierros varhain; pidetään AI-kerros erillään muusta backendistä | Tarkistetaan Sprint 1–2 aikana |
| R2 | RAG:n avainsanahaku ei löydä kysymykseen sopivia dokumenttikohtia | Keskitaso | Korkea | Käytetään rajattua Markdown- ja TXT-kokoelmaa; testataan ennalta määritellyillä kysymyksillä ja dokumentoidaan tulokset; semanttista hakua harkitaan vain testinäytön perusteella | Tarkistetaan ennen RAG:n hyväksymistä |
| R3 | Viiden viikon työmäärä ei riitä kaikkiin sovittuihin toimintoihin | Keskitaso | Korkea | Seurataan edistymistä viikoittain; nostetaan poikkeama päätettäväksi ja sovitaan muutoksista muodollisesti, eikä US-09:ää tai US-14:ää käsitellä automaattisesti valinnaisina | Arvioidaan viikoittain |
| R4 | Docker-palvelut, Ollaman mallin lataus tai ympäristömuuttujat eivät toimi yhdessä | Keskitaso | Korkea | Aloitetaan Compose-rakenne Sprint 1:ssä; testataan puhtaalla käynnistyksellä, mallin saatavuudella ja backend–Ollama-yhteydellä; dokumentoidaan asetukset ja salaisuuksien käsittely | Tarkistetaan jokaisessa merkittävässä integraatiossa |
| R5 | Käyttäjä voi nähdä tai muuttaa toisen käyttäjän tietoja | Keskitaso | Korkea | Tarkistetaan omistajuus backendissä; lisätään luvattoman käytön testit; ei luoteta pelkästään käyttöliittymän piilotuksiin | Testataan ennen toimitusta |
| R6 | Salasanoja tai muita salaisuuksia käsitellään turvattomasti | Matala–keskitaso | Korkea | Tallennetaan salasanat vain turvallisesti tiivistettyinä; ADMINin reset-komento toimii vain backendin ylläpitoympäristössä, näyttää väliaikaisen salasanan kerran eikä kirjaa sitä lokeihin; pakotetaan vaihto ja mitätöidään vanhat istunnot | Tarkistetaan koodi ja repository ennen demoa |
| R7 | Käyttöliittymän käännökset jäävät osittaisiksi | Keskitaso | Keskitaso | Keskitetään tekstit kieliresursseihin; testataan tärkeimmät näkymät suomeksi ja englanniksi | Tarkistetaan Sprint 4:ssä |
| R8 | Testaus ja dokumentointi jäävät viime hetkeen | Keskitaso | Korkea | Kirjataan testit toteutuksen yhteydessä; varataan Sprint 5:een erillinen aika integraatiotestaukselle ja dokumentoinnille | Tarkistetaan Sprint-arvioinnissa |
| R9 | Paikallisen GGUF-mallin koko, resurssitarve tai lisenssiehdot estävät luotettavan esittelyn | Keskitaso | Korkea | Testataan mallin lataus ja käyttö projektin Docker-ympäristössä varhain; tarkistetaan mallin ja työkalujen lisenssit sekä käytön ehdot ennen toimitusta | Tarkistetaan Sprint 1:ssä ja ennen esittelyä |
| R10 | Kirjautumisen IP-kohtainen käyttöraja tunnistaa Docker-proxyn eikä todellista asiakasta tai luottaa virheelliseen välitystietoon | Keskitaso | Keskitaso | Määritetään frontend-proxylle kiinteä IP erillisessä Compose-verkossa; luetaan `X-Forwarded-For` vain luotetulta proxylta ja valitaan ketjusta ensimmäinen luottamaton osoite oikealta alkaen; testataan myös väärät ja virheelliset otsakkeet | Yksikkötestit läpäisty; varmennetaan todellisessa LAN-käytössä ennen sen käyttöönottoa |
| R11 | Samanaikaiset kirjautumiset aiheuttavat MySQL-deadlockin istuntojen siivouksen ja lisäyksen välillä | Matala–keskitaso | Keskitaso | Siirretään vanhentuneiden istuntojen siivous kirjautumistransaktion ulkopuoliseen määräajoin ajettavaan tehtävään; poistetaan löydetyt rivit erissä ensisijaisavaimen perusteella | Siivouskyselyn yksikkötesti; rinnakkaistesti MySQL:llä ennen toimitusta |

### 7.1 Riskin toteutumisen toimintatapa

Kun riski toteutuu:

1. kirjataan ongelma ja sen vaikutus GitHub Issueen tai projektin seurantaan
2. arvioidaan vaikutus Sprintin tavoitteeseen, laajuuteen ja aikatauluun
3. valitaan korjaava toimenpide tai rajataan toiminnallisuutta
4. päivitetään riskirekisteri ja tarvittaessa muutosloki
5. testataan korjaus ja kirjataan tulos.

## 8. Edistymisen seuranta

### 8.1 Työn tilat

Työtä seurataan Product Backlogin ja GitHub Issues -tehtävien avulla. Käytetään seuraavia tiloja:

- **To Do** – työtä ei ole aloitettu
- **In Progress** – työ on käynnissä
- **In Review** – toteutus odottaa tarkastelua tai testien läpikäyntiä
- **Done** – hyväksymiskriteerit täyttyvät ja tarvittava dokumentaatio on päivitetty.

Tehtävää ei merkitä valmiiksi vain siksi, että koodi on kirjoitettu. Valmius edellyttää, että toiminto on toteutettu, sitä on testattu hyväksymiskriteerien kannalta ja tunnetut puutteet on kirjattu.

### 8.2 Viikoittainen seurantarytmi

Jokaisen viikon alussa:

1. tarkistetaan Sprintin tavoite ja käytettävissä oleva aika
2. valitaan tärkeimmät tehtävät Product Backlogista
3. varmistetaan, että tehtävien riippuvuudet ja hyväksymiskriteerit ovat selvät.

Jokaisen työskentelyjakson aikana:

- päivitetään tehtävien tilat
- kirjataan merkittävät tekniset ongelmat ja päätökset
- tehdään pieniä, ymmärrettäviä Git-committeja
- pidetään keskeneräiset muutokset mahdollisuuksien mukaan erillisissä haaroissa.

Jokaisen viikon lopussa:

1. verrataan valmistuneita tuloksia Sprintin tavoitteeseen
2. suoritetaan tärkeimmät toiminnalliset testit
3. kirjataan keskeneräiset tehtävät ja niiden syyt
4. arvioidaan riskit ja seuraavan viikon työmäärä
5. kirjataan lyhyt retrospektiivi: mikä onnistui, mikä esti etenemistä ja mitä muutetaan.

### 8.3 Edistymisen raportointi

Edistymistä kuvataan ensisijaisesti todennettavilla tuloksilla, ei pelkällä prosenttiluvulla. Esimerkkejä:

- rekisteröityminen ja kirjautuminen läpäisevät määritellyt testit
- käyttäjä voi luoda ja sulkea oman tukipyyntönsä
- keskusteluviesti tallentuu tietokantaan
- RAG-vastaus näyttää käytetyn lähteen tai ilmoittaa, ettei sopivaa lähdettä löytynyt
- käyttöliittymän keskeiset näkymät toimivat suomeksi ja englanniksi
- frontend, backend, tietokanta ja Ollama käynnistyvät dokumentoidulla Docker Compose -komennolla ja backend saa vastauksen Ollamalta
- README, API-dokumentaatio ja ER-kaavio vastaavat toteutunutta järjestelmää.

**Tilanne 27.10.2026:** Projektin tekninen perusrakenne ja Docker-ympäristö on aloitettu. Frontendille on luotu React- ja TypeScript-pohja, backendille FastAPI-perusrakenne ja riippuvuudet. Frontendille ja backendille on lisätty Docker-konfiguraatiot. Docker Composeen on määritelty frontend-, backend-, MySQL-, phpMyAdmin- ja Ollama-palvelut sekä Ollama-mallin alustava käyttöönotto. GGUF-mallin `Modelfile` ja sen sijainti `ollama`-hakemistossa on päivitetty.

**Tämänhetkinen rajaus:** Kyseessä on tekninen runko ja käyttöönottopohja; varsinaisten sovellustoimintojen valmistumista tai koko palvelukokonaisuuden toimivuutta ei ole näiden muutosten perusteella vahvistettu.

**Tilanne 31.10.2026:** Kirjautumisyritysten IP-kohtaisen käyttörajan proxy-käsittelyä ja kirjautumisen istuntosiivousta on korjattu. Frontendille on määritetty osoite `172.30.0.2` Dockerin erillisessä proxy-verkossa; se käyttää backendin verkkoaliasta `backend-proxy` osoitteessa `172.30.0.3` eikä liity backendin kanssa jaettuun oletusverkkoon. Kontit luotiin uudelleen ja frontendin `/api/health`-pyyntö backendille palautti HTTP 200. Vanhentuneet istunnot siivotaan erillisessä taustatehtävässä tunnin välein ja poistetaan erissä ensisijaisavaimen kautta, ei kirjautumistransaktion yhteydessä. Seitsemän backendin yksikkötestiä sekä Compose-konfiguraation tarkistus läpäistiin. Kahden LAN-laitteen välistä IP-välitystä tai rinnakkaisia kirjautumisia todellisella MySQL-palvelulla ei ole vielä varmennettu. Nykyinen Compose-porttisidonta on edelleen `127.0.0.1`, joten palvelu ei tällä asetuksella ole muiden LAN-laitteiden käytettävissä.

**Tilanne 01.11.2026 – Sprint 1:** Sprintin kuuden käyttäjätarinan toteutukset ovat nykyisessä branchissa. Backendin `unittest`-testisarja läpäisi 31/31 testiä. Frontendin TypeScript-tarkistus ja tuotantobuild onnistuivat; lint-tarkistus on puhdas. Alembic-migraatiot testattiin erillisessä tyhjässä MySQL-tietokannassa kahdesti, ja käytössä oleva tietokanta on versiossa `0002_conversations_and_tickets (head)`. Ticket API:n ORM-polut testattiin MySQL:llä transaktion rollbackilla. Ollaman mallin ensimmäinen käyttöönotto testattiin tyhjällä väliaikaisella mallivolyymilla: `poro-helpdesk` muodostui `Modelfile`-tiedostosta ja väliaikaiset Docker-resurssit poistettiin. Koko Compose-pinoa ei ole vielä käynnistetty kerralla täysin tyhjillä MySQL- ja Ollama-volyymeilla. Avoinna ovat rekisteröitymisen ja kirjautumisen API-integraatiotestit, käyttöliittymän manuaalinen hyväksymistarkastus, MySQL:n rinnakkaiskirjautumistesti sekä LAN-välitystesti. LAN-käyttö ja frontendin production-käyttöönotto pysyvät aiemmin sovitusti myöhempään vaiheeseen.

### 8.4 Definition of Done

Käyttäjätarina tai toiminto voidaan merkitä valmiiksi, kun:

- sen hyväksymiskriteerit täyttyvät
- toiminto on testattu asianmukaisesti
- virhetilanteet käsitellään kohtuullisesti
- tietoturva ja käyttöoikeudet on huomioitu toiminnon laajuuden mukaisesti
- koodi on tallennettu GitHubiin ja tarvittaessa tarkastettu Pull Requestissa
- siihen liittyvä dokumentaatio on päivitetty
- tiedossa olevat rajoitteet on kirjattu.

## 9. Muutostenhallinta

Muutoksia voivat olla esimerkiksi uusi ominaisuus, vaatimuksen muuttaminen, teknologian vaihtaminen, Sprint-jaon muuttaminen tai hyväksymiskriteerin tarkentaminen.

### 9.1 Muutoksen käsittely

1. **Ehdotus:** muutoksen tarve ja perustelu kirjataan GitHub Issueen tai muutoslokiin.
2. **Vaikutusarvio:** arvioidaan vaikutus tavoitteisiin, laajuuteen, työmäärään, riippuvuuksiin, tietoturvaan ja aikatauluun.
3. **Priorisointi:** verrataan muutosta nykyisiin P1/P2/P3-tehtäviin ja pakollisiin vaatimuksiin.
4. **Päätös:** projektin toteuttaja päättää pienistä toteutuksen sisäisistä muutoksista. Laajuuteen tai arviointivaatimuksiin vaikuttavat muutokset sovitetaan tarvittaessa opettajan ohjeisiin.
5. **Päivitys:** hyväksytty muutos päivitetään oikeaan lähdedokumenttiin, Product Backlogiin ja tarvittaessa testisuunnitelmaan.
6. **Toteutus ja tarkistus:** muutos toteutetaan, testataan ja sen valmistuminen merkitään seurantaan.

### 9.2 Muutosten periaatteet

- Vaatimusten muutokset kirjataan ensisijaisesti vaatimusmäärittelyyn.
- Käyttäjän tarpeita ja hyväksymiskriteerejä koskevat muutokset kirjataan käyttäjätarinadokumenttiin.
- Työn prioriteetit, arviot ja Sprint-jako ylläpidetään Product Backlogissa.
- Tämä dokumentti päivitetään, kun muutos vaikuttaa projektin laajuuteen, aikatauluun, merkittäviin riskeihin tai hallintakäytäntöihin.
- README toimii projektin esittely-, asennus-, konfigurointi- ja käyttöohjeena. Siinä voidaan kuvata lyhyesti sovelluksen tarkoitus, keskeiset ominaisuudet ja teknologiat; yksityiskohtaiset vaatimukset, Sprint-seuranta, riskit, päätökset ja muutosloki pidetään omissa dokumenteissaan.

## 10. Päätösloki

Merkittävät tekniset ja projektinhallinnalliset päätökset kirjataan tähän taulukkoon. Yksityiskohtaiset toteutuspäätökset voidaan kirjata myös GitHub Issues -tehtäviin.

| ID | Päivämäärä | Päätös | Perustelu | Vaikutus |
|---|---|---|---|---|
| D-01 | 26.10.2026 | Projektin kestoksi määritellään viisi viikkoa ja työmääräksi vähintään 20 tuntia viikossa | Projektin aikataulu ja käytettävissä oleva työaika | Laajuus on pidettävä rajattuna ja prioriteetit selkeinä |
| D-02 | 26.10.2026 | Lopulliseen julkaisuun valitaan RAG, suomen- ja englanninkielinen käyttöliittymä sekä Docker Compose | Tehtävänannon lisäominaisuudet ja projektin oppimistavoitteet | Nämä kolme ominaisuutta suunnitellaan ja testataan erikseen |
| D-03 | 26.10.2026 | US-09 ja US-14 kuuluvat viralliseen toimituslaajuuteen; US-14 sisältää vain käyttäjän kokonaismäärän sekä OPEN/CLOSED-määrät | Ryhmän vahvistama lopullinen laajuus | Tarinoita ei käsitellä valinnaisina; US-09 edellyttää käyttäjän tarkistusta ja vahvistusta |
| D-04 | 26.10.2026 | US-16 sisältää Ollaman ja valitun GGUF-mallin Docker Compose -ympäristössä; Sprint 1 ja sen 33 SP:n suunnitelma säilyvät | Ryhmän vahvistama kontitustapa ja Sprint-päätös | Backend käyttää Ollamaa Compose-verkon kautta; tuotantokäyttöönotto ei kuulu laajuuteen |
| D-05 | 26.10.2026 | Tekoälymallin tavoite on `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`, jota käytetään Ollaman kautta | Projektin valittu paikallinen malli | Malli käynnistetään Ollama-kontissa; mallin tiedoston sijainti ja pysyvä mallivarasto dokumentoidaan |
| D-06 | 26.10.2026 | RAG MVP käsittelee Markdown- ja TXT-dokumentteja avainsanahaulla; semanttinen haku lisätään vain testinäytön perusteella | Rajattu ja testattava MVP-toteutus | Lähdekokoelma rajataan ennen toteutusta; ER-skeemaa ei muuteta ilman uutta pysyvää tietotarvetta |
| D-07 | 26.10.2026 | Työkalujen ja kirjastojen tulee olla maksuttomia, ja niiden lisenssit sekä käyttöehdot tarkistetaan | Ryhmän vahvistama teknologiapäätös | Valinnat ja mahdolliset rajoitteet dokumentoidaan ennen toimitusta |
| D-08 | 31.10.2026 | Backend luottaa vain Compose-verkossa määritettyyn frontend-proxyyn ja käyttää luotetulta proxylta välitetyn osoiteketjun ensimmäistä luottamatonta hopia IP-käyttörajan avaimena | Jaetun proxy-IP:n aiheuttaman käyttäjien ristiinrajoittamisen ja välitetyn otsakkeen väärinkäytön ehkäisy | Frontendin osoite on `172.30.0.2`, luotettu verkko määritetään `TRUSTED_PROXY_IPS`-asetuksella ja logiikka testataan automaattisesti; todellinen LAN-välitys varmennetaan myöhemmin |
| D-09 | 31.10.2026 | Frontend käyttää vain proxy-verkkoa ja kutsuu backendia verkkoaliaksella `backend-proxy` | Varmistetaan, että proxyn ja backendin välinen yhteys käyttää sitä verkkoa, jolla proxyn IP on luotettu | Frontendin ja backendin proxy-verkon osoitteet sekä `/api/health`-reitti varmennettiin konttien uudelleenluonnin jälkeen |
| D-10 | 31.10.2026 | Vanhentuneiden istuntojen siivous suoritetaan kirjautumisesta riippumattomassa tunnin välein ajettavassa tehtävässä; poisto tehdään erissä tunnisteiden perusteella | Vältetään MySQL:n `expires_at`-aluepoiston gap lock -lukkojen ja kirjautumisen sessionlisäyksen välinen deadlock | Kirjautumistransaktio luo vain uuden session; siivoustehtävä kirjaa tietokantavirheet ja jatkaa seuraavalla jaksolla |

## 11. Muutosloki

| Päivämäärä | Versio | Muutos | Tekijä |
|---|---|---|---|
| 26.10.2026 | 0.1 | Projektinhallintadokumentin ensimmäinen versio | Projektin toteuttaja |
| 26.10.2026 | 0.2 | Päivitetty nykytilanne, Sprint-aikataulun tarkennus sekä US-14:n ja US-16:n rajaukset; selkeytetty README:n ja hallintadokumentin vastuut | Projektin toteuttaja |
| 26.10.2026 | 0.3 | Yhtenäistetty virallinen laajuus, RAG MVP, Ollama ja valittu malli, Docker Compose, lisenssiehtojen tarkistus sekä US-09/US-14-sitoumukset | Projektin toteuttaja |
| 31.10.2026 | 0.4 | Dokumentoitu proxy-pohjaisen kirjautumisen IP-rajoituksen muutos, testitulokset ja LAN-varmennuksen avoin tarve | Projektin toteuttaja |
| 31.10.2026 | 0.5 | Pakotettu frontendin backend-reititys luotetun proxy-verkon kautta ja siirretty vanhentuneiden istuntojen siivous kirjautumistransaktion ulkopuolelle | Projektin toteuttaja |
| 01.11.2026 | 0.6 | Korjattu Ollaman mallin alustuskomennon Compose-käsittely; varmennettu tyhjän mallivolyymin alustus, Sprint 1:n testitulokset ja avoimet tarkistukset; korjattu Modelfile-polut ja HomePage-focus-käsittely | Projektin toteuttaja |

## 12. Linkit projektin muihin dokumentteihin

- [Vaatimusmäärittely](01-vaatimusmaarittely.md)
- [Käyttäjätarinat ja hyväksymiskriteerit](02-käyttäjätarinat%20ja%20hyväksymiskriteerit.md)
- [Product Backlog](03-product%20backlog.md)
- [Sprint-suunnitelma](04-sprintin%20suunnitelma.md)
- [Järjestelmän suunnittelu](05-järjestelmän%20suunnittelu.md)
- [README](../README.md)

> **Ylläpitokäytäntö:** päivitä tätä dokumenttia projektin edetessä, erityisesti aikataulun, riskien, merkittävien päätösten ja laajuusmuutosten osalta. Älä kopioi tänne muiden dokumenttien yksityiskohtaisia vaatimuksia tai käyttäjätarinoita; linkitä niiden lähteisiin.
