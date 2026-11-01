# AI HelpDesk - UX/UI Suunnittelu

**Projekt:** AI HelpDesk – Opiskelijaprojekti  
**Dokumentti:** UX/UI-suunnittelun määrittely  
**Versio:** 1.0  
**Päivitetty:** 26.10.2026  
**Tila:** Suunnitteludokumentti – toteutus ja käytettävyystestaus tarkentuvat projektin aikana

---

## 1. Tarkoitus ja rajaus

Tämän dokumentin tarkoitus on määritellä AI HelpDesk -järjestelmän käyttöliittymän rakenne, keskeiset käyttäjäpolut, käyttöliittymäkomponentit sekä käytettävyyteen liittyvät vaatimukset. Dokumentti täydentää vaatimusmäärittelyä, käyttäjätarinoita, Product Backlogia ja järjestelmän suunnittelua.

UX/UI-suunnittelussa keskitytään siihen, että käyttäjä pystyy:
- kirjautumaan sisään ja hallitsemaan omia käyttäjätietojaan;
- kuvaamaan IT-ongelman AI-chatissa ja vastaamaan tarkentaviin kysymyksiin;
- seuraamaan saamiaan ohjeita ja tarkastelemaan mahdollisia tietolähteitä;
- luomaan tukipyynnön keskustelun perusteella tai erikseen;
- tarkastelemaan ja sulkemaan omia tukipyyntöjään;
- käyttämään käyttöliittymää suomeksi tai englanniksi.

Tämä dokumentti määrittelee toiminnallisen käyttöliittymäsuunnitelman, ei lopullista graafista toteutusta. Värit, ikonit, typografia ja tarkat mitat voidaan viimeistellä toteutuksen yhteydessä. Käyttöliittymän on kuitenkin noudatettava tässä määriteltyä rakennetta ja käyttäytymistä.

### 1.1 Suunnitteluperiaatteet

1. **Tehtävä ensin:** käyttäjän pitää löytää AI-chat ja omat tukipyyntönsä ilman turhaa navigointia.
2. **Selkeä seuraava askel:** jokaisella näkymällä on tunnistettava päätarkoitus ja ensisijainen toiminto.
3. **Käyttäjä hallitsee tukipyyntöä:** keskustelusta ei luoda tukipyyntöä automaattisesti. Käyttäjä tarkistaa ja hyväksyy tiedot ennen tallennusta.
4. **Läpinäkyvä AI:** AI:n vastaukset, tarkentavat kysymykset ja tietolähteet erotetaan visuaalisesti toisistaan.
5. **Virheistä voi palautua:** virheilmoituksen jälkeen käyttäjän kirjoittama sisältö säilyy aina, kun se on teknisesti mahdollista.
6. **Tietosuoja ja käyttöoikeudet:** käyttäjä näkee vain omat tietonsa ja tukipyyntönsä.
7. **Kaksikielisyys alusta lähtien:** kaikki käyttöliittymän tekstit toteutetaan käännösavaimilla.
8. **Sovittu laajuus:** käyttöliittymä pidetään projektin laajuuteen sopivana. Viralliseen toimituslaajuuteen kuuluvia käyttäjätarinoita ei käsitellä valinnaisina; uudet ominaisuudet edellyttävät erillistä päätöstä.

## 2. Käyttäjät ja tärkeimmät käyttötapaukset

### 2.1 Ensisijainen käyttäjä

**Opiskelija tai muu järjestelmän käyttäjä**, jolla on IT- tai ohjelmistokehitykseen liittyvä ongelma. Hän haluaa saada ymmärrettäviä ratkaisuohjeita ja tarvittaessa avata tukipyynnön, jonka tilaa voi seurata.

### 2.2 Keskeiset käyttötapaukset

| Käyttötapaus | Käyttäjän tavoite | Odotettu lopputulos |
|---|---|---|
| Rekisteröityminen ja kirjautuminen | Päästä käyttämään palvelua | Käyttäjä pääsee omiin näkymiinsä |
| AI-neuvonnan käyttäminen | Ratkaista IT-ongelma | AI antaa ohjeita ja kysyy tarvittaessa lisätietoja |
| Keskusteluhistorian tarkastelu | Palata aiempaan keskusteluun | Aiemmat viestit näytetään oikeassa järjestyksessä |
| Tukipyynnön luominen | Pyytää jatkoapua | Tukipyyntö tallennetaan ja sille näytetään tunnistetiedot |
| Tukipyyntöjen tarkastelu | Seurata omia pyyntöjä | Käyttäjä näkee omat avoimet ja suljetut pyynnöt |
| Tukipyynnön sulkeminen | Merkitä asia ratkaistuksi | Tukipyynnön tila muuttuu suljetuksi |
| Profiilin ja kielen hallinta | Päivittää omia asetuksia | Muutokset tallennetaan ja valittu kieli otetaan käyttöön |

