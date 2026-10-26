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
| Projektin vastuuhenkilö | Opiskelija / projektin toteuttaja |
| Keskeiset sidosryhmät | Projektin toteuttaja, opettaja/arvioija ja sovelluksen loppukäyttäjät |
| Dokumentin tila | Elävä dokumentti; päivitetään projektin edetessä |

**Nykytilanne 26.10.2026:** vaatimusmäärittely, käyttäjätarinat hyväksymiskriteereineen, Product Backlog, alustava Sprint-suunnitelma ja järjestelmän suunnitteludokumentti on laadittu. Projektin suunnitteludokumentaatiota yhtenäistetään parhaillaan; `backend`- ja `frontend`-hakemistoissa ei vielä ole sovelluksen lähdekooditiedostoja. Toteutuksen edistyminen päivitetään jatkossa seurantaan ja GitHub-tehtäviin, ei tämän tilannekuvauksen kautta.

## 2. Projektin tarkoitus ja tavoitteet

AI HelpDesk on verkkosovellus, jonka avulla käyttäjä voi pyytää apua tietotekniikkaan ja ohjelmistokehitykseen liittyvissä ongelmissa. Käyttäjä voi keskustella tekoälyn kanssa, saada ongelmanratkaisuehdotuksia ja tallentaa ratkaisemattoman ongelman tukipyynnöksi.

Projektin tavoitteet ovat:

1. Toteuttaa toimiva verkkosovellus, jossa on käyttöliittymä, backend, REST-rajapinta ja relaatiotietokanta.
2. Mahdollistaa käyttäjän rekisteröityminen, kirjautuminen ja omien profiilitietojen hallinta.
3. Mahdollistaa tukipyyntöjen luominen, tarkastelu ja sulkeminen sekä tietojen tallentaminen tietokantaan.
4. Tarjota tekoälypohjainen keskustelu, jossa käyttäjä voi kuvata ongelmansa ja saada ehdotuksia sen ratkaisemiseksi.
5. Tallentaa keskusteluviestit ja mahdollistaa tukipyynnön luominen keskustelun perusteella, jos tämä saadaan toteutettua käytettävissä olevan ajan puitteissa.
6. Toteuttaa lopulliseen julkaisuun kolme valittua lisäominaisuutta:
   - tietopohjainen tekoälyneuvonta (RAG)
   - suomen- ja englanninkielinen käyttöliittymä
   - sovelluksen käynnistäminen Docker Composella yhdellä dokumentoidulla komennolla.
7. Toteuttaa projekti GitHub-versionhallintaa ja soveltuvin osin Scrum-käytäntöjä hyödyntäen.
8. Tuottaa tekninen dokumentaatio, testitulokset ja sovelluksen esittely.

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
- MySQL-tietokanta nykyisen järjestelmäsuunnitelman mukaisesti; MariaDB voidaan ottaa käyttöön vaihtoehtona vain, jos valinta vahvistetaan ja tekniset dokumentit sovitetaan siihen
- RAG-pohjainen neuvonta valitusta teknisestä dokumenttikokoelmasta; lähteet ja kokoelman rajaus täsmennetään ennen toteutusta
- käyttöliittymän suomen- ja englanninkieliset tekstit
- Docker Compose -käyttöönotto frontendille, backendille ja tietokannalle
- automaattiset tai toistettavat testit keskeisille toiminnoille
- README, API-dokumentaatio, tietokantakuvaus/ER-kaavio, kuvakaappaukset ja esittely.

### 3.2 Rajauksen ulkopuolelle jäävät asiat

Seuraavat ominaisuudet eivät kuulu sovittuun ydinsisältöön, ellei niitä hyväksytä erikseen muutoksenhallinnan kautta:

- äänen syöttö tai puhevastaukset
- PDF-raporttien luominen
- laaja yritystason IT-palvelunhallinta
- yliopiston keskitettyyn tunnistautumiseen integrointi
- käyttäjän tietokoneella suoritettavien komentojen automaattinen suorittaminen
- täysin itsenäinen ongelmanratkaisu ilman käyttäjän osallistumista
- laajat organisaatioiden väliset käyttöoikeudet ja integraatiot.

Product Backlogin `US-14`-yhteenvetonäkymä on **ehdollinen ja toissijainen**. Sen rajattu toteutus käsittää vain kirjautuneen käyttäjän tukipyyntöjen kokonaismäärän sekä `OPEN`- ja `CLOSED`-tilojen lukumäärät; siihen eivät kuulu kaaviot, suodatukset, aikavertailut tai muiden käyttäjien tiedot. US-14 toteutetaan vain, jos pakolliset toiminnot, kolme valittua lisäominaisuutta, testaus ja dokumentaatio etenevät suunnitellusti. Sitä ei lasketa yhdeksi kolmesta valitusta lisäominaisuudesta.

