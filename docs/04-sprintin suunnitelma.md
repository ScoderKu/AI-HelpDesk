# AI HelpDesk – Sprintin suunnitelma (Scrum framework)

## 1. Sprint-suunnitelman tarkoitus

Tämä dokumentti määrittelee AI HelpDesk -sovelluksen alustavan sprinttisuunnitelman. Suunnitelmassa kuvataan sprinttien tavoitteet, toteutettavat käyttäjätarinat, työmääräarviot, keskeiset tehtävät ja odotetut tulokset.

Käyttäjätarinoiden yksityiskohtaiset kuvaukset ja hyväksymiskriteerit löytyvät dokumentista `02-käyttäjätarinat ja hyväksymiskriteerit.md`. Prioriteetit ja alkuperäiset Story Point -arviot määritellään dokumentissa `03-product backlog.md`.

---

## 2. Sprinttien yleiskuvaus

| Sprintti | Tavoite | Käyttäjätarinat | SP |
|-----------|----------|----------------|----|
| Sprint 1 | Tekninen perusta, käyttäjän tunnistaminen ja Docker Compose | US-01, US-02, US-10, US-11, US-12, US-16 | 33 |
| Sprint 2 | Tukipyyntöjen, profiilin ja salasanan palautuksen hallinta | US-03, US-04, US-05, US-17 | 15 |
| Sprint 3 | Tekoälykeskustelu ja keskusteluhistoria | US-06, US-07, US-08 | 18 |
| Sprint 4 | Käyttökokemuksen täydentäminen | US-09, US-13, US-14 | 9 |
| Sprint 5 | Tietopohjainen tekoälyneuvonta | US-15 | 13 |
| **Yhteensä** |  | **17 käyttäjätarinaa** | **88 SP** |

Story Point -määrät ovat sovitut suunnitteluarviot. Sprint 1 säilytetään 33 SP:n kokonaisuutena ja nykyinen Sprint-jako pidetään ennallaan. US-09, US-14, RAG ja muut lopulliseen toimituslaajuuteen valitut ominaisuudet eivät ole ehdollisia ajan riittävyydelle. Jos kapasiteettiriski toteutuu, se nostetaan päätettäväksi ja muutokset hyväksytään muutostenhallinnan kautta; sitoumuksia ei poisteta hiljaisesti.

---

# 3. Sprint 1 – Tekninen perusta ja käyttäjän tunnistaminen

## 3.1 Sprintin tavoite

Rakentaa sovelluksen tekninen perusta, tietokantayhteys, REST-rajapinnan rakenne, käyttäjän tunnistaminen ja Docker Compose -käynnistys frontendille, backendille, MySQL:lle ja Ollamalle.

Sprintin lopussa sovelluksessa on perusrakenne, johon tukipyyntöjen hallinta ja tekoälytoiminnot voidaan myöhemmin yhdistää.

## 3.2 Sprint Backlog

| ID | Käyttäjätarina | SP |
|----|----------------|----|
| US-10 | REST-rajapinnan käyttäminen | 8 |
| US-11 | Tietojen pysyvä tallentaminen | 5 |
| US-01 | Käyttäjän rekisteröityminen | 5 |
| US-02 | Käyttäjän kirjautuminen | 5 |
| US-12 | Käyttöliittymän käytettävyys | 5 |
| US-16 | Sovelluksen käynnistäminen Docker Composella | 5 |
| **Yhteensä** |  | **33** |

## 3.3 Keskeiset kehitystehtävät

1. Luodaan projektin frontend- ja backend-rakenne.
2. Määritellään MySQL-tietokannan rakenne ja keskeiset taulut.
3. Toteutetaan tietokantayhteys ja tietojen tallennuksen perustoiminnot.
4. Toteutetaan REST-rajapinnan perusrakenne ja yhteiset virhevastaukset.
5. Toteutetaan käyttäjän rekisteröityminen ja salasanan turvallinen tallennus.
6. Toteutetaan kirjautuminen ja suojattujen toimintojen käyttöoikeuksien tarkistaminen.
7. Luodaan käyttöliittymän perusrakenne, navigaatio ja lomakkeiden peruskomponentit.
8. Luodaan frontendin, backendin ja Ollaman Docker-konfiguraatiot sekä Compose-palvelut niille ja MySQL-tietokannalle.
9. Otetaan valittu GGUF-malli automaattisesti käyttöön Ollama-kontissa `Modelfile`-tiedoston avulla ja lisätään mallin sekä MySQL:n pysyvä tallennus ja palveluiden valmiustarkistukset.
10. Lisätään ympäristömuuttujien esimerkkitiedosto ja dokumentoidaan `docker compose up --build`; testataan puhdas käynnistys, mallin saatavuus sekä backendin yhteydet MySQL:ään ja Ollamaan projektin NVIDIA-GPU-ympäristössä. Muiden GPU:iden yhteensopivuutta ei varmenneta projektissa.
11. Testataan keskeiset rekisteröitymis-, kirjautumis-, tietokanta- ja käynnistystoiminnot.

