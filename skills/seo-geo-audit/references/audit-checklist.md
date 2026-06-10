# SEO + GEO audit checklist (14 categories)

Provenance markers: (field) = recurring finding across 115+ real agency audit calls, treat as a strong heuristic, not a law. (measured) = published study or official documentation, sources listed in SKILL.md. Where competitors are known, their measured values override every abstract threshold below: the gap is the finding.

## 1. Method and framing

- 1.1 Technical first, content second. Month one fixes the foundation (headings, indexation, speed, tags); content scales from month two. Why: articles published on a broken foundation rank below their potential, and refitting later costs double. (field)
- 1.2 SEO compounds. No single fix wins; expect roughly "1 percent per action" across dozens of actions. Set this expectation in the report so the owner does not abandon after one week. (field)
- 1.3 One site, full focus. Splitting effort across two domains divides results by more than two: authority, content cadence and links all dilute. Recommend consolidation unless there is a hard business reason. (field)
- 1.4 SEO is an asset. Rankings persist and appreciate like digital real estate; paid traffic stops the day spend stops. Useful framing for prioritization decisions in the report. (field)
- 1.5 Quantify everything. "523 errors, of which 178 are images without alt text" turns an opinion into a scoped project. Count what the script lets you count. (field)

## 2. Tags

- 2.1 Title: main keyword + brand (+ city if local), roughly 30-60 characters. Never "Home", "Welcome" or the bare brand alone on inner pages: the title is the single strongest on-page relevance signal and the SERP headline. (field + measured)
- 2.2 Meta description: 120-160 characters, handwritten, unique per page. Above 160 it truncates; missing means Google improvises. It does not rank directly but drives click-through. Audits regularly find 300-400 character descriptions pasted from body text. (field)
- 2.3 Headings as nested dolls: exactly one H1 (= main keyword), H2 sections, H3 inside H2. No level jumps (H1 to H3), no empty headings, no styling-driven H5 where a paragraph belongs. Why: the heading tree is the machine-readable outline both Google and AI passage retrieval rely on. (field)
- 2.4 Keyword in the slug, natural-language slugs. Descriptive slugs are cited by ChatGPT at 89.78 percent versus 81.11 percent for opaque ones. (measured)
- 2.5 Placement matrix: each of the top 5 target keywords appears in title, H1, at least one H2, URL, first paragraph in bold, meta description, image alts, and incoming internal anchors. Run the matrix per money page. (field)
- 2.6 Open Graph complete (og:title, og:description, og:image), one image per language for localized sites. Social and chat previews are part of how pages earn clicks and shares. 
- 2.7 Consistency details: bullets end with a period, no orphan punctuation. Minor, but sloppy text patterns correlate with sloppy structure elsewhere; flag only when widespread. (field)

## 3. Images

- 3.1 Zero images without alt text. Google does not interpret pixels at scale; it reads the alt attribute. Alt text also feeds the multi-format understanding AI engines use. Purely decorative images get an explicit empty alt (alt=""). The single most frequent audit finding. (field)
- 3.2 200 KB maximum per image, WebP or AVIF. A 2-3 MB photo compresses to under 200 KB with no visible difference and speed is a ranking and crawl-budget factor. (field)
- 3.3 Never lazy-load above the fold. Lazy-loading the hero image delays LCP, the opposite of its purpose. (measured)
- 3.4 Real photos wherever trust is sold (products, team, premises). AI-generated images only inside articles and only photorealistic ones. (field)
- 3.5 Explicit width and height attributes so the browser reserves space (CLS). (measured)

## 4. Performance and indexation

