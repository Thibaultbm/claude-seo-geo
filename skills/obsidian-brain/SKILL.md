---
name: obsidian-brain
description: "Build a local Obsidian vault that acts as the company and founder second brain, the knowledge layer every other skill reads before acting and writes back to. Input: your raw material (PDFs, decks, transcripts, email, WhatsApp exports, loose notes). Output: a structured, linked vault (domain hubs, maps of content, atomic notes) with read-first/write-back protocols, no orphans, and a single source of truth for numbers. Use when the user mentions Obsidian, a vault, a knowledge base, a second brain, importing documents or transcripts, or wants to give Claude context once instead of repeating it every conversation."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.2.0"
---

# Obsidian Brain: the Company Knowledge Layer

Build and maintain a local Obsidian vault that holds everything the business (and the founder behind it) knows, so every other skill reads real context before acting and writes its work back when done.

The framing: Claude is the uranium, raw reasoning power in unlimited supply. The company's knowledge is what that power runs on. The Obsidian vault is the power plant, the infrastructure that turns the two into compounding output. A model without your facts produces generic advice; the same model on a well-built vault produces output that is specific, consistent across sessions, and smarter every week.

Why Obsidian: it stores plain markdown files on the user's own disk. Markdown is what Claude reads and writes natively, local files keep the data private and portable (no export lock-in), and wiki links turn scattered notes into the entity graph of the business. Any folder of markdown works the same way; Obsidian (https://obsidian.md) is simply the best free tool to browse and edit it.

This skill is the foundation of the kit. The other skills do the SEO and GEO work; this one defines where knowledge lives, how it gets in, and how it stays navigable. Four reference files hold the depth, load them when the matching section says so:

- `references/getting-started.md`: the from-zero on-ramp, install Obsidian, connect the agent, run the first scaffold session. Load this first when the user has no vault or no agent set up yet.
- `references/vault-architecture.md`: the full layered structure, frontmatter conventions per note type, hub and MOC patterns, naming and macOS pitfalls.
- `references/import-workflows.md`: step-by-step import for documents, WhatsApp, email and transcripts, plus the multi-agent fan-out for large backlogs.
- `references/link-audit.md`: how to run and read the two bundled scripts that find broken links, orphans, unreachable notes and duplicate people.

If the user is starting from zero (Obsidian not installed, no vault yet, agent not connected), begin with `references/getting-started.md`: it walks install, connecting the agent to the vault folder, and the first scaffold session in order, then this skill takes over.

## When to use

- Scaffolding a vault from scratch, or restructuring a messy one into a navigable graph.
- Importing the user's pile into the vault: PDFs, decks, sales and podcast transcripts, support and analytics exports, email, WhatsApp chats.
- Connecting Claude to existing knowledge before any real work starts.
- Capturing a durable fact the moment the user states it, so it is never asked for twice.
- Auditing the graph: broken links, orphan notes, notes unreachable from the index, duplicate person notes.
- Logging completed SEO actions at the end of a session (every skill in this kit points here).

Boundaries: this skill builds and maintains the knowledge layer. The SEO and GEO work itself belongs to the other skills (seo-geo-audit to diagnose, content skills to produce, geo-tracking to measure). They read from the vault and write to its log; this skill defines how.

## Architecture: entry points, hubs, then notes

A vault is navigable when an agent can land at the top and reach any fact in one or two link hops, never a full-text search. That requires a strict shape (full detail and an example tree in `references/vault-architecture.md`):

1. **One or two entry points.** A company uses one: `00-INDEX.md`. A founder whose personal life and business are entangled uses two: `00-INDEX.md` (business) and a personal index that links to it. Each entry point holds identity, the canonical numbers (or a link to them), the hard rules, and a map of the vault. Anything else lives one hop away.
2. **Domain hubs.** One hub per domain (admin, finance, product, marketing, content, people, health, and so on). The hub is a pure table of contents for its domain, linked from the entry point.
3. **Maps of content (MOC).** Only for large bases (a CRM, a competitor set, a content-idea swipe file). A MOC is a hub for a folder of many same-shaped notes.
4. **Atomic notes.** One subject per note. Reached from a hub or a MOC, never floating.

Why this shape and not flat folders: token economy. The entry point is the only thing an agent must read in full every session; from there it follows links to the two or three notes a task needs. Flat folders and orphan notes force the agent to grep or read everything, which is slow, expensive, and misses files. The graph is the index.

## The three protocols

### Read first

At the start of any task, locate the vault (a folder of .md notes, usually with a `.obsidian` directory; if unknown, ask once and record the path in the vault). Then:

1. Read the entry point (`00-INDEX.md`, plus the personal index if the task is personal). It maps everything.
2. Follow links to the notes the task needs: identity before writing copy, the numbers note before quoting a figure, the action log before recommending anything.
3. Ground every output in those facts. When the vault answers a question, do not ask the user.

