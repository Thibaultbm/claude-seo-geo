---
name: seo-content-blog
description: "Write blog articles that rank on Google and get cited by AI engines (ChatGPT, Perplexity, AI Overviews). Input: a keyword, topic, or existing draft. Output: a publish-ready article, outline, or brief built on a 12-element answer-first skeleton (question H2s, expert quotes, stats, FAQ, internal links, SERP-benchmarked length). Use when writing, rewriting, refreshing, or auditing a blog post, or when one will not rank or get cited by AI engines."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# SEO Blog Content That Ranks and Gets Cited

Write or rewrite blog articles on a 12-element skeleton (field methodology from 115+ agency audits, layered with 2024-2026 citation research) so the same article ranks in Google and gets extracted as an answer by ChatGPT, Perplexity, and Google AI Overviews.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use

- Writing a new blog article from a keyword, topic, or brief.
- Rewriting or refreshing a published post that decayed or never ranked.
- Reviewing a human-written or AI-generated draft before publication.
- Producing an outline or content brief for a writer.
- Planning publication cadence for a blog launch or an established site.

Route adjacent jobs to their own skills:

- Choosing the target keyword, mapping intent, splitting overlapping topics: seo-keyword-research.
- Product, service, or collection page copy: seo-content-product-page, seo-content-service-page, seo-content-collection-page.
- Site-level link routing and silos: seo-internal-linking. Full site diagnosis: seo-geo-audit.

## Workflow

### Step 1. Lock the target

Confirm before writing:

- Primary keyword and the intent behind it (informational or commercial investigation).
- Language and market: a French SERP and a US SERP rarely reward the same article.
- The commercial pages this article must support with internal links.
- Whether an existing article already covers this intent. If yes, rewrite it instead of creating a new one.

Enforce one angle = one article: two articles on the same intent cannibalize each other and split clicks, links, and signals (merge test in seo-keyword-research).

### Step 2. Read the SERP before writing a single line

Fetch the top 3-5 Google results for the keyword and record:

| Per competitor | Why it matters |
|---|---|
| Word count | Sets the length floor; never come in under the median |
| H2 structure and questions answered | The subtopics Google already rewards; this is the coverage checklist |
| Tables, images, videos used | The formats the query expects |
| Publication and update dates | The freshness bar; an aging SERP is an opening |
| People Also Ask questions | Raw material for the FAQ and the question H2s |

For on-page fact collection, run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py). Why this step exists: the SERP is the specification. Google is showing what it already considers a satisfying answer for this query; writing blind produces a worse copy of it.

### Step 3. Set the length from the benchmark

Target the median of the ranking pages or above (thresholds table below). Never plan a rewrite shorter than the page it replaces: replacing long ranking content with shorter content is one of the most common self-inflicted ranking losses observed in audits.

### Step 4. Define the information gain

Name at least one element the current top 5 do not have:

- Original data: your numbers, a small survey, aggregated anonymized client results.
- First-hand experience: you ran the process, with outcomes and photos.
- An expert quote collected for this article.
- A comparison table no competitor built.
- A fresher statistic, with its source linked.

Why: Google holds a patent on scoring pages by information gain (US 11,354,342, "Contextual estimation of link information gain"; a patent signals research direction, not confirmed production use); a page that restates the SERP gives the index no reason to rank it and gives AI engines no reason to cite it. This step is also what makes AI-assisted drafting safe (rules below).

### Step 5. Draft on the 12-element skeleton

Next section. Write the body first; write the title and meta description last, they are sharper once the article exists.

### Step 6. Layer the GEO elements

- Answer-first block at the top.
- Self-contained H2 sections (chunk autonomy).
- At least one expert quote and at least two statistics with sources cited inline.

These are the interventions with measured visibility gains in generative engines (see GEO layer).

### Step 7. Place the links

- 3-5 external authority sources, the first inside the intro.
- 3-5 internal links to commercial pages, styled visibly.

Anchor rules and site-level architecture: seo-internal-linking.

