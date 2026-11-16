# AI HelpDesk – Project Documentation / Projektidokumentaatio

This directory contains the maintained project documentation in English and Finnish. Both language sets use the same document IDs and cover the same scope.

Tämä hakemisto sisältää ylläpidettävän projektidokumentaation englanniksi ja suomeksi. Kieliversioilla on samat dokumenttitunnisteet ja sama sisältölaajuus.

## Document structure / Dokumenttirakenne

| ID | English | Suomi | Purpose |
|---|---|---|---|
| 00 | [Project Management](en/00-Project%20Management.md) | [Projektinhallinta](fi/00-projektinhallinta.md) | Governance, scope, risks, decisions and change history / Ohjaus, rajaus, riskit, päätökset ja muutoshistoria |
| 01 | [Requirements Specification](en/01-Requirement%20Specification.md) | [Vaatimusmäärittely](fi/01-vaatimusmaarittely.md) | What the system must do / Mitä järjestelmän tulee tehdä |
| 02 | [User Stories & Acceptance Criteria](en/02-User%20Stories%20and%20Acceptance%20Criteria.md) | [Käyttäjätarinat ja hyväksymiskriteerit](fi/02-käyttäjätarinat%20ja%20hyväksymiskriteerit.md) | User-visible behavior and acceptance / Käyttäjälle näkyvä toiminta ja hyväksyntä |
| 03 | [System Design](en/03-System%20Design.md) | [Järjestelmän suunnittelu](fi/03-järjestelmän%20suunnittelu.md) | Architecture, data model, APIs and technical behavior / Arkkitehtuuri, tietomalli, API:t ja tekninen toiminta |
| 04 | [UX/UI Design](en/04-UX%20and%20UI%20Design.md) | [UX/UI-suunnittelu](fi/04-ux-ui-suunnittelu.md) | User journeys, navigation and interface behavior / Käyttäjäpolut, navigointi ja käyttöliittymän toiminta |
| 05 | [Product Backlog](en/05-product%20backlog.md) | [Product Backlog](fi/05-product%20backlog.md) | Prioritized work and estimates / Priorisoidut työt ja arviot |
| 06 | [Sprint Plan](en/06-Sprint%20Plan.md) | [Sprint-suunnitelma](fi/06-sprintin%20suunnitelma.md) | Planned implementation increments / Suunnitellut toteutusjaksot |
| 07 | [Third-Party License Review](en/07-Third-Party%20License%20Review.md) | [Kolmansien osapuolten lisenssiselvitys](fi/07-kolmansien%20osapuolten%20lisenssiselvitys.md) | Dependency, model and distribution terms / Riippuvuuksien, mallien ja jakelun ehdot |
| 08 | [Security & Deployment](en/08-security-deployment-considerations.md) | [Tietoturva ja käyttöönotto](fi/08-tietoturva-ja-kayttoonotto.md) | Current controls, deployment boundaries and remaining risks / Nykyiset kontrollit, käyttöönoton rajat ja riskit |

## Supporting material / Tukimateriaali

- [AI agent description (EN)](en/agents/agent-description.md)
- [Tekoälyavustajan kuvaus (FI)](fi/agents/agentin-kuvaus.md)
- [Project acceptance and verification report](../reports/PROJECT_ACCEPTANCE_REPORT.md) – dated evidence and limitations / päivätty näyttö ja rajaukset

## Documentation authority and maintenance / Dokumentaation auktoriteetti ja ylläpito

- Source code, database migrations, configuration and automated tests define the implemented behavior. Documents describe the agreed product and must be reconciled against implementation.
- Requirements and acceptance criteria define expected behavior; System Design and UX/UI Design explain the solution; Backlog and Sprint Plan organize delivery.
- The document order is an information structure, not a rigid chronological workflow. Backlog refinement, architecture and UX design may evolve iteratively.
- Keep English and Finnish versions semantically aligned. Update both when a change affects their content.
- Record implemented, planned and verified states separately. A test is "passed" only when its execution and result are evidenced.
- Keep detailed test evidence in the report; avoid copying the same long test log into several specification documents. Link to the report instead.
- Decision history belongs in Project Management. Current technical behavior belongs in System Design / UX/UI Design. Avoid maintaining parallel feature specifications that can drift.

- Lähdekoodi, tietokantamigraatiot, asetukset ja automaattitestit määrittävät toteutetun toiminnan. Dokumentit kuvaavat sovittua tuotetta ja ne täsmäytetään toteutukseen.
- Vaatimukset ja hyväksymiskriteerit määrittävät odotetun toiminnan; järjestelmän suunnittelu ja UX/UI-suunnittelu kuvaavat ratkaisun; backlog ja Sprint-suunnitelma järjestävät toimitustyön.
- Dokumenttien järjestys on tiedon jäsentelyä, ei jäykkä aikajärjestys. Backlogin tarkentaminen, arkkitehtuuri ja UX-suunnittelu voivat kehittyä iteratiivisesti.
- Pidä englannin- ja suomenkieliset versiot sisällöllisesti yhdenmukaisina. Päivitä molemmat, kun muutos vaikuttaa niiden sisältöön.
- Erota toteutettu, suunniteltu ja varmennettu tila. Testi merkitään läpäistyksi vain, kun suorituksesta ja tuloksesta on näyttö.
- Säilytä yksityiskohtainen testinäyttö raportissa; älä kopioi samaa pitkää testilokia useisiin määrittelydokumentteihin. Viittaa raporttiin.
- Päätöshistoria kuuluu projektinhallintaan. Nykyinen tekninen toiminta kuuluu järjestelmän suunnitteluun ja UX/UI-suunnitteluun. Vältä rinnakkaisia ominaisuusmäärittelyjä, jotka voivat eriytyä toisistaan.