## 3. Pääkäyttäjäpolut

### 3.1 AI-neuvonnasta ratkaisuun tai tukipyyntöön

1. Käyttäjä kirjautuu sisään.
2. Käyttäjä avaa AI-chatin ja kuvaa ongelmansa omin sanoin.
3. AI vastaa tai kysyy ongelman selvittämiseksi tarkentavia kysymyksiä.
4. Käyttäjä vastaa tarkentaviin kysymyksiin.
5. AI ehdottaa ratkaisuohjeita vaiheittain.
6. Jos tietopohjainen haku löytää sopivan lähteen, käyttöliittymä näyttää lähteen tiedot vastauksen yhteydessä.
7. Käyttäjä kokeilee ohjeita.
8. Jos ongelma ratkeaa, käyttäjä voi päättää keskustelun tai jatkaa kysymistä.
9. Jos ongelma ei ratkea, käyttäjä valitsee **Luo tukipyyntö**.
10. Järjestelmä avaa lomakkeen, jossa keskustelun perusteella ehdotettu otsikko ja kuvaus ovat valmiiksi täytettyjä.
11. Käyttäjä tarkistaa ja tarvittaessa muokkaa tietoja, valitsee prioriteetin ja vahvistaa luomisen.
12. Vasta vahvistuksen jälkeen järjestelmä tallentaa tukipyynnön ja näyttää onnistumisilmoituksen sekä linkin tukipyynnön tietoihin.

**UX-vaatimukset**
- Tukipyyntöä ei luoda ilman käyttäjän nimenomaista vahvistusta; peruminen tai lomakkeelta poistuminen ei tallenna pyyntöä.
- Käyttäjä voi muokata automaattisesti ehdotettua otsikkoa ja kuvausta.
- Keskustelun alkuperäiset viestit säilyvät, vaikka AI-vastaus epäonnistuu.
- Jos tietolähdettä ei löydy, käyttöliittymä kertoo tämän selkeästi eikä esitä vastausta dokumentoidun lähteen tukemana.

### 3.2 Tukipyynnön luominen ilman AI-keskustelua

1. Käyttäjä avaa **Tukipyynnöt**.
2. Käyttäjä valitsee **Uusi tukipyyntö**.
3. Käyttäjä täyttää otsikon, kuvauksen ja prioriteetin.
4. Käyttäjä lähettää lomakkeen.
5. Järjestelmä validoi tiedot ja tallentaa tukipyynnön.
6. Käyttöliittymä näyttää onnistumisviestin ja uuden tukipyynnön tiedot.

### 3.3 Tukipyynnön sulkeminen

1. Käyttäjä avaa oman avoimen tukipyyntönsä.
2. Käyttäjä valitsee **Sulje tukipyyntö**.
3. Käyttöliittymä pyytää vahvistuksen, jos sulkeminen on vaikea peruuttaa tai käyttäjä voi tehdä sen vahingossa.
4. Järjestelmä tallentaa tilaksi `CLOSED`.
5. Käyttöliittymä näyttää uuden tilan.

## 4. Informaatioarkkitehtuuri ja navigaatio

### 4.1 Päänavigaatio

Kirjautuneen käyttäjän päänavigaatio sisältää seuraavat kohdat:

- **Etusivu** – tiivis aloitusnäkymä ja tärkeimmät pikatoiminnot.
- **AI-chat** – uusi keskustelu ja aiempien keskustelujen tarkastelu.
- **Tukipyynnöt** – käyttäjän omien tukipyyntöjen lista ja yksityiskohdat.
- **Profiili** – käyttäjän tiedot, käyttöliittymän kieli ja uloskirjautuminen.

Navigaation nimet ja sijainti pysyvät samoina kaikissa kirjautuneen käyttäjän näkymissä. Nykyinen näkymä ilmaistaan visuaalisesti ja tarvittaessa saavutettavalla tilatiedolla.

### 4.2 Sivurakenne

```text
AI HelpDesk
├── Julkiset näkymät
│   ├── Kirjautuminen
│   └── Rekisteröityminen
└── Kirjautuneen käyttäjän näkymät
    ├── Etusivu
    ├── AI-chat
    │   ├── Uusi keskustelu
    │   └── Keskusteluhistoria / keskustelun sisältö
    ├── Tukipyynnöt
    │   ├── Tukipyyntöjen lista
    │   ├── Uusi tukipyyntö
    │   └── Tukipyynnön tiedot
    └── Profiili
        ├── Käyttäjätiedot
        └── Käyttöliittymän kieli
```

