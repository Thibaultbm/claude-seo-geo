---
name: seo-geo-audit
description: Runs a complete SEO + GEO audit of any website, covering technical health, tags, images, site architecture, content, keywords, e-commerce, local, backlinks, and AI visibility (ChatGPT, Perplexity, Google AI Overviews), then delivers a prioritized action plan or a plain-language summary. Use this skill whenever the user gives a URL and wants to know what to improve, asks to audit or review a site, asks why a site does not rank or never gets mentioned by AI assistants, wants to compare a site against competitors, or asks "what is wrong with my site" or "is my site ready for SEO". Also use it to establish a baseline before any larger SEO project. After the audit, hand off deep work to the specialized skills (seo-technical, seo-content-blog, seo-backlinks, geo-visibility, geo-tracking).
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Full SEO + GEO site audit

Audit a website the way a senior practitioner does: collect verifiable facts first, judge them against a field-tested checklist, benchmark against the competitors that actually rank, and deliver a short list of fixes ordered by impact. The methodology was distilled from 115+ real agency audit calls and updated with sourced 2025-2026 evidence on AI search.

## Why this audit is different

1. Facts before judgment. Every claim in the final report must trace back to something measured (by the bundled script, a browser check, or data the owner provided). Never guess a title length or assume a sitemap exists.
2. Competitors over abstract thresholds. "Your page has 400 words" means nothing alone. "The three sites outranking you average 1200 words on this query" is a finding. When competitors are known, benchmark page versus page.
3. Two search worlds at once. Every category is checked twice: does it help Google rankings, and does it help the site get retrieved and cited by ChatGPT, Perplexity and Google AI Overviews. These overlap but do not coincide (AI Mode answers show only about 32 percent URL overlap with the top 10 organic results).

## When to use

- The user provides a URL and wants improvement points, an audit, a review, or a "check".
- A site does not rank, lost traffic, or is invisible in AI assistant answers.
- The user wants a comparison against one or more competitors.
- A baseline is needed before content production, a migration, or a redesign.

## Inputs to gather

Ask only for what is missing; proceed with what exists:

| Input | Required | Note |
|---|---|---|
| Homepage URL | yes | The script also discovers robots.txt, sitemap, llms.txt |
| 1-2 key pages | recommended | Top service, product or article page |
| Competitor URLs | recommended | Enables page-versus-page benchmarking |
| Goals and market | helpful | Local vs national, language, business model |
| GSC / GA4 access | optional | Indexation ratio and traffic facts; otherwise ask the owner for screenshots |

## Phase 1: collect the facts

Run the bundled collector on the homepage plus key pages, and on each competitor page cited later in the report:

```
python3 scripts/seo_audit.py https://example.com /services /blog/top-article
```

It returns, per page: HTTP status, HTTPS, platform fingerprint, title (with generic-title flag), meta description length, full heading hierarchy with level jumps, image alt coverage and weight sample, internal versus external link counts, Open Graph, canonical, JSON-LD types, visible word count, meta robots, and a `likely_js_rendered` flag. Site-wide: robots.txt rules for AI search bots and AI training bots (separately), sitemap declaration and URL count, llms.txt presence.

Known limits, and what to do about each:

| Limit | Fallback |
|---|---|
| `likely_js_rendered: true` (client-side site) | Open the page in a browser to read the real content, and report that AI crawlers cannot see it (they do not execute JavaScript, see seo-technical) |
| Images loaded as CSS backgrounds | Invisible to the parser (total may read 0); verify visually |
| Real-world speed | Ask the user to run https://pagespeed.web.dev (free, no key) on mobile and desktop and share scores |
| Backlink profile | Use GSC Links report or Bing Webmaster Tools if available; paid indexes (Ahrefs, Semrush, Moz) only as an option |
| GSC indexation ratio, Google Business Profile | Ask the owner; never invent these numbers |

## Phase 2: analyze against the checklist

Read `references/audit-checklist.md` now. It contains the full 14-category checklist with thresholds, detection methods, and the reason behind each rule. Work through it in this order, skipping categories that do not apply to the site type:

| # | Category | Applies to |
|---|---|---|
| 1 | Method and framing | all |
| 2 | Tags (title, meta, headings, slugs) | all |
| 3 | Images | all |
| 4 | Performance and indexation | all |
| 5 | Architecture (one intent = one page) | all |
| 6 | Content volume | all |
| 7 | Keywords and intent | all |
| 8 | Blog and articles | sites with a blog (or that need one) |
| 9 | GEO (AI visibility) | all |
| 10 | Conversion signals | all |
| 11 | E-commerce (products, collections) | stores |
| 12 | Backlinks and mentions | all |
| 13 | Local (Google Business Profile) | local businesses |
| 14 | Migration risks | sites about to change domain, CMS or structure |

While analyzing:

- Classify each finding as OK, Fix, or Blocking. A Blocking finding (noindex on the whole site, client-rendered content, hacked pages) invalidates work on everything downstream; say so plainly.
- Count what can be counted ("23 of 31 images have no alt text"), because numbers make the report credible and actionable.
- Identify the 3 highest-impact fixes. Resist listing 40 equal-weight items: the owner will do nothing with that. The philosophy is that SEO compounds many small gains (roughly "1 percent per action", a field heuristic), but the report must still rank them.

## Phase 3: the GEO layer

For the same pages, evaluate AI visibility specifically:

1. Crawler access: from the script output, report blocked AI search bots (these remove the site from AI answers) separately from blocked training bots (a brand-visibility tradeoff, see the canonical table in seo-technical references/ai-crawlers.md).
2. Rendering: if content only exists after JavaScript runs, ChatGPT, Claude and Perplexity cannot read it. This single finding outranks everything else in the GEO section.
3. Citability: score the key pages against the 5-pillar rubric in geo-visibility (answer-first passages, stats and quotes with sources, tables and lists, question headings, E-E-A-T signals, structured data, descriptive slugs).
4. Entity: search the brand name; check that name, one-line description and key facts match across the site, LinkedIn, review platforms and directories.
5. Measurement baseline: note whether the site can even see its AI traffic today (GA4 channel setup), and point to geo-tracking.

## Phase 4: deliver

Read `references/output-templates.md` and pick the format:

- Template A, full audit report: for practitioners; verdict line, what is good, top 3 priorities, findings by category with OK / Fix / Blocking status, ordered action plan.
- Template B, plain-language email: for non-technical owners; no acronyms, every term explained in everyday words, progress acknowledged, honest verdict.

Rules for both: write in the language of the site, open with what is genuinely good (credibility, and most sites do several things right), keep the verdict honest even when it is "rebuild before investing in content", and state explicitly what was not verified and why.

## Handoffs after the audit

| Finding | Skill to apply the fix |
|---|---|
| Crawl, speed, indexation, JS rendering, AI bot access | seo-technical |
| Wrong or missing keywords, cannibalization | seo-keyword-research |
| Weak or thin articles | seo-content-blog |
| Product page issues | seo-content-product-page |
| Service pages missing or merged | seo-content-service-page |
| Category pages with no content | seo-content-collection-page |
| Orphan pages, weak internal links | seo-internal-linking |
| Missing or invalid structured data | seo-schema-markup |
| Weak link profile, no brand mentions | seo-backlinks |
| Local visibility, reviews, GBP | seo-local |
| Low AI citation rate | geo-visibility |
| No AI traffic measurement | geo-tracking |

## Common mistakes

- Auditing only the homepage. Money pages and one article reveal more than the homepage alone.
- Reporting thresholds without competitors. The gap is the finding, not the absolute number.
- Treating GEO as a separate mystical discipline. Most GEO failures found in audits are SEO failures (not indexed, client-rendered, thin content) wearing a new name.
- Inventing data. If speed, backlinks or indexation were not measured, write "not verified" instead of guessing.
- Burying the verdict. The first line of the deliverable answers: is this site ready to grow, does it need a short fix list, or does it need a rebuild first.

## Sources

- AI Mode versus top 10 organic overlap (32 percent URL overlap): https://www.semrush.com/blog/ai-mode-comparison-study/
- AI crawlers do not execute JavaScript (500M+ fetch analysis): https://vercel.com/blog/the-rise-of-the-ai-crawler
- Why ChatGPT cites pages (1.4M prompt study): https://ahrefs.com/blog/why-chatgpt-cites-pages/
- Generative Engine Optimization (controlled study, KDD 2024): https://arxiv.org/abs/2311.09735
- Google guidance on AI features and structured data: https://developers.google.com/search/docs/appearance/ai-features
