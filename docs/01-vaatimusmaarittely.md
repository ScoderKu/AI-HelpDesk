# AI HelpDesk – Vaatimusmäärittely

**Projektin määrittely**

## 1. Projektin yleiskuvaus

AI HelpDesk on tekoälyä hyödyntävä tukipalvelusovellus, jonka tarkoituksena on auttaa käyttäjiä ratkaisemaan tietotekniikkaan ja ohjelmistokehitykseen liittyviä ongelmia. Sovellus tarjoaa keskustelupohjaisen käyttöliittymän, jossa käyttäjä voi kuvata ongelmansa ja saada tekoälyn tuottamia ehdotuksia ongelman ratkaisemiseksi.

Jos ongelmaa ei saada ratkaistua keskustelun aikana, käyttäjä voi luoda tukipyynnön ja seurata sen tilaa sovelluksessa. Käyttäjien tiedot, tukipyynnöt ja keskusteluviestit tallennetaan relaatiotietokantaan.

Projektissa toteutetaan toimiva web-sovellus, joka sisältää käyttöliittymän, palvelinpuolen REST-rajapinnan, tietokannan ja tekoälyintegraation.

## 2. Ongelman kuvaus
Tietotekniikan käyttäjät kohtaavat usein ongelmia, joiden ratkaiseminen vaatii teknistä osaamista tai erillisen tukipalvelun apua. Ongelmien kuvaaminen, oikeiden ohjeiden löytäminen ja tukipyyntöjen hallinta voivat viedä aikaa.

Perinteisessä tukipalvelussa käyttäjä saattaa joutua odottamaan vastausta tai etsimään ratkaisua useista eri lähteistä. Lisäksi ongelman ratkaisemiseen liittyvät tiedot voivat jäädä hajanaisiksi.

AI HelpDesk pyrkii helpottamaan tätä prosessia tarjoamalla tekoälypohjaista neuvontaa, mahdollisuuden esittää tarkentavia kysymyksiä ja keskitetyn paikan tukipyyntöjen hallintaan.

## 3. Projektin tavoitteet

Projektin tavoitteena on suunnitella ja toteuttaa toimiva AI HelpDesk -sovellus, joka täyttää seuraavat tavoitteet:
- Käyttäjä voi rekisteröityä ja kirjautua sisään.
- Käyttäjä voi tarkastella profiilitietojaan, muokata etunimeä, sukunimeä ja käyttäjänimeä sekä vaihtaa salasanansa nykyisen salasanan vahvistuksella. Sähköpostiosoite on vain luettavissa eikä sitä voi muuttaa.
- Käyttäjä voi keskustella tekoälyn kanssa teknisistä ongelmista.
- Tekoäly voi pyytää lisätietoja, kuten käyttöjärjestelmän, virheilmoituksen tai ongelman toistamiseen liittyvät vaiheet.
- Käyttäjä voi luoda tukipyyntöjä, tarkastella omia tukipyyntöjään ja sulkea niitä.
- Sovellus tallentaa käyttäjätiedot, tukipyynnöt ja keskusteluviestit tietokantaan.
- Sovellus tarjoaa REST-rajapinnan tietojen käsittelyä varten.
- Projekti toteutetaan versionhallintaa ja Scrum-menetelmää hyödyntäen.
- Viralliseen toimituslaajuuteen kuuluvat tukipyynnön luominen AI-keskustelusta käyttäjän vahvistuksen jälkeen (US-09) ja kirjautuneen käyttäjän rajattu tukipyyntöyhteenveto (US-14).
- Lopulliseen julkaisuun toteutetaan kolme valittua lisäominaisuutta: tietopohjainen tekoälyneuvonta (RAG), suomen- ja englanninkielinen käyttöliittymä sekä sovelluksen ja Ollaman käynnistäminen Docker Composella yhdellä komennolla.

## 4. Kohderyhmät

Projektin ensisijaisia kohderyhmiä ovat:
- Opiskelijat: voivat pyytää apua ohjelmistoihin, ohjelmointiin ja tietotekniikkaan liittyvissä ongelmissa.
- Muut loppukäyttäjät: voivat käyttää tekoälypohjaista neuvontaa ja hallita omia tukipyyntöjään.
- Projektin kehittäjät: vastaavat sovelluksen toteutuksesta, testauksesta, dokumentoinnista ja ylläpidettävyydestä.

## 5. Projektin rajaus

Projektin laajuus rajataan siten, että sovellus voidaan toteuttaa ja testata viiden viikon opiskelijaprojektin aikana.

### 5.1 Toteutukseen sisältyvät ominaisuudet

