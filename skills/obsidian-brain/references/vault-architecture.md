# Vault architecture (reference)

Load this when scaffolding a vault from scratch, restructuring a messy one, or deciding where a new note belongs. The goal of the shape is one thing: an agent lands at the top and reaches any fact in one or two link hops, never a full-text search.

## The four levels

```
Entry point  ->  Domain hub  ->  Map of content (MOC)  ->  Atomic note
(1 or 2)         (one per         (only for large           (one subject
                  domain)          same-shaped bases)         per note)
```

1. **Entry point.** The only file read in full every session. Holds: identity, the canonical numbers (or a link to the one note that owns them), the hard rules of the project, and a linked map of every hub. Keep everything else one hop away; the entry point is a switchboard, not a container.
2. **Domain hub.** One per domain. A pure table of contents: one line per note in the domain, each line a wikilink plus a few words on what the note is for. The hub is linked from the entry point and links back to it.
3. **Map of content (MOC).** Only when a domain contains a large base of same-shaped notes (a CRM of hundreds of people, a competitor set, a swipe file of content ideas). The MOC is the hub for that folder: it groups and links the notes (by tier, stage, theme). Small domains skip this level and link notes straight from the hub.
4. **Atomic note.** One subject. Reached from a hub or a MOC, never floating.

## One entry point or two

- **A company** uses one entry point, `00-INDEX.md`.
- **A founder whose personal life and business are entangled** uses two: `00-INDEX.md` (business) and a personal index (health, home, family, personal finance). The two link to each other. The reason is access, not separation: a business question enters by the business door, a personal one by the personal door, and neither has to wade through the other. The notes can still link across freely (a personal contact who is also a client links both ways).

Never go past two entry points. More than two and nothing is the top anymore.

## Frontmatter conventions

Every note opens with YAML. Keep keys consistent across the vault so they are queryable. Minimum by note type:

```yaml
# index / hub / MOC
---
title: Marketing
type: index            # index | hub | moc
updated: 2026-06-12
related: "[[00-INDEX]], [[Content]], [[Competitors]]"
---

# reference / fact note
---
title: Brand identity
type: reference
updated: 2026-06-12
related: "[[00-INDEX]], [[Product]]"
---

# person (client, lead, partner)
---
title: Jane Doe
type: person
status: customer       # lead | customer | partner | churned
last_contact: 2026-06-10
related: "[[CRM]], [[Acme Corp]]"
---

# source (an imported document)
---
title: Q2 sales deck
type: source
source: q2-sales-deck.pdf
date: 2026-04-01
related: "[[Product]], [[Proof]]"
---

# rule / decision / feedback
---
title: No calls, self-serve funnel
type: decision
updated: 2026-05-22
related: "[[Funnel]]"
---
```

Notes:

- `related` lists the 2 to 5 nearest notes and makes the graph explicit (Obsidian also shows automatic backlinks, but an explicit `related` is what an agent reads). Quote the whole value when it contains commas.
- A `decision` or `feedback` note adds, in the body, a `Why:` line and a `How to apply:` line. Capturing the reason is what makes the rule reusable later.
- Dates are absolute (`2026-06-12`), never "yesterday" or "next month". An agent reading the note in three months has no other anchor.

## Hub pattern

A hub is a switchboard, not a document. Example:

```markdown
---
title: Admin
type: index
updated: 2026-06-12
related: "[[00-INDEX]], [[_INDEX-perso]]"
---

# Admin

> Navigation: [[00-INDEX|Business index]] | [[_INDEX-perso|Personal index]]

## Company and legal
- [[Company registration]] : entity id, tax number, bank, invoicing rules
- [[Shareholders agreement]] : split, vesting, who signed what

## Finance
- [[Financial plan]] : revenue, cash, runway (the single source for all figures)
```

Each line is a wikilink and a one-clause purpose. No content lives in the hub itself.

## MOC pattern

For a base of many notes. The MOC groups them so none is an orphan and the set is browsable:

```markdown
---
title: CRM (MOC)
type: moc
updated: 2026-06-12
related: "[[Marketing]]"
---

# CRM (MOC)

## Customers (paying)
- [[Jane Doe]] | Acme Corp | since 2026-03
- [[John Smith]] | Beta LLC | since 2026-05

## Leads (in pipeline)
- [[Mary Major]] | demo booked
```

When a base grows past a few hundred notes, generate the MOC from the folder rather than hand-maintaining it, and regenerate it after big imports.

## Twin notes

Sometimes one real thing legitimately has two notes from two angles (a competitor that is both a profile and a crawled-sitemap record; a person who is both a customer and an industry figure). Do not force a merge if the angles are genuinely different, but link them as twins in both directions and say so in one line, so a reader knows the other half exists. If the two notes are the same angle, they are a duplicate, merge them (see link-audit).

## Single source of truth for numbers

Live figures (revenue, subscriber counts, prices, dates that change) live in exactly one note, the one that owns that domain (a financial plan, a pricing note). Every other note that needs the figure links to that note instead of restating it. Restated numbers drift the moment one copy is updated, and the model then quotes whichever copy it read. The entry point may show a dated snapshot for convenience, but it must say which note is canonical and that the snapshot is not.

## Naming and macOS pitfalls

- **Wikilink-hostile characters in filenames.** `#`, `[`, `]`, `|`, `^` break or confuse wikilinks. Keep them out of note titles; write `n1` not `#1`, `(2025)` not `[2025]`.
- **Trailing spaces** in filenames (a frequent export artifact) make links fragile. Strip them.
- **Unicode normalization (macOS).** The filesystem stores names decomposed (NFD), most tools compare composed (NFC). When matching link targets to files in a script, normalize both to NFC, or accented titles appear "missing" when they exist.
- **Relative wikilinks** like `[[../Admin/Note]]` are brittle. Prefer the full vault-root path `[[Admin/Note|Note]]`, or a unique basename, so a moved note does not break the link.
- **Descriptive titles, not clever ones.** The title is read by humans and machines; "Q2 revenue model" beats "the money map".

## Example: a founder-led company vault

A realistic generalized shape (business plus personal, two entry points):

```
vault/
  00-INDEX.md                 Business entry point
  _INDEX-perso.md             Personal entry point
  business/
    Admin.md                  hub
    Marketing.md              hub
    Product.md                hub
    admin/
      Company registration.md
      Financial plan.md       (single source for all figures)
      Shareholders agreement.md
    marketing/
      CRM (MOC).md            moc -> hundreds of person notes
      Competitors (MOC).md    moc
      crm/ ...                person notes
      competitors/ ...        competitor notes
    rules/
      No em dashes.md         decision/rule notes the agent must follow
      Brand voice.md
  personal/
    Health.md                 hub
    Home.md                   hub
    health/ ...
    home/ ...
  people/                     one note per human, chat + CRM merged
  sources/                    one note per imported document
```

Adapt the folder names to the user's language and domains; keep the shape: two entry points at most, a hub per domain, a MOC per large base, atomic notes underneath, everything reachable from the top.
