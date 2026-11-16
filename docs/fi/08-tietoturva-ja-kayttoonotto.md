# Tietoturva ja käyttöönoton huomioitavat asiat

## 1. Tarkoitus ja rajaus

Tämä dokumentti kuvaa AI HelpDesk -opiskelijaprojektin tietoturvan nykytilaa sekä käyttöönoton rajoja. Siinä erotetaan lähdekoodissa toteutetut kontrollit tulevan LAN- ja WAN-käytön suosituksista. Dokumentti ei ole penetraatiotestausraportti, tietoturvasertifikaatti eikä väite OWASP-vaatimusten täydellisestä täyttymisestä.

Projektin laajuus säilyy itsepalveluna toimivana tukipalveluna: käyttäjätili, kirjautuminen, profiili, omat keskustelut, AI-avusteinen neuvonta ja käyttäjän omat tukipyynnöt. Projektiin ei lisätä ylläpitäjä-, tukihenkilö- tai roolipohjaista käyttöoikeusmallia.

## 2. Käyttöympäristöt

| Ympäristö | Käyttötarkoitus | Tietoturvan tila |
|---|---|---|
| Paikallinen kehitys/demo | Kehittäjän kone ja luokkademo | Nykyinen Compose-kokoonpano on tarkoitettu kehityskäyttöön. Frontend käyttää Viten kehityspalvelinta. Paikallinen HTTP vaatii asetuksen `AUTH_COOKIE_SECURE=false`; tätä ei pidä käyttää HTTPS-ympäristössä. |
| Yksityinen LAN | Tuleva käyttö luotetuista lähiverkon laitteista | Ei vielä tuettu tai varmennettu tuotantokäyttö. Edellyttää tuotantobuildattua frontendia, HTTPS-käänteisvälityspalvelinta, luotetun proxyn tarkistusta, palomuurisääntöjä ja laite-/verkkotason hallintaa. |
| Julkinen WAN | Internetin kautta käytettävä palvelu | Ei tuettu eikä tietoturvan osalta validoitu. Vaatii erillisen tuotantokäyttöönoton arvioinnin, suojatun reunainfrastruktuurin, valvonnan, varmistukset, palautussuunnitelman ja jatkuvan päivitysprosessin. |

Kehityspalvelinta tai hallintaliittymiä ei pidä julkaista suoraan Internetiin.

## 3. Sovelluksessa olevat kontrollit

- Palvelinpuolen kirjautumisistunnot tallennetaan MySQL:ään. Selaimen istuntoeväste on HMAC-allekirjoitettu, voimassa enintään kahdeksan tuntia ja käyttää `HttpOnly`- sekä `SameSite=Lax`-asetuksia; `Secure` on konfiguroitavissa.
- Salasanat tallennetaan scrypt-tiivisteinä käyttäjäkohtaisilla satunnaisilla suoloilla. Olemassa olevia parametreja ei muuteta, jotta vanhat salasanatiivisteet säilyvät yhteensopivina.
- Kirjautumisyrityksiä rajoitetaan Redisillä IP-osoitteen ja normalisoidun käyttäjätunnuksen perusteella.
- Rekisteröitymisyrityksiä rajoitetaan IP-osoitteen perusteella (5 yritystä tunnissa). Redis-virhe estää rekisteröinnin sen sijaan, että rajoitus ohitettaisiin.
- Istuntoevästeen sisältävät vaaralliset API-pyynnöt tarkistetaan täsmällistä sallittujen frontend-alkuperien listaa vasten. Kirjautuminen ja rekisteröityminen on rajattu tämän istuntoon perustuvan tarkistuksen ulkopuolelle.
- AI-generointi sarjoitetaan Redis-pohjaisella globaalilla lukolla, jota chat ja tukipyyntöluonnoksen generointi käyttävät. Varattu kapasiteetti palauttaa uudelleenyritykseen ohjaavan vastauksen sen sijaan, että paikallista mallia kuormitettaisiin rinnakkaisilla generoinneilla.
- Yksityisille versionoiduille API-vastauksille asetetaan `Cache-Control: no-store`.
- API-vastaukset saavat perustason selaimen tietoturvaotsakkeet: `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` ja rajoittava `Permissions-Policy`.
- CORS rajataan määritettyihin frontend-alkuperiin sekä sovelluksen tarvitsemiin metodeihin ja otsakkeisiin.
- Tukipyyntöjen ja keskustelujen tietokantakyselyt rajataan tunnistetun käyttäjän omistukseen. Kaikille resurssireiteille tulee ylläpitää kahden käyttäjän IDOR-regressiotestit.