- 4.1 Mobile first: 80-90 percent of typical traffic is mobile, so judge mobile scores first. PageSpeed 75+ on desktop is acceptable; aim higher when competitors are faster. Free check: https://pagespeed.web.dev (field + measured)
- 4.2 Core Web Vitals: LCP under 2.5 s, INP under 200 ms, CLS under 0.1. INP replaced FID in March 2024 and is the most commonly failed vital (roughly 43 percent of sites). Treat CWV as a tiebreaker, not the main lever: fix indexation and content first. (measured)
- 4.3 Sitemap.xml: present, declared in robots.txt, segmented by type for large sites, honest lastmod. The Google sitemap ping endpoint is dead since 2023; submission happens in Search Console. (measured)
- 4.4 robots.txt and AI bots: report blocked AI SEARCH bots (OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User) separately from blocked TRAINING bots (GPTBot, ClaudeBot, CCBot, Google-Extended, and others). Blocking search bots removes the site from AI answers today; blocking training bots is a brand-knowledge tradeoff. Default for visibility-seeking businesses: allow both groups. Full table: seo-technical references/ai-crawlers.md. (measured)
- 4.5 Indexation ratio: indexed versus submitted pages in GSC (3000 of 4000 is healthy; 300 of 4000 is a fire). Inspect and request indexing for priority pages. Never guess this number: ask for GSC access or a screenshot. (field)
- 4.6 Zero orphan pages: every page reachable through at least one internal link. Orphans are crawled late or never, and a page absent from the index is absent from every AI answer too. (field)
- 4.7 404s that had traffic or links get a 301 to the closest equivalent. (field)
- 4.8 Canonicals on duplicates: e-commerce variants, URL parameters, www and non-www, trailing slashes. (field)
- 4.9 HTTPS everywhere, and scan for injected spam (hidden casino or pharma links mean the site is hacked: clean it and harden the CMS before anything else; on WordPress add a security plugin such as Wordfence). A hacked site is a Blocking finding. (field)
- 4.10 GSC and GA4 installed AND the owner actually has access. Audits regularly find neither, or an agency holding the keys. (field)
- 4.11 Bing Webmaster Tools + IndexNow configured. Bing's index is a discovery door for ChatGPT, which makes Bing a first-class citizen in 2026. (measured)
- 4.12 JavaScript rendering gate: the visible content must exist in the raw HTML. No AI crawler executes JavaScript (only Googlebot renders), so client-side content is invisible to ChatGPT, Claude and Perplexity. Test: curl the page or check the script's likely_js_rendered flag. Client-rendered money pages are a Blocking finding for GEO. (measured)
- 4.13 Measurement artifact: Google removed the num=100 parameter in September 2025; GSC impression drops around that date are rank-tracker artifacts, not traffic losses. Do not let the owner misread the graph. (measured)
- 4.14 hreflang with x-default for multilingual sites, bidirectional pairs, language-consistent content per locale. (measured)

## 5. Architecture

- 5.1 One service, one product, one problem = one page. A single page listing everything ranks for nothing, because each query deserves a dedicated relevance target. The most common architecture finding on small business sites. (field)
- 5.2 Local coverage: parent region page plus child city pages, each with unique local content (testimonials, projects, specifics), never a find-and-replace of the city name (doorway page risk). (field)
- 5.3 Blog at /blog as a subdirectory, never a subdomain: authority consolidates on the domain. Linked from the menu or footer so it is crawled and visited. (field)
- 5.4 Light silos for niche sites: 2-3 related articles linked at the bottom of each service page is enough; full cocoon structures are for large sites. (field)
- 5.5 Comparison and alternatives pages: N relevant competitors crossed produce up to N squared "X vs Y" and "X alternatives" pages; comparative listicles are also the most cited format in AI answers (about 32.5 percent of citations). (field + measured)
- 5.6 Page-type wireframes: service pages, product pages and collection pages each have a proven structure; check against the dedicated skills rather than improvising.
- 5.7 Only public content counts. Anything behind a login, a paywall the crawler cannot pass, or a cookie wall is invisible to every engine, classic and AI. (field)

## 6. Content volume

- 6.1 Word ladder (field): 180 words very insufficient; 300 standard minimum; 500+ when the query is competitive; 750 very good; homepage 1500-1800. Master rule: benchmark the top 3-5 ranking pages for the target query and close the gap. Never replace a longer ranking text with a shorter one.
- 6.2 First bolded words of the intro = the main keyword; secondary keywords bolded through the body. Bold is a cheap, visible relevance and scannability signal. (field)
- 6.3 No lorem ipsum (it happens more than expected), no unbroken walls of text: paragraphs of 10-80 words, one idea each. Short self-contained paragraphs are also what AI engines extract. (field + measured)

## 7. Keywords and intent

