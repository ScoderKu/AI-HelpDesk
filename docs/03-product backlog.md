# AI HelpDesk – Product Backlog

## 1. Product Backlogin tarkoitus

Tämä dokumentti määrittelee AI HelpDesk -sovelluksen priorisoidun Product Backlogin. Se sisältää käyttäjätarinoiden tunnisteet, prioriteetit, työmääräarviot, tekniset riippuvuudet ja alustavan sprinttijaon. Lopulliseen julkaisuun valitut lisäominaisuudet ovat US-13 (suomen- ja englanninkielinen käyttöliittymä), US-15 (RAG) ja US-16 (Docker Compose -käynnistys yhdellä komennolla).

Käyttäjätarinoiden täydelliset kuvaukset ja hyväksymiskriteerit on määritelty erillisessä dokumentissa `02-käyttäjätarinat ja hyväksymiskriteerit.md`. Tässä dokumentissa käyttäjätarinoihin viitataan niiden tunnisteilla US-01–US-16.

Product Backlogin tavoitteena on varmistaa, että MVP:n keskeiset toiminnallisuudet toteutetaan ennen monikielistä käyttöliittymää ja RAG-toiminnallisuutta. Docker Compose -ympäristö rakennetaan Sprint 1:ssä kehitys- ja esittely-ympäristöä varten.

---

## 2. Story Point -asteikko

Työmääräarviot perustuvat suhteelliseen Story Point -arviointiin. Arvioinnissa huomioidaan toteutuksen monimutkaisuus, epävarmuus, testauksen tarve ja riippuvuudet muihin toimintoihin.

| Story Points (SP) | Vaikeustaso | Kuvaus |
|------------------|------------|---------|
| 1 | Erittäin pieni | Yksinkertainen ja rajattu tehtävä |
| 2 | Pieni | Selkeä toteutus, jossa on vähän riippuvuuksia |
| 3 | Keskisuuri | Useita toteutusvaiheita tai rajapintamuutoksia |
| 5 | Melko suuri | Useita komponentteja tai tietokantamuutoksia |
| 8 | Suuri | Laaja toiminnallisuus tai useita teknisiä riippuvuuksia |
| 13 | Erittäin suuri | Monimutkainen kokonaisuus, jonka jakamista pienempiin osiin kannattaa harkita |

---

## 3. Product Backlog -taulukko

| Järjestys | ID | Käyttäjätarina | Prioriteetti | SP | Sprintti |
|-----------|----|----------------|-------------|----|----------|
| 1 | US-10 | REST-rajapinnan käyttäminen | P1 | 8 | Sprint 1 |
| 2 | US-11 | Tietojen pysyvä tallentaminen | P1 | 5 | Sprint 1 |
| 3 | US-01 | Käyttäjän rekisteröityminen | P1 | 5 | Sprint 1 |
| 4 | US-02 | Käyttäjän kirjautuminen | P1 | 5 | Sprint 1 |
| 5 | US-12 | Käyttöliittymän käytettävyys | P1 | 5 | Sprint 1 |
| 6 | US-04 | Tukipyynnön luominen | P1 | 5 | Sprint 2 |
| 7 | US-05 | Omien tukipyyntöjen tarkastelu ja sulkeminen | P1 | 5 | Sprint 2 |
| 8 | US-03 | Käyttäjäprofiilin hallinta | P1 | 3 | Sprint 2 |
| 9 | US-06 | Tekoälypohjainen keskustelu | P1 | 8 | Sprint 3 |
| 10 | US-08 | Keskusteluviestien tallentaminen | P1 | 5 | Sprint 3 |
| 11 | US-07 | Tarkentavat kysymykset ja ongelmanratkaisu | P1 | 5 | Sprint 3 |
| 12 | US-09 | Tukipyynnön luominen keskustelusta | P2 | 3 | Sprint 4 |
| 13 | US-13 | Monikielinen käyttöliittymä | P2 | 3 | Sprint 4 |
| 14 | US-14 | Tukipyyntöjen yhteenvetonäkymä | P3 | 3 | Sprint 4 |
| 15 | US-15 | Tietopohjainen tekoälyneuvonta (RAG) | P2 | 13 | Sprint 5 |
| 16 | US-16 | Sovelluksen käynnistäminen Docker Composella | P2 | Arvioitava | Sprint 1 |
| **Yhteensä** |  |  |  | **81 SP + US-16:n arvio** |  |

---

## 4. Käyttäjätarinoiden riippuvuudet

