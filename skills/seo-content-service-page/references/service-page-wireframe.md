# Service Page Wireframe: Fill-In Template

Copy this skeleton when drafting (Phase 4 of the skill). Replace every {placeholder}. Heading levels are mandatory; section order is mandatory. Delete nothing without a documented reason. Each block names the spec rows (SVC-xx in SKILL.md, C-xx in skills/seo-geo-audit/references/common-page-spec.md) it satisfies. Facts the owner has not confirmed stay as `{to confirm}`.

## Metadata (SVC-03, C-01, C-02, C-23)

```
Title:            {service keyword} in {city, if local} | {brand}        (50-60 chars)
Slug:             /{service-keyword}-{city}/
Meta description: {outcome promise}. {proof number}. {call to action}.   (max 160 chars)
Primary keyword:  {exact buyer phrase}
Schema:           Service (or LocalBusiness subtype), Organization reference + sameAs,
                  Person (founder) + sameAs, BreadcrumbList, FAQPage (optional; no rich result since May 2026)
```

## Page skeleton

```
Breadcrumb: Home > Services > {service}                                   (C-19, SVC-21)
H1: {service keyword, phrased for a human, as the outcome}                (SVC-03, SVC-04)

[BLOCK 1: HERO]                                                           (SVC-04, SVC-02)
- Subline: {who it is for} + {one proof element: rating, client count, years}
- CTA button: {primary action: get a quote / book / call}, sticky on mobile
- First paragraph: contains **{primary keyword} (+ {city})** in bold, in the first 100 words
- No carousel, no autoplay video before the promise

[BLOCK 2: LOGOS]                                                          (SVC-05)
- {4-8 client logos, press logos, certifications, review platform rating with count and date}

[BLOCK 3: BENEFITS]  (3-6 cards, outcomes not features)                  (SVC-06)
H2: {what the client gets, summarized}
- Card: {feature} rewritten as {concrete outcome the client obtains} + {number}
- Card: ...
CTA

[BLOCK 4: PROCESS]                                                        (SVC-07)
H2: How it works
1. {step: first contact, what happens, how long}
2. {step: work performed, how long}
3. {step: delivery and result}
4. {optional step: follow-up}
CTA

[BLOCK 5: FOUNDER]                                                        (SVC-08, C-20)
H2: Who you will work with
- Real photo of {founder full name}, not stock (alt = name)
- {role}; {2-4 sentences: why they do this work, for whom, since when, one human detail}
- Checkable credentials: {registration number, certification, years, results}, each linked to the third-party record
- Link to the about page; real profile URLs ({LinkedIn}, {registry}), the same URLs in Person sameAs

[BLOCK 6: SEO TEXT BLOCK]  (750+ words minimum, or the competitor median if higher)   (SVC-09)
H2: {real question buyers ask, e.g. "What does {service} include?"}
- Direct 2-4 sentence answer, then detail: deliverables, scope, what is excluded
H2: {real question, e.g. "How much does {service} cost in {city}?"}          (SVC-10)
- Price, range or "from" in plain text, then what drives the price; "rates as of {month year}"
- Or: why the price is given after a call, and what the call covers
H2: {real question, e.g. "How long does {service} take?"}
- Direct answer, then detail
H2: {real question, e.g. "Is {service} right for you?"}                     (SVC-11)
- For: {list}. Not for: {list}. Service area: {cities, response time} if local
H2: {real question, e.g. "{service} or {alternative}: which one?"}           (SVC-16)
- HTML table: this service vs {DIY / freelancer / in-house / other provider type}, 5-8 buyer criteria,
  at least one row where an alternative wins
H3 subsections as needed: methods, tools, guarantees, why this provider (proof recap with numbers)
- Include: 1+ sourced statistic, 1+ expert or client quotation (SVC-20, GEO layer)
- Bold one fact or benefit every 100-150 words, never whole sentences (SVC-02)

[BLOCK 7: REVIEWS]                                                        (SVC-12, SVC-13, SVC-17)
H2: What clients say
- Rating: {score}/5 on {platform}, {count} reviews, read on {date}
- {First name}, {situation}: "{problem} ... {result with a number if possible}"
- {3+ reviews; embed video reviews when available, with a text summary}
- Case result: {client}, {before}, {after}, {timeframe}, {date}, link to the full case study
- Guarantee, only if one exists: {exact terms, duration, condition}
CTA

[BLOCK 8: FAQ]                                                            (SVC-14)
H2: Frequently asked questions
H3: {People Also Ask question 1}  -> 2-4 sentence direct answer
H3: {PAA question 2}              -> 2-4 sentence direct answer
H3: {sales objection as question} -> 2-4 sentence direct answer

[BLOCK 9: FINAL CTA + RELATED]                                            (SVC-15, SVC-21)
- CTA repeated, one line
- 2-3 related blog posts (each must link back to this page)
- Link to the services hub and 1-2 sibling services

[FOOTER, site-wide]                                                       (SVC-18, C-20, C-24)
- Real social profiles; legal notices and registrations for regulated professions;
  "results not guaranteed" wording next to any results claim
```

