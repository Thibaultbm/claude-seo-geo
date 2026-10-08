---
name: seo-content-comparison-page
description: "Spec, audit, competitor benchmark and build for the bottom-funnel pages that capture buyers at the decision moment: 'X vs Y', 'alternatives to X', 'best X for Y', the comparison hub, and audience or segment pages ('for agencies', 'for freelancers'). Runs four phases: the CMP spec with stable IDs on top of the common page spec, an audit of the existing page with seo_audit.py and section_audit.py, a benchmark against the comparison and alternatives pages that rank on the query (review sites, affiliate lists, the competitors' own vs pages) with page_benchmark.py, then the build: which comparisons deserve a page, URL mapping, a comparison table with sourced and dated competitor facts, the verdict, honest limitations, segment pages that are not find-and-replace, FAQ, schema and the acceptance re-run. Use when planning, auditing or writing comparison, alternatives, best-for or segment pages, when competitors rank for your brand plus alternatives, or when AI assistants recommend competitors on comparison prompts."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "2.0.0"
---

# Comparison, alternatives and segment pages

The last page a buyer reads before deciding. Someone searching "X vs Y" or "alternatives to X" has already accepted the category and is choosing a supplier: the highest-intent pages a site can own, and the format AI assistants reach for when asked to recommend, because a page that compares and concludes is directly usable as an answer.

Two rules make or break the category. The comparison must be verifiably true on the day it is published, and it must concede where a competitor genuinely wins. A page that wins every row, or that states last year's facts, is discounted by readers and by models alike.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read it before writing: the real feature set, real pricing, the competitors that actually come up in sales calls, the objections buyers raise, and the segments the business already serves. Comparison pages assert facts about third parties, so unsourced invention is both a credibility and a legal risk. Log the pages produced to the vault's SEO action log, including the date each comparison was verified, since that date drives the refresh cycle. Structure and protocols: the obsidian-brain skill.

## When to use

- Planning, auditing or writing a "X vs Y", "alternatives to X", "best X for Y", comparison hub or segment page.
- Competitors, review sites or affiliates rank for "{your brand} alternatives" and you do not.
- ChatGPT, Perplexity or AI Overviews recommend competitors on comparison prompts.
- A product serves several distinct customer types and the site has one generic page for all of them.
- A category page exists but never concludes, so it converts nothing.
- An existing comparison page is more than a quarter old, or a competitor changed its pricing or shipped a feature.

| Need | Skill |
|---|---|
| Which comparisons have real demand | seo-keyword-research |
| Which blocks the page is missing, on any page type | seo-page-sections |
| Product facts for your own side | seo-content-product-page |
| Service scope and pricing presentation | seo-content-service-page |
| Linking the comparison hub to its children | seo-internal-linking |
| Schema for the page and its FAQ | seo-schema-markup |
| Getting cited on comparison prompts | geo-visibility |
| Tracking citation share on those prompts | geo-tracking |
| Earning links to the comparison hub | seo-backlinks |

## Phase 1. The spec

Common requirements C-01 to C-26: skills/seo-geo-audit/references/common-page-spec.md

The rows below are what a comparison or segment page adds on top of them. Thresholds are field heuristics from agency audits unless marked measured. Levels follow `seo-page-sections/references/page-type-matrix.md` sections 5 and 6: every row is required unless its Threshold says "recommended" or "optional".

