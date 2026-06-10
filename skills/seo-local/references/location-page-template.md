# Location Page Template (One Page per Establishment)

Each physical location or branch gets its own page, linked from its Google Business Profile. For full copywriting structure (the 9-block wireframe) and city-page architecture, use the seo-content-service-page skill; this template covers the location-specific layer.

## Metadata pattern

```
Title:            {primary service} in {city} | {brand}            (50-60 chars)
Slug:             /{city}/ or /{service}-{city}/
H1:               {primary service} in {city}
Meta description: {promise} in {city}. {proof}. {call to action}.  (max 160 chars)
First paragraph:  {service} + {city} within the first 100 words
Image alts:       describe the image, include {city} where natural
```

## Required on-page elements

- [ ] Full NAP, byte-identical to the Google Business Profile (canonical format)
- [ ] Embedded Google map of the location
- [ ] Opening hours, identical to the profile
- [ ] Services offered at this location, each with price or price range in plain HTML
- [ ] Areas and neighborhoods served from this location
- [ ] Real photos: storefront, team, completed local jobs
- [ ] Reviews from customers of this location (first name + situation + problem + result)
- [ ] Local proof: projects, partnerships, local press mentions
- [ ] FAQ: 3+ questions buyers in this city ask
- [ ] CTA above the fold and after each major section
- [ ] Link to and from the matching Google Business Profile
- [ ] Links to the parent services hub and related city pages

## LocalBusiness schema skeleton

Adapt the type (Plumber, Dentist, Attorney, Restaurant...) to the most specific schema.org subtype available. Values must match the profile exactly. Validation and extensions: seo-schema-markup skill.

```json
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "name": "Dupont Plomberie",
  "image": "https://example.com/photos/storefront-lyon.jpg",
  "url": "https://example.com/emergency-plumber-lyon/",
  "telephone": "+33 4 00 00 00 00",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "12 rue de la Republique",
    "addressLocality": "Lyon",
    "postalCode": "69002",
    "addressCountry": "FR"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 45.764,
    "longitude": 4.8357
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "19:00"
    }
  ],
  "areaServed": ["Lyon", "Villeurbanne", "Caluire-et-Cuire"],
  "sameAs": [
    "https://www.facebook.com/dupontplomberie",
    "https://www.linkedin.com/company/dupontplomberie"
  ]
}
```

Notes:

- Do not embed aggregateRating or review markup about your own business unless the reviews are genuinely displayed on the page and eligible; Google ignores self-serving review markup in several contexts (details: seo-schema-markup skill).
- For service-area businesses with a hidden address, keep the address out of the public page if it is a home address; lead with areaServed.

## Multi-location index

When a brand has several locations:

- One index page (/locations/) listing every branch with NAP and a link to each location page
- Each location page targets its own city, never a shared "we are everywhere" page
- Each Google Business Profile links to its own location page, not the homepage

## GEO check before publishing

- [ ] Every fact an assistant would quote (areas, response time, prices, hours) is in plain HTML text
- [ ] Reviews shown on the page mention the service and the city
- [ ] NAP matches every other citation on the web
- [ ] Page is crawlable by AI agents (seo-technical skill)