## 4. Paikallisen Docker Compose -ympäristön verkkorajaukset

Nykyinen Compose-kokoonpano sitoo frontendin, backendin, phpMyAdminin ja Ollaman host-portit loopback-osoitteeseen (127.0.0.1). MySQL ja Redis eivät julkaise host-portteja. Tämä sopii yhden koneen paikalliseen demoon, mutta ei yksinään muodosta LAN/WAN-tuotantoarkkitehtuuria.

Pidä MySQL, Redis ja Ollama Dockerin sisäisissä verkoissa. Älä julkaise niiden portteja lähiverkkoon tai Internetiin. phpMyAdmin on tietokannan hallintapinta: pidä se pois käytöstä paikallisen kehityksen ulkopuolella tai rajaa se erilliseen hallintaverkkoon/-laitteeseen HTTPS:n ja vahvojen käyttörajoitusten taakse.

Backend luottaa välitettyihin asiakas-IP-osoitteisiin vain erikseen määritetyiltä proxy-osoitteilta tai -verkoilta. Älä lisää `TRUSTED_PROXY_IPS`-asetukseen laajaa tai käyttäjän hallitsemaa verkkoaluetta. Varmista, että todellinen reverse proxy käyttää määritettyä lähdeosoitetta ja korvaa välitysotsakkeet sen sijaan, että luottaisi sokeasti asiakkaan lähettämiin arvoihin.

## 5. Ennen LAN-käyttöönottoa

Ennen kuin sovellus avataan muiden laitteiden käyttöön:

1. Rakenna frontend tuotantobuildiksi ja tarjoa staattiset tiedostot; älä käytä Viten kehityspalvelinta.
2. Aseta sovelluksen eteen ylläpidetty reverse proxy ja pakota HTTPS kelvollisella sertifikaatilla.
3. Aseta `AUTH_COOKIE_SECURE=true` ja määritä `FRONTEND_ORIGINS` sisältämään täsmälliset HTTPS-alkuperät, myös skeema ja portti.
4. Aseta `TRUSTED_PROXY_IPS` vastaamaan täsmällistä proxy-osoitetta/-verkkoa ja varmista asiakas-IP:n välitys toiselta LAN-laitteelta.
5. Sido julkinen kuuntelu vain tarkoitettuun LAN-verkkoliitäntään ja estä palomuurilla muut saapuvat portit.
6. Pidä MySQL, Redis, Ollama ja phpMyAdmin poissa asiakaslaitteiden ulottuvilta.
7. Käytä yksilöllisiä, vahvoja salaisuuksia ja tietokantatunnuksia; pidä `.env` pois versionhallinnasta ja vaihda mahdollisesti paljastuneet tunnukset.
8. Testaa erillisiltä laitteilta kirjautuminen, uloskirjautuminen, rekisteröinnin rajoitus, cross-origin-pyynnöt, istunnon vanheneminen, salasanan vaihto, tukipyyntöjen ja keskustelujen omistajuus sekä AI-kuormitustilanne.

Nämä ovat LAN-käyttöönoton vaatimuksia, eivät väitteitä jo suoritetusta LAN-testauksesta.

## 6. Ennen WAN-käyttöönottoa

Internet-julkaisu vaatii erillisen uhkamallin ja käyttöönoton tietoturvakatselmoinnin. Vähimmäisvaatimuksia ovat:

- Tuotantokäyttöön soveltuva reverse proxy ja tarvittaessa WAF, TLS-asetukset, pyyntökoon ja yhteyksien rajat sekä tiukat palomuurisäännöt.
- Vain HTTPS-sovelluksen sisääntulopiste julkaistaan. MySQL:ää, Redisiä, Ollamaa, phpMyAdminia, Docker-socketia tai sisäisiä palveluportteja ei julkaista.
- Interaktiiviset API-dokumentaatio- ja skeemapäätepisteet poistetaan käytöstä tuotannossa, ellei niille ole dokumentoitua tarvetta ja erillistä pääsynrajausta.
- Kontit ajetaan vähimmillä tarvittavilla oikeuksilla; käytetään ei-root-käyttäjiä, vain luku -tiedostojärjestelmiä, rajattuja Linux-ominaisuuksia ja resurssirajoja silloin kun mahdollista.
- Tuotantokuvat kiinnitetään versioihin tai digest-tunnisteisiin ja Python-/JavaScript-riippuvuudet lukitaan. Päivityksille määritetään ylläpitoprosessi.
- Käyttöön otetaan keskitetty lokitus, tietoturvatapahtumien valvonta, hälytykset, tietosuojan huomioiva säilytysaika ja poikkeamatilanteiden toimintamalli. Salasanoja, istuntoevästeitä, Authorization-otsakkeita tai tarpeettomasti yksityisiä keskusteluja ei kirjata lokeihin.
- MySQL-varmuuskopiot suojataan ja salataan, niiden käyttöoikeudet rajataan ja palautus testataan säännöllisesti.
- Määritetään väärinkäytösten hallinta, saatavuustavoitteet, palautumistavoitteet ja operatiivinen vastuutaho.
- Tehdään riippumaton tietoturva-arviointi ja varmennetaan käyttöoikeus-/IDOR-polut, CSRF-suojaus, käyttörajat, palvelunestohyökkäysten torjunta ja salaisuuksien käsittely.

## 7. Tunnetut rajoitteet ja varmennettavat asiat

Seuraavia asioita ei voida pitää valmiina pelkästään siksi, että edellä kuvatut kontrollit ovat lähdekoodissa:

- LAN-käytön päästä päähän -testaus kahdella fyysisellä laitteella ja suunnitellulla reverse proxyllä.
- Kahden käyttäjän täydellinen IDOR-testimatriisi kaikille tukipyyntö-, keskustelu-, viesti- ja retry-reiteille.
- Tuotantokonttien ei-root-käyttö, vain luku -tiedostojärjestelmä, capability-rajoitukset ja resurssirajat.
- Täysin lukitut riippuvuudet ja kiinnitetyt konttikuvat.
- OpenAPI/Redoc/skeemapäätepisteiden poistaminen käytöstä tuotannossa.
- Lopullisen tuotantofrontendin kanssa yhteensopiva Content Security Policy.
- Pyyntörungon kokorajat sekä reverse proxyssä että ASGI-tasolla.
- AI-lukon, ylikuormitusvastauksen, asiakasyhteyden katkeamisen ja Ollaman aikakatkaisujen kuormitustestaus.
- Tietoturvalokien katselmointi, varmuuskopion palautusharjoitus ja poikkeamatilanteen harjoittelu.
- Muodollinen penetraatiotestaus tai riippumaton varmennus.

## 8. Tietoturvan viitekehys

OWASP ASVS 5.0.0 soveltuu tarkistuslistaksi, kun projektia laajennetaan tai se siirretään luokkademoa laajempaan käyttöön: https://owasp.org/www-project-application-security-verification-standard/ ja https://asvs.owasp.org/.

ASVS on tässä viitekehys, ei sertifiointiväite. Soveltuvat vaatimukset valitaan todellisen käyttöympäristön uhkamallin perusteella. Tason 2 vaatimustenmukaisuutta ei pidä väittää ilman vaatimusten järjestelmällistä tarkistamista ja näyttöä.