## 5. Yleinen käyttöliittymärakenne

### 5.1 Työpöytänäkymä

Kirjautuneen käyttäjän näkymissä käytetään yhteistä sovelluskehystä:
- vasemmalla päänavigaatio;
- yläreunassa sovelluksen nimi, valitun kielen hallinta tarvittaessa ja käyttäjävalikko;
- keskellä sivun otsikko ja varsinainen sisältö;
- toimintopainikkeet sijoitetaan lähelle niitä koskevaa sisältöä.

Esimerkkirunko:

![UI_pc](../photos/UI_pc.png)

### 5.2 Responsiivisuus

- Käyttöliittymän on oltava käyttökelpoinen sekä tietokoneella että kapealla näytöllä.
- Kapealla näytöllä sivunavigaatio voidaan muuttaa avattavaksi valikoksi.
- Lomakkeet ja keskustelun kirjoituskenttä eivät saa vaatia vaakasuuntaista vieritystä.
- Tukipyyntöjen taulukko voidaan esittää mobiilissa korttilistana.
- Ensisijaiset toiminnot eivät saa jäädä piiloon pelkästään leveällä näytöllä näkyvän sivupalkin vuoksi.

## 6. Sivukohtaiset UX/UI-määrittelyt

### 6.1 Kirjautuminen

**Tarkoitus:** antaa rekisteröityneelle käyttäjälle pääsy palveluun.

**Sisältö**
- sovelluksen nimi ja lyhyt kuvaus;
- sähköpostiosoite;
- salasana;
- **Kirjaudu sisään** -painike;
- linkki rekisteröitymiseen;
- virhe- ja lataustila.

**Käyttäytyminen**
- Pakolliset kentät validoidaan.
- Kirjautumisen aikana painike näyttää lataustilan ja estää vahingossa toistuvat lähetykset.
- Virheilmoitus on ymmärrettävä eikä paljasta, onko tietty sähköpostiosoite rekisteröitynyt, jos tämä aiheuttaisi tietoturvariskin.
- Onnistunut kirjautuminen vie käyttäjän etusivulle tai aiemmin pyydettyyn suojattuun näkymään.

**Tyhjä- ja virhetilat**
- virheelliset tai puuttuvat kentät;
- väärät kirjautumistiedot;
- palvelin- tai verkkovirhe;
- kirjautumisen käsittely kesken.

### 6.2 Rekisteröityminen

**Tarkoitus:** luoda uusi käyttäjätili.

**Sisältö**
- etunimi;
- sukunimi;
- käyttäjänimi;
- sähköpostiosoite;
- salasana;
- **Luo tili** -painike;
- linkki kirjautumiseen;
- kenttäkohtaiset validointiviestit.

**Käyttäytyminen**
- Pakolliset kentät ja salasanavaatimukset kerrotaan ennen lähettämistä.
- Käyttäjä saa selkeän palautteen onnistumisesta tai epäonnistumisesta.
- Onnistumisen jälkeen käyttäjä ohjataan määritellyn autentikointivirran mukaisesti kirjautuneeseen näkymään tai kirjautumissivulle.

### 6.3 Etusivu

**Tarkoitus:** ohjata käyttäjä nopeasti tärkeimpään tehtävään.

**Sisältö**
- tervehdys tai lyhyt palvelun kuvaus;
- ensisijainen **Aloita AI-keskustelu** -painike;
- linkki omiin tukipyyntöihin;
- rajattu yhteenveto käyttäjän omien tukipyyntöjen kokonaismäärästä sekä `OPEN`- ja `CLOSED`-tilojen lukumääristä (US-14).

**Priorisointi**
Etusivu pidetään yksinkertaisena ja US-14:n yhteenveto on pakollinen osa sovittua toimituslaajuutta. Se näyttää vain kokonaismäärän sekä `OPEN`- ja `CLOSED`-määrät. Laaja analytiikkapaneeli, monimutkaiset kaaviot, suodatukset, aikavertailut ja viimeisimpien tukipyyntöjen erillinen nosto eivät kuulu tähän määrittelyyn.

### 6.4 AI-chat

**Tarkoitus:** auttaa käyttäjää selvittämään IT-ongelma keskustelemalla.

**Sisältö**
- keskustelun otsikko tai tunniste;
- viestialue;
- käyttäjän ja AI:n viestit selkeästi eroteltuina;
- kirjoituskenttä;
- **Lähetä**-painike;
- **Uusi keskustelu** -toiminto;
- keskusteluhistoriaan siirtyminen;
- **Luo tukipyyntö** -toiminto;
- lähdetiedot AI:n vastauksen yhteydessä silloin, kun RAG-haku löytää käytettävän lähteen.

