# Section Library

How to build each block, not just name it. Companion to SKILL.md phase 4 and to `page-type-matrix.md`.

Each entry gives: what the block is, why it earns its place with both audiences, the minimum bar (below it, report the block as "below bar" rather than present), how to write it, the schema that goes with it, and the ways it usually fails.

Two rules apply to every block in this file. Never assert a fact that is not in the vault, on the site, or from the owner: use `{placeholder}` and collect the placeholders as questions. Never mark up anything a human cannot see on the rendered page.

## Breadcrumb

**What.** A horizontal trail of plain links: Home > Category > Sub-category > Current page. The current page is text, not a link.

**Why.** For the visitor it answers "where am I and how do I go up one level", which is the whole navigation need on a deep page arrived at from search. For a crawler it is a second, explicit statement of the site hierarchy that does not depend on the main menu, and it is what Google renders instead of the raw URL in the result. For an assistant it is category context in one line.

**Minimum bar.** Real anchor elements with real hrefs, matching the URL path, present in raw HTML, on every page deeper than the first level.

**How to write.** Mirror the actual URL hierarchy; a breadcrumb that claims a structure the URLs do not have is worse than none. Use the category names buyers use, not internal taxonomy codes. Keep it to the real depth: do not pad with invented levels.

**Schema.** `BreadcrumbList` with `itemListElement` positions, matching the visible trail exactly.

**Fails when.** It is built from JavaScript only; it shows the current page as a link to itself; it invents a hierarchy for a flat site; it is styled as decoration with no links behind it.

## FAQ block

**What.** Three or more real questions, each an H3, each answered in 40 to 80 words, in visible HTML text, near the bottom of the page.

**Why.** It is the highest-leverage block in this library and required on eight of the eleven page types. Long-tail queries are phrased as questions, so a question heading with a direct answer underneath is the closest possible match to the query. It handles objections at the moment they form, which is a conversion mechanism, not just an SEO one. And it hands an assistant a self-contained passage it can quote without reading the whole page.

**Minimum bar.** Three questions minimum. Each one must be a question a real person asked. Each answer must answer in the first sentence, then add detail. Not an accordion that hides content from the raw HTML.

**How to write.**

1. Source real questions, in this order of quality: customer emails and support tickets, sales call recordings, on-site search logs, review complaints, People Also Ask, Reddit and forum threads, competitor FAQs. Never invent questions. If no source is available, ask the owner for the five questions they answer most often; that conversation takes two minutes and is worth more than an hour of guessing (seo-keyword-research covers the sourcing methods).
2. Keep the question in the customer's words, including the imperfect phrasing. "C'est quoi la différence avec le modèle d'avant" outranks "Quelles sont les différences entre les générations de produits".
3. Answer directly in sentence one. Then justify, qualify, or give the number. An answer that opens with "It depends" wastes the extraction.
4. Include the uncomfortable questions: price, delivery delay, what it does not do, how to cancel. Answering them builds more trust than avoiding them, and the avoided question is exactly what gets searched.
5. Cover a different intent per question. Five phrasings of the same question is one question.
6. Link out from an answer when a page answers it in depth; the FAQ doubles as an internal linking surface.

**Schema.** `FAQPage` with `Question` and `acceptedAnswer`, mirroring the visible text. Note that Google's rich result for FAQ is restricted to a narrow set of authoritative sites, so build the block for the answer itself, not for the star treatment.

**Fails when.** Questions are invented, generic ("What are your opening hours" on a page with no store), or all marketing softballs; answers are one line or three paragraphs; the block is a JavaScript accordion invisible to crawlers; the markup does not match the visible text.

**Template.**

```
H2: {Frequently asked questions / Questions frequentes}

H3: {question in the customer's exact words}
{Direct answer in one sentence.} {Two to four sentences of detail, with a number,
a condition, or a concrete example.} {Optional link to the page that goes deeper.}
```

## Definitions block

**What.** About five terms specific to the product, service or category, each defined in plain language in one or two sentences.

**Why.** It converts the non-expert buyer, who abandons when the page assumes knowledge they do not have. It adds genuine topical depth to a page that would otherwise be thin, using vocabulary that appears in nobody else's copy. And it makes the page a candidate answer for every "what is {term}" query in the category, which is a large share of the informational long tail.

