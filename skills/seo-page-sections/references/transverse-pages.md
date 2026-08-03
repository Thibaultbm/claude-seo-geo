# Transverse Pages: Homepage, Pricing, About, Contact

Fill-in wireframes for the four page types that every site has and no content skill owns. Block lists and levels live in `page-type-matrix.md`; this file is the copywriting layer. Replace every `{placeholder}`, in the language of the site.

These four pages are audited last and matter first. The homepage is the strongest internal link source on the site, pricing is the most abandoned page, about is the entity anchor that validates every author byline, and contact is where a working funnel silently breaks.

## Homepage

The failure mode is a slogan where the offer should be. A visitor who cannot say what the business does after five seconds leaves, and a model that cannot say it after parsing the HTML will not name the company when asked for a recommendation in its category.

### Metadata

```
Title:            {what the business does} for {audience} | {brand}        (50-60 chars)
Meta description: {outcome}. {proof number}. {call to action}.             (max 160 chars)
H1:               {what the business does, in plain words}
Schema:           Organization (+ sameAs to every official profile), WebSite
```

Put the category term in the title. "{Brand} | Home" wastes the highest-authority title on the site.

### Skeleton

```
[HERO]
H1: {what you do} for {who}
Sub: {the outcome they get} + {one proof: rating, client count, years, volume}
CTA: {primary action}          Secondary: {low-commitment action}
[Social proof strip: {4-8 logos, or the review platform rating with its count}]

[PROBLEM / BENEFITS]  3 to 6 items
H2: {the problem you solve, in the visitor's words}
- {problem} -> {what changes}, one line each, at least one with a number

[OFFER OVERVIEW]  the routing block
H2: {what we do}
- {Service or category 1}: one line + link to its page
- {Service or category 2}: ...
Every money page on the site is linked from here. This is the block that makes
the homepage worth its authority.

[HOW IT WORKS]  3 to 5 numbered steps with durations

[PROOF]
H2: {results / what clients say}
- {2-3 reviews: first name, situation, problem, result}
- {1 case study with a number and a timeframe} -> link

[WHO IT IS FOR / NOT FOR]
Two short lists. Qualification raises conversion and relevance at the same time.

[DESCRIPTIVE TEXT BLOCK]  300+ words
H2: {the category term, phrased as a question buyers ask}
Prose that a model can actually read. A homepage of headlines alone gives
retrieval nothing to work with.

[CTA REPEAT]
[FOOTER: contact details, legal links, sitemap-level navigation]
```

### Checks

- [ ] H1 says what the business does, not what it believes
- [ ] Category term appears in the title, H1 and first 100 words
- [ ] Every money page is linked from the body, not only from the menu
- [ ] Proof is specific: numbers, names, dates
- [ ] Organization schema with `sameAs` to LinkedIn and every official profile
- [ ] Contact details reachable from the homepage
- [ ] 300+ words of real prose somewhere on the page

## Pricing page

The most abandoned page type there is, and the one with the clearest fix. A price in an image or injected by JavaScript is invisible to AI crawlers and unusable to comparison surfaces.

### Metadata

```
Title:            {product or service} pricing {and plans} | {brand}       (50-60 chars)
Slug:             /pricing/ or /tarifs/
H1:               {product} pricing
Schema:           Offer or PriceSpecification per plan, matching the visible prices
```

### Skeleton

```
H1: {product} pricing
Sub: {one line: what determines the price, or the promise}

[PLAN CARDS]  price as HTML text, currency, billing period
- {Plan A}: {price}/{period}. For {who}. {3-5 included items}. CTA
- {Plan B}: {price}/{period}. MOST POPULAR, for {who}. {includes everything in A, plus...}. CTA
- {Plan C or Enterprise}: {price or "contact us"}. For {who}. CTA

[COMPARISON TABLE]  same criteria, same order, every plan
| Feature | A | B | C |
Include the rows where a plan does NOT have the feature. Ambiguity here is the
top pre-sale support ticket.

[TOTAL COST CLARITY]
H2: {what else it costs}
Setup fees, overage rates, minimum term, taxes, what happens past the limits.
Answer the hidden-cost objection before it forms.

[GUARANTEE / TRIAL]
{duration}, {conditions}, {how to cancel}. Matches the terms page word for word.

[SOCIAL PROOF]  next to the plans, not in a distant section

[FAQ]  required, and these are the real questions
H3: {What happens if I go over my limit?}
H3: {Can I change plan later?}
H3: {How do I cancel?}
H3: {Do you offer refunds?}
H3: {Are taxes included?}
H3: {Is there a discount for annual billing / nonprofits / teams?}

[CONTACT ROUTE]  for the non-standard case
```