**Viestien esitystapa**
- Käyttäjän viestit ja AI:n vastaukset erotetaan toisistaan sekä visuaalisesti että tekstuaalisesti.
- AI:n tarkentavat kysymykset esitetään keskustelussa samalla tavalla kuin muut AI-viestit.
- Pitkät vastaukset jäsennetään otsikoihin, numeroituihin vaiheisiin ja luettaviin kappaleisiin.
- Lähdetiedot esitetään vastauksesta erillisenä osana, esimerkiksi lähteen nimellä ja linkillä, jos linkki on saatavilla.
- Lähdettä ei näytetä, jos sitä ei ole oikeasti löydetty.

**Käyttäytyminen**
- Tyhjän viestin lähettäminen estetään.
- Lähetyksen aikana näytetään lataustila.
- Käyttäjä saa palautteen, jos vastausta muodostetaan.
- Virheen jälkeen käyttäjän kirjoittama teksti säilyy ja lähettämistä voi yrittää uudelleen.
- Jos keskusteluhistorian tallennus epäonnistuu, käyttäjälle kerrotaan siitä.
- Keskustelun viestit näytetään aikajärjestyksessä.
- Käyttäjä voi aloittaa uuden keskustelun menettämättä aiempia tallennettuja keskusteluja.

**Suositeltu asettelu**

![AIchat](../photos/AIchat.png)

Mobiilissa keskusteluhistoria voidaan avata erillisestä painikkeesta, jotta varsinainen keskustelualue säilyy riittävän leveänä.

### 6.5 Tukipyyntöjen lista

**Tarkoitus:** näyttää käyttäjälle hänen omat tukipyyntönsä.

**Sisältö**
- sivun otsikko **Tukipyynnöt**;
- **Uusi tukipyyntö** -painike;
- lista tai taulukko, jossa näkyvät otsikko, tila, prioriteetti ja luontiaika;
- listan tyhjä-, lataus- ja virhetilat.

**Tilat ja prioriteetit**
- tilat: `OPEN` ja `CLOSED`;
- prioriteetit: `LOW`, `MEDIUM` ja `HIGH`.

Tilat näytetään käyttäjälle valitulla käyttöliittymän kielellä, vaikka tietokannassa käytetään teknisiä arvoja. Esimerkiksi `OPEN` näytetään suomeksi **Avoin** ja englanniksi **Open**.

**Käyttäytyminen**
- Tukipyynnön otsikkoa tai riviä valitsemalla avataan yksityiskohtanäkymä.
- Käyttäjä näkee vain omat tukipyyntönsä.
- Tyhjässä listassa näytetään ohjeteksti ja toiminto uuden tukipyynnön luomiseen.
- Lataus- ja virhetilat esitetään erikseen.

### 6.6 Uusi tukipyyntö

**Tarkoitus:** tallentaa käyttäjän ongelma tukipyynnöksi.

**Kentät**
- otsikko;
- kuvaus;
- prioriteetti (`LOW`, `MEDIUM`, `HIGH`);
- **Luo tukipyyntö** -painike;
- **Peruuta**-toiminto.

**Käyttäytyminen**
- Otsikko ja kuvaus ovat pakollisia.
- Validointivirhe näytetään kyseisen kentän yhteydessä.
- Lomakkeen lähettämisen aikana estetään vahingossa tapahtuva kaksoislähetys.
- Onnistumisen jälkeen näytetään vahvistus ja linkki luotuun tukipyyntöön.
- Virhetilanteessa syötetyt tiedot säilyvät.

Jos lomake avataan AI-keskustelusta, otsikko ja kuvaus voidaan esitäyttää keskustelun perusteella. Käyttäjä voi muuttaa niitä ennen tallentamista.

### 6.7 Tukipyynnön tiedot

**Tarkoitus:** näyttää yhden tukipyynnön tiedot ja tarjota sallittu toiminto.

**Sisältö**
- otsikko ja kuvaus;
- tila;
- prioriteetti;
- luontiaika;
- mahdollinen linkki siihen liittyvään keskusteluun, jos yhteys on tallennettu;
- **Sulje tukipyyntö** -painike avoimelle pyynnölle.

**Käyttäytyminen**
- Sulkemistoiminto on käytettävissä vain avoimelle tukipyynnölle.
- Sulkemisen jälkeen tila päivittyy näkymään.
- Suljetun tukipyynnön kohdalla ei näytetä aktiivista sulkemispainiketta.
- Jos tukipyyntöä ei löydy tai käyttäjällä ei ole siihen oikeutta, näytetään turvallinen virhenäkymä ilman muiden käyttäjien tietoja.

