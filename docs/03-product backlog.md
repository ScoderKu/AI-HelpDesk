# AI HelpDesk – Product Backlog

## 1. Product Backlogin tarkoitus

Tämä dokumentti määrittelee AI HelpDesk -sovelluksen priorisoidun Product Backlogin. Se sisältää käyttäjätarinoiden tunnisteet, prioriteetit, työmääräarviot, tekniset riippuvuudet ja sovitun sprinttijaon. US-09 ja US-14 kuuluvat viralliseen toimituslaajuuteen. Valitut lisäominaisuudet ovat US-13 (suomen- ja englanninkielinen käyttöliittymä), US-15 (RAG) ja US-16 (Docker Compose -käynnistys yhdellä komennolla; mukana myös Ollama).

Käyttäjätarinoiden täydelliset kuvaukset ja hyväksymiskriteerit on määritelty erillisessä dokumentissa `02-käyttäjätarinat ja hyväksymiskriteerit.md`. Tässä dokumentissa käyttäjätarinoihin viitataan niiden tunnisteilla US-01–US-17.

MVP:n perustoiminnot sekä sovitut US-09 ja US-14 toteutetaan niiden Sprint-jaon mukaisesti. RAG ja monikielinen käyttöliittymä toteutetaan omissa Sprint-jaksoissaan. Docker Compose -ympäristö, mukaan lukien Ollama ja valittu malli, rakennetaan Sprint 1:ssä kehitys- ja esittely-ympäristöä varten.

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
| 9 | US-17 | Unohtuneen salasanan palauttaminen ADMINin toimesta | P1 | 2 | Sprint 2 |
| 10 | US-06 | Tekoälypohjainen keskustelu | P1 | 8 | Sprint 3 |
| 11 | US-08 | Keskusteluviestien tallentaminen | P1 | 5 | Sprint 3 |
| 12 | US-07 | Tarkentavat kysymykset ja ongelmanratkaisu | P1 | 5 | Sprint 3 |
| 13 | US-09 | Tukipyynnön luominen keskustelusta | P2 | 3 | Sprint 4 |
| 14 | US-13 | Monikielinen käyttöliittymä | P2 | 3 | Sprint 4 |
| 15 | US-14 | Tukipyyntöjen rajattu yhteenvetonäkymä | P3 | 3 | Sprint 4 |
| 16 | US-15 | Tietopohjainen tekoälyneuvonta (RAG) | P2 | 13 | Sprint 5 |
| 17 | US-16 | Sovelluksen käynnistäminen Docker Composella | P2 | 5 | Sprint 1 |
| **Yhteensä** |  |  |  | **88 SP** |  |

US-16:n 5 SP:n arvio kattaa frontendin, backendin, MySQL:n ja Ollaman Compose-palvelut, GGUF-mallin käyttöönoton Ollama-kontissa, tarvittavat konfiguraatiot, tietokannan ja mallin pysyvän tallennuksen, valmiustarkistukset sekä dokumentoinnin ja käynnistyksen integraatiotestauksen. Arvio ei sisällä tuotantoympäristön käyttöönottoa tai orkestrointia.

---

## 4. Käyttäjätarinoiden riippuvuudet

| Käyttäjätarina | Keskeiset riippuvuudet |
|---------------|-----------------------|
| US-01 | Tietokanta ja käyttäjätietojen tallennus |
| US-02 | US-01, autentikointi ja käyttöoikeuksien hallinta |
| US-03 | US-01, käyttäjäkohtainen tietojen haku, nykyisen salasanan tarkistus ja salasanan turvallinen tiivistäminen |
| US-17 | US-01, autentikointi, käyttäjätietojen haku, salasanatiivisteen luonti ja auth_sessions-istuntojen mitätöinti |
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
| US-14 | Käyttäjän omien tukipyyntöjen tallennus, tilat ja niiden lukumäärät |
| US-15 | US-06, rajattu Markdown/TXT-dokumenttikokoelma, avainsanahaku ja tekoälyintegraatio |
| US-16 | Frontendin, backendin ja Ollaman Docker-konfiguraatiot, Compose-palvelut frontendille, backendille, MySQL:lle ja Ollamalle, mallin käyttöönotto, esimerkkikonfiguraatio, pysyvä tallennus, valmiustarkistukset sekä dokumentointi ja käynnistyksen testaus |

Riippuvuudet eivät tarkoita, että kaikki edeltävät käyttäjätarinat on aina saatettava kokonaan valmiiksi ennen seuraavan aloittamista. Teknisiä perustöitä voidaan toteuttaa rinnakkain.

---

## 5. MVP:n rajaus

MVP-version tavoitteena on toteuttaa AI HelpDesk -sovelluksen keskeinen käyttöpolku.

### MVP sisältää seuraavat käyttäjätarinat:

- US-01: Käyttäjän rekisteröityminen
- US-02: Käyttäjän kirjautuminen
- US-03: Käyttäjäprofiilin hallinta (etunimen, sukunimen ja käyttäjänimen muokkaus; sähköpostin näyttäminen vain luettavana; salasanan vaihto nykyisen salasanan vahvistuksella)
- US-04: Tukipyynnön luominen
- US-05: Omien tukipyyntöjen tarkastelu ja sulkeminen
- US-06: Tekoälypohjainen keskustelu
- US-07: Tarkentavat kysymykset ja ongelmanratkaisu
- US-08: Keskusteluviestien tallentaminen
- US-10: REST-rajapinnan käyttäminen
- US-11: Tietojen pysyvä tallentaminen
- US-12: Käyttöliittymän käytettävyys

US-13 ja US-15 toteutetaan MVP:n peruskäyttöpolun jälkeen niille sovituissa Sprint-jaksoissa, mutta ne kuuluvat lopulliseen toimituslaajuuteen. US-09 ja US-14 kuuluvat myös viralliseen toimituslaajuuteen ja toteutetaan Sprint 4:ssä. US-16 toteutetaan Sprint 1:ssä ja sisältää Ollaman sekä valitun mallin. Näitä käyttäjätarinoita ei käsitellä valinnaisina; laajuuden muuttaminen edellyttää erikseen sovittua päätöstä.

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

AI HelpDesk -sovelluksen Product Backlog sisältää 17 käyttäjätarinaa ja niiden arviot ovat yhteensä 88 Story Pointia. US-09 ja US-14 ovat virallisia toimitussitoumuksia. US-14 on rajattu käyttäjän omien tukipyyntöjen kokonaismäärään ja `OPEN`/`CLOSED`-tilajakaumaan. US-15:n RAG MVP käyttää Markdown- ja TXT-dokumentteja avainsanahaulla; semanttista hakua harkitaan vain testinäytön perusteella. US-16:n 5 Story Pointin arvio kattaa dokumentoidun yhden komennon Compose-käynnistyksen frontendille, backendille, MySQL:lle ja Ollamalle valittu malli mukaan lukien. Tuotantokäyttöönotto ja orkestrointi eivät sisälly arvioon.

Backlogin ensimmäinen tavoite on rakentaa toimiva tekninen perusta, toteuttaa käyttäjien tunnistaminen ja tukipyyntöjen hallinta sekä mahdollistaa tekoälypohjainen keskustelu.