`US-16`-tarinan 5 Story Pointin arvio kattaa frontendin ja backendin kontit, MySQL:n Compose-palvelun, esimerkkikonfiguraation, tietokannan pysyvän tallennuksen, valmiustarkistukset sekä dokumentoinnin ja käynnistyksen testauksen. AI-palvelun kontitus ja tuotantoympäristön käyttöönotto eivät kuulu tähän rajaukseen.

### 3.3 Laajuuden hallinnan periaate

Viiden viikon aikaraja on kiinteämpi rajoite kuin yksittäisten lisätoimintojen määrä. Jos aikataulu uhkaa ylittyä, työ rajataan uudelleen seuraavassa järjestyksessä:

1. säilytetään tietoturvan, tietojen eheyden ja ydinkäyttöpolun kannalta välttämättömät toiminnot
2. toteutetaan kaikki tehtävänannon pakolliset vaatimukset
3. toteutetaan kolme valittua lisäominaisuutta rajatussa mutta todennettavassa laajuudessa
4. siirretään ensin muut valinnaiset ja viimeistelyä parantavat ominaisuudet myöhempään vaiheeseen.

Laajuutta ei kasvateta hiljaisesti. Muutokset kirjataan ja niiden vaikutus aikatauluun, työmäärään ja hyväksymiskriteereihin arvioidaan.

## 4. Roolit ja vastuut

Projekti toteutetaan opiskelijaprojektina. Yksi henkilö voi hoitaa useita rooleja; roolien nimeäminen auttaa kuitenkin pitämään vastuut selkeinä.

| Rooli | Vastuu |
|---|---|
| Projektin toteuttaja / Developer | Suunnittelee, toteuttaa, testaa ja dokumentoi sovelluksen sekä ylläpitää GitHub-repositorya. |
| Product Owner -vastuu | Priorisoi Product Backlogin ja tekee ehdotukset laajuuden muutoksista projektin tavoitteiden perusteella. Opiskelija hoitaa tämän vastuun, ellei opettaja määrää muuta. |
| Scrum Master -vastuu | Suunnittelee viikoittaisen työskentelyn, seuraa esteitä ja arvioi Sprintin lopputulosta. Opiskelija soveltaa käytäntöjä omaan työskentelyynsä. |
| Testausvastuu | Laatii testit, suorittaa ne ja kirjaa havaitut virheet sekä testitulokset. |
| Opettaja / arvioija | Arvioi työn tehtävänannon ja sovittujen arviointikriteerien perusteella sekä antaa tarvittaessa palautetta. Ei oleteta päivittäiseksi projektin päätöksentekijäksi. |
| Loppukäyttäjä | Antaa näkökulman sovelluksen käytettävyyteen ja tarpeisiin; käyttäjärooli kuvataan vaatimuksissa ja käyttäjätarinoissa. |

Jos projektin toteuttaa yksi opiskelija, erillistä kehitystiimiä tai usean henkilön hyväksymisketjua ei oleteta. Git-haaroja ja Pull Requesteja käytetään mahdollisuuksien mukaan versionhallinnan ja tarkasteluprosessin harjoitteluun; käytännöt pidetään projektin kokoon nähden kevyinä.

## 5. Aikataulu ja välitavoitteet

Projektin tavoitekesto on viisi viikkoa. Alla olevat M1–M5-välitavoitteet ovat viikkokohtaisia tavoitetuloksia. Product Backlogin ja Sprint-suunnitelman viiden Sprintin jako on alustava; Sprinttien tarkka kesto ja viikkotavoitteiden suhde Sprintteihin vahvistetaan Sprint Planningissa.

| Välitavoite | Ajankohta | Keskeinen työ | Valmistumisen näyttö |
|---|---|---|---|
| M1 – Suunnittelu ja tekninen perusta | Viikko 1 | Vaatimusten ja backlogiin tutustuminen, arkkitehtuuri- ja tietomalliratkaisujen tarkentaminen, repositoryn käytännöt, Docker Composen perusrakenne | Dokumentoidut arkkitehtuuriratkaisut ja käynnistettävä kehitysympäristö tai selkeästi kirjattu tekninen este |
| M2 – Backend, tietokanta ja käyttäjähallinta | Viikko 2 | Tietokantamalli, yhteys tietokantaan, REST-rajapinnan perusrakenne, rekisteröityminen ja kirjautuminen | Tietokanta toimii ja käyttäjähallinnan keskeiset testit läpäistään |
| M3 – Tukipyyntöjen ydinkulku | Viikko 3 | Tukipyyntöjen luonti, omien pyyntöjen tarkastelu ja sulkeminen, käyttöoikeuksien tarkistukset, keskustelun tekninen perusta | Käyttäjä pystyy kirjautuneena hallitsemaan omia tukipyyntöjään |
| M4 – AI-chat ja käyttöliittymän kielet | Viikko 4 | AI-integraatio, keskusteluviestien tallennus, tarkentavat kysymykset, suomen- ja englanninkielinen käyttöliittymä; RAG:n tekninen kokeilu | AI-chat toimii hallitusti ja kielivalinta on testattu; RAG:n lähteet ja toteutuspolku on täsmennetty |
| M5 – RAG, integrointi ja toimitusvalmius | Viikko 5 | RAG:n viimeistely sovitulla dokumenttikokoelmalla, Docker Compose -kokonaisuuden tarkistus, regressiotestaus, dokumentaatio ja demo | Kolme valittua lisäominaisuutta on todennettu sovitussa laajuudessa; README, API-dokumentaatio, ER-kaavio ja demo ovat valmiit |