### 6.8 Keskusteluhistoria

**Tarkoitus:** antaa käyttäjälle mahdollisuus palata aiempaan AI-keskusteluun.

**Sisältö**
- tallennettujen keskustelujen lista;
- keskustelun otsikko tai lyhyt tunniste;
- viimeisimmän viestin aika, jos tieto on saatavilla;
- valitun keskustelun viestit.

**Käyttäytyminen**
- Keskustelut järjestetään johdonmukaisesti, esimerkiksi viimeisimmän viestin mukaan.
- Valittu keskustelu avautuu viesteineen.
- Tyhjässä historiassa näytetään ohje uuden keskustelun aloittamiseen.
- Käyttäjä ei voi avata toisen käyttäjän keskustelua.

### 6.9 Profiili ja kieliasetus

**Tarkoitus:** näyttää käyttäjän tiedot, mahdollistaa sallittujen profiilitietojen päivittäminen, salasanan vaihtaminen ja käyttöliittymän kielen hallinta.

**Profiilitiedot**
- etunimi – muokattavissa;
- sukunimi – muokattavissa;
- käyttäjänimi – muokattavissa;
- sähköpostiosoite – näytetään vain luettavana, eikä käyttöliittymä tarjoa sen muuttamista.

**Salasanan vaihtaminen**
- erillinen **Vaihda salasana** -toiminto;
- nykyisen salasanan kenttä;
- uuden salasanan kenttä;
- uuden salasanan vahvistuskenttä;
- **Vaihda salasana** -painike ja onnistumis-/virheilmoitus.

**Muut toiminnot**
- kielen valinta: suomi / englanti;
- **Tallenna muutokset** -painike profiilitiedoille;
- **Kirjaudu ulos** -toiminto.

**Kaksikielisyys**
- Kielen vaihtaminen päivittää käyttöliittymän tekstit ilman, että käyttäjän tarvitsee kirjautua uudelleen.
- Valinta säilyy seuraavalla käyttökerralla, esimerkiksi selaimen paikallisessa tallennuksessa.
- Kielen valintaa ei saa toteuttaa vain yksittäisessä näkymässä: myös navigaatio, lomakkeet, validointiviestit, painikkeet, tilat ja virheilmoitukset käännetään.
- Käyttöliittymän kieli ja AI:n vastauksen kieli ovat eri asioita. AI:lle välitetään keskustelun kieli tai käyttäjän valinta selkeästi, mutta AI-vastausten kieli ei saa perustua pelkästään siihen, mitä kieltä jokin yksittäinen käyttöliittymän teksti käyttää.

## 7. Yhteiset käyttöliittymäkomponentit

| Komponentti | Käyttötarkoitus | Käyttäytyminen |
|---|---|---|
| Päänavigaatio | Siirtyminen pääsivujen välillä | Nykyinen sivu erottuu selvästi |
| Ensisijainen painike | Sivun tärkein toiminto | Yksi selkeä ensisijainen toiminto kerrallaan |
| Toissijainen painike/linkki | Peruminen tai vaihtoehtoinen toiminto | Ei kilpaile visuaalisesti ensisijaisen kanssa |
| Lomakekenttä | Tietojen syöttäminen | Label, tarvittaessa ohje ja kenttäkohtainen virhe |
| Tilaindikaattori | Tukipyynnön tilan näyttäminen | Teksti ja visuaalinen ero; ei pelkkä väri |
| Viestikupla/viestikortti | Käyttäjän ja AI:n viestit | Lähettäjä on tunnistettavissa myös ilman väriä |
| Lähdekortti | RAG-lähteen näyttäminen | Lähteen nimi ja linkki, jos saatavilla |
| Ilmoitus | Onnistuminen, varoitus tai virhe | Lyhyt, ymmärrettävä ja toimintaan ohjaava |
| Tyhjän näkymän tila | Sisältöä ei ole vielä | Selittää tilanteen ja tarjoaa seuraavan toiminnon |
| Lataustila | Pyyntö on käynnissä | Estää toistuvat lähetykset ja kertoo odottamisesta |

## 8. Kaksikielisyys ja saavutettavuus

### 8.1 Käännökset

Kaikki käyttöliittymän tekstit toteutetaan käännösavaimilla, ei suoraan komponentteihin kirjoitettuina teksteinä. Esimerkkejä:

```text
nav.home
nav.chat
nav.tickets
nav.profile
auth.login
auth.register
ticket.status.open
ticket.status.closed
ticket.priority.low
ticket.priority.medium
ticket.priority.high
chat.send
chat.newConversation
chat.createTicket
common.save
common.cancel
common.loading
error.generic
```

