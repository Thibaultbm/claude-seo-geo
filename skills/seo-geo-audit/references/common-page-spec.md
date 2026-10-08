# Common page spec (every page type)

The requirements every indexable page must meet, whatever its type. Each page skill (homepage, service, product, collection, comparison, blog, local, page sections) adds its own page-specific spec on top of this one. One requirement lives in one place: this file is the canonical source for the rows below, and the page skills link here instead of repeating them.

"Verified by" names the finding code `scripts/seo_audit.py` raises when the requirement fails (section 15 of audit-checklist.md), or the block `section_audit.py` detects. "Manual" means a human or the model judges it from the page.

## C. Common requirements

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| C-01 | Title tag with the target keyword near the front | 30-60 characters, unique | title_short, title_long | Strongest on-page relevance signal and the SERP headline |
| C-02 | Meta description written by hand | 120-160 characters, unique | meta_missing, meta_short, meta_long | The first conversion surface |
| C-03 | Exactly one H1 containing the target keyword | 1 | h1_missing, h1_multiple | The page's declared topic |
| C-04 | Heading tree without jumps or empty headings | H1 then H2 then H3 | heading_jumps, heading_empty | The outline machines read |
| C-05 | Self-referencing canonical | present, absolute | canonical_missing, canonical_other | Duplicate control |
| C-06 | Open Graph and Twitter card | og:title, og:description, og:image, og:url, twitter:card | og_missing, og_image_missing, twitter_missing | Link previews where shares happen |
| C-07 | Head basics | viewport, html lang, charset, favicon | viewport_missing, lang_missing, charset_missing, favicon_missing | Mobile-first indexing, language targeting, result icon |
| C-08 | Length at or above the competitor median for the query | page-type floor in the page skill | thin_content, page_benchmark.py "words" | Coverage the SERP already rewards |
| C-09 | Semantic bolding | target keyword bold once in the first paragraph; one bold phrase on a fact or benefit every 100-150 words; never whole sentences | no_bold, kw_not_bold | Visible relevance and scannability; skimmers read bold and headings |
| C-10 | Keyword placement | title and H1 terms in 60%+ of the zones (title, H1, H2-H6, meta, URL, first 100 words, bold, image alt) | kw_placement_low, kw_not_in_intro | The placement matrix |
| C-11 | No over-optimization | no term above 2.5% of content words (brand names aside), never above 7% | keyword_stuffing | Stuffing lowers rankings and generative visibility |
| C-12 | Readable, extractable text | readability 60+; paragraphs 40-80 words, none above 150 | readability, long_paragraphs | Long blocks lose readers and extract poorly |
| C-13 | Question headings where the section answers a question | 3+ on content pages | no_question_h2, page_benchmark.py "question_h" | Maps to People Also Ask and AI sub-queries |
| C-14 | Numbers with their source | 2+ statistics, each attributed | no_stats, citability counts | Statistics and sources carry measured citation gains |
| C-15 | Images | alt on every informative image (alt="" for decorative), WebP or AVIF, 200 KB max, width and height set, first image eager | alt_missing, alt_quality, image_weight, image_format, image_dimensions, lcp_lazy | Image search, speed, layout stability |
| C-16 | Body links to the pages that sell | 3+ descriptive body links to commercial pages (offer, product, service, contact) | no_cta_money, home_no_money_links, generic_anchor, empty_anchor | Authority and readers flow through body links |
| C-17 | No internal nofollow | 0 | internal_nofollow, nofollow_share | Throwing away your own link equity |
| C-18 | Valid structured data for the page type | parses, required properties filled, none empty, nothing marked up that the page does not show | jsonld_invalid, schema_none, schema_entity, schema_article, schema_fields | Entity graph for AI engines, remaining rich results |
| C-19 | Breadcrumb on every page below the homepage | visible + BreadcrumbList | breadcrumb_missing, section_audit "breadcrumb" | Hierarchy for crawlers and users |
| C-20 | Real social profiles | links to profiles, never to a network homepage or `#`; the same URLs in `sameAs` | social_placeholder, social_missing | Entity consistency |
| C-21 | Content in the server HTML | headings, prices, FAQ answers, author, schema present without JavaScript | likely_js_rendered, render_check.py | AI crawlers do not execute JavaScript |
| C-22 | Indexable, snippet allowed | no noindex by mistake, no nosnippet, max-snippet not under 50 | noindex, snippet_capped, meta_refresh | Out of the index or out of AI Overviews |
| C-23 | Clean URL | natural-language slug with the keyword, under 100 characters, lowercase, hyphens | url_hygiene | Descriptive slugs are cited more often |
| C-24 | Claims are honest | results and income promises carry a "not guaranteed" disclaimer; superlatives ("n°1", "best") carry a source; regulated topics (gambling, finance, health) carry the legal notices | claim_no_disclaimer, superlative_claim, gambling_notice_missing | Your Money or Your Life scrutiny and advertising law |
| C-25 | No em dashes or en dashes | 0 | em_dashes | The most recognizable AI-writing tell |
| C-26 | Speed and weight | HTML under 1.5 MB, DOM under 1500 elements, no mixed content; Core Web Vitals from PageSpeed when available | html_size, dom_size, mixed_content (manual for Core Web Vitals) | Ranking and crawl factor |

## How a page skill uses this file

1. Phase 1 (spec): the page skill's own table (its IDs, for example SVC-01) plus every C row above.
2. Phase 2 (audit): run `seo_audit.py` on the page; each finding code maps to a C row or a page-specific row. Mark every row Pass, Fail or Not verifiable.
3. Phase 3 (benchmark): run `page_benchmark.py --type <type> <client> <competitors>`; the C rows whose metric sits below the competitor median move up in priority.
4. Phase 4 (build): fix every Fail, then re-run the scripts. The page is done when no C row and no page-specific row fails, or when a remaining Fail is a written owner decision.