### Comparison, alternatives, best-for and hub pages (`section_audit.py --type comparison`)

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| CMP-01 | The page earns its URL: one comparison, one URL; built for a query with demand or a competitor named in sales calls | "X vs Y" and "Y vs X" share one URL; no second page already ranking for the term | manual (seo-keyword-research, Search Console) | Near-duplicate comparison pages cannibalize each other and none ranks |
| CMP-02 | Literal, stable slug per family (extends C-23) | `/{you}-vs-{competitor}/`, `/{competitor}-alternatives/`, `/best-{category}-for-{use-case}/`, `/compare/`; never changed once it ranks | url_hygiene, manual | The slug is a retrieval signal, and these pages accumulate links over years |
| CMP-03 | Title and H1 name both sides, or the brand plus "alternatives", exactly as searched (extends C-01, C-03) | exact query phrasing in both; title adds the deciding difference or the year | h1_missing, title_short, title_long, manual | Exact-match queries; the H1 must match the phrasing |
| CMP-04 | Verdict in the first 100 words: who each option suits, in a concrete situation | first 100 words; names names; a number where possible; repeated at the end | section_audit "verdict_block", kw_not_in_intro, manual | The passage an assistant quotes; burying it forfeits the citation |
| CMP-05 | Real HTML comparison table | `<table>`, 6-12 criteria, same criteria in the same order for every option; never an image or styled divs | section_audit "comparison_table", page_benchmark "tables" | The single most extractable block on the page |
| CMP-06 | Criteria chosen from buyer decision factors, before scoring | ordered by influence on the decision; includes total cost, migration effort, contract terms where relevant | manual | Criteria picked after scoring bend toward your strengths and read as rigged |
| CMP-07 | At least one row where a competitor genuinely wins | 1+ row, stated without hedging | manual | The credibility mechanism of the whole page |
| CMP-08 | Your own limitations, in your own words, in a named block | 1 H2 block, 2+ specific limitations | manual | Otherwise a review site states them, where you control nothing |
| CMP-09 | Pricing of every option as HTML text, with the date checked | every option, same plan tier compared, "verified {date}" | section_audit "price_in_text", "pricing_block", manual | The most compared dimension, and the fastest to go stale |
| CMP-10 | Best-for verdicts per option or per use case | 1 per option or 3+ use cases, plus "choose neither if" | section_audit "verdict_block", manual | One page answers many intent variants |
| CMP-11 | Per-option detail sections | one H2 per option, same criteria in the same order | heading_jumps, manual | Jagged criteria read as bias |
| CMP-12 | Every competitor fact sourced from the competitor's own public material, linked and dated | 100% of third-party rows; unverifiable cells read "not published"; disputable claims quoted, not paraphrased | manual (verification log) | A wrong fact about a competitor is a legal risk and the page's fastest credibility loss |
| CMP-13 | Methodology block | what was compared, on which plans, how, when, by whom, from which sources | manual | Provenance separates a quotable comparison from a promotional one |
| CMP-14 | Visible publication date and last verification date, in the page and in `dateModified` | verification no older than one quarter | section_audit "freshness_signal", date_missing, manual | Undated comparison claims are unusable to a careful reader and to a model |
| CMP-15 | Author with credentials and demonstrable experience of the options compared, linked to an author page with real profiles (C-20) | named author, credentials, Person with `sameAs` | section_audit "author_block", author_missing, author_page_link, social_placeholder | E-E-A-T on a page whose whole value is judgment |
| CMP-16 | FAQ including the uncomfortable questions | 3+ questions: "is X better", "why is X cheaper", "can I migrate", "what is the catch" | section_audit "faq", no_question_h2 | The questions buyers and AI sub-queries actually ask |
| CMP-17 | Migration or switching section | recommended on head-to-head and alternatives pages: what transfers, time, cost | manual | Captures the highest-intent moment of the query |
| CMP-18 | Real, current screenshots of each option | recommended, 1+ per option, alt text (C-15) | section_audit "images", alt_missing | Proof the comparison was actually performed |
| CMP-19 | Definitions of the criteria compared | recommended, one line per non-obvious criterion | section_audit "definitions" | A criterion nobody understands cannot persuade |
| CMP-20 | Cross-links to your product and pricing pages, the hub and the sibling comparisons; hub built once 3+ comparison pages exist | C-16 plus a link to the hub and 2+ siblings | section_audit "internal_links", no_cta_money | Routes the decided visitor to conversion; prevents cannibalization |
| CMP-21 | CTA with the risk-reducer next to it | 1 after the verdict, 1 at the end | section_audit "cta" | A page with no next step converts nothing |
| CMP-22 | Comparative advertising conditions met (Phase 4, step 6) | like with like; material, relevant, verifiable, representative features; no denigration; no brand confusion; descriptive use of marks; affiliate relationship disclosed | manual | Lawful under Directive 2006/114/EC only on these conditions |
| CMP-23 | Alternatives pages: a "why people leave {brand}" block, and you included honestly, not automatically first | 3-5 real reasons quoted and linked from review platforms; 4-8 options | section_audit "reviews", manual | The block that makes the page trusted, and where the long tail lives |
| CMP-24 | Best-for pages: an explicit selection rule | how options were shortlisted, what was excluded and why | manual | A list with no inclusion rule is an opinion, not a comparison |
| CMP-25 | Comparison term bolded and placed (applies C-09, C-10, C-11) | "{you} vs {competitor}" bold once in the first paragraph; bold on deciding differences and verdict facts every 100-150 words, never whole sentences or table rows; placement 60%+ (measured by the script); no term above 2.5% | no_bold, kw_not_bold, kw_placement_low, keyword_stuffing | Visible relevance and scannability; competitor names inflate density like brand names, so judge before rewriting |
| CMP-26 | Honest claims (applies C-24) | no unsourced "best", "#1", "leader" about yourself; a best-for title is backed by its stated criterion and selection rule | superlative_claim, claim_no_disclaimer | An unbacked superlative is discounted first by readers and quality raters |
| CMP-27 | Schema per family, no empty nodes (applies C-18) | head-to-head: FAQPage, Article or WebPage with author and `dateModified`, Organization; alternatives and best-for: add ItemList; nothing marked up that the page does not show | schema_none, schema_fields, jsonld_invalid | Entity graph and provenance machines can read |
| CMP-28 | Length at or above the median of the comparison pages ranking on the query (C-08) | no fixed floor: the SERP sets it | page_benchmark "words", thin_content | Comparison SERPs range from short head-to-heads to long lists |