- Käyttäjän rekisteröityminen ja kirjautuminen.
- Käyttäjäprofiilin tarkastelu ja muokkaaminen.
- Tukipyyntöjen luominen, tarkastelu ja sulkeminen.
- Tukipyyntöjen tilan ja prioriteetin hallinta.
- Tekoälypohjainen chat ja ongelmanratkaisu.
- Keskusteluviestien tallentaminen tietokantaan.
- Tukipyynnön luominen keskustelusta käyttäjän tarkistuksen ja vahvistuksen jälkeen.
- Tukipyyntöjen rajattu yhteenveto: käyttäjän kokonaismäärä ja `OPEN`/`CLOSED`-määrät.
- Tietopohjainen tekoälyneuvonta (RAG) Markdown- ja TXT-dokumenteista avainsanahaulla.
- Suomen- ja englanninkielinen käyttöliittymä.
- Frontendin, backendin, MySQL:n ja Ollaman käynnistäminen Docker Composella yhdellä komennolla.
- REST-rajapinta sovelluksen tietojen käsittelyyn.
- MySQL-tietokanta.
- GitHub-versionhallinta, haarat ja Pull Request -käytännöt.
- Tekninen dokumentaatio ja sovelluksen esittely.

### 5.2 Toteutuksen ulkopuolelle rajatut ominaisuudet

Seuraavat ominaisuudet eivät kuulu ensimmäiseen toteutusversioon, ellei niiden lisääminen ole myöhemmin tarpeellista:
- Laajamittaisen yritystason IT-palvelunhallinnan toteuttaminen.
- Yliopiston keskitetyn tunnistautumisjärjestelmän integrointi.
- Käyttäjän tietokoneella suoritettavien komentojen automaattinen suorittaminen.
- Täysin itsenäinen ongelmanratkaisu ilman käyttäjän osallistumista.
- Laaja organisaatioiden välinen käyttöoikeuksien ja tukipalveluroolien hallinta.

## 6. Toiminnalliset vaatimukset

Sovelluksen on täytettävä seuraavat toiminnalliset vaatimukset.

| Tunnus | Vaatimus |
|---|---|
| FR-01 | Käyttäjä voi rekisteröityä ja kirjautua sisään. |
| FR-02 | Käyttäjä voi tarkastella profiilitietojaan, muokata etunimeä, sukunimeä ja käyttäjänimeä sekä vaihtaa salasanansa nykyisen salasanan vahvistuksella. Sähköpostiosoite on vain luettavissa eikä sitä voi muuttaa. |
| FR-03 | Käyttäjä voi luoda uuden tukipyynnön. |
| FR-04 | Käyttäjä voi tarkastella ja sulkea omia tukipyyntöjään. |
| FR-05 | Tukipyynnössä on otsikko, kuvaus, tila, prioriteetti, luontiaika ja käyttäjän tunniste. |
| FR-06 | Sovellus tarjoaa käyttöliittymän tekoälypohjaista keskustelua varten. |
| FR-07 | Tekoäly voi esittää tarkentavia kysymyksiä ja ehdottaa ongelmanratkaisuvaiheita. |
| FR-08 | Keskusteluviestit tallennetaan tietokantaan. |
| FR-09 | Käyttäjä voi luoda tukipyynnön AI-keskustelusta vasta tarkistettuaan ja vahvistettuaan ehdotetut tiedot; ilman vahvistusta tukipyyntöä ei luoda. |
| FR-10 | Sovellus tarjoaa REST-rajapinnan tukipyyntöjen ja muiden tietojen käsittelyyn. |
| FR-11 | Käyttäjät, tukipyynnöt ja viestit tallennetaan MySQL-tietokantaan. |
| FR-12 | Projektin lähdekoodi ja kehityshistoria hallitaan GitHubissa. |
| FR-13 | AI HelpDesk hakee kysymykseen liittyviä kohtia rajatusta Markdown- ja TXT-dokumenttikokoelmasta avainsanahaulla, välittää löydetyn sisällön Ollama-mallille ja näyttää käytetyn lähteen tiedot. Jos sopivaa sisältöä ei löydy, järjestelmä ei esitä vastausta dokumentaation vahvistamana. Semanttinen haku lisätään vain, jos testinäyttö osoittaa avainsanahaun riittämättömäksi. |
| FR-14 | Käyttöliittymä on käytettävissä suomeksi ja englanniksi, ja käyttäjän kielivalinta säilyy. |
| FR-15 | Frontend, backend, MySQL-tietokanta, Ollama-palvelu ja valittu tekoälymalli voidaan ottaa käyttöön Docker Composella yhdellä README:ssä dokumentoidulla komennolla. Backend käyttää Ollamaa Compose-verkon kautta. |
| FR-16 | Kirjautunut käyttäjä voi tarkastella omien tukipyyntöjensä kokonaismäärää sekä `OPEN`- ja `CLOSED`-tiloissa olevien pyyntöjen määriä; muilta käyttäjiltä ei palauteta tietoja. |

