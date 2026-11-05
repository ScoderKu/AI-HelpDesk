# AI HelpDesk — Account Access and Password Recovery

- **Document ID:** KB-PROJECT-11
- **Status:** verified from `backend/app/main.py`, `backend/app/admin.py`, `backend/tests/test_admin_password_reset.py`, and README on 2026-11-05
- **RAG Scope:** project-specific
- **Applies to:** password change, forgotten password, and administrator-assisted reset
- **Keywords:** forgot password, forgotten password, password reset, password recovery, unohdin salasanani, unohtunut salasana, salasanan palautus, salasanan nollaus

## If a user forgot their password / Jos käyttäjä on unohtanut salasanansa

If someone says “I forgot my password”, “how do I reset my password”, “unohdin salasanani”, “olen unohtanut salasanani”, or asks for “salasanan palautus” or “salasanan nollaus”, explain that the current application has no public self-service reset page, public reset API, email recovery, or one-time-code flow. The AI assistant cannot reset an account. The user should contact an authorized helpdesk administrator through the organization's approved channel and complete identity verification outside the AI chat. Do not ask the user to share a password, temporary password, one-time code, or unnecessary personal information in chat.

Jos käyttäjä on unohtanut salasanansa, hän ei voi käyttää tavallista salasanan vaihtoa ilman nykyistä salasanaa. Sovelluksessa ei ole julkista itsepalveluna toimivaa salasanan palautussivua, palautusrajapintaa, sähköpostipalautusta tai kertakäyttökoodia. Tekoälyavustaja ei voi palauttaa tai vaihtaa salasanaa. Käyttäjän tulee ottaa yhteyttä organisaation valtuutettuun helpdesk-ylläpitäjään hyväksytyn asiointikanavan kautta ja varmentaa henkilöllisyytensä sovitun käytännön mukaisesti. Käyttäjä ei saa lähettää salasanaa, väliaikaista salasanaa tai kertakäyttökoodia tekoälykeskusteluun.

After an administrator-assisted reset, the user signs in with a temporary password, changes it before using other protected features, then signs in again with the new password. If the user is already signed in and knows the current password, they can use the profile's password-change form instead.

Ylläpitäjän tekemän palautuksen jälkeen käyttäjä kirjautuu väliaikaisella salasanalla, vaihtaa sen ennen muiden suojattujen toimintojen käyttöä ja kirjautuu vielä uudelleen uudella salasanalla. Jos käyttäjä on jo kirjautunut sisään ja muistaa nykyisen salasanansa, hän voi vaihtaa salasanan profiilin salasananvaihtolomakkeella.

## Authorized operator procedure / Valtuutetun ylläpitäjän toiminta

Only an authorized operator with access to the protected backend/Docker environment can perform the reset, using the documented backend maintenance command in README. The command generates a temporary password, stores only its hash, invalidates the user's existing sessions, and prints the temporary password once after the database transaction succeeds. Deliver it only through a separately verified secure channel. Never put it in chat, tickets, email, command-line arguments, files, or logs. Re-running the command creates a new temporary password and invalidates the previous one.

Vain suojattuun backend-/Docker-ympäristöön oikeutettu ylläpitäjä voi tehdä palautuksen README-ohjeen mukaisella backendin ylläpitokomennolla. Komento tallentaa vain väliaikaisen salasanan tiivisteen, mitätöi käyttäjän aiemmat istunnot ja tulostaa väliaikaisen salasanan yhden kerran vasta tietokantatransaktion onnistuttua. Salasana toimitetaan käyttäjälle erikseen varmennetun turvallisen kanavan kautta. Sitä ei saa kirjoittaa chattiin, tikettiin, sähköpostiin, komentoriville, tiedostoon tai lokiin. Komennon uusi suoritus luo uuden väliaikaisen salasanan ja mitätöi edellisen.

Do not tell an ordinary end user to run the maintenance command or imply that the AI has performed the reset. Direct the user to the authorized administrator; keep operational details for verified operators.
