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

**Tilannekuvan rajaus:** 26.10.2026 päivätyt tiedot kuvaavat projektin suunnitteluvaihetta, eivät nykyistä toteutustilannetta. Toteutuksen ja varmennuksen ajantasainen yhteenveto ylläpidetään tämän dokumentin kohdassa 8.3.

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
- Ollama-mallin käyttö Compose-ympäristössä; projektin oletusmalli on `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`, ja asiakkaan malli voidaan vaihtaa dokumentoiduilla ympäristöasetuksilla
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

**Rajaus 27.10.2026:** Tuolloin kyseessä oli tekninen runko ja käyttöönottopohja; varsinaisten sovellustoimintojen valmistumista tai koko palvelukokonaisuuden toimivuutta ei ollut vielä vahvistettu.

**Tilanne 31.10.2026:** Kirjautumisyritysten IP-kohtaisen käyttörajan proxy-käsittelyä ja kirjautumisen istuntosiivousta on korjattu. Frontendille on määritetty osoite `172.30.0.2` Dockerin erillisessä proxy-verkossa; se käyttää backendin verkkoaliasta `backend-proxy` osoitteessa `172.30.0.3` eikä liity backendin kanssa jaettuun oletusverkkoon. Kontit luotiin uudelleen ja frontendin `/api/health`-pyyntö backendille palautti HTTP 200. Vanhentuneet istunnot siivotaan erillisessä taustatehtävässä tunnin välein ja poistetaan erissä ensisijaisavaimen kautta, ei kirjautumistransaktion yhteydessä. Seitsemän backendin yksikkötestiä sekä Compose-konfiguraation tarkistus läpäistiin. Kahden LAN-laitteen välistä IP-välitystä tai rinnakkaisia kirjautumisia todellisella MySQL-palvelulla ei ole vielä varmennettu. Nykyinen Compose-porttisidonta on edelleen `127.0.0.1`, joten palvelu ei tällä asetuksella ole muiden LAN-laitteiden käytettävissä.

**Tilanne 01.11.2026 – Sprint 1:** Sprintin kuuden käyttäjätarinan toteutukset ovat nykyisessä branchissa. Backendin `unittest`-testisarja läpäisi 31/31 testiä. Frontendin TypeScript-tarkistus ja tuotantobuild onnistuivat; lint-tarkistus on puhdas. Alembic-migraatiot testattiin erillisessä tyhjässä MySQL-tietokannassa kahdesti, ja käytössä oleva tietokanta on versiossa `0002_conversations_and_tickets (head)`. Ticket API:n ORM-polut testattiin MySQL:llä transaktion rollbackilla. Ollaman mallin ensimmäinen käyttöönotto testattiin tyhjällä väliaikaisella mallivolyymilla: `poro-helpdesk` muodostui `Modelfile`-tiedostosta ja väliaikaiset Docker-resurssit poistettiin. Koko Compose-pinoa ei ole vielä käynnistetty kerralla täysin tyhjillä MySQL- ja Ollama-volyymeilla. Avoinna ovat rekisteröitymisen ja kirjautumisen API-integraatiotestit, käyttöliittymän manuaalinen hyväksymistarkastus, MySQL:n rinnakkaiskirjautumistesti sekä LAN-välitystesti. LAN-käyttö ja frontendin production-käyttöönotto pysyvät aiemmin sovitusti myöhempään vaiheeseen.

**Tilanne 04.11.2026 – Sprintit 1–4 ja demo-valmistelu:** Sprinttien 1–3 ydintoiminnot ovat toteutettuina nykyisessä paikallisessa työkopiossa, ja Sprint 4:n US-09, US-13 ja US-14 ovat myös toteutettu kooditasolla. Käyttöliittymässä on nyt AI-keskustelusta luotava tukipyyntö, kielivalinta FI/EN sekä kirjautuneen käyttäjän tukipyyntöjen yhteenveto. Sprintin 5 RAG-neuvonta sekä jäljellä oleva integraatio- ja hyväksymistestaus ovat edelleen kesken.