## 7. Ei-toiminnalliset vaatimukset

- Tietoturva: salasanoja ei tallenneta selväkielisinä. Käyttäjä voi käyttää ja muokata vain niitä tietoja, joihin hänellä on oikeus.
- Tietojen eheys: tietokannan tietojen on säilyttävä johdonmukaisina ja liittymien on oltava oikein määriteltyjä.
- Käytettävyys: käyttöliittymän on oltava selkeä ja tärkeimpien toimintojen on oltava helposti löydettävissä.
- Ylläpidettävyys: lähdekoodin on oltava rakenteeltaan selkeä ja jaettu tarkoituksenmukaisiin osiin.
- Luotettavuus: sovelluksen on käsiteltävä virhetilanteet hallitusti ja annettava käyttäjälle ymmärrettävä palaute.
- Tietosuoja: käyttäjien henkilötietoja ja keskustelutietoja käsitellään vain sovelluksen toiminnan kannalta tarpeellisessa laajuudessa.
- Teknologioiden käyttöehdot: työkalujen ja kirjastojen tulee olla maksuttomia, ja lisenssit sekä käyttöehdot tarkistetaan ennen käyttöönottoa.
- Testattavuus: keskeisille toiminnoille on laadittava testit, joiden avulla vaatimusten toteutuminen voidaan todentaa.

## 8. Teknologiset rajoitteet ja vaatimukset

Projektin teknisten ratkaisujen on täytettävä seuraavat ehdot:
- Tietokantana käytetään MySQL-järjestelmää.
- Backend tarjoaa REST-rajapinnan.
- Tekoälyintegraatio käyttää Ollamaa Docker-kontissa ja mallia `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`.
- Ollama-ympäristö testataan NVIDIA-GPU:lla. Muiden GPU-valmistajien tai -tyyppien yhteensopivuutta ei varmenneta; niitä käyttävä testaa yhteensopivuuden itse.
- Frontendin ja backendin on toimittava yhdessä.
- Valittujen työkalujen ja kirjastojen tulee olla maksuttomia, ja niiden lisenssit sekä käyttöehdot tarkistetaan ennen käyttöönottoa.
- Lähdekoodia hallitaan GitHubissa.
- Kehityksessä käytetään haaroja ja Pull Request -toimintoa.
- Lopullinen julkaisu sisältää kolme valittua lisäominaisuutta: RAG-neuvonnan, suomen- ja englanninkielisen käyttöliittymän sekä yhden komennon Docker Compose -käynnistyksen.

## 9. Valitut teknologiset lähtökohdat

Seuraavat teknologiat ovat sovitut lähtökohdat ennen toteutusta.

| Osa-alue | Ehdotettu teknologia |
|---|---|
| Frontend | React |
| Backend | Python ja FastAPI |
| Tietokanta | MySQL |
| Tekoälypalvelu | Ollama Docker Compose -palveluna |
| Tekoälymalli | `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf` |
| API-dokumentaatio | OpenAPI / Swagger UI |
| Versionhallinta | Git ja GitHub |
| Kontitus ja kehitysympäristö | Docker Compose: frontend, backend, MySQL ja Ollama |

Malli ja muut työkalut testataan käytettävissä olevilla resursseilla. Ollama-testaus rajataan NVIDIA-GPU:hun; muiden GPU:iden yhteensopivuutta ei varmenneta projektissa. Mallin, työkalujen ja kirjastojen lisenssit sekä käyttöehdot tarkistetaan ennen niiden sisällyttämistä toimitukseen.

## 10. Oletukset

- Tekoälyn tuottamat vastaukset voivat olla virheellisiä, joten käyttäjälle ei luvata ongelman automaattista ratkeamista.
- US-09 ja US-14 kuuluvat viralliseen toimituslaajuuteen; niiden toteutus ei ole ehdollinen jäljelle jäävälle ajalle.
- RAG MVP käyttää ryhmän ennen toteutusta rajaamaa Markdown- ja TXT-dokumenttikokoelmaa sekä avainsanahakua. Semanttinen haku ei kuulu alkuperäiseen MVP-laajuuteen.
- Ollama ja valittu GGUF-malli ajetaan Docker Compose -ympäristössä. Sprint 1:n sisältö ja suunnitelma säilyvät ennallaan.
- ER-/tietokantaskeemaa ei muuteta RAG:n vuoksi, ellei toteutuksessa ilmene uutta pysyvää tietotarvetta.

## 11. Projektin onnistumiskriteerit