Suomen- ja englanninkieliset vastineet ylläpidetään keskitetysti. Uutta käyttöliittymätekstiä lisättäessä tarkistetaan molemmat kielet.

### 8.2 Saavutettavuuden perusvaatimukset

- Kaikilla lomakekentillä on näkyvä tai ohjelmallisesti yhdistetty nimi.
- Painikkeiden tekstit kertovat toiminnon; pelkkiä epäselviä ikoneita vältetään.
- Tekstin ja taustan kontrasti on riittävä.
- Tilan tai prioriteetin merkitys ei välity ainoastaan värillä.
- Käyttöliittymää voi käyttää näppäimistöllä.
- Kohdistuksen sijainti näkyy selvästi.
- Virheviestit ovat ymmärrettäviä ja liittyvät oikeaan kenttään tai toimintoon.
- Otsikkotasot ovat loogisessa järjestyksessä.
- Dynaamiset lataus- ja onnistumisviestit esitetään tavalla, jonka avustavat teknologiat voivat havaita mahdollisuuksien mukaan.

## 9. Käyttöliittymän tilat ja virhetilanteet

Jokaisessa tietoa hakevassa tai tallentavassa näkymässä huomioidaan vähintään seuraavat tilat:

| Tila | Käyttöliittymän toiminta |
|---|---|
| Lataus | Näytetään latausilmaisin ja estetään tarpeeton kaksoislähetys |
| Onnistuminen | Kerrotaan, mitä tallennettiin tai mitä tapahtui |
| Validointivirhe | Näytetään korjattava virhe kentän lähellä |
| Verkkovirhe | Kerrotaan, ettei toimintoa voitu suorittaa, ja tarjotaan uudelleenyritystä |
| Ei sisältöä | Kerrotaan, ettei tietoja vielä ole, ja tarjotaan seuraava toiminto |
| Ei käyttöoikeutta | Näytetään turvallinen ilmoitus paljastamatta suojattuja tietoja |
| AI-palvelun virhe | Säilytetään käyttäjän teksti ja tarjotaan uudelleenyritystä |
| RAG-lähdettä ei löydy | Kerrotaan, ettei sopivaa lähdettä löytynyt; lähdettä ei keksitä |
| Istunto vanhentunut | Ohjataan kirjautumaan uudelleen ja vältetään syötettyjen tietojen tarpeetonta häviämistä |

Virheilmoituksen tulee kertoa käyttäjälle:
1. mitä tapahtui;
2. voiko käyttäjä tehdä jotain;
3. säilyivätkö syötetyt tiedot, jos se on tilanteessa olennaista.

Teknisiä pinojälkiä, tietokantavirheitä tai muita sisäisiä yksityiskohtia ei näytetä loppukäyttäjälle.

## 10. Tietosuoja ja luottamus käyttöliittymässä

- Kirjautumista vaativat näkymät eivät näy kirjautumattomalle käyttäjälle.
- Käyttöliittymä ei luota pelkästään siihen, että navigaatio piilottaa muiden käyttäjien tiedot. Backend tarkistaa käyttöoikeudet jokaisessa suojatussa pyynnössä.
- Tukipyynnön ja keskustelun tiedot näytetään vain oikeutetulle käyttäjälle.
- Käyttäjälle kerrotaan selkeästi, milloin tukipyyntö tallennetaan.
- AI:n tuottamat ohjeet esitetään ehdotuksina. Käyttäjälle ei anneta virheellistä vaikutelmaa siitä, että AI olisi aina oikeassa.
- RAG-lähde näytetään vain, jos haku palauttaa todellisen lähteen.
- Käyttöliittymässä ei näytetä salasanoja tai tarpeettomia henkilötietoja.

## 11. UX/UI-hyväksymiskriteerit

Seuraavat kriteerit täydentävät käyttäjätarinoiden hyväksymiskriteerejä. Ne eivät korvaa käyttäjätarinoissa määriteltyjä toiminnallisia vaatimuksia.