### Audience and segment pages (`section_audit.py --type audience`)

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| CMP-29 | The segment earns its own page | all four: distinct vocabulary, distinct primary problem, distinct proof available, real search demand; otherwise a section on the main page | manual (seo-keyword-research) | Segments failing one condition produce near-duplicates |
| CMP-30 | Slug and H1 name the segment as it names itself | `/for-{segment}/` or `/{category}-for-{segment}/`; exact segment wording in the H1 | h1_missing, url_hygiene, manual | Recognition in the first second, and the exact query |
| CMP-31 | The segment's problem in its own vocabulary in the first 100 words, passing the non-duplication test | a reader from segment A can tell, within the first paragraph, that the segment B page was not written for them | kw_not_in_intro, manual (read sibling pages side by side) | The proof the page was written for them, not templated |
| CMP-32 | Segment-specific benefits, not the generic feature list | 3-6, in the segment's units (billable hours, order volume, case load) | manual | Otherwise a duplicate of the homepage with a swapped title |
| CMP-33 | The segment's workflow: "How {segment} use {product}" | 1 block from real customer interviews, with their tools and constraints | section_audit "process_block", manual | The block that makes the page non-duplicable |
| CMP-34 | Proof from the same segment | recognizable peer logos, reviews, 1 case study with a number | section_audit "social_proof_logos", "reviews" | Proof from a different segment does not transfer |
| CMP-35 | The objection specific to this segment, answered | 1+ H2; rarely price (compliance, team size, integrations, seasonality, procurement) | manual | Each segment has its own blocker |
| CMP-36 | Pricing or plan for this segment, as text | recommended, in the segment's terms | section_audit "price_in_text", "pricing_block" | Segments differ on budget and unit |
| CMP-37 | FAQ in the segment's vocabulary | 3+ questions | section_audit "faq" | Long tail, and it keeps siblings distinct |
| CMP-38 | CTA phrased for the segment; integrations or constraints that matter only to it | CTA required; integrations optional | section_audit "cta", manual | "Book a team demo" and "start free" are different asks |
| CMP-39 | Cross-links to sibling segment pages and the main product page | all siblings + product page | section_audit "internal_links" | A mis-routed visitor self-corrects; prevents cannibalization |
| CMP-40 | Segment page schema, no empty nodes (applies C-18) | FAQPage; Service or Product; Organization | schema_none, schema_fields | Entity clarity for the offer this segment buys |

## Phase 2. Audit the existing page

Skip this phase when no page exists yet; Phase 3 then sets the bar for the build.

1. Inventory first. List every page that already targets a comparison term: Search Console queries containing "vs", "versus", "alternative", "compare", "for {segment}", and a `site:` search. Two URLs for one comparison, or a segment page and the main product page ranking alternately, fail CMP-01 or CMP-29 before any copy is read.
2. Run the two collectors on each page:

