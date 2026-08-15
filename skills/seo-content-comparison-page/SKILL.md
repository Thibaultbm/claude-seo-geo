---
name: seo-content-comparison-page
description: "Build the bottom-funnel pages that capture buyers at the decision moment: 'X vs Y', 'alternatives to X', 'best X for Y', and audience or segment pages ('for agencies', 'for freelancers'). Input: your product or service, the competitors or segments to cover, and the market. Output: the page plan (which comparisons deserve a page, URL and keyword mapping), the full page structure, a verified feature comparison table, per-use-case verdicts, an honest limitations block, the FAQ, and the schema. Use when planning or writing comparison, versus, alternatives, best-for or segment landing pages, when competitors rank for your own brand plus alternatives, or when AI assistants recommend competitors instead of you on comparison prompts."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Comparison, alternatives and segment pages

The last page a buyer reads before deciding. Someone searching "X vs Y" or "alternatives to X" has already accepted the category and is choosing a supplier, which makes these the highest-intent pages a site can own. They are also the format AI assistants reach for when asked to recommend something, because a page that compares options and concludes is directly usable as an answer, while a page that only praises itself is not.

Two rules make or break the whole category. The comparison must be verifiably true on the day it is published, and it must concede where a competitor genuinely wins. A page that wins every row is discounted by readers and by models, which destroys exactly the credibility the page exists to create.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read it before writing: the real feature set, real pricing, the competitors that actually come up in sales calls, the objections buyers raise, and the segments the business already serves. Comparison pages assert facts about third parties, so unsourced invention is both a credibility and a legal risk. Log the pages produced to the vault's SEO action log, including the date each comparison was verified, since that date drives the refresh cycle. Structure and protocols: the obsidian-brain skill.

## When to use

- Planning or writing a "X vs Y", "alternatives to X", "best X for Y" or segment page.
- Competitors, review sites or affiliates rank for "{your brand} alternatives" and you do not.
- ChatGPT, Perplexity or AI Overviews recommend competitors on comparison prompts.
- A product serves several distinct customer types and the site has one generic page for all of them.
- A category page exists but never concludes, so it converts nothing.

## Phase 1: decide which pages deserve to exist

Do not build one page per competitor by default. Build the pages the market actually searches, then let the rest be sections inside them.

| Page family | Query pattern | Build when | Intent |
|---|---|---|---|
| Head-to-head | "{you} vs {competitor}", "{competitor} vs {you}" | The competitor is named in sales calls, or the query has real volume | Deciding between two finalists |
| Your alternatives | "{you} alternatives", "alternative to {you}" | You have any brand recognition | Retention: own the page where doubts are answered |
| Their alternatives | "{competitor} alternatives", "alternative to {competitor}" | The competitor is bigger than you | Acquisition: the single highest-yield page family for a challenger |
| Best-for | "best {category} for {use case}", "best {category} {year}" | You are credible in a niche of the category | Category-level shortlisting |
| Comparison hub | "{category} comparison" | Three or more of the above exist | Distributes authority, prevents cannibalization |
| Segment | "{category} for {audience}" | A segment has distinct problems, vocabulary or workflow | Recognition and qualification |

Mapping rules:

1. One comparison, one URL. "X vs Y" and "Y vs X" are the same page; pick one URL and be consistent everywhere. Do not create both.
2. Do not build a head-to-head page for a competitor nobody searches. Make it a row in the alternatives page instead.
3. "{competitor} alternatives" pages outperform "{you} vs {competitor}" pages for a challenger brand, because the searcher has already decided to leave the competitor and is open, rather than defending a preference.
4. Segment pages must differ by more than find and replace. Test: could a reader from segment A tell, in the first paragraph, that the segment B page was not written for them? If not, merge them.
5. Keep the URL literal and stable: `/{you}-vs-{competitor}/`, `/{competitor}-alternatives/`, `/for-agencies/`. The slug is a retrieval signal, and these pages accumulate links over years.

Verify the demand with seo-keyword-research before committing, and check which existing page already ranks for the term to avoid cannibalizing it.

## Phase 2: gather verifiable facts

Every claim about a third party must be checkable on that third party's own public material, on the day you write it.

| Fact | Acceptable source | Never |
|---|---|---|
| Pricing | The competitor's public pricing page, dated | A number a salesperson remembers |
| Features | The competitor's docs, pricing page, changelog | Assumption from their marketing copy |
| Limits and quotas | Their published limits or terms | Inference |
| Support and SLA | Their published terms | Anecdote |
| User sentiment | Named review platforms, quoted and linked | Invented complaints |
| Your own facts | Your product, the vault, the owner | Aspiration |

Record, per row, where it was verified and when. That record becomes the methodology block on the page and the input to the refresh cycle. If a fact cannot be verified, write "not published" in the cell. An honest gap reads as rigor; a guess that turns out wrong destroys the page.

For anything about a competitor that is disputable, prefer their words to your paraphrase: quote and link.

## Phase 3: build the page

Read `references/comparison-page-patterns.md` now. It carries the fill-in wireframes for each page family, the criteria-selection method, the verdict formulas, and the segment page structure.

The block list, levels and page order live in `seo-page-sections/references/page-type-matrix.md`, sections 5 and 6. Non-negotiables:

1. **Verdict in the first 100 words.** Who each option is for, stated plainly. This is the passage that gets quoted. A page that makes the reader scroll to learn the conclusion forfeits the citation to a page that does not.
2. **A real HTML comparison table.** Not an image, not divs styled as a table. Same criteria for every option, in the same order.
3. **Criteria the buyer decides on**, not the criteria you win. Choose them before looking at who wins each one.
4. **At least one row where a competitor genuinely wins**, stated without hedging. This is the credibility mechanism of the entire page, and the reason a model will treat the page as a source rather than as marketing.
5. **Your own limitations, in your own words**, in a named block. The alternative is a reader finding them on a review site, where you control nothing.
6. **Pricing as HTML text**, with the date checked, for every option.
7. **Best-for verdicts per use case.** One page then answers many query variants: "best for solo", "best for teams", "best on a budget".
8. **Methodology and date.** What was compared, how, when, by whom. Provenance is what separates a quotable comparison from a promotional one.
9. **FAQ including the uncomfortable questions**: "is X actually better", "can I migrate", "why is X cheaper", "what is the catch".
10. **Zero em dashes.** Never leave an em dash (U+2014) or an en dash (U+2013) in copy that goes live on a client site. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text, and on a page whose whole value is being trusted over a competitor's marketing, reading as machine output is the one thing it cannot afford. The rule covers the verdict, the table cells, the FAQ, the methodology block, the metadata and the schema strings. Sweep for both characters before delivery. Hyphens in compound words and ranges written with "to" are untouched.

## Phase 4: stay legal and stay honest

Comparative advertising is lawful across the EU under Directive 2006/114/EC, and in most markets, but only under conditions that happen to match what makes a comparison page work: it must not be misleading, it must compare goods meeting the same needs, it must compare features that are material, relevant, verifiable and representative, and it must not denigrate the competitor or create confusion between brands. Check the rules of the market being written for before publishing.

Practical translation:

- Compare like with like. Comparing your top plan against a competitor's free tier is both dishonest and outside the safe harbor.
- Every claim must be verifiable by a reader from public sources. Link them.
- Use the competitor's name and mark descriptively, to identify them, not in a way that suggests endorsement or affiliation. Do not use their logo as if it were a partnership.
- No denigration. State the difference, not a judgment of their competence.
- Do not misrepresent an old version as current. Date the comparison.
- If the comparison sits on an affiliate or review page, disclose the commercial relationship.

Honesty is also the GEO mechanism here, not only the legal one. Models weight pages that state limitations and cite sources, and a page whose every row favors its author reads as promotional to a reader and to a retrieval system alike.

## Phase 5: maintain, or take it down

Comparison pages decay faster than any other page type, because they depend on facts you do not control. A page claiming a competitor lacks a feature they shipped last year is worse than no page: it is the first thing a competitor's sales team screenshots.

| Trigger | Action |
|---|---|
| Every quarter | Re-verify every price and every feature row; update the date |
| Competitor ships a major feature | Update the affected rows within days |
| Your own pricing or feature set changes | Update every comparison page at once |
| The comparison can no longer be maintained | Retire the page and redirect it, rather than leaving it stale |

Put the verification date on the page and in the vault log. Track the pages in geo-tracking: comparison pages are where AI citation share moves first and most visibly.

## Common mistakes

- Winning every row. The fastest way to lose the credibility the page exists to build.
- Never concluding. "It depends on your needs" forfeits the answer to whoever does conclude.
- Comparing on your strengths. Criteria must be chosen from what buyers decide on, before checking who wins.
- Building a page per competitor regardless of demand. Thin near-duplicate pages compete with each other and none of them ranks.
- Segment pages produced by find and replace. Same page, swapped noun, split signal, nothing ranks.
- Stale facts with no date. Undated comparison claims are unusable to a careful reader and to a model.
- Comparison as an image. The most extractable block on the page, rendered unextractable.
- Ignoring "{your brand} alternatives". Someone will own that page; it should be you.

## Handoffs

| Need | Skill |
|---|---|
| Which comparisons have real demand | seo-keyword-research |
| Which blocks the page is missing | seo-page-sections |
| Product facts for your own side | seo-content-product-page |
| Service scope and pricing presentation | seo-content-service-page |
| Linking the comparison hub to its children | seo-internal-linking |
| Schema for the page and its FAQ | seo-schema-markup |
| Getting cited on comparison prompts | geo-visibility |
| Tracking citation share on those prompts | geo-tracking |
| Earning links to the comparison hub | seo-backlinks |

## Sources

- Directive 2006/114/EC on misleading and comparative advertising (conditions under which comparison is lawful in the EU): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32006L0114
- Why ChatGPT cites pages (1.4M prompt study): https://ahrefs.com/blog/why-chatgpt-cites-pages/
- Generative Engine Optimization: statistics, quotations and citations raise visibility (controlled study, KDD 2024): https://arxiv.org/abs/2311.09735
- AI Mode versus top 10 organic overlap (32 percent URL overlap): https://www.semrush.com/blog/ai-mode-comparison-study/
- Google guidance on AI features and structured data: https://developers.google.com/search/docs/appearance/ai-features
- Google structured data policies (markup must match visible content): https://developers.google.com/search/docs/appearance/structured-data/sd-policies