## 3.4 Odotetut tulokset

1. Sovelluksen frontend ja backend toimivat yhdessä.
2. Tietokantaan voidaan tallentaa ja hakea tietoja.
3. Käyttäjä voi rekisteröityä ja kirjautua sisään.
4. REST-rajapinnan perusrakenne on käytettävissä.
5. Käyttöliittymän keskeiset näkymät ja navigaatio ovat olemassa.
6. Frontend, backend, MySQL ja Ollama sekä valittu tekoälymalli ovat käytettävissä README:ssä dokumentoidun Docker Compose -käynnistyksen jälkeen.

## 3.5 Sprintin hyväksyminen

Sprintti voidaan hyväksyä, kun Sprint Backlogiin valitut ja valmiiksi merkityt käyttäjätarinat täyttävät alkuperäisen `02-käyttäjätarinat ja hyväksymiskriteerit.md`-dokumentin hyväksymiskriteerit ja yhteiset Definition of Done -ehdot.

---

# 4. Sprint 2 – Tukipyyntöjen ja profiilin hallinta

## 4.1 Sprintin tavoite

Mahdollistaa käyttäjän omien profiilitietojen ja tukipyyntöjen hallinta sekä unohtuneen salasanan turvallinen palautus ADMINin backend-komennolla ilman erillistä hallintakäyttöliittymää.

Sprintin lopussa käyttäjä pystyy luomaan tukipyynnön, tarkastelemaan omia pyyntöjään ja sulkemaan ratkaistun pyynnön.

## 4.2 Sprint Backlog

| ID | Käyttäjätarina | SP |
|----|----------------|----|
| US-04 | Tukipyynnön luominen | 5 |
| US-05 | Omien tukipyyntöjen tarkastelu ja sulkeminen | 5 |
| US-03 | Käyttäjäprofiilin hallinta | 3 |
| US-17 | Unohtuneen salasanan palauttaminen ADMINin toimesta | 2 |
| **Yhteensä** |  | **15** |

## 4.3 Keskeiset kehitystehtävät

1. Toteutetaan profiilitietojen hakeminen sekä etunimen, sukunimen ja käyttäjänimen päivittäminen; sähköpostiosoite näytetään vain luettavana.
2. Toteutetaan erillinen salasanan vaihtaminen: nykyisen salasanan tarkistus, uuden salasanan validointi ja vahvistuskentän tarkistus; uusi salasana tallennetaan vain turvallisesti tiivistettynä.
3. Toteutetaan ADMINille backend-komento: luodaan satunnainen väliaikainen salasana, tallennetaan vain sen tiiviste, asetetaan pakotettu vaihto ja mitätöidään vanhat istunnot.
4. Väliaikaisella salasanalla kirjautunut käyttäjä saa käyttää vain salasanan vaihtoa ja uloskirjautumista, kunnes salasana on vaihdettu.
3. Toteutetaan tukipyynnön luontilomake ja tietojen validointi.
4. Tallennetaan tukipyynnön otsikko, kuvaus, tila, prioriteetti, luontiaika ja omistaja.
5. Toteutetaan käyttäjän omien tukipyyntöjen luettelonäkymä.
6. Toteutetaan yksittäisen tukipyynnön tietojen tarkastelu.
6. Toteutetaan tukipyynnön sulkeminen.
7. Varmistetaan, ettei käyttäjä voi tarkastella tai muuttaa toisen käyttäjän tukipyyntöä luvattomasti.
8. Testataan tietojen tallennus, päivitys, haku ja käyttöoikeuksien tarkistaminen.

## 4.4 Odotetut tulokset

1. Käyttäjä voi tarkastella profiilitietojaan, päivittää etunimen, sukunimen ja käyttäjänimen sekä vaihtaa salasanan nykyisen salasanan vahvistuksella. Sähköpostiosoite näkyy mutta sitä ei voi muuttaa.
2. ADMIN voi palauttaa unohtuneen salasanan backend-komennolla; käyttäjä joutuu vaihtamaan väliaikaisen salasanan eikä vanhoilla istunnoilla voi enää käyttää tiliä.
2. Käyttäjä voi luoda tukipyynnön.
3. Käyttäjä näkee omat tukipyyntönsä ja niiden tilat.
4. Käyttäjä voi sulkea oman avoimen tukipyyntönsä.
5. Tukipyyntöjen käyttöoikeudet tarkistetaan backendissä.

