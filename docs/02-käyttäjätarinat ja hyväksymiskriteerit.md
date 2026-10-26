
# AI HelpDesk – Käyttäjätarinat ja hyväksymiskriteerit

## 1. Käyttäjäroolit

### 1.1 Rekisteröitynyt käyttäjä

Rekisteröitynyt käyttäjä voi kirjautua sovellukseen, hallita omaa profiiliaan, keskustella tekoälyn kanssa sekä luoda ja hallita omia tukipyyntöjään.

### 1.2 Sovelluksen kehittäjä

Sovelluksen kehittäjä vastaa sovelluksen teknisestä toteutuksesta, tietokannasta, REST-rajapinnasta, tekoälyintegraatiosta, testauksesta ja dokumentoinnista.

## 2. Käyttäjätarinat ja hyväksymiskriteerit

### US-01: Käyttäjän rekisteröityminen

- Roolina opiskelijana
- Haluan rekisteröityä AI HelpDesk -sovellukseen.
- Jotta voin käyttää palvelun toimintoja omalla käyttäjätililläni.

**Hyväksymiskriteerit**

**AC-01.1 – Onnistunut rekisteröityminen**

- Oletetaan, että käyttäjällä ei ole vielä käyttäjätiliä.
- Kun käyttäjä antaa etunimen, sukunimen, käyttäjänimen, sähköpostiosoitteen ja salasanan kelvollisessa muodossa ja lähettää lomakkeen.
- Niin järjestelmä luo käyttäjätilin ja tallentaa käyttäjän tiedot tietokantaan.
- Salasana tiivistetään palvelinpuolella; asiakas ei voi lähettää `password_hash`-arvoa tallennettavaksi.

**AC-01.2 – Virheelliset tiedot**

- Oletetaan, että käyttäjä on rekisteröitymislomakkeella.
- Kun jokin pakollinen tieto puuttuu tai on virheellinen.
- Niin järjestelmä näyttää virheilmoituksen eikä luo käyttäjätiliä.

**AC-01.3 – Käytössä oleva sähköpostiosoite**

- Oletetaan, että sähköpostiosoite kuuluu jo olemassa olevalle käyttäjätilille.
- Kun käyttäjä yrittää rekisteröityä samalla sähköpostiosoitteella.
- Niin järjestelmä estää uuden tilin luomisen ja näyttää virheilmoituksen.

**AC-01.4 – Salasanan turvallisuus**

- Oletetaan, että käyttäjän rekisteröityminen onnistuu.
- Kun salasana tallennetaan tietokantaan.
- Niin salasana tallennetaan turvallisesti tiivistettynä eikä selväkielisenä.

### US-02: Käyttäjän kirjautuminen

- Roolina rekisteröityneenä käyttäjänä
- Haluan kirjautua sovellukseen.
- Jotta voin käyttää omia tietojani ja sovelluksen suojattuja toimintoja.

**Hyväksymiskriteerit**

**AC-02.1 – Onnistunut kirjautuminen**

- Oletetaan, että käyttäjällä on voimassa oleva käyttäjätili.
- Kun käyttäjä antaa oikean sähköpostiosoitteen ja salasanan.
- Niin järjestelmä sallii kirjautumisen ja avaa sovelluksen suojatut toiminnot.

**AC-02.2 – Virheelliset kirjautumistiedot**

- Oletetaan, että käyttäjä yrittää kirjautua sovellukseen.
- Kun sähköpostiosoite tai salasana on virheellinen.
- Niin järjestelmä estää kirjautumisen ja näyttää virheilmoituksen.

**AC-02.3 – Pääsy suojattuihin toimintoihin**

- Oletetaan, että käyttäjä ei ole kirjautunut sisään.
- Kun käyttäjä yrittää käyttää kirjautumista edellyttävää toimintoa.
- Niin järjestelmä estää pääsyn kyseiseen toimintoon.

### US-03: Käyttäjäprofiilin hallinta

- Roolina rekisteröityneenä käyttäjänä
- Haluan tarkastella ja muokata omia profiilitietojani.
- Jotta tietoni pysyvät ajan tasalla.