Viimeisimmät tekniset muutokset: AI-pyynnöt saman keskustelun sisällä sarjoitetaan Redis-lukolla; tietokantatransaktio ja yhteys vapautetaan ennen Ollaman odotusta, ja assistant-vastaus tallennetaan lyhyessä erillisessä tietokantaistunnossa. Tallennetun käyttäjäviestin vastausta voi yrittää uudelleen ilman viestin kaksoistallennusta. Ollaman virheelliset vastausrakenteet käsitellään palveluvirheinä, ja chat POST tarkistaa pyynnön `Origin`-otsakkeen sallitusta frontend-alkuperästä. Lisäksi päivittäinen siivous poistaa erissä yli kolme kalenterikuukautta vanhat suljetut tukipyynnöt ja passiiviset keskustelut; keskustelu säilytetään, jos siihen liittyy avoin tai säilytysajan piirissä oleva tukipyyntö. Tämä on pysyvä poisto.

Käyttöliittymää on levennetty työtilanäkymissä, tukipyyntöjen LOW/MEDIUM/HIGH-prioriteetit erottuvat väreillä, käyttäjän etu- ja sukunimi sekä sähköpostiosoite ovat profiilissa vain luettavina, ja kirjautumis-/rekisteröitymisnäkymät käyttävät pakotetun salasananvaihdon kanssa yhtenäistä kaksiosaista korttirakennetta. Profiilin API hyväksyy muutettavaksi vain käyttäjänimen. Sprint 4:n mukana lisättiin ticket-draft -tyyppinen AI-haku keskustelusta, kielivalinta ja yhteenveto omista tukipyynnöistä.

04.11.2026 varmennus: backendin 65 `unittest`-testiä läpäisivät; frontendin `npm run lint` sekä TypeScript-tarkistus ja `npm run build` onnistuivat. Tämä on vahvistettu kooditasolla ja ajantasainen nykyiselle branchille. Jäljellä olevat hyväksymistestit koskevat pääasiassa luotettavaa clean Compose -käynnistystä, oikeaa LAN-välitystä kahdella laitteella ja manuaalista whole-app acceptance testia.

Tämä tilanne kuvaa paikallista työkopiota 04.11.2026. Sprint 4:n status on koodin tasolla vahvistettu, mutta demo- ja tuotantotason hyväksymistestaus on vielä ajoitettu ennen virallista demoa.

**Hyväksyntäpäivitys 05.11.2026:** Projektin toteuttaja on vahvistanut käyttäjätarinoiden **US-01–US-17** käytännön hyväksymiskriteerit suoritetuiksi. Tämä sisältää myös US-07:n ja US-15:n, jotka odottivat aiemmin demokierroksen hyväksyntää. Tarinakohtainen hyväksyntä ei yksin vahvista kaikkien toimituskokonaisuuden tehtävien, kuten dokumentaation ja lisenssien tarkistuksen, valmistumista.

Vahvistus sisältää koko Compose-pinon käynnistyksen tyhjillä MySQL- ja Ollama-volyymeilla (US-16); projektin toteuttaja vahvisti tämän 05.11.2026. LAN-välitystesti on erillinen käyttöympäristön tarkistus: nykyisen Compose-tiedoston portit on sidottu `127.0.0.1`-osoitteeseen, eikä LAN-käytettävyys sisälly paikalliseen käynnistyshyväksyntään.

**Toimitustarkistukset (05.11.2026):** Kolmansien osapuolten lisensseistä ja käyttöehdoista on tehty alustava inventointi [lisenssiselvitykseen](07-kolmansien%20osapuolten%20lisenssiselvitys.md). Inventointi on alustavalla tasolla valmis; jakelua koskevia toimia on vielä avoinna: projektin oman lisenssin valinta, oletus-GGUF-mallin lähteen/revision ja tarkistussumman sekä vaadittujen Llama-ilmoitusten kirjaaminen, Redis 7.4:n ehtojen vahvistaminen ja transitiivisten riippuvuuksien sekä kuvadigestien inventointi.

