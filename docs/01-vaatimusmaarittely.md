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
- Käyttäjä voi rekisteröityä, kirjautua sisään ja muokata omia profiilitietojaan.
- Käyttäjä voi keskustella tekoälyn kanssa teknisistä ongelmista.
- Tekoäly voi pyytää lisätietoja, kuten käyttöjärjestelmän, virheilmoituksen tai ongelman toistamiseen liittyvät vaiheet.
- Käyttäjä voi luoda tukipyyntöjä, tarkastella omia tukipyyntöjään ja sulkea niitä.
- Sovellus tallentaa käyttäjätiedot, tukipyynnöt ja keskusteluviestit tietokantaan.
- Sovellus tarjoaa REST-rajapinnan tietojen käsittelyä varten.
- Projekti toteutetaan versionhallintaa ja Scrum-menetelmää hyödyntäen.
- Lopulliseen julkaisuun toteutetaan kolme valittua lisäominaisuutta: tietopohjainen tekoälyneuvonta (RAG), suomen- ja englanninkielinen käyttöliittymä sekä sovelluksen käynnistäminen Docker Composella yhdellä komennolla.

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
- Tietopohjainen tekoälyneuvonta (RAG).
- Suomen- ja englanninkielinen käyttöliittymä.
- Sovelluksen käynnistäminen Docker Composella yhdellä komennolla.
- REST-rajapinta sovelluksen tietojen käsittelyyn.
- MySQL- tai MariaDB-tietokanta.
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
| FR-02 | Käyttäjä voi tarkastella ja muokata omia profiilitietojaan. |
| FR-03 | Käyttäjä voi luoda uuden tukipyynnön. |
| FR-04 | Käyttäjä voi tarkastella ja sulkea omia tukipyyntöjään. |
| FR-05 | Tukipyynnössä on otsikko, kuvaus, tila, prioriteetti, luontiaika ja käyttäjän tunniste. |
| FR-06 | Sovellus tarjoaa käyttöliittymän tekoälypohjaista keskustelua varten. |
| FR-07 | Tekoäly voi esittää tarkentavia kysymyksiä ja ehdottaa ongelmanratkaisuvaiheita. |
| FR-08 | Keskusteluviestit tallennetaan tietokantaan. |
| FR-09 | Sovellus voi tarjota mahdollisuuden luoda tukipyyntö, jos ongelma jää ratkaisematta. |
| FR-10 | Sovellus tarjoaa REST-rajapinnan tukipyyntöjen ja muiden tietojen käsittelyyn. |
| FR-11 | Käyttäjät, tukipyynnöt ja viestit tallennetaan MySQL- tai MariaDB-tietokantaan. |
| FR-12 | Projektin lähdekoodi ja kehityshistoria hallitaan GitHubissa. |
| FR-13 | AI HelpDesk hakee käyttäjän kysymykseen liittyvää teknistä dokumentaatiota ja välittää löydetyn sisällön tekoälylle vastauksen muodostamista varten. |
| FR-14 | Käyttöliittymä on käytettävissä suomeksi ja englanniksi, ja käyttäjän kielivalinta säilyy. |
| FR-15 | Frontend, backend ja MySQL-tietokanta voidaan käynnistää Docker Composella yhdellä README:ssä dokumentoidulla komennolla. |

## 7. Ei-toiminnalliset vaatimukset

- Tietoturva: salasanoja ei tallenneta selväkielisinä. Käyttäjä voi käyttää ja muokata vain niitä tietoja, joihin hänellä on oikeus.
- Tietojen eheys: tietokannan tietojen on säilyttävä johdonmukaisina ja liittymien on oltava oikein määriteltyjä.
- Käytettävyys: käyttöliittymän on oltava selkeä ja tärkeimpien toimintojen on oltava helposti löydettävissä.
- Ylläpidettävyys: lähdekoodin on oltava rakenteeltaan selkeä ja jaettu tarkoituksenmukaisiin osiin.
- Luotettavuus: sovelluksen on käsiteltävä virhetilanteet hallitusti ja annettava käyttäjälle ymmärrettävä palaute.
- Tietosuoja: käyttäjien henkilötietoja ja keskustelutietoja käsitellään vain sovelluksen toiminnan kannalta tarpeellisessa laajuudessa.
- Testattavuus: keskeisille toiminnoille on laadittava testit, joiden avulla vaatimusten toteutuminen voidaan todentaa.

## 8. Teknologiset rajoitteet ja vaatimukset

Projektin teknisten ratkaisujen on täytettävä seuraavat ehdot:
- Tietokantana käytetään MySQL- tai MariaDB-järjestelmää.
- Backend tarjoaa REST-rajapinnan.
- Tekoälyintegraatio käyttää hyväksyttyä tekoälymallia tai -palvelua.
- Frontendin ja backendin on toimittava yhdessä.
- Lähdekoodia hallitaan GitHubissa.
- Kehityksessä käytetään haaroja ja Pull Request -toimintoa.
- Lopullinen julkaisu sisältää kolme valittua lisäominaisuutta: RAG-neuvonnan, suomen- ja englanninkielisen käyttöliittymän sekä yhden komennon Docker Compose -käynnistyksen.