```
python3 skills/seo-geo-audit/scripts/seo_audit.py https://example.com/you-vs-competitor/ /competitor-alternatives/
python3 skills/seo-page-sections/scripts/section_audit.py --type comparison https://example.com/you-vs-competitor/
python3 skills/seo-page-sections/scripts/section_audit.py --type audience https://example.com/for-agencies/
```

3. Map the output to the spec. Each `seo_audit.py` finding code fails the C row or CMP row that lists it in "Verified by"; each `section_audit.py` block marked missing fails its CMP row (`verdict_block` CMP-04 and CMP-10, `comparison_table` CMP-05, `price_in_text` CMP-09, `freshness_signal` CMP-14, `author_block` CMP-15, `faq` CMP-16 and CMP-37, `process_block` CMP-33, `social_proof_logos` and `reviews` CMP-34). `keyword_stuffing` on a competitor name is usually the comparison itself: judge before rewriting.
4. Do the manual rows. The scripts cannot judge truth, so open each competitor's public pricing page, docs and changelog and check every row of the table (CMP-12): a price, a limit or a "lacks feature X" that is no longer true fails the page. Read the verification date (CMP-14), look for the row a competitor wins (CMP-07), the limitations block (CMP-08) and the legal conditions (CMP-22). For segment pages, read the sibling pages side by side for the non-duplication test (CMP-31).
5. Mark every C row and every CMP row Pass, Fail or Not verifiable, with the evidence (finding code, block, URL of the source checked).

A page that ranks and converts is fixed in place: keep the URL (CMP-02), re-verify, update the date. Rebuilding from scratch throws away accumulated signals.

## Phase 3. Benchmark the competitors

For a comparison page, the competitors are not your business rivals' homepages: they are the pages that already rank, and that AI assistants cite, on the exact comparison query.

1. Pick 3-5 pages from the SERP of the target query ("{you} vs {competitor}", "{competitor} alternatives", "best {category} for {use case}", "{category} for {segment}") and from the answers ChatGPT, Perplexity and AI Overviews give to the same prompt. Mix the types that show up: review platforms and software directories, affiliate and editorial listicles, and the competitors' own vs and alternatives pages, including the page a competitor wrote about you ("{competitor} vs {you}", "{you} alternatives" on their domain). AI Mode and the organic top 10 share about a third of their URLs (32 percent overlap, measured by Semrush), so the cited pages matter as much as the ranked ones.
2. Run the benchmark:

```
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type comparison https://example.com/you-vs-competitor/ https://competitor.com/competitor-vs-you/ https://review-site.com/you-vs-competitor https://publisher.com/best-category-tools/
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type audience https://example.com/for-agencies/ https://rival.com/agencies/ https://rival2.com/solutions/agencies/
```

3. Read the output in this order:
   - Blocks half or more of the competitors have and the client does not (`comparison_table`, `verdict_block`, `price_in_text`, `faq`, `author_block`, `freshness_signal`): each is a CMP row moving to the top of the build.
   - Schema types competitors use and the client does not (often FAQPage, ItemList, Review on review platforms): adopt only what the page will truly show (CMP-27).
   - Metrics below the competitor median (`words`, `tables`, `statistics`, `question_h`, `bold`, `placement`, `money_links`): the C rows they map to move up in priority.
4. Read the competitor pages yourself for what the script cannot see:
   - The criteria they compare: their union is the candidate list for CMP-06, before you score anything.
   - Their facts and dates: a stale price or a "lacks feature" claim about the client is both an opening (be the current page) and something to correct, on your own page, with a source, never with denigration.
   - Whether they concede any row, state limitations or show a methodology: most do not, which is the gap.
   - The reasons for leaving they cite and the review quotes they use (CMP-23).
   - What the AI answers say about the client and on which source they lean (geo-visibility).
5. Define the information gain: what the page will contain that none of the ranking pages has. Candidates only the client can provide: hands-on test results with numbers, a migration guide with real time and cost, a total cost of ownership calculation including setup and overage, a fresher verification date, real screenshots, the uncomfortable FAQ answered, per-segment verdicts, quotes from customers who switched. Write it down in one line; the build must deliver it.