### Step 8. Finalize assets and metadata

- 3 images (1 cover + 2 in body), alt text on all, WebP, 200 KB max each.
- FAQ built from 3 real People Also Ask questions.
- Title 30-60 characters, meta description 120-160 characters.
- Natural-language slug containing the keyword (measured citation gap in the GEO layer).

### Step 9. Verify

Run the pre-publish checklist (Output format section), then sweep the Common mistakes list.

## The 12-element article skeleton

Apply every element. Each one exists because its absence showed up as a recurring loss across 115+ agency audits.

**1. Title tag + meta description.** Title 30-60 characters with the primary keyword near the front, phrased as a reason to click, not a label. Meta description 120-160 characters, written by hand. Why: beyond roughly 60 characters Google truncates the title; a hand-written description controls the SERP pitch instead of letting Google assemble one from random page text, and the snippet is the first conversion surface of the article.

**2. Cover image + single H1 + breadcrumb.** Exactly one H1, containing the primary keyword. A visible breadcrumb trail (markup details: seo-schema-markup). Why: multiple H1s blur the topical focus of the page; the breadcrumb tells crawlers and AI engines where the page sits in the site hierarchy.

**3. Visible author + reading time.** Real name, photo, role, linked to an author page. Why: E-E-A-T accountability. Anonymous content is easier for quality systems and AI engines to discount, especially on money or health adjacent topics. Reading time sets expectations and reduces pogo-sticking.

**4. Table of contents.** Anchor links to every H2, placed near the top. Why: orients readers on long pages, can produce jump links in Google results, and hands machine readers the subtopic map in one block.

**5. Answer-first summary block.** Directly after the H1 or first paragraph: give THE answer to the title query in 2-4 sentences, before any background. Why: AI engines extract passages and economize tokens; a complete answer at the top is the answer served directly, and it is the most cited passage of a page. It doubles as featured snippet material. This is the highest-leverage GEO element in the skeleton.

**6. Intro with bolded keyword + first authority link.** The first sentence contains the primary keyword in bold. The first of the external sources is linked inside the intro. Why: instantly confirms topical match for readers, parsers, and ranking systems; an early citation marks the article as sourced from the first screen (citing sources is measured at +30% generative visibility, see GEO layer).

**7. Body sections.** H2s phrased as real questions whenever the section answers one. Secondary keywords and key facts in bold (semantic bolding, not decoration). Several images, comparison tables for anything comparable, expert quotes where claims need weight. Why: question H2s map to People Also Ask and to the sub-queries AI engines generate; tables are the most extractable comparison format; quotes and statistics carry measured citation gains.

**8. External sources: 3-5, three accepted types only.** Government or institutional sites, major media, scientific studies. Never a competitor. Followed links, not nofollow. First one in the intro. Why: these source classes are what quality raters and fact-checking systems treat as ground truth; linking a competitor donates authority and a citation path on your own keyword; nofollow on a source you hand-picked signals you do not vouch for your own evidence.

**9. Internal links: 3-5 to pages that sell.** Target products, services, collections, pricing. Visible style: underlined plus a distinct color. Why: articles capture informational traffic; internal links are the mechanism that converts that traffic and authority into commercial rankings (articles lift commercial pages). An invisible link gets no clicks, and internal click-through is a usage signal. Site-wide routing: seo-internal-linking.

**10. Conclusion with bold + CTA.** Restate the answer, bold the takeaway, end on one call to action pointing at the most relevant commercial page. Why: the conclusion is the second-most-read block for skimmers; an article without a next step wastes the traffic it earns.

**11. FAQ: 3 questions from People Also Ask.** Pull real PAA questions for the keyword and answer each in 2-4 sentences. Why: FAQ rich results are gone (deprecated for most sites by Google in August 2023, fully retired by May 2026), but the question-answer format remains one of the most extracted structures in AI answers: each pair is an autonomous chunk that matches a real sub-query.