Rekisteröitymisen ja kirjautumisen MySQL-integraatio, mukaan lukien kahdeksan samanaikaista kirjautumista, läpäisi paikallisessa Compose-ympäristössä 05.11.2026. Toistettava valinnainen testi on tiedostossa `backend/tests/test_auth_mysql_integration.py`; tavallinen backend-testiajo ohittaa tämän testin, ellei sitä erikseen oteta käyttöön. Paikallinen API-/tietokantavarmennus on tehty. Todellisten LAN-laitteiden välinen IP-välitys jää ympäristötarkistukseksi, jota ei voi varmentaa henkilökohtaisessa kehitysympäristössä. Nämä ovat toimitus- ja ympäristötarkistuksia, eivät hyväksymättömiä käyttäjätarinoita; LAN-käyttö pysyy laajuuden ulkopuolella, ellei toimituskohde sitä edellytä.

**Varmennuspäivitys (05.11.2026):** Backendin 86 testistä 85 läpäisi ja valinnainen MySQL-integraatiotesti ohitettiin normaalissa testiajossa. Erillinen integraatiotesti läpäisi rekisteröitymisen ja kahdeksan samanaikaista MySQL-kirjautumista paikallisessa Compose-ympäristössä. Frontendin lint, TypeScript-tarkistus ja tuotantobuild onnistuivat. Compose tukee Ollama-rekisteristä haettavan mallin tai paikallisesta Modelfile-tiedostosta luotavan mallin valintaa; oletuksena käytetään projektin Poro-mallia. Asiakkaan käyttöönotto-ohje on README-tiedostossa.

**US-15-testihavainto ja uusintatesti (05.11.2026):** Ensimmäinen suomenkielinen säilytysaikakysymys palautti heikosti aiheeseen liittyviä Knowledge Base -osumia. Avustaja vastasi virheellisesti 7 ja 30 päivän säilytysajoilla ja viittasi tiedostoon `knowledge/05-data-model.md`, jota nykyisessä korpuksessa ei ole. Tietopohjan ja vastauskäsittelyn päivityksen jälkeen toteuttaja uusi US-15:n käytännön hyväksyntätestin ja vahvisti kriteerien täyttyvän. Alkuperäinen virhe kirjataan silti mallin ja RAG:n rajoitteeksi ja se ohjaa jatkokehitystä.

**Tekoälyn testauksessa havaitut rajoitteet (US-07 ja US-15, 05.11.2026):** Käytännön testauksessa malli vastasi toisinaan väärällä kielellä; erityisesti suomenkieliseen kysymykseen tuli englanninkielinen vastaus. Malli myös keksi sovellukseen itsepalveluna toimivan “Forgot Password” -sivun ja sähköpostilinkkipalautuksen, joita toteutuksessa ei ole. Aiemmassa RAG-testissä se keksi säilytysajat ja viittasi korpuksesta puuttuvaan tiedostoon. Salasanan palautus ohjataan nyt kiinteällä, projektin mukaiseen tietoon perustuvalla vastauksella, kielentunnistusta on vahvistettu ja lähteettömien projektivastausten ohjeistusta tiukennettu. Korjaukset vähentävät havaittuja virheitä, mutta eivät takaa, että generatiivinen malli noudattaa ohjeita aina.

