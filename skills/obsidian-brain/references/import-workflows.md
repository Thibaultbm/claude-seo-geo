# Import workflows (reference)

Load this when moving the user's existing knowledge into the vault: documents, WhatsApp chats, email, transcripts, spreadsheets. The principle is always the same: one note per source, then route the facts to the domain notes, then make them reachable from the index. A pile of converted files nobody links to is storage, not a brain.

## The general dump (any document)

1. **Collect the pile.** PDFs, slide decks, Word and Excel, sales and podcast transcripts, support and analytics exports, old audits. Claude reads all of these directly; no conversion tool needed.
2. **One note per source** in `sources/`, frontmatter `source`, `date`, `type`, then the content: full text for short documents, a faithful structured summary plus key quotes and exact numbers for long ones. Preserve customer and prospect phrasing verbatim where it appears, it is raw material for keywords and copy.
3. **Route the facts.** Update the domain note the source informs (`company/`, `market/`, `people/`) with what it revealed, linking back to the source note. Routing is the step that turns a document into knowledge.
4. **Update the index** with one line per new note, under the right hub.
5. **Flag conflicts**, do not overwrite. A new deck that contradicts `identity.md` gets both versions dated and a question to the user about which is current.

Priority for a large pile: identity and product docs, then sales transcripts and chats (customer language), then past SEO and analytics, then the rest.

## Multi-agent fan-out (large backlogs)

When the pile is hundreds of files or chats, one session cannot hold it. Fan out:

1. **Partition** the work into batches of 10 to 20 documents, or one batch per domain or per source type.
2. **Spawn one sub-agent per batch**, in parallel. Each sub-agent gets a tight brief: convert its files to `sources/` notes, extract facts in a fixed structure, and return a compact report (notes created, facts found, conflicts). Tell each agent to return data, not prose.
3. **Reconcile centrally.** The main agent collects the reports, routes facts into the domain notes, resolves conflicts across batches (two sources, one truth), and updates the index once at the end.
4. **Keep agents read-or-write-scoped** so two agents do not edit the same domain note at once. Sub-agents write their own `sources/` notes freely; only the main agent edits shared hubs and the index.

This is the same pattern used to convert a few thousand WhatsApp messages or dozens of call transcripts in one pass: parallel extraction, single reconciliation.

## WhatsApp (the high-value, overlooked source)

A founder's WhatsApp holds real client conversations, objections, prices quoted, promises made: the customer language and deal history that exists nowhere else. Getting it into the vault:

1. **Install WhatsApp Desktop** on the computer (or use WhatsApp Web) and sign in, so the chats are readable on the same machine as the vault.
2. **Export the conversations that matter.** WhatsApp's own export is per conversation: open a chat, use Export chat, choose "without media" for a clean text file. Do this for the clients, leads and partners worth keeping; you rarely need all 600 chats, you need the 80 that carry business. For a full archive, a desktop export of the local chat database is possible but heavier; per-chat text export is the reproducible path for most users.
3. **One note per contact** in `people/` (or a `chats/` folder that you then merge), frontmatter `chat`, `type`, `messages`, `first_message`, `last_message`. Body: a dated summary of what the relationship is and where it stands, plus verbatim quotes that carry objections, pricing, or commitments. Do not paste thousands of raw lines; extract the signal.
4. **Merge into the person.** If the contact already has a CRM note, merge the chat into it so there is one note per human, not a chat note and a card living apart. `scripts/person_matches.py` finds these pairs across folders.
5. **Classify** business vs personal as you go, and link each person note from the CRM MOC (business) or the personal index (friends, family).

Large chat archives use the fan-out above: one sub-agent per slice of contacts.

## Email

1. **Get the mailbox readable locally.** Export to an `.mbox` (Apple Mail and Thunderbird both do this), or connect over IMAP. An `.mbox` is plain text Claude reads directly.
2. **Two passes.** A thematic pass (find the threads that carry durable facts: contracts, prices, decisions, intros) and a chronological sweep for completeness. Track which mailboxes are done at the bottom of a sweep note so the next session does not redo them.
3. **Route, do not archive.** A thread becomes a fact in a domain note (a decision, a contact, a number), linked to a `sources/` note only if the raw thread is worth keeping. Most threads leave a one-line fact and no source note.

## Transcripts (sales calls, podcasts, videos)

One note per transcript in `sources/`. Extract, do not store whole: the decisions made, the objections raised (verbatim, they are gold for FAQ and copy), the numbers stated, the customer's own words for what they want. Route objections to `customers.md`, decisions to the relevant rule or decision note. A 60-minute transcript should leave a half-page of routed facts, not a wall of text.

## Spreadsheets and CSV exports

A CSV that is a database (a contact list, a product catalogue) stays as the raw source file, and you build a MOC plus one note per row only for the rows that need narrative (people you have a relationship with, products with a story). Do not explode a 2000-row analytics export into 2000 notes; summarize it in one note and keep the CSV in `sources/`.

## Routing, conflicts, and cross-linking people

- **Routing rule.** The dump is done when the fact is findable from the index, not when the file is converted. Always finish by updating the hub line and the `related` links.
- **Conflicts.** Two sources disagree on a number or a date: keep both, dated, and flag for the user. Never let an import silently overwrite a hand-written fact.
- **One person, one note.** The same human shows up as a WhatsApp contact, a CRM card, and an email sender. Merge to one note, keep the others as redirects or delete them, and link that person from every context they belong to (their company, the deal, the personal index if also a friend). Running `person_matches.py` after each import surface the new duplicates to merge.
- **Secrets never import.** Recovery codes, 2FA seeds, passwords and API keys that appear in documents or chats do not go into the vault. Note that they exist and where the user keeps them (a password manager), never the value.