| ID | Hyväksymiskriteeri | Testaus |
|---|---|---|
| UX-01 | Kirjautumisen ja rekisteröitymisen lomakkeissa on selkeät kenttänimet ja ymmärrettävät virheilmoitukset. | Testaa tyhjät kentät ja virheelliset tiedot |
| UX-02 | Kirjautuneen käyttäjän päänavigaatio pysyy johdonmukaisena näkymästä toiseen. | Siirry kaikkien pääsivujen välillä |
| UX-03 | Käyttäjä erottaa omat viestinsä AI:n viesteistä. | Tarkastele vähintään yhtä keskustelua |
| UX-04 | AI-chatissa voi lähettää viestin, nähdä lataustilan ja jatkaa virhetilanteesta. | Testaa onnistuminen ja simuloitu virhe |
| UX-05 | Tukipyyntöä ei luoda AI-keskustelusta ilman käyttäjän tarkistusta ja hyväksyntää. | Käynnistä luonti ja peruuta ennen tallennusta |
| UX-06 | Tukipyynnön otsikko, kuvaus, tila, prioriteetti ja luontiaika ovat löydettävissä. | Avaa tukipyyntöjen lista ja yksityiskohdat |
| UX-07 | Käyttäjä voi sulkea avoimen tukipyynnön, ja tila päivittyy näkyvästi. | Sulje testitukipyyntö |
| UX-08 | Tyhjä lista, lataus ja virhetilanne on esitetty erikseen. | Testaa tyhjällä käyttäjätilillä ja virhetilanteessa |
| UX-09 | Käyttöliittymän kielen voi vaihtaa suomen ja englannin välillä. | Vaihda kieltä eri näkymissä |
| UX-10 | Kielen valinta säilyy seuraavalla käyttökerralla toteutusratkaisun mukaisesti. | Päivitä sivu tai avaa sovellus uudelleen |
| UX-11 | RAG-lähde näkyy vastauksen yhteydessä vain silloin, kun lähde on oikeasti saatavilla. | Testaa löytyvä ja löytymätön lähde |
| UX-12 | Käyttöliittymän tärkeimmät toiminnot toimivat kapealla näytöllä ilman tarpeetonta vaakavieritystä. | Testaa selainikkunan kapealla leveydellä |
| UX-13 | Tukipyyntöjen tila ja prioriteetti eivät erotu ainoastaan värin perusteella. | Tarkista tekstit ja visuaaliset tunnisteet |
| UX-14 | Käyttäjä näkee vain omat tukipyyntönsä ja keskustelunsa. | Testaa kahdella eri testikäyttäjällä |
| UX-15 | Käyttäjän viesti säilyy AI-palvelun virheen jälkeen, jos se on jo kirjoitettu tai lähetetty. | Simuloi AI-palvelun virhe |
| UX-16 | Etusivu näyttää vain kirjautuneen käyttäjän tukipyyntöjen kokonaismäärän sekä `OPEN`- ja `CLOSED`-määrät; tyhjän tilin arvot ovat nollia. | Testaa käyttäjätilillä, jolla on pyyntöjä ja tyhjällä tilillä; vertaa lukumääriä tietokantaan |
| UX-17 | Profiilissa etunimi, sukunimi ja käyttäjänimi ovat muokattavissa, mutta sähköpostiosoite on vain luettavissa. | Muokkaa sallittuja kenttiä ja varmista, ettei sähköpostille ole muokkaustoimintoa |
| UX-18 | Salasanan vaihto pyytää nykyisen salasanan, uuden salasanan ja vahvistuksen sekä näyttää onnistumis- tai virhepalautteen. | Testaa oikea ja väärä nykyinen salasana sekä poikkeava vahvistus |

## 12. Käytettävyystestaussuunnitelma

Testaus tehdään projektin aikana kehitysympäristössä. Testaamiseen käytetään testikäyttäjiä ja testitietoja, ei oikeita arkaluonteisia henkilötietoja.

### 12.1 Testiskenaariot

1. **Kirjautuminen:** käyttäjä kirjautuu sisään oikeilla ja väärillä tunnuksilla.
2. **AI-neuvonta:** käyttäjä kuvaa ongelman, vastaa tarkentavaan kysymykseen ja lukee ratkaisuehdotuksen.
3. **Tukipyynnön luominen:** käyttäjä luo pyynnön AI-keskustelusta, tarkistaa esitäytetyt tiedot ja hyväksyy tallennuksen.
4. **Tukipyynnön hallinta:** käyttäjä löytää pyynnön listalta, avaa sen ja sulkee sen.
5. **Keskusteluhistoria:** käyttäjä avaa aiemman keskustelun.
6. **Kielenvaihto:** käyttäjä vaihtaa suomen englanniksi ja takaisin.
7. **Virhetilanteet:** käyttäjä kohtaa verkkovirheen tai AI-palvelun virheen ja pystyy jatkamaan.
8. **Käyttöoikeudet:** kahden testikäyttäjän tiedot eivät näy ristiin.
9. **Mobiilinäkymä:** käyttäjä suorittaa tärkeimmät toiminnot kapealla näytöllä.

### 12.2 Testitulosten kirjaaminen

