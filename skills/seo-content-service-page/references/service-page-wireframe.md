# Service Page Wireframe: Fill-In Template

Copy this skeleton when drafting. Replace every {placeholder}. Heading levels are mandatory; section order is mandatory. Delete nothing without a documented reason.

## Metadata

```
Title:            {service keyword} in {city, if local} | {brand}        (50-60 chars)
Slug:             /{service-keyword}-{city}/
Meta description: {outcome promise}. {proof number}. {call to action}.   (max 160 chars)
Primary keyword:  {exact buyer phrase}
Schema:           Service or LocalBusiness, Person (founder), Organization + sameAs, FAQPage
```

## Page skeleton

```
H1: {service keyword, phrased for a human}

[BLOCK 1: HERO]
- Subline: {who it is for} + {one proof element: rating, client count, years}
- CTA button: {primary action: get a quote / book / call}
- First paragraph: contains {primary keyword} (+ {city}) in the first 100 words

[BLOCK 2: LOGOS]
- {4-8 client logos, press logos, certifications, review platform rating}

[BLOCK 3: BENEFITS]  (3-6 cards, outcomes not features)
H2: {what the client gets, summarized}
- Card: {feature} rewritten as {concrete outcome the client obtains}
- Card: ...
CTA

[BLOCK 4: PROCESS]
H2: How it works
1. {step: first contact, what happens, how long}
2. {step: work performed}
3. {step: delivery and result}
4. {optional step: follow-up}
CTA

[BLOCK 5: FOUNDER]
H2: Who you will work with
- Real photo of {founder full name}, not stock
- {2-4 sentences: why they do this work, for whom, since when, one human detail}

[BLOCK 6: SEO TEXT BLOCK]  (750+ words minimum, benchmark top 3 competitors)
H2: {real question buyers ask, e.g. "What does {service} include?"}
- Direct 2-4 sentence answer, then detail
H2: {real question, e.g. "How much does {service} cost in {city}?"}
- Price or price range in plain text, then what drives the price
H2: {real question, e.g. "How long does {service} take?"}
- Direct answer, then detail
H3 subsections as needed: methods, tools, deliverables, who it is for / not for
- Include: 1+ sourced statistic, 1+ expert or client quotation (GEO layer)

[BLOCK 7: REVIEWS]
H2: What clients say
- {First name}, {situation}: "{problem} ... {result with a number if possible}"
- {3+ reviews; embed video reviews when available}
CTA

[BLOCK 8: FAQ]
H2: Frequently asked questions
H3: {People Also Ask question 1}  -> 2-4 sentence direct answer
H3: {PAA question 2}              -> 2-4 sentence direct answer
H3: {sales objection as question} -> 2-4 sentence direct answer

[BLOCK 9: FINAL CTA + RELATED]
- CTA repeated, one line
- 2-3 related blog posts (each must link back to this page)
```

## City page variant (child of a region page)

Use for "service + city" pages under a parent region page. Everything above applies, plus:

```
Title:  {service keyword} {city} | {brand}
H1:     {service keyword} in {city}
URL:    /{service-keyword}-{city}/
```

Mandatory unique local substance (the anti-doorway test):

- 1+ review from a client located in {city}
- 1+ completed project in {city} with a real photo
- City specifics: neighborhoods served, response time from base, local rules or permits
- Local phone number if one exists
- {city} present in: title, URL, H1, meta description, first paragraph, 1+ image alt
- Link up to the parent region page and to the main service page

Side-by-side test before publishing: open this city page next to another one. If only the city name differs, the page is a doorway page (Google spam policy risk). Add real local substance or do not publish.

## Bookable service variant (e-tourism, experiences, appointments)

Use when the service is a reservable offer (an activity, an experience, a slot). The 9 blocks still apply; the hero and proof shift toward booking:

```
- Breadcrumb (Home > Category > this offer)
- Image slider of the real offer at the top, with a persistent "Book" CTA
- Short article describing the experience (doubles as the SEO text block, block 6)
- Options and variants (durations, dates, formats, prices in plain text)
- Reviews from past customers (block 7)
- Internal links to related offers
```

## Pre-publish checklist

- [ ] One service, one intent, one primary keyword
- [ ] All 9 blocks present, in order
- [ ] Word count meets or beats the top 3 ranking competitors
- [ ] CTA above the fold + after blocks 3, 4, 7, and at the end
- [ ] Founder photo is real, founder is named
- [ ] Price or price range in plain HTML text
- [ ] Every H2 in the text block is a question with a direct 2-4 sentence answer
- [ ] 1+ sourced statistic and 1+ quotation in the text block
- [ ] FAQ has 3+ real questions
- [ ] 2-3 related posts linked, each linking back
- [ ] Schema added via the seo-schema-markup skill
- [ ] Verified with the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py)