## 4.5 Sprintin hyväksyminen

Sprintti voidaan hyväksyä, kun valittujen käyttäjätarinoiden hyväksymiskriteerit täyttyvät ja tukipyyntöjen tallennus, haku sekä käyttöoikeudet toimivat testatuissa tilanteissa.

---

# 5. Sprint 3 – Tekoälykeskustelu ja keskusteluhistoria

## 5.1 Sprintin tavoite

Toteuttaa AI HelpDesk -sovelluksen keskeinen tekoälyominaisuus. Käyttäjän on pystyttävä keskustelemaan tekoälyn kanssa, saamaan tarkentavia kysymyksiä ja tarkastelemaan aiempia keskustelujaan.

## 5.2 Sprint Backlog

| ID | Käyttäjätarina | SP |
|----|----------------|----|
| US-06 | Tekoälypohjainen keskustelu | 8 |
| US-08 | Keskusteluviestien tallentaminen | 5 |
| US-07 | Tarkentavat kysymykset ja ongelmanratkaisu | 5 |
| **Yhteensä** |  | **18** |

## 5.3 Keskeiset kehitystehtävät

1. Konfiguroidaan Docker Compose -ympäristössä toimiva Ollama ja valittu GGUF-malli.
2. Toteutetaan backendin ja Ollama-palvelun välinen integraatio Compose-verkon kautta.
3. Toteutetaan keskustelunäkymä ja viestin lähettäminen.
4. Näytetään tekoälyn vastaukset käyttöliittymässä.
5. Välitetään tarvittava keskustelukonteksti jatkokysymyksissä.
6. Toteutetaan tarkentavien kysymysten käsittely ja ongelman ratkaisemiseen liittyvät ehdotukset.
7. Tallennetaan käyttäjän viestit ja tekoälyn vastaukset tietokantaan.
8. Toteutetaan aiempien keskustelujen hakeminen ja näyttäminen oikeassa järjestyksessä.
9. Käsitellään tekoälypalvelun virheet ja aikakatkaisut.
10. Testataan keskustelun normaali toiminta, jatkokysymykset, tallennus ja virhetilanteet.

## 5.4 Odotetut tulokset

1. Käyttäjä voi lähettää teknistä ongelmaa koskevan viestin Dockerissa toimivalle Ollama-palvelulle.
2. Tekoälyn vastaus näytetään keskustelunäkymässä.
3. Keskustelua voidaan jatkaa aiemman kontekstin perusteella.
4. Tekoäly voi pyytää ongelman selvittämiseksi tarvittavia lisätietoja.
5. Käyttäjän ja tekoälyn viestit tallennetaan tietokantaan.
6. Käyttäjä voi tarkastella tallennettuja keskustelujaan.

## 5.5 Sprintin hyväksyminen

Sprintti voidaan hyväksyä, kun keskustelun lähettäminen, vastausten näyttäminen ja viestien tallentaminen toimivat hyväksymiskriteerien mukaisesti. Myös tekoälypalvelun virhetilanteet on käsiteltävä hallitusti.

---

# 6. Sprint 4 – Käyttökokemuksen täydentäminen

## 6.1 Sprintin tavoite

Laajentaa sovelluksen toiminnallisuuksia ja parantaa käyttökokemusta. Käyttäjä voi luoda tukipyynnön keskustelusta, vaihtaa käyttöliittymän kieltä ja seurata tukipyyntöjen yhteenvetoa.

## 6.2 Sprint Backlog

| ID | Käyttäjätarina | SP |
|----|----------------|----|
| US-09 | Tukipyynnön luominen keskustelusta | 3 |
| US-13 | Monikielinen käyttöliittymä | 3 |
| US-14 | Tukipyyntöjen yhteenvetonäkymä | 3 |
| **Yhteensä** |  | **9** |

## 6.3 Keskeiset kehitystehtävät

1. Lisätään mahdollisuus luoda tukipyyntö keskustelun perusteella.
2. Muodostetaan tukipyynnön luonnokseen tarvittavat tiedot keskustelun sisällöstä.
3. Annetaan käyttäjän tarkistaa ja hyväksyä tukipyynnön luominen.
4. Toteutetaan suomen- ja englanninkieliset käyttöliittymätekstit.
5. Toteutetaan kielivalinta ja valitun kielen säilyttäminen sovitulla tavalla.
6. Toteutetaan tukipyyntöjen kokonaismäärän ja tilajakauman yhteenveto.
7. Testataan uusien toimintojen käyttöliittymä, tiedot ja virhetilanteet.