### If prices cannot be published

Publish the drivers and a range. "From {X}, depending on {driver 1}, {driver 2}, {driver 3}" outperforms silence at every step of the funnel, and it captures the "{service} price" query that a quote form never will. A pricing page with no number ranks for nothing and converts the already-convinced only.

### Checks

- [ ] `curl` on the page returns the prices as text
- [ ] Currency and billing period stated on every price
- [ ] Comparison table includes the exclusions, not only the inclusions
- [ ] Setup fees, overage and minimum term stated
- [ ] Cancellation and refund answered in the FAQ
- [ ] Schema prices match the displayed prices exactly
- [ ] Recommended plan marked, with who it is for

## About page

The entity anchor. Everything an assistant says about the company when asked "who is {brand}" is assembled from this page plus the profiles it links to. It is also the page that validates every author byline elsewhere on the site, so its weakness propagates.

### Metadata

```
Title:            About {brand} | {what the business does}                 (50-60 chars)
Slug:             /about/ or /a-propos/
H1:               About {brand}
Schema:           Organization (+ sameAs), Person per named team member
```

### Skeleton

```
H1: About {brand}
Lead: {what the company does}, {since when}, {for whom}, {one proof number}.
Answer-first: the facts before the story.

[STORY]
H2: {why we started}
{Why the business exists, what was wrong with the alternatives, what changed.}
This is the one page where narrative outperforms optimization. Keep it honest
and specific; the generic founding story is worse than none.

[TEAM]
H2: {who we are}
- {Full name}, {role}. {Credential that can be checked}. {Link to LinkedIn}
  [real photo, never stock]

[FACTS]  the block assistants reuse
- Founded: {year}          - Team size: {n}
- Locations: {cities}      - Clients served: {n}
- Registration: {legal entity, number}
- Certifications / memberships: {with links}

[PROOF]
H2: {press, awards, partnerships}
{Third-party validation, each with an outbound link to the source.}

[METHOD OR VALUES]  optional
Only if it states something a competitor could not copy word for word.

[CONTACT + CTA]
{Address, contact route, and a link to the services or products.}
```

### Consistency rule

The company name, one-line description, founding year and location must be identical on this page, on LinkedIn, in directories, on review platforms and in the schema. Divergence fragments the entity, which is the most common cause of a brand being described wrongly, or not at all, by AI assistants. Audit the divergence before rewriting the prose.

### Checks

- [ ] Real photos of real, named people
- [ ] At least one credential per person, verifiable off-site
- [ ] Founding year, size, location, legal entity stated
- [ ] Every press or award claim links to its source
- [ ] Organization + Person schema with `sameAs`
- [ ] Name and one-line description match every off-site profile

## Contact page

Where a working funnel silently breaks. Audit it by using it: submit the form and see what happens.

### Metadata

```
Title:            Contact {brand}                                          (50-60 chars)
Slug:             /contact/
H1:               Contact {brand}
Schema:           ContactPoint within Organization; LocalBusiness if there is a location
```

### Skeleton

```
H1: Contact {brand}
Lead: {which channel to use for what}, and {response time}.

[CHANNELS]  all as text, all linked
- Phone: {number}          -> tel: link
- Email: {address}         -> mailto: link
- Address: {full postal address}
- {Chat, WhatsApp, or other, if genuinely monitored}

[RESPONSE TIME]
"{We answer within X}" . The unanswered question of every contact page.

[ROUTING]
- Sales: {channel}
- Support: {channel}
- Press, partnerships: {channel}
Sends the wrong request to the right place instead of to the void.

[FORM]  minimum viable fields
{Name}, {email}, {message}, and only the fields a human will actually use.
Required fields marked. Real confirmation state after submit.

[HOURS]        {days and times}
[MAP]          {if there is a physical location}
[FAQ LINK]     {deflect the answerable questions}
```

### Checks

- [ ] Phone and email are text with `tel:` and `mailto:`, never images
- [ ] Form submits, and the confirmation state is visible and unambiguous
- [ ] Response time stated
- [ ] Field count minimized; no phone number demanded for a document download
- [ ] Address matches the Google Business Profile byte for byte
- [ ] Form submissions actually arrive (test it, then check the inbox and the spam folder)