**Hyväksymiskriteerit**

**AC-03.1 – Profiilin tarkastelu**

- Oletetaan, että käyttäjä on kirjautunut sisään.
- Kun käyttäjä avaa profiilisivun.
- Niin järjestelmä näyttää käyttäjän omat profiilitiedot.

**AC-03.2 – Profiilin päivittäminen**

- Oletetaan, että käyttäjä on avannut profiilisivunsa.
- Kun käyttäjä muokkaa etunimeään, sukunimeään tai käyttäjänimeään ja tallentaa muutokset.
- Niin järjestelmä tallentaa muutokset tietokantaan ja näyttää päivitetyt tiedot.
- MVP:ssä sähköpostiosoitetta ja salasanaa ei muuteta profiilin päivityksessä. Niiden mahdollinen muuttaminen edellyttää erillistä vahvistettua toimintoa.

**AC-03.3 – Virheelliset profiilitiedot**

- Oletetaan, että käyttäjä muokkaa profiilitietojaan.
- Kun käyttäjä syöttää virheellisiä tietoja.
- Niin järjestelmä näyttää virheilmoituksen eikä tallenna virheellisiä muutoksia.

### US-04: Tukipyynnön luominen

- Roolina rekisteröityneenä käyttäjänä
- Haluan luoda uuden tukipyynnön.
- Jotta voin tallentaa teknisen ongelmani ja seurata sen käsittelyä.

**Hyväksymiskriteerit**

**AC-04.1 – Tukipyynnön luominen**

- Oletetaan, että käyttäjä on kirjautunut sisään.
- Kun käyttäjä antaa tukipyynnön otsikon ja kuvauksen sekä lähettää lomakkeen; prioriteetti voidaan antaa tai jättää pois.
- Niin järjestelmä luo tukipyynnön ja tallentaa sen tietokantaan.
- Backend asettaa omistajan tunnistetun käyttäjän perusteella, tilaksi `OPEN` ja puuttuvaksi prioriteetiksi `MEDIUM`; asiakas ei voi asettaa omistajaa tai alkuperäistä tilaa.

**AC-04.2 – Tukipyynnön perustiedot**

- Oletetaan, että käyttäjä luo uuden tukipyynnön.
- Kun tukipyyntö tallennetaan onnistuneesti.
- Niin järjestelmä tallentaa otsikon, kuvauksen, tilan, prioriteetin, luontiajan ja pyynnön omistajan.
- Keskustelusta luodussa tukipyynnössä tallennetaan myös lähdekeskustelun tunniste; itsenäisesti luodussa pyynnössä lähdekeskustelu on tyhjä.

**AC-04.3 – Pakolliset tiedot puuttuvat**

- Oletetaan, että käyttäjä on avaamassa uutta tukipyyntöä.
- Kun otsikko tai kuvaus puuttuu.
- Niin järjestelmä ilmoittaa puuttuvista tiedoista eikä luo tukipyyntöä.

### US-05: Omien tukipyyntöjen tarkastelu ja sulkeminen

- Roolina rekisteröityneenä käyttäjänä
- Haluan tarkastella omia tukipyyntöjäni ja sulkea ratkaistut pyynnöt.
- Jotta voin seurata ja hallita omien ongelmieni käsittelyä.

**Hyväksymiskriteerit**

**AC-05.1 – Tukipyyntöjen luettelo**

- Oletetaan, että käyttäjä on kirjautunut sisään ja hänellä on tallennettuja tukipyyntöjä.
- Kun käyttäjä avaa tukipyyntöjen näkymän.
- Niin järjestelmä näyttää käyttäjän omat tukipyynnöt.

**AC-05.2 – Tukipyynnön tiedot**

- Oletetaan, että käyttäjä tarkastelee omia tukipyyntöjään.
- Kun käyttäjä avaa yksittäisen tukipyynnön.
- Niin järjestelmä näyttää pyynnön otsikon, kuvauksen, tilan, prioriteetin ja luontiajan.

**AC-05.3 – Tukipyynnön sulkeminen**