**Aikataulun tarkennus:** Product Backlogin alustavassa jaossa `US-16` (Docker Compose) on Sprint 1:ssä, `US-13` (monikielisyys) Sprint 4:ssä ja `US-15` (RAG) Sprint 5:ssä. Dockerin perusrakenne aloitetaan aikaisin. RAG-ratkaisua voidaan kokeilla aiemmin, vaikka sen hyväksytty kokonaisuus on alustavasti sijoitettu Sprint 5:een. Tämä Sprint-jako ei yksinään määritä Sprinttien kestoa.

Sprintin tavoite on suunnitelma, ei lupaus siitä, että jokainen tehtävä valmistuu hinnalla millä hyvänsä. Jos työmääräarviot tai tekniset esteet muuttuvat, Product Backlog ja jäljellä olevat tavoitteet tarkistetaan.

## 6. Keskeiset riippuvuudet

| Kohde | Riippuvuus | Hallintatapa |
|---|---|---|
| Käyttäjähallinta | Tietomalli, tietokantayhteys, salasanan turvallinen käsittely ja autentikointi | Toteutetaan ja testataan ennen suojattujen toimintojen laajentamista |
| Tukipyyntöjen hallinta | REST-rajapinta, tietokanta ja kirjautuneen käyttäjän tunnistaminen | Testataan sekä omistajan oikeudet että luvattoman käytön estäminen |
| Keskusteluhistorian tallennus | Keskustelun ja viestien tietomalli sekä tietokantayhteys | Määritellään viestien ja keskustelujen väliset suhteet arkkitehtuurivaiheessa |
| AI-chat | Backendin yhteys valittuun AI-malliin tai -palveluun | Tehdään pieni integraatiokoe varhaisessa vaiheessa ja käsitellään palveluvirheet |
| RAG | AI-chat, rajatut lähdedokumentit, dokumenttien käsittely ja hakuratkaisu | Rajataan lähdeaineisto; testataan sekä relevantit haut että tilanne, jossa lähdettä ei löydy |
| Monikielinen käyttöliittymä | Käyttöliittymän tekstien erottaminen kieliresursseihin | Sovitaan kielivalinnan tallennustapa ja testataan tärkeimmät näkymät molemmilla kielillä |
| Docker Compose | Frontendin, backendin ja tietokannan käynnistysasetukset, ympäristömuuttujat ja verkkoyhteydet | Testataan palvelut yhdessä ja kirjataan yksi toistettava käynnistyskomento |
| Lopullinen toimitus | Testitulokset, dokumentaatio ja käynnistysprosessin toimivuus | Varaa viimeiseen Sprintiin aikaa koko sovelluksen läpikäyntiin ja puuttuvien kohtien korjaamiseen |

Riippuvuus ei aina tarkoita, että koko edeltävän toiminnon pitää olla valmis ennen seuraavan aloittamista. Esimerkiksi RAG:n lähdedokumentteja ja Dockerin rakennetta voidaan valmistella rinnakkain, kunhan integraatiot testataan kokonaisuutena.

## 7. Riskienhallinta

Riskit arvioidaan laadullisesti vaikutuksen ja todennäköisyyden perusteella. Rekisteriä päivitetään vähintään jokaisen Sprintin lopussa sekä silloin, kun uusi merkittävä este ilmenee.