The difference between generic advice and a usable deliverable is context: the right facts, the real voice, and the history of what was already tried. Reading first removes the three biggest sources of wasted sessions: wrong facts, wrong voice, repeated work.

### Capture (write things down as they are said)

When the user states a durable fact, a decision, a number, a contact, a rule, a status change, record it immediately. This is what stops the vault from going stale and stops Claude from asking twice.

1. **Is it durable?** Capture facts that will matter next week, not conversation-only asides. If asked to remember something the code or git history already records, capture instead what was non-obvious about it (the why, the constraint).
2. **Smallest correct home.** Does a note already own this subject? Append a dated line. New subject? Create one atomic note in the right domain. Never open a second note on a subject that already has one.
3. **Concise format.** Frontmatter (`title`, `type`, `updated`, `related`) then the fact in one to three lines. For a decision or a piece of feedback, add a `why` and how to apply it. No prose padding; the vault is read by machines too.
4. **Link on the way in.** Give the note at least one outbound link and make sure at least one note links back to it (add it to its domain hub). A note that nothing points to is invisible.
5. **Numbers have one home.** Live figures (revenue, counts, prices) live in exactly one note. Everywhere else, link to it; never recopy a number, copies drift and the model later quotes the stale one.
6. **Additive and dated.** Append and date changes; never silently rewrite history. If a new fact contradicts an old one, note both with dates and flag it.

### Write back

At the end of any session that changed something (content published, tags fixed, links built, a decision made), append one dated entry to `seo/action-log.md` in the exact format below. The log is what makes session N+1 start where session N ended, and it is the dataset that later correlates actions with ranking and AI-citation changes.

## Vault structure

Scaffold this tree for an SEO and GEO engagement (the SEO-specific filenames below are fixed anchors the rest of the kit reads; the surrounding shape generalizes to any domain per `references/vault-architecture.md`):

```
company-vault/
  00-INDEX.md            Business entry point: identity, numbers, rules, map of the vault
  _INDEX-perso.md        Optional second entry point for personal life, links back to 00-INDEX
  company/
    identity.md          Canonical one-line description, mission, tone, founding facts
    product.md           Offers, features, pricing, differentiators
    customers.md         Personas, real customer language, objections from sales calls
    proof.md             Results, case studies, numbers usable in content
  market/
    competitors.md       One section per competitor: positioning, strengths, links
    keywords-map.md      Keyword to page mapping (from seo-keyword-research)
    prompt-panel.md      The 50-100 buyer prompts tracked monthly (geo-tracking)
  content/
    calendar.md          Planned and in-progress pieces
    published.md         One line per published URL: date, target keyword, status
  seo/
    action-log.md        Dated log of every SEO action taken (format below)
    audits/              One note per audit (seo-geo-audit output lands here)
    experiments.md       Hypotheses being tested, with check-back dates
  people/
    ...                  One note per person (client, lead, partner); merge chat + CRM here
  sources/
    ...                  Converted dumps: one note per source document
```

Rules that keep the vault useful:

| Rule | Why |
|---|---|
| One fact lives in one note; link with [[wikilinks]] elsewhere | Duplicated facts drift apart; links keep one source of truth |
| Every note gets frontmatter: title, type, updated, related | Provenance and relations make facts trustable, updatable, navigable |
| No orphans: every note has at least one inbound and one outbound link | An unlinked note is invisible to navigation and to the agent |
| Bidirectional: if A links B, B (or its hub) links back | One-way links hide half the graph |
| One person, one note: merge the WhatsApp chat and the CRM card | The same human in two files means two half-truths |
| Numbers live in one note; everyone else links to it | Recopied figures drift; the model quotes the stale one |
| Additive updates: append and date, never silently rewrite history | The vault is the company memory; destroyed context never returns |
| No secrets: passwords, API keys, tokens, recovery codes never enter the vault | Notes get synced, shared, pasted into prompts; treat the vault as shareable |

## Importing everything (the dump)

Goal: move everything the company knows into linked markdown. Full procedures, including the WhatsApp path and the parallel fan-out, are in `references/import-workflows.md`; the essentials:

1. **Collect the pile.** PDFs, decks, Word and Excel files, sales and podcast transcripts, support and analytics exports, email, WhatsApp chats, old audits. Claude reads all these formats directly.
2. **One note per source** in `sources/` with frontmatter (`source`, `date`, `type`) and the content: full text for short documents, a faithful structured summary with key quotes and numbers for long ones. Keep customer phrasing verbatim, it is raw material for keywords and copy.
3. **Route the facts.** Update the relevant `company/`, `market/` or `people/` note with what the source revealed, linking back to the source. A dump is done when its facts are findable from the entry point, not when the file is converted.
4. **Update the index** with one line per new note, under the right hub.
5. **Flag conflicts** instead of overwriting: if a new deck contradicts `identity.md`, note both versions with dates and ask which is current.

