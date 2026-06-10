---
name: obsidian-brain
description: Sets up and maintains a local Obsidian vault as the company's second brain, so every SEO and GEO skill in this kit works from real company knowledge instead of guesses. Covers the vault structure for a business (identity, product, customers, competitors, keywords), the dump workflow that converts PDFs, decks, transcripts and docs into linked markdown notes, the read-first protocol (Claude pulls context from the vault before acting), and the SEO action log updated at the end of every session. Use this skill whenever the user mentions Obsidian, a vault, a knowledge base, a second brain, connecting Claude to company data or docs, dumping company files for AI, centralizing business knowledge, or asks how to give Claude context about their company, or why Claude keeps asking for facts they already wrote down. Also use it at the start of any SEO engagement to scaffold the vault, and at the end of sessions to log actions. For the SEO work itself, hand off to the other skills in this kit.
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Obsidian Brain: the Company Knowledge Layer

Build and maintain a local Obsidian vault that holds everything the business knows, so that every other skill in this kit reads real company context before acting and writes its actions back when done.

The framing: Claude is the uranium, raw reasoning power in unlimited supply. Company knowledge is what that power runs on. The Obsidian vault is the power plant, the infrastructure that turns the two into compounding output. Uranium without a plant produces nothing usable; a model without your company's facts produces generic SEO advice. The vault is what makes the output specific, consistent across sessions, and smarter every week.

Why Obsidian specifically: it stores plain markdown files on the user's own disk. Markdown is the format Claude reads and writes natively, local files mean the company's data stays private and portable (no export lock-in), and Obsidian's wiki links turn scattered notes into the entity graph of the business. Any folder of markdown notes works the same way; Obsidian (https://obsidian.md) is simply the best free tool to browse and edit it.

## When to use

- Setting up a knowledge vault for a business from scratch (or restructuring a messy one).
- Dumping company files into the vault: PDFs, pitch decks, sales call transcripts, podcast and video transcripts, support ticket exports, analytics exports, old audits.
- Connecting Claude to existing company knowledge before SEO work starts.
- Logging completed SEO actions at the end of a session (every skill in this kit points here).
- Answering "how do I give Claude the context about my company once, instead of repeating it every conversation".

Boundaries: this skill builds and maintains the knowledge layer. The SEO and GEO work itself belongs to the other skills (seo-geo-audit to diagnose, content skills to produce, geo-tracking to measure). They read from the vault and write to its log; this skill defines how.

## The two protocols every skill follows

### Read first

At the start of any task, detect the vault: look for a folder of .md notes, typically with a .obsidian directory, in or near the working directory, or ask the user where their vault lives (then remember it in the vault itself). If a vault exists:

1. Read `00-INDEX.md` first: it maps the vault.
2. Read the notes relevant to the task: brand identity before writing copy, keywords map before choosing targets, action log before recommending anything already tried.
3. Ground every output in those facts. When the vault answers a question, do not ask the user.

Why: the difference between generic advice and a usable deliverable is context. A vault that holds the canonical brand description, the real customer language from call transcripts, and the history of what was already attempted removes the three biggest sources of wasted sessions: wrong facts, wrong voice, repeated work.

### Write back

At the end of any session that changed something (content published, tags fixed, links built, settings changed), append one entry to `seo/action-log.md` using the exact format below. Never skip this: the log is what makes session N+1 start where session N ended, and it is the dataset that later correlates actions with ranking and AI citation changes.

## Vault structure

Scaffold this tree (adapt names to the company's language; keep the shape):

```
company-vault/
  00-INDEX.md            The map: what lives where, one line per note
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
  sources/
    ...                  Converted dumps: one note per source document
```

Rules that keep the vault useful:

| Rule | Why |
|---|---|
| One fact lives in one note; link with [[wikilinks]] elsewhere | Duplicated facts drift apart; links keep one source of truth |
| Every note gets frontmatter: source, date, type | Provenance makes facts trustable and updatable |
| Plain language, short notes, descriptive titles | The vault is read by humans and machines; clever titles defeat both |
| Additive updates: append and date, never silently rewrite history | The vault is also the company memory; destroyed context never comes back |
| No secrets: passwords, API keys, tokens never enter the vault | Notes get synced, shared, and pasted into prompts; treat the vault as shareable |

## The dump workflow

Goal: move everything the company knows into linked markdown, in one pass per batch of files.

1. Collect the pile: PDFs, slide decks, Word and Excel files, sales call transcripts, podcast and video transcripts, support exports, analytics exports, old audits and reports. Claude reads all of these formats directly.
2. For each document, create one note in `sources/` with frontmatter (`source`, `date`, `type`) and the extracted content: full text for short documents, a faithful structured summary plus key quotes and numbers for long ones. Keep customer phrasing verbatim where it appears: real language is raw material for keywords and copy.
3. Route the facts: update the relevant `company/` or `market/` note with what the source revealed, linking back to the source note. The dump is not done when the file is converted; it is done when its facts are findable from the INDEX.
4. Update `00-INDEX.md` with one line per new note.
5. Flag conflicts instead of overwriting: if a new deck contradicts `identity.md`, note both versions with dates and ask the user which is current.

Batch sizing: 10-20 documents per session keeps quality high. For a large backlog, prioritize in this order: identity and product docs, sales call transcripts (customer language), past SEO work, everything else.

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
- Customer language captured from transcripts feeds the question-form headings and FAQ answers that AI engines extract (seo-content-blog, geo-visibility).

## Output format

When scaffolding a vault, deliver:

1. The created tree (folders and notes actually written, with the INDEX filled in).
2. For each `company/` and `market/` note: the content drafted from available sources, with explicit `TODO` markers where facts are missing and the user must fill in.
3. A dump plan for the user's file pile: batches, priority order, where each batch will land.
4. The empty `seo/action-log.md` with the format documented at the top.

When dumping files, deliver: the list of notes created in `sources/`, the `company/` and `market/` notes updated, conflicts flagged, and the INDEX diff.

When logging a session, deliver: the exact log entry appended, quoted back to the user.

## Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Dumping files without routing the facts | A folder of summaries nobody reads is storage, not a brain | Step 3 of the dump workflow: route facts to company/ and market/ notes |
| Duplicating facts across notes | Versions drift; the model quotes the stale one | One fact, one note, links everywhere else |
| Treating the vault as write-only | Context exists but never grounds the work | The read-first protocol, every session |
| Skipping the action log | Next session re-recommends what was already done | One entry per action, every time |
| Storing credentials in notes | Vaults get synced and pasted into prompts | Secrets live in a password manager, never in markdown |
| Rewriting history during updates | The company memory loses its memory | Append and date; flag conflicts instead of overwriting |
| One giant note for everything | Retrieval pulls the whole blob or nothing | Short notes, descriptive titles, linked from the INDEX |

## Cross-references

- seo-geo-audit: audit outputs land in `seo/audits/`; the audit reads `company/` notes for business context.
- seo-keyword-research: produces `market/keywords-map.md` and feeds `market/prompt-panel.md`.
- geo-visibility: consumes the canonical description from `company/identity.md` for entity consistency.
- geo-tracking: runs the monthly panel from `market/prompt-panel.md` and stores results next to the action log.
- seo-content-blog and the other content skills: read `company/` and `customers.md` for voice and facts, log published pieces to `content/published.md` and the action log.

## Sources

- Obsidian: https://obsidian.md (free for personal and commercial use, local markdown files)
- The read-first and write-back protocols, vault shape, and batch sizes are field practice from running AI-assisted SEO engagements on local knowledge bases (2024-2026), labeled as practice, not measured studies.