- 7.1 Nobody types jargon. The internal name of the offer is rarely the query. Validate with autocomplete, People Also Ask, related searches, forum phrasing. (field)
- 7.2 Intent decides the page type: transactional queries deserve a product or service page; informational queries deserve an article that links to the money page. Mismatched intent does not rank. (field)
- 7.3 Long-tail AND head terms: long-tail converts and is reachable quickly, head terms build over months. A portfolio, not a choice. (field)
- 7.4 Local pattern: city in title, URL, H1, meta, first paragraph, image alts. (field)
- 7.5 Cannibalization: one keyword = one page. Test: google both phrasings; if the results are the same, it is one intent, so merge the pages and 301 the loser. (field)
- 7.6 Ranking first on a zero-volume keyword while the technical base is broken is vanity, not progress. Check volumes before celebrating positions. (field)
- 7.7 AI fan-out keywords: AI engines split questions into sub-queries and sample 10-20 sources. Ultra-niche question pages win citations that classic rankings never show. See seo-keyword-research for prompt research. (measured + field)

## 8. Blog and articles

- 8.1 The 12-element article skeleton (title and meta, cover and H1 and breadcrumb, author and reading time, table of contents, answer-first summary, keyword-bolded intro with the first source, structured body, 3-5 external sources, 3-5 internal links, conclusion, CTA, FAQ): full detail in seo-content-blog.
- 8.2 Three images per article: one cover, two in the body, all alt-tagged and compressed. (field)
- 8.3 Sources: government or institutional, major media, scientific studies. Never a competitor. Follow links. The first source appears in the intro: it signals research from the first screen. (field)
- 8.4 AI-written content is not penalized; lazy content is. Read the top 5 ranking pages first, then add information gain (original data, first-hand experience, a sharper angle). (field + measured)
- 8.5 Rewrite existing winners before writing new articles: a page with history responds faster than a new URL. Never refresh only the date: engines compare the content. (field)
- 8.6 One angle = one article, otherwise the articles cannibalize each other. (field)
- 8.7 Three to five visible internal links (underlined, colored) per article toward money pages. (field)
- 8.8 Volume by phase (field): launch 45-75 articles (up to 100 in content-rich niches), established sites about 20 per month. Quality gates first: skeleton complete, sources real, angle unique.
- 8.9 Articles exist to lift commercial pages: informational traffic plus internal links push the pages that sell. An article program with no internal linking plan leaks its value. (field)
- 8.10 Video: embed from YouTube rather than self-hosting (weight, plus a second search surface). (field)
- 8.11 Comparative and commercial content refreshed every 60-90 days with honest dateModified: freshness measurably boosts citation odds on commercial queries. (measured)

## 9. GEO

- 9.1 FAQ section (3 People Also Ask questions) on every important page. FAQ rich results are gone from Google SERPs (May 2026), but the question-answer format is precisely what AI engines extract. The content matters, not the markup. (measured)
- 9.2 Answer-first summary at the top of articles plus a table of contents: AI engines extract passages and a summary that answers in 2-4 sentences is the most extractable passage on the page. (field + measured)
- 9.3 Ultra-niche question pages: where AI engines sample few sources, an exact-match answer page gets the citation. (field)
- 9.4 Multi-surface presence: YouTube appears in a meaningful share of AI answers (field heuristic, around 15 percent), review platforms and LinkedIn are heavily cited in "best X" answers. The site is one surface among several. (field + measured)
- 9.5 AI Overviews: do not chase them as a separate project; they reduce clicks (position 1 CTR down as much as 58 percent on covered queries) and obey passage-level quality. Optimize passages and let coverage follow. (measured)
- 9.6 AI engines recommend product and service pages directly. Keep money pages self-sufficient: specs, FAQ, comparisons, prices in server-rendered HTML. (field + measured)
- 9.7 Citation tracking: replay a fixed prompt panel monthly per engine (geo-tracking). A meaningful share of buyers now asks an AI assistant before ever searching. (field)
- 9.8 The two binary gates first: AI crawler access (4.4) and server-rendered content (4.12). When either fails, nothing else in this section matters yet.
- 9.9 Entity consistency: identical name, one-line description and key facts across the site, LinkedIn, review platforms, directories. Models learn the brand from co-occurrence across sources. (measured)
- 9.10 llms.txt: report presence as a fact. No major engine confirms reading it (about 0.1 percent of AI bot hits request it). Generating one is harmless; selling it as a lever is dishonest. (measured)