## 6.4 Odotetut tulokset

1. Käyttäjä voi siirtyä ratkaisemattomasta keskustelusta tukipyynnön luomiseen, tarkistaa ja muokata ehdotettua otsikkoa ja kuvausta sekä vahvistaa luomisen.
2. Tukipyyntöä ei luoda ilman käyttäjän nimenomaista vahvistusta; hylkäys tai peruutus ei luo pyyntöä.
3. Käyttäjä voi vaihtaa käyttöliittymän suomen ja englannin välillä.
4. Käyttäjä voi tarkastella omien tukipyyntöjensä kokonaismäärää ja `OPEN`/`CLOSED`-määriä; tyhjässä yhteenvedossa kaikki määrät ovat nollia.

## 6.5 Sprintin hyväksyminen

Sprintti voidaan hyväksyä, kun lisäominaisuudet täyttävät niille määritellyt hyväksymiskriteerit ja toimivat yhdessä aiemmin toteutettujen toimintojen kanssa.

---

# 7. Sprint 5 – Tietopohjainen tekoälyneuvonta (RAG)

## 7.1 Sprintin tavoite

Laajentaa tekoälyneuvontaa siten, että vastauksissa voidaan hyödyntää teknistä dokumentaatiota. Tavoitteena on parantaa vastausten osuvuutta ja mahdollistaa vastausten yhdistäminen käytettävissä oleviin lähteisiin.

## 7.2 Sprint Backlog

| ID | Käyttäjätarina | SP |
|----|----------------|----|
| US-15 | Tietopohjainen tekoälyneuvonta (RAG) | 13 |
| **Yhteensä** |  | **13** |

## 7.3 Keskeiset kehitystehtävät

1. Rajataan ennen toteutusta hyväksytty tekninen dokumenttikokoelma Markdown- ja TXT-tiedostoihin.
2. Toteutetaan tiedostojen lukeminen ja käsittely avainsanahakua varten.
3. Haetaan kyselyn avainsanoihin sopivat dokumenttikohdat ja niiden lähdetiedot.
4. Määritellään testikysymykset ja arvioidaan avainsanahaun osuvuutta sekä tyhjän tuloksen käsittelyä.
5. Välitetään löydetty sisältö ja todelliset lähdetiedot Ollama-mallille vastauksen muodostamista varten.
6. Näytetään lähdetiedot käyttöliittymässä silloin, kun niitä on saatavilla.
7. Käsitellään tilanne, jossa sopivaa dokumentaatiota ei löydy.
8. Testataan hakutulosten relevanssia, vastausten laatua ja virhetilanteita.

## 7.4 Odotetut tulokset

1. Järjestelmään voidaan lisätä teknistä dokumentaatiota.
2. Käyttäjän kysymykseen liittyvää sisältöä voidaan hakea dokumentaatiosta.
3. Tekoäly voi muodostaa vastauksen löydetyn sisällön perusteella.
4. Löydettyjen sisältöjen todelliset lähdetiedot näytetään käyttäjälle.
5. Järjestelmä ei esitä dokumentaation puuttuessa vastausta dokumentaation vahvistamana.

## 7.5 Sprintin hyväksyminen

Sprintti voidaan hyväksyä, kun dokumentaation haku ja tekoälyintegraatio toimivat määriteltyjen hyväksymiskriteerien mukaisesti.

RAG MVP:n hakutapa on avainsanahaku Markdown- ja TXT-tiedostoista. Semanttista hakua ei toteuteta oletuksena; sen lisääminen edellyttää dokumentoitua näyttöä siitä, ettei avainsanahaku täytä määriteltyjä testikriteerejä.

Jos toteutus osoittautuu liian laajaksi yhden Sprintin aikana, käyttäjätarina jaetaan pienempiin osiin, esimerkiksi dokumentaation indeksointiin, haun toteutukseen ja tekoälyintegraatioon.

---

# 8. Yhteiset Sprint-käytännöt

## 8.1 Sprint Planning

Ennen Sprintin alkua kehitystiimi:

1. Tarkistaa Product Backlogin prioriteetit ja riippuvuudet.
2. Valitsee Sprintin tavoitteeseen sopivat käyttäjätarinat.
3. Varmistaa, että hyväksymiskriteerit ovat ymmärrettäviä.
4. Arvioi tiimin käytettävissä olevan kapasiteetin.
5. Jakaa käyttäjätarinat tarvittaessa pienempiin teknisiin tehtäviin.