- Oletetaan, että käyttäjä omistaa avoimen tukipyynnön.
- Kun käyttäjä valitsee tukipyynnön sulkemisen.
- Niin järjestelmä muuttaa pyynnön tilan suljetuksi ja tallentaa muutoksen.
- Sulkeminen on erillinen toiminto; käyttäjä ei voi muuttaa tilaa suoraan tukipyynnön yleisellä päivityspyynnöllä.

**AC-05.4 – Käyttöoikeuksien tarkistaminen**

- Oletetaan, että tukipyyntö kuuluu toiselle käyttäjälle.
- Kun käyttäjä yrittää tarkastella tai muuttaa kyseistä tukipyyntöä.
- Niin järjestelmä estää luvattoman toiminnon.

### US-06: Tekoälypohjainen keskustelu

- Roolina teknisen ongelman kanssa työskentelevänä käyttäjänä
- Haluan keskustella tekoälyn kanssa ongelmastani.
- Jotta saan ehdotuksia ongelman ratkaisemiseksi.

**Hyväksymiskriteerit**

**AC-06.1 – Viestin lähettäminen**

- Oletetaan, että käyttäjä on kirjautunut sisään ja avannut oman AI HelpDesk -keskustelunsa.
- Kun käyttäjä kirjoittaa ongelmansa ja lähettää viestin.
- Niin järjestelmä välittää viestin käytössä olevalle tekoälymallille tai -palvelulle.

**AC-06.2 – Tekoälyn vastaus**

- Oletetaan, että tekoälypalvelu vastaanottaa käyttäjän viestin onnistuneesti.
- Kun tekoäly tuottaa vastauksen.
- Niin järjestelmä näyttää vastauksen keskustelun käyttöliittymässä.

**AC-06.3 – Tekoälypalvelun virhetilanne**

- Oletetaan, että käyttäjä lähettää viestin tekoälylle.
- Kun tekoälypalvelu ei ole käytettävissä tai pyyntö epäonnistuu.
- Niin järjestelmä näyttää ymmärrettävän virheilmoituksen.

**AC-06.4 – Keskustelun jatkaminen**

- Oletetaan, että käyttäjä on saanut tekoälyn vastauksen.
- Kun käyttäjä lähettää uuden viestin samaan keskusteluun.
- Niin järjestelmä välittää tekoälylle tarvittavan keskustelukontekstin ja näyttää uuden vastauksen.

### US-07: Tarkentavat kysymykset ja ongelmanratkaisu

- Roolina teknistä ongelmaa selvittävänä käyttäjänä
- Haluan saada tekoälyltä tarkentavia kysymyksiä tarvittaessa.
- Jotta voin antaa ongelman ratkaisemiseksi tarvittavat tiedot ja saada sopivampia ohjeita.

**Hyväksymiskriteerit**

**AC-07.1 – Tarkentavan kysymyksen esittäminen**

- Oletetaan, että käyttäjän ongelmakuvaus ei sisällä riittävästi tietoja.
- Kun tekoäly tarvitsee lisätietoja ongelman ymmärtämiseksi.
- Niin tekoäly esittää tilanteeseen liittyvän tarkentavan kysymyksen.

**AC-07.2 – Teknisen ympäristön selvittäminen**

- Oletetaan, että ongelman ratkaisu riippuu käyttöjärjestelmästä, ohjelmistoversiosta tai virheilmoituksesta.
- Kun tekoäly tarvitsee näitä tietoja.
- Niin tekoäly pyytää käyttäjää antamaan tarvittavat lisätiedot.

**AC-07.3 – Ratkaisuehdotusten antaminen**

- Oletetaan, että käyttäjä on antanut ongelman selvittämiseen tarvittavat tiedot.
- Kun tekoäly muodostaa vastauksen.
- Niin järjestelmä näyttää ongelmaan liittyviä ratkaisuehdotuksia ja seuraavia vaiheita.

### US-08: Keskusteluviestien tallentaminen

- Roolina rekisteröityneenä käyttäjänä
- Haluan tallentaa keskusteluviestini tietokantaan.
- Jotta voin tarkastella aiempia keskustelujani myöhemmin.