## Phase 4. Build

### Step 1. Decide which pages deserve to exist (CMP-01, CMP-02, CMP-29)

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
3. "{competitor} alternatives" pages outperform "{you} vs {competitor}" pages for a challenger brand (field heuristic), because the searcher has already decided to leave the competitor and is open, rather than defending a preference.
4. Own "{your brand} alternatives". Someone will rank for it; it should be you, with your migration path one click away.
5. Segment pages must differ by more than find and replace (CMP-29, CMP-31). If not, merge them.
6. Keep the URL literal and stable (CMP-02).

Verify the demand with seo-keyword-research before committing, and check which existing page already ranks for the term to avoid cannibalizing it.

### Step 2. Gather verifiable facts (CMP-09, CMP-12, CMP-14)

Every claim about a third party must be checkable on that third party's own public material, on the day you write it.

| Fact | Acceptable source | Never |
|---|---|---|
| Pricing | The competitor's public pricing page, dated | A number a salesperson remembers |
| Features | The competitor's docs, pricing page, changelog | Assumption from their marketing copy |
| Limits and quotas | Their published limits or terms | Inference |
| Support and SLA | Their published terms | Anecdote |
| User sentiment | Named review platforms, quoted and linked | Invented complaints |
| Your own facts | Your product, the vault, the owner | Aspiration |

Record, per row, the source URL and the date verified. That log becomes the methodology block (CMP-13) and the input to the refresh cycle. If a fact cannot be verified, write "not published" in the cell: an honest gap reads as rigor, a wrong guess destroys the page. For anything disputable, quote and link the competitor's own words rather than paraphrasing. Client facts nobody confirmed stay `{to confirm}`.

### Step 3. Choose the criteria and build the table (CMP-05, CMP-06, CMP-07, CMP-19)

Read `references/comparison-page-patterns.md` now. It carries the criteria-selection method, the fill-in wireframe of every family, the verdict formulas, the segment structure and the pre-publish checklist.