**Minimum bar.** About five terms, terms actually used elsewhere on the page, defined without using the term inside its own definition.

**How to write.** Pick the terms a first-time buyer would have to look up: materials, standards, units, technical specs, industry jargon. Define in the buyer's language, then say why it matters for their decision, which is what turns a glossary into a sales asset. Keep each entry to one or two sentences.

**Schema.** `DefinedTerm` inside a `DefinedTermSet`, optional and low-value; the block works without it.

**Fails when.** The terms are obvious ("delivery: the act of delivering"); the definitions are copied from a dictionary; the block defines terms that appear nowhere else on the page.

**Template.**

```
H2: {Key terms / Definitions}

H3: {Term}
{One-sentence plain-language definition.} {One sentence on why it matters when choosing.}
```

## Comparison table

**What.** A real HTML table comparing this option against the two or three closest alternatives, criterion by criterion.

**Why.** Comparison is the last step before a purchase decision, and a buyer who has to leave the page to compare usually does not come back. For assistants, a table is the single most extractable structure on a page: rows map directly onto the "best X for Y" answers that shopping and software queries produce.

**Minimum bar.** A real `<table>` in HTML, not an image and not a set of divs styled as a table. Three or more criteria. Named alternatives, not "Brand A". Factually accurate on the day it is written.

**How to write.** Choose criteria the buyer actually decides on, not the criteria you win. Include at least one row where an alternative is genuinely better: a table where you win every row is discounted by readers and by models, and it is the fastest way to lose the credibility the block exists to create. State the date the comparison was verified. Recheck it on a schedule, since competitor pricing and features move.

**Schema.** None specific. Do not attempt to mark up competitor data as your own product.

**Fails when.** It is an image; the competitor rows are outdated or wrong; every row favors the author; the criteria differ per option so nothing is actually comparable.

## Spec table

**What.** Every measurable attribute of the product in an HTML table: dimensions, weight, materials, capacity, compatibility, standards, warranty.

**Why.** Specification queries are high-intent and specific ("stove under 350 g", "chair for 1m90"). A table is machine-readable, so an assistant filtering on a spec can retrieve the page. For the buyer it prevents the return that comes from a wrong assumption.

**Minimum bar.** Complete rather than partial, in a real table, with units. A three-row spec table on a technical product is below bar.

**How to write.** List every attribute the buyer could filter on, including the unflattering ones. Give units and the measurement condition where it matters ("boil time: 1 L in 3 min 40 s, sea level, no wind"). Keep the spec table separate from the description: the description sells, the table informs.

**Fails when.** Specs live only in a PDF or an image; units are missing; the table contradicts the description or the schema.

## Answer-first opening

**What.** The page's core promise, stated plainly, in the first 100 words: what this is, who it is for, what it costs or delivers.

**Why.** It is the passage that gets extracted into AI answers and featured snippets, and it is where a human decides whether to keep reading. A page that opens with a brand narrative forfeits both.

**Minimum bar.** The primary keyword and the core promise both appear before the fold, in prose, not only in a heading.

**How to write.** Two to four sentences. Sentence one names what the page is about in the reader's vocabulary. Sentence two says who it is for or what it produces. Sentence three carries a number: price, duration, weight, result. Then the page can breathe.

**Fails when.** The page opens with the company's history; the promise is a slogan; the first real content is below three screens of hero imagery.

## Reviews and testimonials

**What.** Real customer reviews, server-rendered as HTML text, in the format: first name, situation, problem, result.

**Why.** Specific proof from a recognizable peer is the strongest objection killer that exists, and it is the block visitors seek out. The vocabulary in real reviews is long-tail keyword material no copywriter would produce. For assistants, reviews are the sentiment evidence behind a recommendation.

**Minimum bar.** Real, attributed, in HTML text, at least three. Reviews loaded from a third-party widget after JavaScript do not count as present, since neither Google nor an AI crawler reads them reliably.

**How to write.** Do not write them. Select and format them. Prefer reviews that name a situation and a measurable result over reviews that say "great product". Place two or three near the decision point (the buy box, the CTA) and the full list lower down. If video reviews exist, put one above the written list.

**Schema.** `Review` and `AggregateRating`, only for reviews displayed on that page, only with values that match what is shown.