## 8.2 Sprintin aikana

1. Kehitystyötä seurataan sovitulla tehtävätaululla.
2. Toteutuksen edistyminen ja esteet käsitellään säännöllisesti.
3. Koodi testataan ja tarkistetaan ennen yhdistämistä päähaaraan.
4. Uudet vaatimukset lisätään Product Backlogiin ja priorisoidaan erikseen.
5. Sprintin tavoitetta ei muuteta ilman yhteistä arviota muutoksen vaikutuksista.

## 8.3 Sprintin katselmointi (Sprint Review)

Sprintin lopussa tarkastellaan toteutettuja toimintoja ja niiden vastaavuutta hyväksymiskriteereihin.

1. Esitellään toimiva ohjelmistoversio.
2. Tarkistetaan valmiiksi merkityt käyttäjätarinat.
3. Kerätään palaute ja tunnistetaan tarvittavat muutokset.
4. Päivitetään Product Backlog havaintojen perusteella.

## 8.4 Sprintin retrospektiivi (Sprint Retrospective)

Kehitystiimi arvioi Sprintin lopussa:

1. Mikä sujui hyvin?
2. Mitkä ongelmat hidastivat toteutusta?
3. Miten yhteistyötä ja teknisiä käytäntöjä voidaan parantaa?
4. Mitä konkreettista parannusta kokeillaan seuraavassa Sprintissä?

---

# 9. Definition of Done

Käyttäjätarina voidaan merkitä valmiiksi, kun:

1. Kaikki käyttäjätarinan hyväksymiskriteerit täyttyvät.
2. Toteutus on yhdistetty sovellukseen.
3. Syötteiden validointi ja virhetilanteiden käsittely toimivat.
4. Käyttöoikeudet ja tietoturva on huomioitu.
5. Tarvittavat yksikkö- ja integraatiotestit läpäisevät.
6. Käyttöliittymän toiminta on tarkistettu.
7. Dokumentaatio on päivitetty tarvittaessa.
8. Toteutus on katselmoitu sovitun kehitysprosessin mukaisesti.

Sprinttiä ei pidetä automaattisesti onnistuneena vain siksi, että kaikki suunnitellut Story Pointit on käsitelty. Tärkeintä on Sprintin tavoitteen saavuttaminen ja toimivan, testatun ohjelmiston tuottaminen.

---

# 10. Riskit ja suunnitelman tarkentaminen

| Riski | Vaikutus | Hallintatoimenpide |
|---------|----------|--------------------|
| Tietokannan tai REST-rajapinnan viivästyminen | Muiden toimintojen toteutus viivästyy | Toteutetaan tekninen perusta ensin ja määritellään rajapinnat varhain |
| Tekoälypalvelun virheet tai rajoitukset | Keskustelutoiminto ei toimi luotettavasti | Testataan integraatio varhain ja toteutetaan virheiden käsittely |
| Liian suuri työmäärä yhdessä Sprintissä | Osa toiminnallisuuksista jää keskeneräiseksi | Jaetaan tarinoita pienempiin osiin ja mukautetaan Sprintin sisältöä |
| RAG-toteutuksen tekninen epävarmuus | Viimeisen Sprintin tavoite voi viivästyä | Tehdään tekninen selvitys ja rajataan ensimmäinen toteutus |
| Käyttöoikeusvirheet | Käyttäjien tietoja voi paljastua luvattomasti | Testataan backendin käyttöoikeustarkistukset ja tietojen omistajuus |

---

# 11. Yhteenveto

AI HelpDesk -sovelluksen alustava Sprint Plan koostuu viidestä Sprintistä ja 17 käyttäjätarinasta. Tarinoiden alustava kokonaisarvio on **88 Story Pointia**, sisältäen Sprint 1:een sijoitetun US-16:n 5 Story Pointin arvion.

1. Sprint 1 luo sovelluksen teknisen perustan.
2. Sprint 2 toteuttaa profiilin ja tukipyyntöjen hallinnan.
3. Sprint 3 tuo käyttöön tekoälykeskustelun ja keskusteluhistorian.
4. Sprint 4 täydentää käyttökokemusta ja muita Backlogin toimintoja.
5. Sprint 5 laajentaa tekoälyneuvontaa teknisen dokumentaation avulla.

Suunnitelma on alustava. Sprinttien tarkka sisältö, kesto ja työmäärä vahvistetaan kehittäjän kapasiteetin, teknisten riippuvuuksien ja projektin vaatimusten perusteella.
