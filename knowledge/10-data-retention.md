# AI HelpDesk — Data Retention

- **Document ID:** KB-PROJECT-10
- **Status:** verified from `backend/app/main.py`, `backend/tests/test_session_cleanup.py`, and README on 2026-11-05
- **RAG Scope:** project-specific
- **Applies to:** scheduled deletion of closed tickets and inactive conversations
- **Keywords:** data retention, retention period, deletion, closed ticket, inactive conversation, tietojen säilytys, säilytysaika, poistaminen, suljettu tukipyyntö, passiivinen keskustelu

## Retention rules / Tietojen säilytyssäännöt

The daily background task permanently deletes eligible closed tickets after three calendar months, using `tickets.closed_at` as the cutoff field. It permanently deletes inactive conversations after three calendar months without activity, using `conversations.updated_at` as the cutoff field. These are calendar months, not fixed periods of 30, 60, or 90 days. There are no `DELETE_TICKET_AFTER_DAYS` or `DELETE_CHAT_AFTER_DAYS` settings in the current implementation.

Suljettuja tukipyyntöjä ja passiivisia keskusteluja säilytetään kolme kalenterikuukautta ennen poistamista. Suljetut tukipyynnöt poistetaan pysyvästi, kun `closed_at`-aikaleimasta on kulunut kolme kalenterikuukautta. Passiiviset keskustelut poistetaan pysyvästi, kun `updated_at`-aikaleimasta on kulunut kolme kalenterikuukautta ilman toimintaa. Kyse ei ole 7, 30 tai 90 päivän kiinteästä ajasta, eikä nykyisessä toteutuksessa ole asetuksia `DELETE_TICKET_AFTER_DAYS` tai `DELETE_CHAT_AFTER_DAYS`.

If a conversation is linked to an open ticket, it is retained. It is also retained while a linked ticket has not yet reached that ticket's own three-calendar-month retention cutoff. When an eligible conversation is deleted, its messages are deleted with it. Deletion is permanent and is not an archive or undo operation.

Jos keskustelu liittyy avoimeen tukipyyntöön, keskustelu säilytetään. Keskustelu säilytetään myös silloin, kun siihen liittyvän tukipyynnön oma kolmen kalenterikuukauden säilytysaika ei ole vielä täyttynyt. Kun keskustelu voidaan poistaa, myös sen viestit poistetaan. Poisto on pysyvä eikä tietoja voi palauttaa arkistosta.

## Finnish test wording / Suomenkieliset hakulauseet

Questions such as “Kuinka kauan suljettuja tukipyyntöjä ja passiivisia keskusteluja säilytetään ennen poistamista?”, “Kuinka monta kuukautta tukipyyntö säilytetään?” and “Poistetaanko keskustelu, jos siihen liittyy avoin tukipyyntö?” refer to this policy. Answer in the user's language and do not invent day-based environment variables.