**Fails when.** Reviews are invented or bought; they are trapped in a JavaScript widget; the marked-up rating does not match the displayed one; the same three testimonials appear on every page of the site.

## Rating summary

**What.** Star rating and review count, next to the H1.

**Why.** Most visitors never reach the review section. Putting the aggregate at the top delivers the proof to everyone, not to the minority who scroll.

**Minimum bar.** Visible above the fold, with the count, backed by the reviews actually on the page.

**Fails when.** The rating is displayed with no reviews behind it, or is marked up without being displayed.

## Price in HTML text

**What.** The price, currency and billing period as selectable text in the HTML source.

**Why.** A price rendered as an image, injected by JavaScript, or hidden behind a form is invisible to AI crawlers, which do not execute JavaScript, and unusable to shopping surfaces. It is also the most searched attribute of any commercial page.

**Minimum bar.** `curl` on the page shows the price. If it does not, the block is missing regardless of what the browser displays.

**How to write.** For services that cannot publish a fixed price, publish the range and the drivers ("from {X}, depending on surface area, access and finish"). A range beats silence at every measured step of the funnel.

**Schema.** `Offer` with `price`, `priceCurrency`, `availability`, matching the visible price exactly.

**Fails when.** Price is an image; price comes from a script; the schema price and the displayed price disagree; a discount is displayed without the reference price rules the market requires.

## Reassurance and trust badges

**What.** Delivery time and cost, returns window, payment security, guarantee, as text near the CTA.

**Why.** These are the three or four objections alive at the exact moment of the decision. As text rather than icons, they are also machine-readable offer facts that shopping surfaces and assistants reuse.

**Minimum bar.** Text, not icon-only. Specific, not "fast delivery": a number of days, an amount, a window.

**Fails when.** Badges are decorative images with no text; the claims contradict the terms page; "free shipping" is stated without its threshold.

## Call to action

**What.** The next step, as a button or link, above the fold and repeated after each long section.

**Why.** A page with no next step converts nothing, and on a long page the decision moment arrives at unpredictable scroll depths.

**Minimum bar.** One primary action, visually dominant, phrased as the action the visitor takes. Repeated after long blocks.

**How to write.** Use the verb of the actual next step, in the visitor's words: "Get a quote", "Book a slot", "Add to cart", "Start free". Add the risk-reducer next to it where one exists ("no card required", "answer within 24 h"). Offer a secondary, lower-commitment action for the visitor who is not ready.

**Fails when.** Every button is equally weighted; the label is "Submit"; the only CTA sits at the very bottom.

## Process or how it works

**What.** The engagement, in three to five numbered steps, each with what happens and how long it takes.

**Why.** In services, the top objection is not price, it is the fear of an unknown process. Numbered steps with durations remove it. As an ordered list, the block is also cleanly extractable.

**Minimum bar.** Numbered, three or more steps, with a duration or a trigger per step.

**Fails when.** Steps are abstract ("we listen, we deliver, we care"); no durations; the process described does not match the one the business runs.

## Benefit bullets

**What.** Three to five one-line outcomes, near the top.

**Why.** Skimmers decide here, and assistants lift these lines verbatim because they are short, declarative and self-contained.

**Minimum bar.** Outcomes, not features. One line each. Concrete.

**How to write.** Translate each feature into what the buyer gets: "grade 1 titanium burner" becomes "survives wet packs and salt air without a coating". Put a number in at least one.

**Fails when.** They restate specs; they are three words long; they are adjectives ("quality, reliable, innovative").

## Author, founder and expertise block

**What.** A real person, named, photographed, with the credentials that make them credible on this subject.

**Why.** This is the E-E-A-T block. It is what separates a real business from a template, and on a page whose value is judgment (comparison, advice, service), it is what makes the judgment worth anything.

**Minimum bar.** Real name, real photo (not stock), a credential that can be checked, and a link to a profile that corroborates it.

**How to write.** Two to four sentences: why they do this work, for whom, since when, and one human detail. Link to LinkedIn or an equivalent so the claim is verifiable.

**Schema.** `Person` with `sameAs`, and `author` on the relevant content type.

**Fails when.** The byline is the company name; the photo is stock; the credentials cannot be verified anywhere else on the web.

## Social proof logos

**What.** Client logos, press mentions, certifications, review platform rating.