Käytössä on 8 miljardin parametrin kvantisoitu paikallinen malli. Sen rajallinen kapasiteetti voi osaltaan heikentää ohjeiden noudattamista, kielten välistä johdonmukaisuutta ja haettujen lähteiden täsmällistä käyttöä; tämä on uskottava vaikuttava tekijä, ei todiste siitä, että mallin koko yksin aiheutti jokaisen virheen. US-15 käyttää lisäksi avainsana- ja token-etuliitehakua, ei semanttista hakua tai suomen kielen taivutusmuotoja ymmärtävää analyysiä. Se voi siksi ohittaa olennaisen kohdan tai palauttaa heikon osuman. Suurempi malli voi parantaa kieli- ja ohjeiden noudattamisen laatua, mutta se ei yksin korjaa hakujen puutteita, keskeneräisiä lähdeasiakirjoja tai virheellisiä väitteitä. Mahdollinen mallinvaihto arvioidaan samoilla suomen- ja englanninkielisillä hyväksymiskysymyksillä sekä resurssi-, viive-, lisenssi- ja lähdeviitetarkistuksilla.

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
| D-05 | 26.10.2026 | Tekoälyn oletusmalli on `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`, jota käytetään Ollaman kautta | Projektin valitsema paikallinen oletusmalli; asiakkaan asennukseen voi määrittää muun yhteensopivan Ollama-mallin | Malli käynnistetään Ollama-kontissa; mallivalinta ja pysyvä mallivarasto dokumentoidaan |
| D-06 | 26.10.2026 | RAG MVP käsittelee Markdown- ja TXT-dokumentteja avainsanahaulla; semanttinen haku lisätään vain testinäytön perusteella | Rajattu ja testattava MVP-toteutus | Lähdekokoelma rajataan ennen toteutusta; ER-skeemaa ei muuteta ilman uutta pysyvää tietotarvetta |
| D-07 | 26.10.2026 | Työkalujen ja kirjastojen tulee olla maksuttomia, ja niiden lisenssit sekä käyttöehdot tarkistetaan | Ryhmän vahvistama teknologiapäätös | Valinnat ja mahdolliset rajoitteet dokumentoidaan ennen toimitusta |
| D-08 | 31.10.2026 | Backend luottaa vain Compose-verkossa määritettyyn frontend-proxyyn ja käyttää luotetulta proxylta välitetyn osoiteketjun ensimmäistä luottamatonta hopia IP-käyttörajan avaimena | Jaetun proxy-IP:n aiheuttaman käyttäjien ristiinrajoittamisen ja välitetyn otsakkeen väärinkäytön ehkäisy | Frontendin osoite on `172.30.0.2`, luotettu verkko määritetään `TRUSTED_PROXY_IPS`-asetuksella ja logiikka testataan automaattisesti; todellinen LAN-välitys varmennetaan myöhemmin |
| D-09 | 31.10.2026 | Frontend käyttää vain proxy-verkkoa ja kutsuu backendia verkkoaliaksella `backend-proxy` | Varmistetaan, että proxyn ja backendin välinen yhteys käyttää sitä verkkoa, jolla proxyn IP on luotettu | Frontendin ja backendin proxy-verkon osoitteet sekä `/api/health`-reitti varmennettiin konttien uudelleenluonnin jälkeen |
| D-10 | 31.10.2026 | Vanhentuneiden istuntojen siivous suoritetaan kirjautumisesta riippumattomassa tunnin välein ajettavassa tehtävässä; poisto tehdään erissä tunnisteiden perusteella | Vältetään MySQL:n `expires_at`-aluepoiston gap lock -lukkojen ja kirjautumisen sessionlisäyksen välinen deadlock | Kirjautumistransaktio luo vain uuden session; siivoustehtävä kirjaa tietokantavirheet ja jatkaa seuraavalla jaksolla |
| D-11 | 03.11.2026 | Suljetut tukipyynnöt ja käyttämättömät keskustelut poistetaan pysyvästi kolmen kalenterikuukauden jälkeen | Rajataan tietokannan kasvua sovitulla säilytyskäytännöllä | Päivittäinen erissä suoritettava taustatehtävä käyttää `closed_at`- ja `updated_at`-aikoja; avoimeen tai säilytysaikaiseen pyyntöön liittyvää keskustelua ei poisteta |
| D-12 | 03.11.2026 | Käyttäjä ei voi muuttaa etu- tai sukunimeään profiilista; käyttäjänimi on ainoa muokattava profiilikenttä | Käyttäjän vahvistama käyttöoikeus- ja profiilikäytäntö | Etu- ja sukunimi näytetään lukittuina, ja backendin PATCH-skeema hylkää muut nimet |

## 11. Muutosloki