**12. Three images.** 1 cover + 2 in the body. Every image: descriptive alt text, WebP format, 200 KB max. Why: images break up text walls (dwell time), rank in image search, and alt text is the only image content text-based AI crawlers can read. Oversized images degrade Core Web Vitals.

## Rules and thresholds

Word count (field heuristics from 115+ agency audits, not Google statements):

| Word count | Verdict |
|---|---|
| Under 180 | Critically thin: rewrite, expand, or merge into another article |
| 300 | Minimum standard for a simple informational query |
| 500 or more | Required when the SERP is competitive |
| 750 or more | Comfortable baseline for most commercial-adjacent topics |
| Master rule | Benchmark the top 3-5 ranking pages and close the gap; the live SERP overrides every fixed number above |

Publication cadence (field heuristics):

| Situation | Cadence |
|---|---|
| Niche topic volume | Estimate the total addressable topics first (for example 500-600 exploitable subjects around one city) to size the corpus and the runway, separate from the monthly pace |
| Blog launch | 45-75 articles for the initial corpus, up to 100 in a content-rich niche |
| Established site | Around 20 articles per month |
| Hand-written daily cap | Roughly 20 pieces per day; past that, quality and information gain slip |
| Programmatic scale | Some sites publish 2000-4000 templated pages in a single day and get them indexed, but this is exactly the pattern Google's scaled content abuse policy targets: each page must add real value for users, not merely be unique (policy and indexation conditions in seo-technical) |
| Priority order | Rewrite existing articles that already earn impressions BEFORE creating new ones |
| Comparative listicles | Refresh every 60-90 days with real changes, an honest dateModified, and a visible date on page |

Volume versus cadence: the topic-volume estimate tells you how big the opportunity is and how long it will take to cover; the monthly cadence is the sustainable pace. Size the niche once, then pace against it. The daily cap governs hand-written articles; the 2000-4000 per day figures are programmatic generation, a different lane that lives or dies on per-page uniqueness, not on editorial craft (field heuristics from 115+ agency audits).

Breaking-news lane: for genuinely time-sensitive topics, the Top stories and News surfaces can index a fresh article within minutes and draw sharp traffic spikes. There is no approval step anymore: Google News inclusion has been automatic for policy-compliant sites since Publisher Center stopped accepting publication submissions in April 2024, and Top stories has not required Google News inclusion since 2019. What earns the surface is news-grade freshness plus a News sitemap and an RSS or Atom feed (see seo-technical). Treat this as a separate lane, not a tactic for evergreen content (field heuristic from 115+ agency audits).