**Hyväksymiskriteerit**

**AC-08.1 – Käyttäjän viestin tallentaminen**

- Oletetaan, että kirjautunut käyttäjä lähettää viestin omaan keskusteluunsa.
- Kun viesti hyväksytään tallennettavaksi.
- Niin järjestelmä tallentaa viestin tietokantaan ja liittää sen oikeaan keskusteluun sekä käyttäjään.

**AC-08.2 – Tekoälyn vastauksen tallentaminen**

- Oletetaan, että tekoäly on tuottanut vastauksen käyttäjän viestiin.
- Kun vastaus käsitellään onnistuneesti.
- Niin järjestelmä tallentaa vastauksen tietokantaan.

**AC-08.3 – Aiemman keskustelun tarkastelu**

- Oletetaan, että käyttäjällä on tallennettuja keskusteluviestejä.
- Kun käyttäjä avaa aiemman keskustelunsa.
- Niin järjestelmä näyttää tallennetut viestit oikeassa järjestyksessä.
- Käyttäjä ei voi tarkastella toisen käyttäjän keskusteluja tai viestejä.

### US-09: Tukipyynnön luominen keskustelusta

- Roolin AI HelpDesk -keskustelua käyttävänä käyttäjänä
- Haluan luoda tukipyynnön keskustelun perusteella.
- Jotta voin säilyttää ongelman tiedot myöhempää käsittelyä varten.

**Hyväksymiskriteerit**

**AC-09.1 – Tukipyynnön luontiehdotus**

- Oletetaan, että käyttäjän ongelma ei ratkea keskustelun aikana.
- Kun ongelma tarvitsee jatkokäsittelyä ja käyttäjä on kirjautunut sisään.
- Niin järjestelmä tarjoaa käyttäjälle mahdollisuuden luoda tukipyynnön.

**AC-09.2 – Tukipyynnön luominen**

- Oletetaan, että käyttäjä hyväksyy tukipyynnön luomisen.
- Kun tarvittavat tiedot on vahvistettu.
- Niin järjestelmä luo tukipyynnön ja tallentaa sen tietokantaan.
- Tukipyyntö linkitetään keskusteluun vain, jos keskustelu kuuluu samalle kirjautuneelle käyttäjälle.

**AC-09.3 – Käyttäjän päätöksen kunnioittaminen**

- Oletetaan, että järjestelmä ehdottaa tukipyynnön luomista.
- Kun käyttäjä hylkää ehdotuksen.
- Niin järjestelmä ei luo tukipyyntöä automaattisesti.

### US-10: REST-rajapinnan käyttäminen

- Roolina sovelluksen kehittäjänä
- Haluan käsitellä tukipyyntöjä REST-rajapinnan kautta.
- Jotta frontend ja backend voivat vaihtaa tietoja hallitusti.

**Hyväksymiskriteerit**

**AC-10.1 – Tukipyyntöjen hakeminen**

- Oletetaan, että käyttäjä on kirjautunut sisään ja hänellä on oikeus tarkastella omia tukipyyntöjään.
- Kun frontend lähettää tukipyyntöjen hakupyynnön.
- Niin rajapinta palauttaa käyttäjän omat tukipyynnöt.

**AC-10.2 – Tukipyynnön luominen**

- Oletetaan, että käyttäjä on kirjautunut sisään ja pyyntö sisältää kelvolliset tiedot.
- Kun frontend lähettää tukipyynnön luontipyynnön.
- Niin backend validoi tiedot, tallentaa tukipyynnön ja palauttaa asianmukaisen vastauksen.

**AC-10.3 – Tukipyynnön päivittäminen**

- Oletetaan, että käyttäjällä on oikeus muuttaa kyseistä tukipyyntöä.
- Kun frontend lähettää sallitun päivityspyynnön.
- Niin backend tarkistaa käyttöoikeudet ja tiedot ennen muutoksen tallentamista.

**AC-10.4 – Virheelliset tai luvattomat pyynnöt**

- Oletetaan, että rajapinta vastaanottaa virheellisen tai luvattoman pyynnön.
- Kun backend käsittelee pyynnön.
- Niin rajapinta palauttaa asianmukaisen HTTP-virhekoodin ja virhevastauksen.