Jokaisesta testistä kirjataan:
- testipäivä;
- testattu toiminto;
- odotettu tulos;
- toteutunut tulos;
- havaittu ongelma;
- korjaustoimenpide ja tila.

Käytettävyystestauksen tavoitteena on löytää tehtävän suorittamista estävät ongelmat ennen projektin palautusta. Testaus voidaan tehdä kehittäjän omana tarkistuslistana ja mahdollisuuksien mukaan toisella henkilöllä, joka ei ole toteuttanut kyseistä näkymää.

## 13. Toteutusjärjestys ja yhteys sprintteihin

UX/UI-työ tehdään vaiheittain muun kehityksen rinnalla. Tarkka toteutusjärjestys sovitetaan Sprintin suunnitelmaan ja Product Backlogiin.

| Vaihe | UX/UI-työ | Yhteys toiminnallisuuksiin |
|---|---|---|
| Sprint 1 | Yleinen sovelluskehys, navigaatio, kirjautumisen ja rekisteröitymisen perusrakenne, käännösavainten pohja | Perusrakenne ja autentikointi |
| Sprint 2 | Tukipyyntöjen lista, luontilomake, yksityiskohdat ja profiili | Tukipyyntöjen hallinta |
| Sprint 3 | AI-chatin viestialue, kirjoituskenttä, lataus- ja virhetilat, keskusteluhistoria | AI-keskustelu |
| Sprint 4 | Keskustelusta tukipyyntöön -polku, kaksikielisyyden täydentäminen, käytettävyystestaus | Integrointi ja kielituki |
| Sprint 5 | RAG-lähdekortit, lähteettömän vastauksen tila, kokonaispolun testaus | Tietopohjainen AI-neuvonta |

Toteutusjärjestys noudattaa sovittua Sprint-jakoa ja teknisiä riippuvuuksia. Docker Compose sisältää frontendin, backendin, MySQL:n ja Ollaman valitulla mallilla. Keskustelusta tukipyynnön luonti (US-09) edellyttää käyttäjän tietojen tarkistusta ja vahvistusta; etusivun rajattu yhteenveto (US-14) kuuluu toimitukseen. Kolme valittua lisäominaisuutta (Docker Compose Ollama-palveluineen, suomen- ja englanninkielinen käyttöliittymä sekä RAG) sekä US-09 ja US-14 ovat lopullisen toimituslaajuuden sitoumuksia.

## 14. Rajaukset ja jatkokehitys

Tämän UX/UI-määrittelyn ensimmäiseen versioon eivät kuulu:
- yksityiskohtainen visuaalinen brändiohje;
- lopullinen pikselintarkka prototyyppi;
- ääni- tai puhekäyttöliittymä;
- PDF-vienti;
- laaja analytiikka- tai hallintapaneeli;
- monimutkaiset käyttäjäroolit tai ylläpitäjän hallintanäkymä, ellei niitä lisätä vaatimusmäärittelyyn.

US-14:n rajattu etusivuyhteenveto kuuluu toimituslaajuuteen. Sen ulkopuolelle jäävät laajat analytiikkaominaisuudet ja muut tässä dokumentissa rajaamattomat dashboard-laajennukset. Mahdolliset uudet ominaisuudet kirjataan ensin Product Backlogiin ja hyväksytään muutostenhallinnan kautta.

## 15. Yhteys muihin projektidokumentteihin

Tämä dokumentti täydentää seuraavia dokumentteja:
- [Projektinhallinta](00-projektinhallinta.md) – projektin hallinta, tavoitteet, rajaukset ja riskit;
- [Vaatimusmäärittely](01-vaatimusmaarittely.md) – toiminnalliset ja ei-toiminnalliset vaatimukset;
- [Käyttäjätarinat ja hyväksymiskriteerit](02-käyttäjätarinat%20ja%20hyväksymiskriteerit.md) – käyttäjätarinat ja hyväksymiskriteerit;
- [Product Backlog](03-product%20backlog.md) – priorisoidut kehitystehtävät;
- [Sprint-suunnitelma](04-sprintin%20suunnitelma.md) – sprinttien tavoitteet ja tehtävät;
- [Järjestelmän suunnittelu](05-järjestelmän%20suunnittelu.md) – arkkitehtuuri, vastuut ja API-rakenne.

Jos tämän dokumentin ja vaatimusmäärittelyn välillä havaitaan ristiriita, asia tarkistetaan ennen toteutusta ja muutokset kirjataan asianmukaisiin dokumentteihin.

---

## Muutoshistoria

| Versio | Päiväys | Muutos |
|---|---|---|
| 1.0 | 26.10.2026 | Ensimmäinen UX/UI-suunnittelun määrittely |