| Käyttäjätarina | Keskeiset riippuvuudet |
|---------------|-----------------------|
| US-01 | Tietokanta ja käyttäjätietojen tallennus |
| US-02 | US-01, autentikointi ja käyttöoikeuksien hallinta |
| US-03 | US-01, käyttäjäkohtainen tietojen haku |
| US-04 | US-10, US-11 ja käyttäjän tunnistaminen |
| US-05 | US-04, US-10, US-11 ja käyttöoikeuksien tarkistaminen |
| US-06 | REST-rajapinta ja tekoälypalvelun integraatio |
| US-07 | US-06 ja keskustelukontekstin käsittely |
| US-08 | US-11 ja keskustelujen tietomalli |
| US-09 | US-04, US-06 ja keskustelutietojen saatavuus |
| US-10 | Backendin perusrakenne ja rajapintojen määrittely |
| US-11 | Tietomalli, tietokantayhteys ja viite-eheys |
| US-12 | Käyttöliittymän perusrakenne ja sovelluksen toiminnallisuudet |
| US-13 | Käyttöliittymän tekstien erottaminen kielikohtaisiin resursseihin |
| US-14 | Tukipyyntöjen tallennus ja hakutoiminnot |
| US-15 | US-06, dokumentaation käsittely, hakuratkaisu ja tekoälyintegraatio |
| US-16 | Frontendin, backendin ja MySQL-tietokannan käynnistys- ja konfiguraatiotarpeet |

Riippuvuudet eivät tarkoita, että kaikki edeltävät käyttäjätarinat on aina saatettava kokonaan valmiiksi ennen seuraavan aloittamista. Teknisiä perustöitä voidaan toteuttaa rinnakkain.

---

## 5. MVP:n rajaus

MVP-version tavoitteena on toteuttaa AI HelpDesk -sovelluksen keskeinen käyttöpolku.

### MVP sisältää seuraavat käyttäjätarinat:

- US-01: Käyttäjän rekisteröityminen
- US-02: Käyttäjän kirjautuminen
- US-03: Käyttäjäprofiilin hallinta
- US-04: Tukipyynnön luominen
- US-05: Omien tukipyyntöjen tarkastelu ja sulkeminen
- US-06: Tekoälypohjainen keskustelu
- US-07: Tarkentavat kysymykset ja ongelmanratkaisu
- US-08: Keskusteluviestien tallentaminen
- US-10: REST-rajapinnan käyttäminen
- US-11: Tietojen pysyvä tallentaminen
- US-12: Käyttöliittymän käytettävyys

US-13 ja US-15 ovat MVP:n ulkopuolella mutta valittu toteutettaviksi lopulliseen julkaisuun. US-16:n Docker Compose -käynnistys toteutetaan Sprint 1:ssä kehitys- ja esittely-ympäristön perustaksi. US-09 ja US-14 voidaan priorisoida jäljellä olevan ajan ja projektin tarpeiden mukaan.

---

## 6. Backlogin hallinta

Product Backlogia ylläpidetään koko kehitysprojektin ajan.

1. Käyttäjätarinat järjestetään ensisijaisesti niiden arvon, prioriteetin, riskien ja riippuvuuksien perusteella.
2. Kehittäjä tarkentaa Story Point -arviot ennen toteutusta.
3. Liian suuret käyttäjätarinat jaetaan pienempiin, testattaviin kokonaisuuksiin.
4. Hyväksymiskriteerit tarkistetaan alkuperäisestä `02-käyttäjätarinat ja hyväksymiskriteerit.md`-dokumentista.
5. Uudet vaatimukset lisätään backlogiin ja priorisoidaan suhteessa olemassa oleviin vaatimuksiin.
6. Toteutustila päivitetään projektin aikana esimerkiksi tiloilla **To Do**, **In Progress**, **In Review** ja **Done**.

---

## 7. Definition of Ready

Käyttäjätarina on valmis valittavaksi Sprintiin, kun:

1. Käyttäjätarinalla on yksilöllinen tunniste ja selkeä tavoite.
2. Hyväksymiskriteerit löytyvät `02-käyttäjätarinat ja hyväksymiskriteerit.md`-dokumentista.
3. Prioriteetti on määritelty.
4. Työmääräarvio on tehty kehitystiimin kanssa.
5. Keskeiset riippuvuudet ja tekniset epävarmuudet on tunnistettu.
6. Tarina on riittävän pieni toteutettavaksi yhden Sprintin aikana.

---

## 8. Yhteenveto

AI HelpDesk -sovelluksen Product Backlog sisältää 16 käyttäjätarinaa. Arvioiduista tarinoista kertyy 81 Story Pointia; US-16:n arvio lisätään, kun toteutuksen laajuus on tarkennettu.

Backlogin ensimmäinen tavoite on rakentaa toimiva tekninen perusta, toteuttaa käyttäjien tunnistaminen ja tukipyyntöjen hallinta sekä mahdollistaa tekoälypohjainen keskustelu.