**Why.** Borrowed credibility, absorbed in under a second, before any claim has to be believed.

**Minimum bar.** Real and permitted. Four or more. With alt text naming each organization, since a wall of logo images is otherwise invisible to machines.

**Fails when.** Logos are used without permission; they are one client from six years ago; they are an image sprite with no alt text.

## Verdict block

**What.** On a comparison page, the explicit recommendation: who each option is for, in the first 100 words and again at the end.

**Why.** It is the passage an assistant quotes when answering "which is better". A comparison that never concludes forfeits the citation to the competitor page that does conclude.

**Minimum bar.** A named recommendation per use case, not a hedge.

**How to write.** "Choose X if {situation}. Choose Y if {different situation}." Recommend the competitor where the competitor genuinely wins; that is what makes the rest of the page believable.

**Fails when.** It concludes "it depends on your needs"; every use case resolves to the author's own product.

## Case study

**What.** One client, one problem, what was done, the measurable result, with a timeframe.

**Why.** The strongest asset a service business owns, and the most quotable proof format there is.

**Minimum bar.** Named or clearly situated client, a number, a timeframe, and permission to publish.

**Fails when.** It is anonymous and unnumbered; the result has no baseline; the client did not consent.

## Cross-links

**What.** Contextual links out to the parent page, the siblings, and the supporting content.

**Why.** They carry crawl paths, distribute authority, and give the page its topical neighborhood. Anchor text is a direct relevance signal.

**Minimum bar.** At least three contextual internal links in the body, with descriptive anchor text, not "click here" or a bare URL.

**How to write.** Link from a sentence that earns the link, not from a "related pages" dump. Send commercial pages up to their parent and across to their siblings; send informational pages down into the commercial ones. Details and silo rules: seo-internal-linking.

**Fails when.** The page is orphaned; every link uses the same anchor; the links sit only in the footer.

## Freshness signal

**What.** A visible published or updated date, and content that proves the date.

**Why.** Both readers and assistants discount undated content on any subject that moves.

**Minimum bar.** A visible date backed by real changes. Bumping the date without changing the content is a trust failure, and it is detectable.

**Fails when.** The date is only in the schema; the page says 2026 and cites 2022 data.

## Contact details and NAP

**What.** Phone, email and address as text, with `tel:` and `mailto:` links.

**Why.** A number inside an image cannot be tapped on a phone or read by a machine, and NAP consistency is the most common blocker in local ranking.

**Minimum bar.** Text, linked, and byte-identical to the Google Business Profile and to every directory listing.

**Schema.** `PostalAddress` and `ContactPoint` within `Organization` or `LocalBusiness`.

**Fails when.** Contact details are an image; the format differs between the site, the profile and the directories; there is no address at all on a business that has one.

## Form

**What.** The conversion form, with the fewest fields that make the lead usable.

**Why.** Every additional field costs completions. The expected response time is the unanswered question of every contact page.

**Minimum bar.** Works without JavaScript errors, states what happens next, shows a real confirmation state, and states the response time.

**Fails when.** Submission appears to do nothing; the confirmation is a blank page; required fields are not marked; the form asks for a phone number to send a PDF.

## Table of contents

**What.** Anchor links to the H2s, on articles and long pages.

**Why.** Navigation for the reader, and an explicit outline of the page's structure for machines.

**Minimum bar.** Real anchor links to real ids, in HTML.

**Fails when.** It is generated client-side; the anchors do not resolve.

## Guarantee and risk reversal

**What.** The refund, trial or warranty terms, stated at the decision point.

**Why.** It converts the hesitant buyer by moving the risk onto the seller, and it answers a query that gets searched by name ("{brand} refund policy").

**Minimum bar.** Specific terms with a duration and the conditions, matching the legal terms page.

**Fails when.** It says "satisfaction guaranteed" with no mechanism; the stated terms contradict the terms and conditions.

## Video

**What.** Product in use, a video review, or a founder explaining the service.

**Why.** It outperforms text for conversion where it exists, and a transcript adds indexable content the page would not otherwise have.

**Minimum bar.** Hosted so it does not wreck page speed, with a text transcript or summary on the page.

**Schema.** `VideoObject` with a real thumbnail, description and duration.

**Fails when.** The video is the only place a key fact appears; there is no transcript; the embed blocks rendering.
