# WIP: porting the Figma master wireframe into the skills

Working document for the `claude/website-audit-skills-8zm9pm` branch. Delete before merge.

## Goal

The Figma (`MasterWireFrame`) holds the house page templates: which sections every page type must have, and which elements go inside each section. It is not readable by an agent (private file, no Figma connector, WebFetch returns 403). Port it into the skills so that anyone auditing a site with this kit gets told which pages and which blocks are missing, and gets the missing content written for them.

Not building an audit product yet. Audit output only, for now.

## State: done and pushed

Commit `ee19069` plus the archetype pass.

**New skill `seo-page-sections`** ("what is missing on this page"):

- `SKILL.md`: 5 phases (archetype and page type, detect, grade, write the missing blocks, deliver). Two output formats: build brief for practitioners, client checklist for owners. The client checklist works on sites that cannot be crawled (noindex, staging, behind a login), which is the Stephen case.
- `references/site-archetypes.md`: the 3 archetypes and their page inventories, block lists for 10 archetype-specific page types, header and footer house rules, the 6 marketing levers. Built from the 5 screenshots received.
- `references/page-type-matrix.md`: required / recommended / optional blocks, in page order, with the reason for each, for 11 core page types, plus a universal baseline.
- `references/section-library.md`: how to BUILD each block (minimum bar, how to write it, schema, failure modes). This is what lets Claude write the missing FAQ instead of only naming the gap.
- `references/transverse-pages.md`: fill-in wireframes for homepage, pricing, about, contact.
- `scripts/section_audit.py`: zero-dependency detector, reports which blocks are present in raw HTML with the evidence per verdict, FR and EN. Tested on fixtures only (outbound network is blocked in the session).

**New skill `seo-content-comparison-page`**: X vs Y, alternatives, best-for, and customer segment pages. Page-family demand mapping, criteria-selection method, the honesty rules that make a comparison citable, EU comparative advertising conditions, maintenance cycle.

**Wiring**: `seo-geo-audit` hands off to both and states the altitude split (site health vs page blocks). README, AGENTS.md, plugin manifests updated to 17 skills, version 1.2.0. `python3 scripts/validate_skills.py` passes.

## What the screenshots established

Three archetypes, not one flat list of page types:

| Archetype | Page types in the Figma |
|---|---|
| Shopify store | Home, Collection, Produit, Article, Blog, A propos, Contact, Affiliation, 404 |
| Webflow / WordPress | Home, Collection, Service, Article, Blog, Call, Page Auteur, Outil HTML, A propos, Contact, Wall Of Love, Affiliation, 404 |
| Marketplace | Home, Collection, Service, Reference, Login/Signup, TOP 10 |

Plus a `Base SEO + CRO` board: Header / Footer rules, and the 6 marketing levers (reciprocite, coherence, preuve sociale, sympathie, autorite, rarete).

Header rules read off the wireframe: fixed-size logo in a block link to home; drop the explicit Home link when the header has under 5 links; dropdown once a category holds more than 3 pages; contact link mandatory; strong-colored CTA to the call or quote page; "Pilliers" exposed in the nav.

Footer rules: fixed-size logo in a block link to home; pillar page links mandatory, grouped by subject under column headings; social links with `nofollow noreferrer noopener`; links to the legal pages.

## What is still open

1. **Per-page section detail.** Only the zoomed-out board views were legible. The individual frames (the stack of sections inside Home, Produit, Service, Collection, Article, Blog, Call, Page Auteur, Outil HTML, Wall Of Love, Affiliation, Reference, TOP 10) have not been read. The block lists currently in the skills come from what the repo already knew plus established practice, not from the Figma frames. Reconcile them: what the Figma has in addition, what it lacks that is marked R, what diverges.
2. **Comparison and segment pages are not in the Figma yet.** They were built from established patterns. The original plan was to add them to the Figma; the skills now hold the spec, so the Figma can follow from the skills rather than the reverse.
3. **The detector has never run against a live site.** Outbound network is blocked in this environment. Run `python3 skills/seo-page-sections/scripts/section_audit.py <url>` on a few real client sites and tune the keyword sets in `KW` from the false positives and negatives.
4. **Languages.** The detector covers FR and EN. Any other market degrades to "not found", which reads as a false negative.
5. **Two calls to confirm.** FAQ is marked required on 8 of 11 core page types. Price as HTML text is required everywhere a price exists.
6. **Stephen deliverable** (noindex site, needs a checklist to implement himself): use `seo-page-sections` Format B. Not yet produced.

## To resume in a fresh conversation

Paste this:

> Repo `claude-seo-geo`, branch `claude/website-audit-skills-8zm9pm`. Read `WIP-figma-to-skills.md` first, then `skills/seo-page-sections/references/site-archetypes.md` and `page-type-matrix.md`. I am uploading the detailed Figma frame screenshots for {page types}. Reconcile the block lists in the skills with what the frames actually show: add what the Figma has and the skills lack, flag what the Figma lacks that is marked R, and ask me about anything that diverges. Do not create a PR.