## City page variant (child of a region page, SVC-24)

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

Side-by-side test before publishing: open this city page next to another one. If only the city name differs, the page is a doorway page (Google spam policy risk). Add real local substance or do not publish. Audit with `section_audit.py --type location`.

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

## JSON-LD skeleton (SVC-22, SVC-23)

One graph per page. The Organization is defined once (on the homepage) and referenced here by `@id`; the founder Person likewise. Keep a property only when the page shows its value: drop `offers` when no price is visible, drop `areaServed` when the service is not tied to a place. No empty strings, no Review or AggregateRating about your own business.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "@id": "https://example.com/emergency-plumber-lyon/#service",
      "name": "Emergency plumber in Lyon",
      "serviceType": "Emergency plumbing",
      "description": "{one-sentence description matching the page intro}",
      "url": "https://example.com/emergency-plumber-lyon/",
      "provider": { "@id": "https://example.com/#organization" },
      "areaServed": { "@type": "City", "name": "Lyon" },
      "offers": {
        "@type": "Offer",
        "priceCurrency": "EUR",
        "priceSpecification": { "@type": "PriceSpecification", "minPrice": 90, "maxPrice": 250, "priceCurrency": "EUR" }
      }
    },
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Dupont Plomberie",
      "url": "https://example.com/",
      "sameAs": ["{real profile URL}", "{real profile URL}"],
      "founder": { "@id": "https://example.com/about/#person" }
    },
    {
      "@type": "Person",
      "@id": "https://example.com/about/#person",
      "name": "{founder full name}",
      "jobTitle": "{role}",
      "url": "https://example.com/about/",
      "sameAs": ["{LinkedIn profile URL}", "{registry or certification URL}"]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
        { "@type": "ListItem", "position": 2, "name": "Services", "item": "https://example.com/services/" },
        { "@type": "ListItem", "position": 3, "name": "Emergency plumber in Lyon", "item": "https://example.com/emergency-plumber-lyon/" }
      ]
    }
  ]
}
```

For a local single-location business whose page is the business itself, replace Service with the matching LocalBusiness subtype (Plumber, Dentist, LegalService) carrying `address`, `telephone` and `openingHoursSpecification` exactly as shown on the page. Field rules and eligibility: seo-schema-markup.

## Pre-publish checklist (feeds the acceptance test)

- [ ] One service, one intent, one primary keyword (SVC-01)
- [ ] All 9 blocks present, in order
- [ ] Word count meets or beats the competitor median from page_benchmark.py (SVC-09, C-08)
- [ ] Keyword bold in the first paragraph, one bold fact every 100-150 words, placement 60%+, no term above 2.5% (SVC-02)
- [ ] CTA above the fold + after blocks 3, 4, 7, and at the end (SVC-15)
- [ ] Founder photo is real, founder is named, credentials link to checkable records, about page linked (SVC-08)
- [ ] Price or price range in plain HTML text, or why it comes after a call (SVC-10)
- [ ] Every H2 in the text block is a question with a direct 2-4 sentence answer (SVC-09)
- [ ] 1+ sourced statistic and 1+ quotation in the text block (SVC-20)
- [ ] Rating shown with platform, count and date read; reviews real and formatted (SVC-13)
- [ ] Comparison table versus the alternatives when the buyer weighs them (SVC-16)
- [ ] Results claims carry a disclaimer, superlatives a source, regulated topics their notices (SVC-18)
- [ ] FAQ has 3+ real questions (SVC-14)
- [ ] 2-3 related posts linked, each linking back; breadcrumb present (SVC-21)
- [ ] JSON-LD graph valid, no empty nodes, no self-serving review markup (SVC-22, SVC-23)
- [ ] Zero em dashes and en dashes in every delivered field (C-25)
- [ ] Verified with seo_audit.py, section_audit.py --type service and page_benchmark.py (acceptance test in SKILL.md)