### US-11: Tietojen pysyvä tallentaminen

- Roolina sovelluksen käyttäjänä
- Haluan että käyttäjätietoni, tukipyyntöni ja keskusteluviestini tallennetaan pysyvästi.
- Jotta voin jatkaa sovelluksen käyttöä menettämättä tallennettuja tietoja.

**Hyväksymiskriteerit**

**AC-11.1 – Tietojen tallentaminen**

- Oletetaan, että käyttäjä luo tukipyynnön tai lähettää tallennettavan keskusteluviestin.
- Kun backend käsittelee tallennuspyynnön onnistuneesti.
- Niin tiedot tallennetaan MySQL- tai MariaDB-tietokantaan.

**AC-11.2 – Tallennettujen tietojen hakeminen**

- Oletetaan, että tietoja on tallennettu tietokantaan.
- Kun sovellus hakee kyseisiä tietoja uudelleen.
- Niin järjestelmä palauttaa oikeat tiedot käyttöoikeuksien mukaisesti.

**AC-11.3 – Tietojen väliset suhteet**

- Oletetaan, että tietokannassa on käyttäjiä, tukipyyntöjä ja viestejä.
- Kun tietoja tallennetaan ja yhdistetään toisiinsa.
- Niin tietokannan avaimet ja viite-eheys varmistavat tietojen oikeat suhteet.

### US-12: Käyttöliittymän käytettävyys

- Roolina sovelluksen käyttäjänä
- Haluan käyttää selkeää ja johdonmukaista käyttöliittymää.
- Jotta löydän tarvittavat toiminnot helposti ja ymmärrän sovelluksen antamat ilmoitukset.

**Hyväksymiskriteerit**

**AC-12.1 – Keskeisten toimintojen löytäminen**

- Oletetaan, että käyttäjä on kirjautunut sovellukseen.
- Kun käyttäjä avaa sovelluksen päänäkymän.
- Niin hän löytää linkit keskusteluun, tukipyyntöihin ja profiiliin.

**AC-12.2 – Toimintojen palaute**

- Oletetaan, että käyttäjä suorittaa toiminnon sovelluksessa.
- Kun toiminto onnistuu tai epäonnistuu.
- Niin käyttöliittymä näyttää asianmukaisen palautteen.

**AC-12.3 – Lomakkeiden validointi**

- Oletetaan, että käyttäjä täyttää sovelluksen lomaketta.
- Kun pakollisia tietoja puuttuu tai tiedot ovat virheellisiä.
- Niin käyttöliittymä kertoo, mitä tietoja käyttäjän tulee korjata.

## 3. Valitut lisäominaisuudet

Seuraavat kolme lisäominaisuutta on valittu toteutettaviksi lopulliseen julkaisuun. Monikielinen käyttöliittymä ja RAG toteutetaan MVP:n jälkeen. Docker Compose -ympäristö perustetaan Sprint 1:ssä kehitys- ja esittely-ympäristöä varten.

### US-13: Monikielinen käyttöliittymä

- Roolina sovelluksen käyttäjänä
- Haluan vaihtaa käyttöliittymän kielen suomen ja englannin välillä.
- Jotta voin käyttää sovellusta itselleni sopivalla kielellä.

**Hyväksymiskriteerit**

**AC-13.1 – Kielen vaihtaminen**

- Oletetaan, että käyttäjä avaa sovelluksen.
- Kun käyttäjä valitsee suomen tai englannin.
- Niin käyttöliittymä näyttää tekstit valitulla kielellä.

**AC-13.2 – Valitun kielen säilyttäminen**

- Oletetaan, että käyttäjä on valinnut käyttöliittymän kielen.
- Kun käyttäjä siirtyy sovelluksen toiseen näkymään.
- Niin valinta säilyy selaimessa näkymästä toiseen ja seuraavalla kirjautumiskerralla.

**AC-13.3 – Käyttöliittymän käännösten kattavuus**