**WhatsApp** is the highest-value and most-overlooked source: install WhatsApp Desktop on the computer so the chats are readable locally, export conversations, and write one note per contact, then merge each into that person's existing CRM note so there is a single note per human. Exact steps in `references/import-workflows.md`.

**Large backlogs** (hundreds of files or chats): fan out. Run one sub-agent per batch or per domain in parallel, each converting and routing its slice, then reconcile and update the index once. The fan-out pattern and batch sizing (10-20 documents, or one domain per agent) are in the reference.

Priority order for a big pile: identity and product docs first, then sales transcripts and chats (customer language), then past SEO work, then everything else.

## Maintaining the graph (link audit)

A vault decays: renamed notes leave broken links, imports land orphans, duplicates creep in. Run the audit periodically (after any big import, and on request). Two bundled standard-library scripts, detailed in `references/link-audit.md`:

- `scripts/link_graph.py <vault>`: lists broken wikilinks, orphan notes (no inbound link), notes unreachable from the entry point, and duplicate basenames. A healthy vault returns zero of the first three.
- `scripts/person_matches.py <vault>`: finds the same person across folders (chat vs CRM vs contacts) so duplicates can be merged into one note.

The fix playbook (repair broken links, link orphans into their hub, merge duplicate people, normalize relative links) is in the reference. Record the audit as an entry in the action log.

## The SEO action log (exact format)

Append entries to `seo/action-log.md`, newest first:

```markdown
## 2026-06-10
- Skill: seo-content-blog
- Action: published "how to choose a commercial coffee machine" targeting "commercial coffee machine for cafe"
- Pages: /blog/commercial-coffee-machine-guide (new), /products/pro-line (3 internal links added)
- Expected effect: rank for the long-tail set within 8-12 weeks, lift /products/pro-line
- Check on: 2026-08-10
```

One entry per action, every field every time. The `Check on` date is what `experiments.md` and future sessions sweep to verify whether actions worked.

## GEO layer

The vault is not just operational memory; it directly serves AI visibility:

- The canonical one-line description in `company/identity.md` is the single string reused verbatim on the site, LinkedIn, review platforms and directories. Entity consistency is what lets models state facts about the brand with confidence (the why and the workflow live in geo-visibility).
- `market/prompt-panel.md` holds the buyer prompts whose answers are tracked monthly (geo-tracking). Keeping the panel in the vault makes the measurement reproducible across sessions and people.
- The action log plus monthly tracking results form the only dataset that can answer "did our GEO work move citations": actions dated on one side, mention rates dated on the other.
- Customer language captured from transcripts and chats feeds the question-form headings and FAQ answers that AI engines extract (seo-content-blog, geo-visibility).

## Output format

When scaffolding a vault, deliver: the created tree (folders and notes actually written, index filled in), each `company/` and `market/` note drafted from available sources with explicit `TODO` markers where facts are missing, a batched dump plan for the user's pile, and the empty `seo/action-log.md` with its format at the top.

When dumping files, deliver: the notes created in `sources/`, the notes updated, conflicts flagged, and the index diff.

When auditing, deliver: the script output, the list of fixes applied, and a log entry.

When logging a session, deliver: the exact log entry appended, quoted back to the user.

## Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Dumping files without routing the facts | A folder of summaries nobody reads is storage, not a brain | Route facts to the company/, market/ and people/ notes |
| Duplicating facts (especially numbers) across notes | Versions drift; the model quotes the stale one | One fact, one note, link everywhere else |
| Leaving imported notes as orphans | Unreachable from the index, invisible to the agent | Link every note into its hub on the way in |
| The same person in a chat note and a CRM card | Two half-records of one human | Merge into one note per person (person_matches.py finds them) |
| Treating the vault as write-only | Context exists but never grounds the work | Read-first, every session |
| Skipping the action log | Next session re-recommends what was already done | One entry per action, every time |
| Storing credentials in notes | Vaults get synced and pasted into prompts | Secrets live in a password manager, never in markdown |
| One giant note for everything | Retrieval pulls the whole blob or nothing | Short notes, descriptive titles, linked from a hub |

## Cross-references

- seo-geo-audit: audit outputs land in `seo/audits/`; the audit reads `company/` notes for business context.
- seo-keyword-research: produces `market/keywords-map.md` and feeds `market/prompt-panel.md`.
- geo-visibility: consumes the canonical description from `company/identity.md` for entity consistency.
- geo-tracking: runs the monthly panel from `market/prompt-panel.md` and stores results next to the action log.
- seo-content-blog and the other content skills: read `company/` and `customers.md` for voice and facts, log published pieces to `content/published.md` and the action log.

## Sources

- Obsidian: https://obsidian.md (free for personal and commercial use, local markdown files)
- The architecture, protocols, import workflows, linking rules and audit are field practice from building and maintaining AI-assisted knowledge vaults (2024-2026), labeled as practice, not measured studies.