| Päivämäärä | Versio | Muutos | Tekijä |
|---|---|---|---|
| 26.10.2026 | 0.1 | Projektinhallintadokumentin ensimmäinen versio | Projektin toteuttaja |
| 26.10.2026 | 0.2 | Päivitetty nykytilanne, Sprint-aikataulun tarkennus sekä US-14:n ja US-16:n rajaukset; selkeytetty README:n ja hallintadokumentin vastuut | Projektin toteuttaja |
| 26.10.2026 | 0.3 | Yhtenäistetty virallinen laajuus, RAG MVP, Ollama ja valittu malli, Docker Compose, lisenssiehtojen tarkistus sekä US-09/US-14-sitoumukset | Projektin toteuttaja |
| 31.10.2026 | 0.4 | Dokumentoitu proxy-pohjaisen kirjautumisen IP-rajoituksen muutos, testitulokset ja LAN-varmennuksen avoin tarve | Projektin toteuttaja |
| 31.10.2026 | 0.5 | Pakotettu frontendin backend-reititys luotetun proxy-verkon kautta ja siirretty vanhentuneiden istuntojen siivous kirjautumistransaktion ulkopuolelle | Projektin toteuttaja |
| 01.11.2026 | 0.6 | Korjattu Ollaman mallin alustuskomennon Compose-käsittely; varmennettu tyhjän mallivolyymin alustus, Sprint 1:n testitulokset ja avoimet tarkistukset; korjattu Modelfile-polut ja HomePage-focus-käsittely | Projektin toteuttaja |
| 03.11.2026 | 0.7 | Päivitetty Sprinttien 1–5 tilanne, backendin chat- ja retention-ratkaisut, profiilin muokkausrajaus sekä testauksen ja käyttöönoton avoimet tarkistukset | Projektin toteuttaja |

## 12. Linkit projektin muihin dokumentteihin

- [Vaatimusmäärittely](01-vaatimusmaarittely.md)
- [Käyttäjätarinat ja hyväksymiskriteerit](02-käyttäjätarinat%20ja%20hyväksymiskriteerit.md)
- [Product Backlog](03-product%20backlog.md)
- [Sprint-suunnitelma](04-sprintin%20suunnitelma.md)
- [Järjestelmän suunnittelu](05-järjestelmän%20suunnittelu.md)
- [README](../../README.md)

> **Ylläpitokäytäntö:** päivitä tätä dokumenttia projektin edetessä, erityisesti aikataulun, riskien, merkittävien päätösten ja laajuusmuutosten osalta. Älä kopioi tänne muiden dokumenttien yksityiskohtaisia vaatimuksia tai käyttäjätarinoita; linkitä niiden lähteisiin.

## 13. Keskustelun elinkaaren päätösloki (2026-11-13)

| ID | Päiväys | Päätös / muutos | Perustelu | Toteutus / tila |
|---|---|---|---|---|
| D-13 | 13.11.2026 | Sivupalkin Uusi keskustelu luo aina itsenäisen keskustelun; jatkaminen on erillinen lapsikeskustelutoiminto | Uuden keskustelun aloittaminen ei saa huomaamatta muuttua jatkamiseksi | Toteutettu branchissa feature/conversation-lifecycle |
| D-14 | 13.11.2026 | Lapsikeskustelu edellyttää käyttäjän tarkistamaa otsikkoa ja ei-tyhjää kontekstiyhteenvetoa; siihen tallennetaan emokeskusteluviittaus ja yhteenvetovedos | Säilytetään käyttäjän päätösvalta ja rajattu peritty konteksti kopioimatta emokeskustelun viestihistoriaa | Toteutettu; migraatio 0008_conversation_tree.py |
| D-15 | 13.11.2026 | Aloita jatkokeskustelu näytetään vain, kun viimeisimmän valmistuneen generoinnin kontekstikäyttö ylittää tiukasti 70 % | Jatkokeskustelu tarjotaan kontekstin lähestyessä kapasiteettia ilman, että keskeneräisen luonnoksen arviota käsitellään mitattuna arvona | Toteutettu frontendissä; tarkan raja-arvon erillinen testinäyttö vielä tarvitaan |

Kehittäjä ilmoitti itsenäisen keskustelun ja jatkokeskustelun toimintojen toimivan manuaalisessa toimintatestauksessa. Frontendin build ja Dockerissa suoritettu lint onnistuivat. Dokumentaatio kirjaa tämän ilmoituksen eikä väitä suorittamattomia raja-arvo- tai virhetilannetestejä tehdyiksi.

### Lisäys muutoslokiin

| Päivämäärä | Versio | Muutos | Tekijä |
|---|---|---|---|
| 13.11.2026 | 0.8 | Kirjattu itsenäisen ja jatkokeskustelun päätökset, toteutustila ja dokumentaation synkronointikäytäntö | Projektin toteuttaja |