Google Discover lane: for most publishers Discover is a bigger organic surface than Google News. It cannot be targeted with keywords; it rewards the same fundamentals plus its documented specifics: large images (1200px+, enabled via max-image-preview:large), honest non-clickbait titles, E-E-A-T, and topical entity clarity (https://developers.google.com/search/docs/appearance/google-discover). Discover traffic is volatile by design; report it separately and never build a forecast on it.

Why rewrite-first: an existing URL has age, links, and impression history; lifting it from position 8 to position 3 outperforms a new URL starting from zero. Never republish with only a new date: Google compares content versions, and a date-only refresh is deceptive freshness. Flag this risk whenever a user asks for it.

Title and answer-block patterns:

| Query type | Title pattern | Answer-first block shape |
|---|---|---|
| How-to | How to <task>: <number or benefit> | Outcome, number of steps, time required, the one critical warning |
| Definition | What Is <term>? <scope> | Term, category, differentiator, main use case, in 2-4 sentences |
| Comparison | Best <category> for <audience> (<year>) | The winner, for whom, the runner-up, the deciding criterion |
| Cost | <thing> Cost: <range or factors> | The realistic range first, then the 2-3 factors that move it |

Why patterns instead of creativity: the top block must answer the query in the retrieval frame engines use; cleverness belongs in the development, the first screen belongs to the answer.

AI-assisted drafting:

| Rule | Detail |
|---|---|
| Google's position | AI involvement is not penalized as such; content with no added value is, whoever wrote it |
| Mandatory order | Read the top 5 SERP results FIRST, then write with a named information gain |
| Risk to flag | Generating articles that restate what already ranks, at scale, is what the scaled content abuse spam policy targets |
| What wins | Information gain beats word count: original data, tested experience, expert input |

Punctuation, non-negotiable: never ship an em dash.

Client-facing copy carries zero em dashes (U+2014) and zero en dashes (U+2013). Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text: one is enough for a reader, or the client, to file the whole page as machine output, and the trust cost lands on the site, not on the draft. The rule covers every character you deliver: body copy, H1 and H2s, title tag, meta description, FAQ answers, alt text, CTAs, schema strings, image captions. Sweep the finished draft for both characters before handing it over. Hyphens in compound words and ranges written with "to" are untouched.

Media:

| Element | Rule | Why |
|---|---|---|
| Video | Embed from YouTube, never upload to your own server | Page weight stays low and the video earns a second surface (YouTube search) plus a multi-channel signal |
| Images | 3 per article, alt text on all, WebP, 200 KB max | Speed, image SERPs, and machine-readable descriptions |
| Substack or Medium mirror | Set the syndicated copy to no-index; rank the canonical version on the owned site (a WordPress or similar) | The owned site carries the SEO; the mirror serves the email or follower audience. A crawlable duplicate splits signals and can outrank the original, so de-index the copy (field heuristic from 115+ agency audits) |

## GEO layer

How the skeleton performs in generative engines, with measured numbers:

- **Measured (Princeton GEO study, KDD 2024, 10,000 queries):** adding expert quotes raised generative visibility by roughly 41%, adding statistics by roughly 32%, citing sources by roughly 30%, fluency improvements by roughly 28%. Keyword stuffing DECREASED visibility. These wins map directly to skeleton elements 6, 7, and 8.
- **Measured (Ahrefs, 1.4M ChatGPT prompts):** semantic similarity between the title plus content and the fan-out sub-queries is the strongest citation predictor; the answer-first block and question-form H2s exist to match those sub-queries. Pages with natural-language slugs were cited in 89.78% of eligible cases vs 81.11% for opaque slugs. Median age of cited pages is around 500 days: authority compounds on a URL, so rewrite in place and never churn URLs.
- **Measured (ALM Corp):** comparative listicles ("Best X for Y") draw roughly 32.5% of AI citations. Maintain comparison content deliberately and refresh it every 60-90 days.
- **Google AI Overviews:** assembled from indexed, extractable passages; the answer-first block and self-contained H2 sections are the units it lifts.
- **Perplexity:** favors fresh, well-sourced pages; visible dates and inline-cited statistics matter most there.
- **Chunk autonomy:** every H2 section must stand alone: direct answer in 2-4 sentences, then development, with no "as we saw above" references. AI engines retrieve isolated chunks without surrounding context; a dependent chunk is an unusable chunk.

Boundaries: passage-level citability rules live in geo-visibility; AI crawler access (robots.txt, user agents, rendering) lives in seo-technical; measuring AI citations and traffic lives in geo-tracking.

## Output format

Deliver every article in this exact structure:

```markdown
## Article metadata
- Primary keyword: <keyword> | Intent: <informational / commercial investigation>
- Title (30-60 chars): <title>
- Meta description (120-160 chars): <description>
- Slug: /blog/<natural-language-slug-with-keyword>
- SERP benchmark: top results at <N1>, <N2>, <N3> words; target <N> words
- Information gain: <the element the top 5 do not have>
- Internal link targets: <3-5 commercial URLs>
- External sources: <3-5 URLs, each tagged gov / media / study>

# <H1 containing the primary keyword>

[Cover image: <description> | alt: "<descriptive alt>" | WebP, under 200 KB]

By <author name>, <role>. <X> min read.

[Table of contents: anchor links to all H2s]

**In short:** <the complete answer in 2-4 sentences>

<Intro: first sentence with **primary keyword** in bold; first authority source linked here>

## <Question-form H2>
<Direct answer in 2-4 sentences.>
<Development: bolded secondary keywords, image or comparison table where data is comparable,
expert quote where a claim needs weight, internal link where a commercial page fits.>

## <Next H2 sections, same pattern, each self-contained>

## Conclusion
<Restated answer with **bolded takeaway**. One CTA to <commercial page>.>

## FAQ

### <People Also Ask question 1>
<2-4 sentence answer.>

### <People Also Ask question 2>
<2-4 sentence answer.>

### <People Also Ask question 3>
<2-4 sentence answer.>
```

Pre-publish checklist (verify every line, report failures to the user):

- [ ] Title 30-60 characters, keyword near the front
- [ ] Meta description 120-160 characters, hand-written
- [ ] One H1 containing the keyword; breadcrumb present
- [ ] Author and reading time visible
- [ ] Answer-first block within the first screen
- [ ] Primary keyword bolded in the first sentence
- [ ] First external source linked in the intro; 3-5 total; gov, media, or study only; followed; zero competitors
- [ ] 3-5 visible internal links to commercial pages
- [ ] Every H2 section self-contained (no "as seen above")
- [ ] FAQ = 3 real People Also Ask questions
- [ ] 3 images, all with alt text, WebP, 200 KB max
- [ ] Length at or above the SERP benchmark
- [ ] Information gain named and actually present in the text
- [ ] Zero em dashes and zero en dashes anywhere in the deliverable, commas instead

## Common mistakes

- **Writing before reading the SERP.** Produces a copy of position 1 with less authority: unrankable and uncitable by design.
- **Burying the answer.** 300 words of context before the point; AI engines extract from the top of the page, and readers bounce.
- **"As mentioned above" cross-references.** Breaks chunk autonomy; the retrieved passage becomes unusable on its own.
- **Citing competitors as sources.** Donates authority and a citation path on your own keyword.
- **Nofollow on hand-picked sources.** Undermines the sourced-content signal you are trying to send.
- **Shorter rewrites.** Replacing a 1500-word ranking page with a 700-word version loses the coverage that earned the ranking.
- **Date-only refreshes.** Google compares versions; unchanged content with a new date is deceptive freshness. Flag the risk.
- **Invented FAQ questions.** Use People Also Ask; made-up questions match no real query and no fan-out sub-query.
- **Keyword stuffing.** Measured to reduce generative visibility (Princeton study) on top of the classic over-optimization risk.
- **Self-hosted video.** Page weight up, and the YouTube surface is lost. Embed instead.
- **Zero internal links to money pages.** The article ranks and sells nothing; informational traffic dies on the page.
- **Heavy images.** A 1.2 MB cover image hurts Core Web Vitals on every visit. Compress to WebP under 200 KB.
- **Em dashes left in the copy.** Reads as AI output to readers and to the client. Replace each one with a comma before delivery.

## Sources

- Princeton GEO study, "GEO: Generative Engine Optimization" (KDD 2024): https://arxiv.org/abs/2311.09735
- Ahrefs, analysis of 1.4M ChatGPT prompts and citation patterns: https://ahrefs.com/blog/why-chatgpt-cites-pages/
- ALM Corp, listicle share of AI citations (single-source study, not independently replicated): https://almcorp.com/blog/ai-citations-listicles-articles-product-pages/
- Search Engine Land, query fan-out optimization guide: https://searchengineland.com/guide/how-to-optimize-for-query-fan-out
- Google patent US 11,354,342 (contextual estimation of link information gain): https://patents.google.com/patent/US11354342B2/en
- Google Search Central, guidance on AI-generated content: https://developers.google.com/search/blog/2023/02/google-search-and-ai-content
- Google spam policies (scaled content abuse): https://developers.google.com/search/docs/essentials/spam-policies
- Google, FAQ and HowTo rich result deprecation: https://developers.google.com/search/blog/2023/08/howto-faq-changes
- Google, title link guidance: https://developers.google.com/search/docs/appearance/title-link
- Word counts, cadence, link counts, source types, image budgets: field heuristics from 115+ agency audits, not Google statements.