- Oletetaan, että käyttäjä on valinnut suomen tai englannin.
- Kun käyttäjä käyttää sovelluksen tuettuja näkymiä ja toimintoja.
- Niin käyttöliittymän tekstit ja käyttäjälle näytettävät ilmoitukset ovat valitulla kielellä.

Kielivalinta koskee käyttöliittymää. Tekoälyn vastauskieli määräytyy keskustelun kielen ja agentin kieliohjeiden mukaan.

### US-14: Tukipyyntöjen yhteenvetonäkymä

- Roolina tukipyyntöjä hallitsevana käyttäjänä
- Haluan nähdä yhteenvedon omista tukipyynnöistäni.
- Jotta voin seurata niiden määrää ja tiloja yhdestä näkymästä.

**Hyväksymiskriteerit**

**AC-14.1 – Yhteenvedon näyttäminen**

- Oletetaan, että kirjautuneella käyttäjällä on tallennettuja tukipyyntöjä.
- Kun käyttäjä avaa yhteenvetonäkymän.
- Niin järjestelmä näyttää vain käyttäjän omien tukipyyntöjen kokonaismäärän sekä OPEN- ja CLOSED-tiloissa olevien pyyntöjen määrät.

**AC-14.2 – Tyhjä yhteenveto**

- Oletetaan, ettei kirjautuneella käyttäjällä ole tukipyyntöjä.
- Kun käyttäjä avaa yhteenvetonäkymän.
- Niin järjestelmä näyttää kokonaismäärän ja molempien tilojen määrän nollana.

**AC-14.3 – Yhteenvedon päivittäminen**

- Oletetaan, että käyttäjä luo tai sulkee oman tukipyyntönsä.
- Kun yhteenvetonäkymän tiedot päivitetään.
- Niin kokonaismäärä ja tilakohtaiset määrät vastaavat käyttäjän tallennettuja tukipyyntöjä.

Yhteenveto rajataan lukumääriin. Se ei sisällä kaavioita, suodatuksia, aikavertailuja eikä muiden käyttäjien tukipyyntöjä. MVP:n tilat ovat OPEN ja CLOSED.

### US-15: Tietopohjainen tekoälyneuvonta (RAG)

- Roolina teknistä ongelmaa selvittävänä käyttäjänä
- Haluan että tekoäly hyödyntää teknistä dokumentaatiota vastauksissaan.
- Jotta saan dokumentaatioon perustuvia ja paremmin kohdennettuja ohjeita.

**Hyväksymiskriteerit**

**AC-15.1 – Dokumentaation hakeminen**

- Oletetaan, että järjestelmään on lisätty teknistä dokumentaatiota.
- Kun käyttäjä esittää dokumentaatioon liittyvän kysymyksen.
- Niin järjestelmä hakee kysymykseen liittyvää sisältöä ja välittää sen tekoälylle.

**AC-15.2 – Dokumentaation puuttuminen**

- Oletetaan, ettei sopivaa dokumentaatiota löydy.
- Kun tekoäly muodostaa vastauksen.
- Niin järjestelmä ei väitä vastausta löydetyn dokumentaation vahvistamaksi.

**AC-15.3 – Lähteiden näyttäminen**

- Oletetaan, että kyselyyn liittyvää dokumentaatiota löytyy.
- Kun järjestelmä näyttää tekoälyn muodostaman vastauksen.
- Niin käyttöliittymä näyttää myös saatavilla olevat lähdetiedot.

### US-16: Sovelluksen käynnistäminen Docker Composella

- Roolina sovelluksen kehittäjänä tai ylläpitäjänä
- Haluan käynnistää sovelluksen dokumentoidulla yhdellä Docker Compose -komennolla.
- Jotta kehitys- ja esittely-ympäristö voidaan ottaa käyttöön toistettavasti.

**Hyväksymiskriteerit**

**AC-16.1 – Käynnistys yhdellä komennolla**

- Oletetaan, että Docker ja Docker Compose ovat käytettävissä ja vaaditut ympäristömuuttujat on asetettu.
- Kun käyttäjä suorittaa README:ssä dokumentoidun käynnistyskomennon.
- Niin sovelluksen frontend, backend ja MySQL-tietokanta käynnistyvät ilman erillisiä manuaalisia käynnistysvaiheita.