Projekti katsotaan onnistuneeksi, kun:
- Käyttäjä voi rekisteröityä, kirjautua sisään ja muokata profiiliaan.
- Käyttäjä voi luoda, tarkastella ja sulkea tukipyyntöjä.
- Käyttäjä voi luoda keskustelusta tukipyynnön vasta tarkistettuaan ja vahvistettuaan tiedot.
- Käyttäjä näkee vain omien tukipyyntöjensä kokonaismäärän sekä `OPEN`- ja `CLOSED`-määrät.
- Tukipyynnöt ja keskusteluviestit tallentuvat tietokantaan.
- Tekoälychat toimii Ollama-palvelun ja valitun mallin avulla Docker Compose -ympäristössä.
- REST-rajapinnan keskeiset toiminnot on toteutettu ja testattu.
- Valitut lisäominaisuudet toimivat: RAG hyödyntää rajattuja Markdown- ja TXT-lähteitä avainsanahaulla, käyttöliittymä tukee suomea ja englantia, ja sovellus sekä Ollama käynnistyvät Docker Composella dokumentoidulla yhdellä komennolla.
- Lähdekoodi, kehityshistoria ja tarvittavat Pull Requestit löytyvät GitHubista.
- README, tietokantakuvaus, ER-kaavio, kuvakaappaukset ja API-dokumentaatio ovat saatavilla.

## 12. Vaatimusten jäljitettävyys

Seuraava taulukko yhdistää toiminnalliset vaatimukset käyttäjätarinoihin, hyväksymiskriteereihin ja todennustapaan. Testitunnukset ovat suunniteltuja tunnisteita, jotka täsmennetään testitapauksiksi toteutuksen yhteydessä.

| Vaatimus | Käyttäjätarina ja hyväksymiskriteerit | Todentaminen |
|---|---|---|
| FR-01 | US-01 (AC-01.1–AC-01.4), US-02 (AC-02.1–AC-02.3) | TEST-01: rekisteröityminen, kirjautuminen ja käyttöoikeuden tarkistus |
| FR-02 | US-03 (AC-03.1–AC-03.5) | TEST-02: profiilin haku, sallittujen tietojen päivitys, salasanan vaihto ja sähköpostin muuttamisen esto |
| FR-03 | US-04 (AC-04.1–AC-04.3) | TEST-03: tukipyynnön luominen ja kenttien validointi |
| FR-04 | US-05 (AC-05.1–AC-05.4) | TEST-04: omien pyyntöjen listaus, sulkeminen ja omistajuustarkistus |
| FR-05 | US-04 (AC-04.2) | TEST-05: tukipyynnön kentät, oletusarvot ja aikaleimat |
| FR-06 | US-06 (AC-06.1–AC-06.4) | TEST-06: kirjautuneen käyttäjän viestin lähetys ja tekoälyvastaus |
| FR-07 | US-07 (AC-07.1–AC-07.3) | TEST-07: tarkentavan kysymyksen ja ratkaisuehdotuksen tarkistus |
| FR-08 | US-08 (AC-08.1–AC-08.3) | TEST-08: viestien tallennus ja historian järjestys |
| FR-09 | US-09 (AC-09.1–AC-09.4) | TEST-09: tietojen tarkistus, vahvistettu luonti, hylkäys/peruutus ja keskustelun omistajuuden tarkistus |
| FR-10 | US-10 (AC-10.1–AC-10.4) | TEST-10: API:n onnistuneet, virheelliset ja luvattomat pyynnöt |
| FR-11 | US-11 (AC-11.1–AC-11.3) | TEST-11: pysyvä tallennus, haku ja viite-eheys |
| FR-12 | Ei käyttäjätarinaa; projektikäytäntö | TEST-12: GitHub-repository, haarat ja Pull Request -historia |
| FR-13 | US-15 (AC-15.1–AC-15.4) | TEST-13: Markdown/TXT-avainsanahaku, löydetyn lähteen näyttäminen ja tyhjän hakutuloksen käsittely |
| FR-14 | US-13 (AC-13.1–AC-13.3) | TEST-14: suomen- ja englanninkielinen käyttöliittymä sekä kielivalinnan säilyminen |
| FR-15 | US-16 (AC-16.1–AC-16.4) | TEST-15: frontendin, backendin, MySQL:n, Ollaman ja mallin käynnistys README:n yhdellä Docker Compose -komennolla sekä backendin Ollama-yhteys |
| FR-16 | US-14 (AC-14.1–AC-14.4) | TEST-16: kirjautuneen käyttäjän kokonaismäärä ja OPEN/CLOSED-määrät tyhjässä ja täydessä tilanteessa sekä omistajuuden tarkistus |