Choose 6-12 criteria from what buyers decide on (sales calls, support tickets, review sites, the benchmark's union of criteria), order them by influence, and only then fill in the values. If you win every row, the criteria are wrong: add the dimensions buyers raise when they choose someone else. The table is a real `<table>`, same criteria in the same order for every option, prices as text, a "Verified {date} from {sources}" line under it.

### Step 4. Write the verdict (CMP-04, CMP-10)

Who each option is for, stated plainly, in the first 100 words, then repeated at the end. Use the formula that fits the family (routing for alternatives, situational for head-to-head, single winner for best-for, honest exit when neither fits): name names, use a concrete situation rather than an adjective, put a number in it where possible, and never resolve every case to your own product. Write it last and rewrite it twice: it is the passage that gets quoted.

### Step 5. Write the page, block by block

Follow the family wireframe in the reference; the block list, levels and order also live in `seo-page-sections/references/page-type-matrix.md`, sections 5 and 6. Non-negotiables, each tied to its row:

1. Verdict in the first 100 words (CMP-04).
2. A real HTML comparison table (CMP-05), criteria chosen before scoring (CMP-06).
3. At least one row where a competitor genuinely wins, stated without hedging (CMP-07): the reason a model treats the page as a source rather than as marketing.
4. Your own limitations, in your own words, in a named block (CMP-08).
5. Pricing as HTML text with the date checked, for every option, like plan against like plan (CMP-09).
6. Best-for verdicts per use case (CMP-10): one page then answers "best for solo", "best for teams", "best on a budget".
7. Methodology and date: what was compared, how, when, by whom (CMP-13, CMP-14).
8. FAQ with the uncomfortable questions (CMP-16), migration section where switching is the intent (CMP-17).
9. Author block with credentials and real profiles (CMP-15).

Copy rules:

- Semantic bolding (CMP-25, C-09): the comparison term bold once in the first paragraph; then one bold phrase every 100-150 words on a deciding difference, a price or a verdict fact; never whole sentences, never decoration.
- Placement (CMP-25, C-10): the comparison term in the title, H1, first 100 words, at least two H2s, the meta description, the slug and one image alt, aiming at 60%+ coverage.
- Density (CMP-25, C-11): no term above 2.5% of content words; competitor and brand names aside, but do not repeat "X vs Y" in every heading.
- Numbers with sources (C-14): prices, limits, test results, review counts, each attributed and dated.
- Question H2s (C-13) where a section answers a buyer question ("Is {competitor} cheaper than {you}?").
- Zero em dashes and en dashes (C-25). Never leave an em dash (U+2014) or an en dash (U+2013) in copy that goes live on a client site. Replace each with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the most recognizable tell of AI-written text, and a page whose whole value is being trusted over a competitor's marketing cannot afford to read as machine output. The rule covers the verdict, the table cells, the FAQ, the methodology block, the metadata and the schema strings; sweep for both characters before delivery. Hyphens in compound words and ranges written with "to" are untouched.

### Step 6. Stay legal and stay honest (CMP-22, CMP-26)

Comparative advertising is lawful across the EU under Directive 2006/114/EC, and in most markets, but only under conditions that happen to match what makes a comparison page work: it must not be misleading, it must compare goods meeting the same needs, it must compare features that are material, relevant, verifiable and representative, and it must not denigrate the competitor or create confusion between brands. Check the rules of the market being written for before publishing.

- Compare like with like. Comparing your top plan against a competitor's free tier is both dishonest and outside the safe harbor.
- Every claim must be verifiable by a reader from public sources. Link them.
- Use the competitor's name and mark descriptively, to identify them, not in a way that suggests endorsement or affiliation. Do not use their logo as if it were a partnership.
- No denigration. State the difference, not a judgment of their competence.
- Do not misrepresent an old version as current. Date the comparison.
- If the comparison sits on an affiliate or review page, disclose the commercial relationship.
- No unsourced superlatives about yourself (C-24); results promises carry their disclaimer.

### Step 7. Segment pages (CMP-29 to CMP-40)

Same product, one customer type. Before building a set, check each segment for distinct vocabulary, a distinct primary problem, distinct proof available and real search demand; segments that fail any of those become a section on the main page. Then follow Family 5 in the reference: the problem in the segment's own vocabulary in the first 100 words, benefits in the segment's units, the workflow block, proof from the same segment, the segment's own objection, its pricing, an FAQ in its vocabulary, a CTA phrased for it, cross-links to siblings. The workflow and proof blocks require talking to real customers rather than imagining them: without that material, the page should not exist yet.

### Step 8. Schema and metadata (CMP-27, CMP-40)

| Family | Title pattern (50-60 chars) | Schema |
|---|---|---|
| Head-to-head | {You} vs {Competitor}: {the deciding difference} ({year}) | FAQPage; Article or WebPage with author and `dateModified`; Organization |
| Alternatives | {n} best {brand} alternatives in {year} (compared) | FAQPage; ItemList; Article or WebPage |
| Best-for | {n} best {category} for {use case} ({year}) | FAQPage; ItemList |
| Hub | Compare {category} options | WebPage; ItemList of the children; BreadcrumbList |
| Segment | {Product} for {segment}: {their specific outcome} | FAQPage; Service or Product; Organization |

BreadcrumbList on every one (C-19). The author is a Person with `sameAs` to real profiles (C-20). Every property filled or removed, never empty; nothing marked up that the page does not show, in particular no rating or review markup for a competitor or for yourself that the page does not display. Templates: seo-schema-markup.

### Step 9. Acceptance test

Re-run the Phase 2 and Phase 3 commands on the staged or live page:

```
python3 skills/seo-geo-audit/scripts/seo_audit.py https://example.com/you-vs-competitor/
python3 skills/seo-page-sections/scripts/section_audit.py --type comparison https://example.com/you-vs-competitor/
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type comparison https://example.com/you-vs-competitor/ {the same competitor URLs}
```

The page is done when: no high or critical finding; `comparison_table`, `verdict_block`, `price_in_text`, `faq`, `author_block` and `freshness_signal` (or the segment blocks for `--type audience`) all found; BOLD above zero with the comparison term among the samples; PLACEMENT 60% or more; no `schema_none`, `schema_fields`, `social_placeholder` or `em_dashes`; no block that half the competitors have still missing; word count at or above the competitor median; every CMP manual row checked (sources, competitor-wins row, limitations, legal, verification date logged in the vault). A remaining Fail is either fixed or a written owner decision.

## Maintain, or take it down (CMP-14)

Comparison pages decay faster than any other page type, because they depend on facts you do not control. A page claiming a competitor lacks a feature they shipped last year is worse than no page: it is the first thing a competitor's sales team screenshots.

| Trigger | Action |
|---|---|
| Every quarter | Re-verify every price and every feature row; update the date |
| Competitor ships a major feature | Update the affected rows within days |
| Your own pricing or feature set changes | Update every comparison page at once |
| The comparison can no longer be maintained | Retire the page and redirect it, rather than leaving it stale |

Put the verification date on the page and in the vault log. Keep the URL through every refresh (CMP-02).

## GEO layer (CMP-04, CMP-07, CMP-08, CMP-12)

Honesty is the GEO mechanism here, not only the legal one. Models weight pages that state limitations and cite sources, and a page whose every row favors its author reads as promotional to a reader and to a retrieval system alike. Adding statistics, quotations and cited sources raised visibility in generative answers in a controlled study (Princeton GEO, KDD 2024, measured). The verdict in the first 100 words is the quotable passage; the dated, sourced table is the extractable one; both must be in the server HTML (C-21). Track the comparison prompts in geo-tracking: comparison pages are where AI citation share moves first and most visibly.

## Deliverable

```markdown
## 1. Spec scorecard
| ID | Requirement | Status (Pass / Fail / Not verifiable) | Evidence |
(every C row and every CMP row for the page family; segment rows only for segment pages)

## 2. Audit findings
(page inventory and cannibalization check; seo_audit.py scores and high or medium findings;
section_audit.py blocks; competitor facts found stale or wrong; or "new page")

## 3. Competitor benchmark
(the ranking and AI-cited pages chosen, page_benchmark.py table, blocks and schema types
the client lacks, metrics below the median, criteria union, the information gain chosen)

## 4. Build
(page plan: families, URLs and keywords; then per page: metadata, the copy block by block
with the bolding visible, the comparison table, the verification log (fact, source URL,
date), JSON-LD, internal links; placeholders {to confirm} for unverified facts)

## 5. Acceptance
(scripts re-run: remaining findings, each either fixed or a written owner decision;
next verification date)
```

## Common mistakes

- Winning every row. The fastest way to lose the credibility the page exists to build.
- Never concluding. "It depends on your needs" forfeits the answer to whoever does conclude.
- Comparing on your strengths. Criteria must be chosen from what buyers decide on, before checking who wins.
- Building a page per competitor regardless of demand. Thin near-duplicate pages compete with each other and none of them ranks.
- Building both "X vs Y" and "Y vs X".
- Segment pages produced by find and replace. Same page, swapped noun, split signal, nothing ranks.
- Stale facts with no date. Undated comparison claims are unusable to a careful reader and to a model.
- Comparison as an image. The most extractable block on the page, rendered unextractable.
- Ignoring "{your brand} alternatives". Someone will own that page; it should be you.
- Benchmarking against the competitors' homepages instead of the comparison pages that rank on the query.
- Rebuilding or moving a ranking comparison page instead of re-verifying it in place.
- Bolding whole table rows or the competitor's name everywhere: bold is for the deciding facts.

## Sources

- Directive 2006/114/EC on misleading and comparative advertising (conditions under which comparison is lawful in the EU): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32006L0114
- Why ChatGPT cites pages (1.4M prompt study): https://ahrefs.com/blog/why-chatgpt-cites-pages/
- Generative Engine Optimization: statistics, quotations and citations raise visibility (controlled study, KDD 2024): https://arxiv.org/abs/2311.09735
- AI Mode versus top 10 organic overlap (32 percent URL overlap): https://www.semrush.com/blog/ai-mode-comparison-study/
- Google guidance on AI features and structured data: https://developers.google.com/search/docs/appearance/ai-features
- Google structured data policies (markup must match visible content): https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Common page spec C-01 to C-26 and the script finding codes: skills/seo-geo-audit/references/common-page-spec.md, skills/seo-geo-audit/references/audit-checklist.md section 15.
- Criteria counts, 100-word verdict, quarterly refresh, bold cadence, challenger heuristic: field heuristics from agency audits, not Google statements.
