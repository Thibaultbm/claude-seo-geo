---
name: seo-audit-pdf
description: "Turn a finished SEO + GEO audit into a client-ready PDF report with a fixed, polished layout. Input: the findings of an audit (usually from seo-geo-audit and the skills it hands off to). Output: one A4 PDF where no block is ever split across two pages, with a verdict, measured strengths, top priorities, every finding by category, an ordered action plan with no dates or delays, what was not verified, and the method. Use when an audit must be sent as a PDF, attached to an email, forwarded to a developer, or when the user asks for an audit report, a PDF audit, or a client deliverable."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# SEO + GEO audit report (PDF)

The audit skills find the problems. This skill packages them into the document the client actually reads, forwards to a developer, and judges the agency on. A correct audit in an ugly or confusing PDF loses the sale: the layout is part of the deliverable.

## Hard rules (a report that breaks one is not sent)

1. **No dates, no delays, no schedule.** Never write when an action will be done or how long it takes: no "week 1", "month 2", "in 3 weeks", "by Q1", no "When" or "Timeline" column, no Gantt, no effort-in-days. Fixes can be shipped very fast today (AI-assisted development, template-level changes), so any delay printed in the report is false and caps the client's ambition. Order replaces dates: the action plan is numbered by impact, and that order is the only sequencing. The only date allowed is the date the audit was run.
2. **Nothing is ever cut across two pages.** Every unit of meaning (a finding, a priority, a KPI row, an action, a section heading with its first block) is atomic: if it does not fit in the space left on the page, it moves whole to the next page. White space at the bottom of a page is fine; a finding split in two is not. The template enforces this with `break-inside: avoid` on every block and `break-after: avoid` on every heading; never put findings in a long `<table>` (rows split badly), use the card components.
3. **Every claim is measured.** Each number comes from the audit data (scripts, browser check, PageSpeed, Search Console, owner data). What was not measured goes in "Not verified", never in the findings.
4. **Writing rules:** language of the site; no em dash (U+2014) or en dash (U+2013), commas, colons or parentheses instead; compact numbers and amounts (3000€, 98/100, 45%); numbered lists written `1.` `2.`; every technical term explained in plain words the first time it appears (the PDF is forwarded to people who are not SEO experts); no acronym left unexplained.
5. **The owner's own recommendations are included.** If the user added recommendations to the email or notes that accompany the audit, they appear in the PDF too, in the right finding and in the action plan, so the email and the PDF never contradict each other.

## Inputs

| Input | Source |
|---|---|
| Findings with status (OK, To fix, Priority) and measured facts | seo-geo-audit, Phase 2 and 3 |
| Scores and speed | `seo_audit.py`, PageSpeed (or the Sorank PageSpeed tool) |
| Site-level counts (orphans, broken links, duplicates) | `site_crawl.py` |
| What a crawler without JavaScript sees | `render_check.py --ua-compare` |
| Accompanying email or notes | the user (read them before writing, rule 5) |

If the audit has not been run yet, run seo-geo-audit first. This skill does not collect data.

## Workflow

1. Copy `assets/report-template.html` to the working folder (for example `audit-<domain>/report.html`).
2. Fill it, keeping the component classes. The structure and what goes in each section are below. Delete the example blocks you do not use; never add inline styles that override the break rules.
3. Render and check:

```
python3 scripts/render_pdf.py audit-<domain>/report.html "audit-<domain>/Audit SEO GEO <domain>.pdf" --png
```

The script prints the PDF with headless Chrome (A4, page numbers in the footer, backgrounds kept), then lints the text: it fails on any dash character, any schedule or delay word (week, month, day, timeline, deadline and their French equivalents), any "When" column, and spaced thousands such as "3 000 €". A legitimate hit inside a measured fact (a case study that says "20000 followers in 2 months") is allowed with `--allow "2 months"`. With `--png` it writes one image per page next to the PDF.

4. Open every page image and check it by eye: no block cut at the bottom of a page, no heading alone at the bottom of a page, no empty page, no text overflowing a card. Fix and render again until clean. Then delete the page images.
5. If the PDF replaces an earlier version, overwrite the same file name, and re-attach it wherever the old one was attached (the email draft keeps the old attachment otherwise).

## Report structure

| # | Section | Component | Content |
|---|---|---|---|
| 1 | Cover band | `.cover` | Domain, one-line definition of SEO and GEO, audit date, scope (pages analysed, pages checked in a browser, competitors) |
| 2 | Verdict | `.verdict` (`.ok`, `.warn` or `.bad`) | One of three: ready to grow, a few corrections first then accelerate, rebuild before investing. One or two sentences why |
| 3 | What is already good | `.kpis` (4 tiles) + `.checklist` | Measured strengths first: credibility, and the reader keeps reading. End with an honest reference point ("better than 90% of the sites we audit") |
| 4 | The priorities | `.prio` cards, 3 to 6 | For each: finding (measured), why it matters, action, expected effect, tags for scope (number of pages) and who does it (developer, writer, owner). No effort in time |
| 5 | Detail by category | `.cat` sections of `.finding` cards | One card per point, with a status pill: `ok` OK, `fix` To fix, `prio` Priority, `watch` To watch, `minor` Minor. Categories in the order of the seo-geo-audit checklist, skipping those that do not apply |
| 6 | Action plan, in order | `.plan` list | Numbered by impact. Each action: what to do, the pages it touches, who does it. No date, no duration, no effort column |
| 7 | Not verified, and method | `.two-col` | What was out of reach and what access would unlock it; how the data was collected |

Keep it readable: the priorities section must be understandable alone by someone who reads nothing else. Group template-level problems ("one fix repairs 142 pages") and say so, because it turns a scary number into good news.

## Design system (already in the template)

- A4, 16 mm margins, footer with the domain and `page / total` on every page.
- One accent color, status colors for pills only (green OK, amber to fix, red priority, blue to watch, grey minor), dark ink on white, soft grey tiles.
- Inter for text (Google Fonts, falls back to the system font offline), tabular figures for numbers.
- Each `h2` section starts with a short lead sentence; the first block after a heading is glued to it.
- `.page-break` forces a new page before a major section when the previous one ends low on the page; use it sparingly, after checking the page images.

## Common mistakes

- Writing a "When" or "Week" column out of habit. The order of the plan is the schedule.
- Putting 20 findings in one `<table>`: rows split across pages and the header repeats badly. Use `.finding` cards.
- Leaving an old PDF attached to the email draft after re-rendering.
- Copying the email text into the PDF verbatim: the email is the summary, the PDF is the detail that a developer can execute.