**AC-16.2 – Palveluiden valmius**

- Oletetaan, että Docker Compose -käynnistys on suoritettu.
- Kun palvelut ovat valmiita vastaanottamaan pyyntöjä.
- Niin frontend pystyy käyttämään backendia ja backend pystyy käyttämään tietokantaa.

**AC-16.3 – Konfiguraatio ja salaisuudet**

- Oletetaan, että sovelluksen käynnistämiseen tarvitaan konfiguraatioarvoja tai salaisuuksia.
- Kun kehittäjä valmistelee paikallisen ympäristön.
- Niin README ja esimerkkikonfiguraatio kertovat vaaditut arvot, eikä repository sisällä oikeita salaisuuksia.

Docker Compose käynnistää sovelluksen kontitetut osat. Tekoälypalvelun käynnistys tai ulkoinen saatavuus määritellään erikseen valitun AI-palvelun konfiguraatiossa.

US-16:n laajuuteen kuuluvat frontendin ja backendin Dockerfile-tiedostot, frontendin, backendin ja MySQL:n Compose-palvelut, tarvittavat ympäristömuuttujat sisältävä esimerkkitiedosto ilman oikeita salaisuuksia, MySQL:n pysyvä tallennus, palveluiden valmiustarkistukset sekä käynnistyskomennon dokumentointi ja toiminnan testaus. Yhden komennon esimerkki on `docker compose up --build`. Tekoälypalvelun kontitus, tuotantoympäristön käyttöönotto ja orkestrointi eivät kuulu tarinan laajuuteen.

## 4. Prioriteettitaulukko

| Prioriteetti | Kuvaus | Toteutusperiaate |
|---|---|---|
| P1 – Korkea | Projektin pakollisten vaatimusten täyttämisen kannalta välttämätön toiminnallisuus | Toteutetaan ensin |
| P2 – Keskitaso | Tärkeä toiminnallisuus, joka täydentää sovelluksen käyttöä | Toteutetaan P1-toimintojen jälkeen |
| P3 – Matala | Hyödyllinen lisäominaisuus, joka ei ole MVP-version edellytys | Toteutetaan, jos aikaa jää |

**Käyttäjätarinoiden alustavat prioriteetit**

| Käyttäjätarina | Prioriteetti |
|---|---|
| US-01: Käyttäjän rekisteröityminen | P1 |
| US-02: Käyttäjän kirjautuminen | P1 |
| US-03: Käyttäjäprofiilin hallinta | P1 |
| US-04: Tukipyynnön luominen | P1 |
| US-05: Omien tukipyyntöjen tarkastelu ja sulkeminen | P1 |
| US-06: Tekoälypohjainen keskustelu | P1 |
| US-07: Tarkentavat kysymykset ja ongelmanratkaisu | P1 |
| US-08: Keskusteluviestien tallentaminen | P1 |
| US-09: Tukipyynnön luominen keskustelusta | P2 |
| US-10: REST-rajapinnan käyttäminen | P1 |
| US-11: Tietojen pysyvä tallentaminen | P1 |
| US-12: Käyttöliittymän käytettävyys | P1 |
| US-13: Monikielinen käyttöliittymä | P2 – valittu lisäominaisuus |
| US-14: Tukipyyntöjen yhteenvetonäkymä | P3 |
| US-15: Tietopohjainen tekoälyneuvonta (RAG) | P2 – valittu lisäominaisuus |
| US-16: Sovelluksen käynnistäminen Docker Composella | P2 – valittu lisäominaisuus |

## 5. Yhteenveto

Tässä dokumentissa on määritelty AI HelpDesk -sovelluksen käyttäjätarinat, hyväksymiskriteerit ja erillinen prioriteettitaulukko.

Käyttäjätarinat ja hyväksymiskriteerit on yhdistetty Product Backlogiin ja alustavaan Sprint-suunnitelmaan. Toteutuksen ja testauksen edetessä hyväksymiskriteerien täyttyminen todennetaan jäljitettävyystaulukon mukaisesti.