| ID | Riski | Todennäköisyys | Vaikutus | Ehkäisevä toimenpide / varasuunnitelma | Seuranta |
|---|---|---|---|---|---|
| R1 | AI-mallin tai -palvelun integrointi vie odotettua enemmän aikaa | Keskitaso | Korkea | Testataan yhteys ja yksi kysymys-vastaus-kierros varhain; pidetään AI-kerros erillään muusta backendistä | Tarkistetaan Sprint 1–2 aikana |
| R2 | RAG:n hakutulokset ovat heikkoja tai lähteet eivät vastaa kysymykseen | Korkea | Korkea | Käytetään pientä, hallittua dokumenttikokoelmaa; testataan tunnetuilla kysymyksillä; näytetään lähteet ja kerrotaan, jos sopivaa lähdettä ei löydy | Tarkistetaan ennen RAG:n hyväksymistä |
| R3 | Viiden viikon työmäärä ei riitä kaikkiin toimintoihin | Keskitaso | Korkea | Priorisoidaan pakolliset toiminnot ja kolme valittua lisäominaisuutta; jätetään ensin ehdollinen US-14 ja muut ei-välttämättömät viimeistelyt toteuttamatta | Arvioidaan viikoittain |
| R4 | Docker-palvelut eivät toimi yhdessä tai ympäristömuuttujat puuttuvat | Keskitaso | Korkea | Aloitetaan Compose-rakenne Sprint 1:ssä; testataan puhtaalla käynnistyksellä; dokumentoidaan asetukset ja salaisuuksien käsittely | Tarkistetaan jokaisessa merkittävässä integraatiossa |
| R5 | Käyttäjä voi nähdä tai muuttaa toisen käyttäjän tietoja | Keskitaso | Korkea | Tarkistetaan omistajuus backendissä; lisätään luvattoman käytön testit; ei luoteta pelkästään käyttöliittymän piilotuksiin | Testataan ennen toimitusta |
| R6 | Salasanoja tai muita salaisuuksia käsitellään turvattomasti | Matala–keskitaso | Korkea | Tallennetaan salasanat vain turvallisesti tiivistettyinä; ei lisätä tunnuksia, API-avaimia tai `.env`-salaisuuksia repositoryyn | Tarkistetaan koodi ja repository ennen demoa |
| R7 | Käyttöliittymän käännökset jäävät osittaisiksi | Keskitaso | Keskitaso | Keskitetään tekstit kieliresursseihin; testataan tärkeimmät näkymät suomeksi ja englanniksi | Tarkistetaan Sprint 4:ssä |
| R8 | Testaus ja dokumentointi jäävät viime hetkeen | Keskitaso | Korkea | Kirjataan testit toteutuksen yhteydessä; varataan Sprint 5:een erillinen aika integraatiotestaukselle ja dokumentoinnille | Tarkistetaan Sprint-arvioinnissa |
| R9 | Valittu AI-palvelu ei ole käytettävissä esittelyhetkellä | Keskitaso | Keskitaso–korkea | Testataan virhetilanteet ja dokumentoidaan palvelun asetukset; varmistetaan etukäteen, että esittely-ympäristö toimii | Tarkistetaan ennen lopullista esittelyä |

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
- frontend, backend ja tietokanta käynnistyvät dokumentoidulla Docker Compose -komennolla
- README, API-dokumentaatio ja ER-kaavio vastaavat toteutunutta järjestelmää.

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
| D-03 | 26.10.2026 | `US-14`-yhteenvetonäkymä käsitellään toissijaisena | Ajan riittävyys ja valittujen lisäominaisuuksien suojaaminen | Ominaisuus toteutetaan vain, jos ydinsisältö etenee suunnitellusti |
| D-04 | 26.10.2026 | `US-16`:n alustava arvio on 5 SP; rajaus kattaa kehitys- ja esittely-ympäristön Docker Compose -käynnistyksen | Backlogin tarkennettu toteutuslaajuus | AI-palvelun kontitus ja tuotantokäyttöönotto eivät kuulu arvioon |

## 11. Muutosloki

| Päivämäärä | Versio | Muutos | Tekijä |
|---|---|---|---|
| 26.10.2026 | 0.1 | Projektinhallintadokumentin ensimmäinen versio | Projektin toteuttaja |
| 26.10.2026 | 0.2 | Päivitetty nykytilanne, Sprint-aikataulun tarkennus sekä US-14:n ja US-16:n rajaukset; selkeytetty README:n ja hallintadokumentin vastuut | Projektin toteuttaja |

## 12. Linkit projektin muihin dokumentteihin

- [Vaatimusmäärittely](01-vaatimusmaarittely.md)
- [Käyttäjätarinat ja hyväksymiskriteerit](02-käyttäjätarinat%20ja%20hyväksymiskriteerit.md)
- [Product Backlog](03-product%20backlog.md)
- [Sprint-suunnitelma](04-sprintin%20suunnitelma.md)
- [Järjestelmän suunnittelu](05-järjestelmän%20suunnittelu.md)
- [README](../README.md)

> **Ylläpitokäytäntö:** päivitä tätä dokumenttia projektin edetessä, erityisesti aikataulun, riskien, merkittävien päätösten ja laajuusmuutosten osalta. Älä kopioi tänne muiden dokumenttien yksityiskohtaisia vaatimuksia tai käyttäjätarinoita; linkitä niiden lähteisiin.