## 10. Conversion signals

- 10.1 Reviews and testimonials visible high on the page, formatted as first name + situation + problem + result; video testimonials outperform text. Anonymous five-star walls convince nobody. (field)
- 10.2 Email capture timed to fire 10-20 seconds before the average session ends (or at 10-20 percent scroll), never on landing. Technical trap seen in audits: a popup injected at the top of the DOM can break the heading hierarchy; place it at the end of the body. (field)
- 10.3 A clear CTA after every major section. The audit checks that a motivated reader is never more than one screen away from the next step. (field)

## 11. E-commerce

- 11.1 Collection pages carry the store's SEO: 400-800 words of rich text at the BOTTOM of each collection (below the product grid). At the top it pushes products below the fold and costs conversions. Detail: seo-content-collection-page. (field)
- 11.2 Product pages: 150-200 words minimum of unique description, plus FAQ and around 5 term definitions at the bottom. Detail: seo-content-product-page. (field)
- 11.3 Real product photos, Shopping-compliant data. (field)
- 11.4 Article bottoms in a store: product slider, then email capture, then related articles: the article-to-revenue bridge. (field)
- 11.5 Under roughly 100 visitors per day, prioritize traffic volume over conversion micro-testing: at a typical 2-4 percent conversion rate there is nothing to test yet. (field)
- 11.6 Reassurance badges (payment, delivery, returns) near the buy button. (field)
- 11.7 ChatGPT Shopping: for stores, submitting the product feed (OpenAI Agentic Commerce spec) is the single highest-leverage GEO action. (measured)

## 12. Backlinks and mentions

- 12.1 An old domain is gold: authority history compounds. Never let it expire, never migrate away casually. (field)
- 12.2 Topical relevance beats raw authority, and the linking site's language should match the target market. (field)
- 12.3 Authority also comes from content: linkable assets (tools, data, studies) earn what outreach cannot buy safely. (field + measured)
- 12.4 Disavow is generally useless: Google ignores spam links by default; the tool matters only under a manual action. (measured)
- 12.5 Healthy profile shape: gradual velocity (2-5 per day at most during campaigns), a natural mix of follow and nofollow (100 percent dofollow looks engineered), varied anchors. (field)
- 12.6 Mentions over links for AI visibility: brand mentions, linked or not, correlate about 3 times more with AI answer presence than backlinks (0.664 versus 0.218). Audit both the link profile and where the brand is talked about. Detail: seo-backlinks. (measured)
- 12.7 Review platform presence for the market (G2, Capterra, Trustpilot, trade directories): these pages rank and get cited in "best X" answers. (measured)

## 13. Local

- 13.1 Reviews are the number one local ranking factor. Four pillars of a Google Business Profile that ranks: review count and velocity, a 100 percent complete profile (budget about 90 minutes to fill everything), regular posts (weak signal, still worth it), and the strength of the linked website. (field)
- 13.2 Profile name: guidelines require the exact business name. Names with trade and city added do rank better, and also risk suspension for guideline violation. Report both facts; the owner decides. (field, risk explicit)
- 13.3 The linked website's SEO lifts Maps rankings: GBP and site are one system. (field)
- 13.4 NAP (name, address, phone) strictly identical across site, GBP, directories and socials: citation coherence builds entity trust for Google and for LLMs. (field + measured)
- 13.5 Suspended profile: reinstatement with documents (proof of address, business registration, storefront photos) through the official appeal; never create a duplicate profile, it poisons the case. (field)

## 14. Migration

- 14.1 Stay on the same domain whenever possible and touch lightly: it is easy to break rankings and very hard to build them. Treat every migration as a risk project. (field)
- 14.2 301 every URL from a full GSC export (queries and pages), not just the menu: long-tail pages hold the traffic nobody remembers. (field)
- 14.3 Hide pages from the menu rather than deleting them when they rank. (field)
- 14.4 CMS reality check: WordPress, Shopify and Webflow hold up at content scale; trendy client-rendered site builders are fragile for large SEO sites (rendering, speed, URL control). (field)
- 14.5 Content ownership: confirm an export path exists before committing to any platform. (field)
- 14.6 Deduplicate mirrors: the same articles published on a second platform (newsletter mirrors, Medium copies) need canonicals or noindex on the copy. (field)
