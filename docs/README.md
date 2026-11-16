AI HelpDesk is a bilingual (Finnish/English) technical-support web application. Users can ask an AI assistant about IT and software-development issues, manage their own support tickets, and review saved conversations.

# AI HelpDesk – Project Documentation

This directory contains the maintained project documentation in English and Finnish. The two language editions are organized separately below. Each document uses the same ID in both languages and covers the same agreed scope.

## English documentation

| ID | Document | Purpose |
|---|---|---|
| 00 | [Project Management](en/00-Project%20Management.md) | Project objectives, scope, schedule, responsibilities, risks, decisions and change history |
| 01 | [Requirements Specification](en/01-Requirement%20Specification.md) | Functional and non-functional system requirements |
| 02 | [User Stories & Acceptance Criteria](en/02-User%20Stories%20and%20Acceptance%20Criteria.md) | User needs and observable acceptance criteria |
| 03 | [System Design](en/03-System%20Design.md) | Architecture, data model, APIs and technical behavior |
| 04 | [UX/UI Design](en/04-UX%20and%20UI%20Design.md) | User journeys, navigation and interface behavior |
| 05 | [Product Backlog](en/05-product%20backlog.md) | Priorities, estimates and delivery scope |
| 06 | [Sprint Plan](en/06-Sprint%20Plan.md) | Planned implementation increments and sprint goals |
| 07 | [Third-Party License Review](en/07-Third-Party%20License%20Review.md) | Dependency, model and distribution terms |
| 08 | [Security & Deployment](en/08-security-deployment-considerations.md) | Implemented controls, deployment boundaries and remaining risks |

**Additional English material**
- [AI agent description](en/agents/agent-description.md)
- [Project Acceptance and Verification Report](../reports/PROJECT_ACCEPTANCE_REPORT.md) – dated test evidence, limitations and outstanding verification

## Suomenkielinen dokumentaatio

Tämä hakemisto sisältää projektin ylläpidettävän suomenkielisen dokumentaation. Dokumenttien tunnisteet vastaavat englanninkielisiä versioita, ja molemmat kieliversiot kuvaavat samaa sovittua sisältöä.

| ID | Dokumentti | Tarkoitus |
|---|---|---|
| 00 | [Projektinhallinta](fi/00-projektinhallinta.md) | Tavoitteet, rajaus, aikataulu, vastuut, riskit, päätökset ja muutoshistoria |
| 01 | [Vaatimusmäärittely](fi/01-vaatimusmaarittely.md) | Toiminnalliset ja ei-toiminnalliset järjestelmävaatimukset |
| 02 | [Käyttäjätarinat ja hyväksymiskriteerit](fi/02-käyttäjätarinat%20ja%20hyväksymiskriteerit.md) | Käyttäjien tarpeet ja todennettavat hyväksymiskriteerit |
| 03 | [Järjestelmän suunnittelu](fi/03-järjestelmän%20suunnittelu.md) | Arkkitehtuuri, tietomalli, API:t ja tekninen toiminta |
| 04 | [UX/UI-suunnittelu](fi/04-ux-ui-suunnittelu.md) | Käyttäjäpolut, navigointi ja käyttöliittymän toiminta |
| 05 | [Product Backlog](fi/05-product%20backlog.md) | Prioriteetit, arviot ja toimituksen laajuus |
| 06 | [Sprint-suunnitelma](fi/06-sprintin%20suunnitelma.md) | Suunnitellut toteutusjaksot ja sprinttien tavoitteet |
| 07 | [Kolmansien osapuolten lisenssiselvitys](fi/07-kolmansien%20osapuolten%20lisenssiselvitys.md) | Riippuvuuksien, mallien ja jakelun ehdot |
| 08 | [Tietoturva ja käyttöönotto](fi/08-tietoturva-ja-kayttoonotto.md) | Toteutetut kontrollit, käyttöönoton rajat ja jäljellä olevat riskit |

**Suomenkielinen lisämateriaali**
- [Tekoälyavustajan kuvaus](fi/agents/agentin-kuvaus.md)
- [Projektin hyväksyntä- ja testausraportti](../reports/PROJECT_ACCEPTANCE_REPORT.md) – päivätty testausnäyttö, rajoitteet ja avoimet varmennukset

## Documentation authority and maintenance / Dokumentaation auktoriteetti ja ylläpito

- Source code, database migrations, configuration and automated tests define the implemented behavior. Documents describe the agreed product and must be reconciled against the implementation.
- Requirements and acceptance criteria define expected behavior. System Design and UX/UI Design explain the solution. Backlog and Sprint Plan organize the work.
- Test results and verification status have one canonical location: the Project Acceptance and Verification Report. Do not copy detailed test logs into every document.
- When a technical or structural change affects the agreed behavior, update the affected English and Finnish documents together in the same change.
- Lähdekoodi, tietokantamigraatiot, konfiguraatiot ja automaattiset testit määrittävät toteutetun toiminnan. Dokumentaatio kuvaa sovitun tuotteen, ja se on sovitettava toteutukseen.
- Vaatimukset ja hyväksymiskriteerit määrittävät odotetun toiminnan. Järjestelmän suunnittelu ja UX/UI-suunnittelu kuvaavat ratkaisun. Backlog ja Sprint-suunnitelma ohjaavat työn toteutusta.
- Testituloksilla ja varmennuksen tilalla on yksi ensisijainen sijainti: projektin hyväksyntä- ja testausraportti. Yksityiskohtaisia testilokeja ei kopioida jokaiseen dokumenttiin.
- Kun tekninen tai rakenteellinen muutos vaikuttaa sovittuun toimintaan, päivitä kaikki vaikutuksen alaiset suomen- ja englanninkieliset dokumentit samassa muutoksessa.