## 9. Alustavat teknologiset valinnat

Seuraavat teknologiat ovat projektin alustava ehdotus.

| Osa-alue | Ehdotettu teknologia |
|---|---|
| Frontend | React |
| Backend | Python ja FastAPI |
| Tietokanta | MySQL |
| Tekoäly | Ollama |
| API-dokumentaatio | OpenAPI / Swagger UI |
| Versionhallinta | Git ja GitHub |
| Kontitus | Docker |

Tekoälymalli valitaan sen perusteella, että se pystyy tuottamaan hyödyllisiä teknisiä ohjeita ja että sen käyttö on mahdollista projektin käytettävissä olevilla resursseilla.

## 10. Oletukset

- Tekoälyn tuottamat vastaukset voivat olla virheellisiä, joten käyttäjälle ei luvata ongelman automaattista ratkeamista.
- Kolme valittua lisäominaisuutta kuuluvat lopulliseen julkaisuun. Monikielinen käyttöliittymä ja RAG toteutetaan MVP:n jälkeen; Docker Compose -ympäristö perustetaan Sprint 1:ssä.

## 11. Projektin onnistumiskriteerit

Projekti katsotaan onnistuneeksi, kun:
- Käyttäjä voi rekisteröityä, kirjautua sisään ja muokata profiiliaan.
- Käyttäjä voi luoda, tarkastella ja sulkea tukipyyntöjä.
- Tukipyynnöt ja keskusteluviestit tallentuvat tietokantaan.
- Tekoälychat toimii oikean tekoälymallin tai -palvelun avulla.
- REST-rajapinnan keskeiset toiminnot on toteutettu ja testattu.
- Valitut lisäominaisuudet toimivat: RAG hyödyntää dokumentaatiota, käyttöliittymä tukee suomea ja englantia, ja sovellus käynnistyy Docker Composella dokumentoidulla yhdellä komennolla.
- Lähdekoodi, kehityshistoria ja tarvittavat Pull Requestit löytyvät GitHubista.
- README, tietokantakuvaus, ER-kaavio, kuvakaappaukset ja API-dokumentaatio ovat saatavilla.

## 12. Vaatimusten jäljitettävyys

Seuraava taulukko yhdistää toiminnalliset vaatimukset käyttäjätarinoihin, hyväksymiskriteereihin ja todennustapaan. Testitunnukset ovat suunniteltuja tunnisteita, jotka täsmennetään testitapauksiksi toteutuksen yhteydessä.

| Vaatimus | Käyttäjätarina ja hyväksymiskriteerit | Todentaminen |
|---|---|---|
| FR-01 | US-01 (AC-01.1–AC-01.4), US-02 (AC-02.1–AC-02.3) | TEST-01: rekisteröityminen, kirjautuminen ja käyttöoikeuden tarkistus |
| FR-02 | US-03 (AC-03.1–AC-03.3) | TEST-02: oman profiilin haku ja sallittujen tietojen päivitys |
| FR-03 | US-04 (AC-04.1–AC-04.3) | TEST-03: tukipyynnön luominen ja kenttien validointi |
| FR-04 | US-05 (AC-05.1–AC-05.4) | TEST-04: omien pyyntöjen listaus, sulkeminen ja omistajuustarkistus |
| FR-05 | US-04 (AC-04.2) | TEST-05: tukipyynnön kentät, oletusarvot ja aikaleimat |
| FR-06 | US-06 (AC-06.1–AC-06.4) | TEST-06: kirjautuneen käyttäjän viestin lähetys ja tekoälyvastaus |
| FR-07 | US-07 (AC-07.1–AC-07.3) | TEST-07: tarkentavan kysymyksen ja ratkaisuehdotuksen tarkistus |
| FR-08 | US-08 (AC-08.1–AC-08.3) | TEST-08: viestien tallennus ja historian järjestys |
| FR-09 | US-09 (AC-09.1–AC-09.3) | TEST-09: vahvistettu luonti, hylkäyksen käsittely ja keskustelun omistajuuden tarkistus |
| FR-10 | US-10 (AC-10.1–AC-10.4) | TEST-10: API:n onnistuneet, virheelliset ja luvattomat pyynnöt |
| FR-11 | US-11 (AC-11.1–AC-11.3) | TEST-11: pysyvä tallennus, haku ja viite-eheys |
| FR-12 | Ei käyttäjätarinaa; projektikäytäntö | TEST-12: GitHub-repository, haarat ja Pull Request -historia |
| FR-13 | US-15 (AC-15.1–AC-15.3) | TEST-13: dokumentaation haku, lähteen näyttäminen ja tyhjän hakutuloksen käsittely |
| FR-14 | US-13 (AC-13.1–AC-13.3) | TEST-14: suomen- ja englanninkielinen käyttöliittymä sekä kielivalinnan säilyminen |
| FR-15 | US-16 (AC-16.1–AC-16.3) | TEST-15: sovelluksen käynnistys puhtaassa ympäristössä README:n yhdellä Docker Compose -komennolla |