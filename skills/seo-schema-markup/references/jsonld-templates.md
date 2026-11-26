# JSON-LD templates

Ready-to-adapt blocks for the types that still pay in 2026. Conventions:

- Placeholders use {{DOUBLE_BRACES}}. Resolve every one before shipping: search the build output for {{ as a release check.
- Stable @id values follow the pattern {{SITE_URL}}/#organization and {{PAGE_URL}}#article so nodes can reference each other across pages.
- Delete any optional property you cannot fill truthfully. A missing field is valid; an invented value is a policy violation.
- Every value must match the visible page (price, rating, dates, names).
- Serve these server-rendered in a script tag of type application/ld+json. Client-side injection is invisible to AI crawlers (see the seo-technical skill).

## Organization (sitewide entity anchor)

Only list sameAs profiles that actually exist; wrong or dead profile links fragment the entity instead of consolidating it.

    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "@id": "{{SITE_URL}}/#organization",
      "name": "{{BRAND}}",
      "legalName": "{{LEGAL_NAME}}",
      "url": "{{SITE_URL}}/",
      "logo": {
        "@type": "ImageObject",
        "url": "{{SITE_URL}}/assets/logo-600x600.png",
        "width": 600,
        "height": 600
      },
      "description": "{{ONE_FACTUAL_SENTENCE}}",
      "foundingDate": "{{YYYY-MM-DD}}",
      "founder": {
        "@type": "Person",
        "name": "{{FOUNDER_NAME}}"
      },
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer support",
        "email": "{{SUPPORT_EMAIL}}"
      },
      "sameAs": [
        "https://www.linkedin.com/company/{{LINKEDIN_SLUG}}",
        "https://www.crunchbase.com/organization/{{CRUNCHBASE_SLUG}}",
        "https://www.g2.com/products/{{G2_SLUG}}",
        "https://en.wikipedia.org/wiki/{{WIKIPEDIA_PAGE}}"
      ]
    }

## WebSite

    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "@id": "{{SITE_URL}}/#website",
      "url": "{{SITE_URL}}/",
      "name": "{{BRAND}}",
      "publisher": { "@id": "{{SITE_URL}}/#organization" },
      "inLanguage": "{{LANG_CODE}}"
    }

## Article / BlogPosting

dateModified only changes when the content meaningfully changes. Auto-bumping it on every deploy teaches engines to ignore it.

    {
      "@context": "https://schema.org",
      "@type": "Article",
      "@id": "{{PAGE_URL}}#article",
      "headline": "{{TITLE_UNDER_110_CHARS}}",
      "description": "{{META_DESCRIPTION}}",
      "image": "{{FEATURED_IMAGE_URL}}",
      "datePublished": "{{YYYY-MM-DD}}",
      "dateModified": "{{YYYY-MM-DD_ONLY_WHEN_REALLY_UPDATED}}",
      "author": {
        "@type": "Person",
        "@id": "{{SITE_URL}}/team/{{AUTHOR_SLUG}}/#person",
        "name": "{{AUTHOR_NAME}}",
        "url": "{{SITE_URL}}/team/{{AUTHOR_SLUG}}/"
      },
      "publisher": { "@id": "{{SITE_URL}}/#organization" },
      "mainEntityOfPage": "{{PAGE_URL}}"
    }

## Product + Offer + AggregateRating

Remove the aggregateRating block entirely when the page displays no reviews. Price and availability must match the visible offer.

    {
      "@context": "https://schema.org",
      "@type": "Product",
      "@id": "{{PAGE_URL}}#product",
      "name": "{{PRODUCT_NAME}}",
      "image": ["{{IMAGE_URL_1}}", "{{IMAGE_URL_2}}"],
      "description": "{{PRODUCT_DESCRIPTION}}",
      "sku": "{{SKU}}",
      "brand": { "@type": "Brand", "name": "{{BRAND}}" },
      "offers": {
        "@type": "Offer",
        "url": "{{PAGE_URL}}",
        "price": "{{PRICE_AS_DISPLAYED}}",
        "priceCurrency": "{{ISO_CURRENCY}}",
        "availability": "https://schema.org/InStock",
        "priceValidUntil": "{{YYYY-MM-DD}}"
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "{{REAL_AVERAGE_AS_DISPLAYED}}",
        "reviewCount": "{{REAL_COUNT_AS_DISPLAYED}}"
      }
    }

## Review (each review displayed on the page)

One Review per review the visitor can read on that page, nested in the item reviewed (Product, SoftwareApplication, Course, Event), next to the AggregateRating. Author, date, rating and text are the ones displayed; a review shown without a star rating keeps reviewBody and drops reviewRating.

    "review": [
      {
        "@type": "Review",
        "author": { "@type": "Person", "name": "{{REVIEWER_NAME_AS_DISPLAYED}}" },
        "datePublished": "{{YYYY-MM-DD}}",
        "reviewRating": { "@type": "Rating", "ratingValue": "{{STARS_AS_DISPLAYED}}", "bestRating": "5" },
        "reviewBody": "{{REVIEW_TEXT_AS_DISPLAYED}}"
      }
    ]

## SoftwareApplication (SaaS, app, browser extension)

The node that carries the plans and the reviews of a software product: eligible for stars, where Organization is not. One Offer per plan shown on the page; drop aggregateRating and review when the page displays no review.

    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "@id": "{{SITE_URL}}/#software",
      "name": "{{PRODUCT_NAME}}",
      "applicationCategory": "BusinessApplication",
      "operatingSystem": "Web",
      "url": "{{SITE_URL}}/",
      "publisher": { "@id": "{{SITE_URL}}/#organization" },
      "offers": [
        {
          "@type": "Offer",
          "name": "{{PLAN_NAME}}",
          "price": "{{PRICE_AS_DISPLAYED}}",
          "priceCurrency": "{{ISO_CURRENCY}}",
          "priceSpecification": {
            "@type": "UnitPriceSpecification",
            "price": "{{PRICE_AS_DISPLAYED}}",
            "priceCurrency": "{{ISO_CURRENCY}}",
            "billingDuration": "P1M",
            "unitCode": "MON"
          }
        }
      ],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "{{REAL_AVERAGE_AS_DISPLAYED}}",
        "reviewCount": "{{REAL_COUNT_AS_DISPLAYED}}"
      },
      "review": [ "{{REVIEW_NODES_AS_ABOVE}}" ]
    }

Declare it fully once (homepage or pricing page) and reference it by @id elsewhere. A testimonials band repeated on every page is marked up on the page about the software, not on every blog post.

## VideoObject

One per video the page plays. thumbnailUrl and uploadDate are required for video results; duration in ISO 8601 (PT2M30S = 2 minutes 30 seconds).

    {
      "@context": "https://schema.org",
      "@type": "VideoObject",
      "name": "{{VIDEO_TITLE}}",
      "description": "{{VIDEO_DESCRIPTION}}",
      "thumbnailUrl": "{{THUMBNAIL_URL}}",
      "uploadDate": "{{YYYY-MM-DD}}",
      "duration": "{{PT2M30S}}",
      "embedUrl": "{{EMBED_URL}}"
    }

## LocalBusiness

Name, address, and phone identical to the Google Business Profile, character for character (see the seo-local skill). Use the most specific subtype that fits (Dentist, Restaurant, Plumber) instead of plain LocalBusiness when one exists.

    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "@id": "{{SITE_URL}}/#localbusiness",
      "name": "{{BUSINESS_NAME_EXACTLY_AS_ON_GBP}}",
      "url": "{{SITE_URL}}/",
      "image": "{{STOREFRONT_PHOTO_URL}}",
      "telephone": "{{E164_PHONE}}",
      "priceRange": "{{SYMBOLIC_RANGE}}",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "{{STREET}}",
        "addressLocality": "{{CITY}}",
        "postalCode": "{{POSTAL_CODE}}",
        "addressCountry": "{{ISO_COUNTRY}}"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "{{LAT}}",
        "longitude": "{{LON}}"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
          "opens": "09:00",
          "closes": "18:00"
        }
      ],
      "sameAs": ["{{GOOGLE_BUSINESS_PROFILE_URL}}"]
    }

## BreadcrumbList

The last item carries no "item" URL: it is the current page.

    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "{{SITE_URL}}/" },
        { "@type": "ListItem", "position": 2, "name": "{{SECTION}}", "item": "{{SECTION_URL}}" },
        { "@type": "ListItem", "position": 3, "name": "{{CURRENT_PAGE_NAME}}" }
      ]
    }

## Person (author)

    {
      "@context": "https://schema.org",
      "@type": "Person",
      "@id": "{{SITE_URL}}/team/{{AUTHOR_SLUG}}/#person",
      "name": "{{AUTHOR_NAME}}",
      "url": "{{SITE_URL}}/team/{{AUTHOR_SLUG}}/",
      "image": "{{HEADSHOT_URL}}",
      "jobTitle": "{{JOB_TITLE}}",
      "worksFor": { "@id": "{{SITE_URL}}/#organization" },
      "sameAs": [
        "https://www.linkedin.com/in/{{LINKEDIN_SLUG}}",
        "https://x.com/{{X_HANDLE}}"
      ]
    }

## Course (training, mentoring or coaching program)

For a program with a curriculum (modules, sessions, a defined workload). One-to-one coaching with no syllabus is a Service instead. Show the price on the page if it is in the markup.

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "@id": "https://example.com/program/#course",
  "name": "Program name",
  "description": "What the learner will be able to do at the end, in one or two sentences.",
  "provider": { "@id": "https://example.com/#organization" },
  "inLanguage": "fr",
  "educationalLevel": "Beginner to intermediate",
  "offers": {
    "@type": "Offer",
    "category": "Paid",
    "price": "997",
    "priceCurrency": "EUR",
    "url": "https://example.com/program/"
  },
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "Online",
    "courseWorkload": "PT30H"
  }
}
```

`courseWorkload` is the total estimated time to complete the program as an ISO 8601 duration (PT30H = 30 hours); for a recurring rhythm (1 hour a day) use `courseSchedule` with `repeatFrequency` and `duration` instead. Never mark up a price, a rating or a session that the page does not show.

## Wiring it together: one graph

A blog post page declaring Article, its author, and the publisher in a single @graph. The Organization and Person nodes can be short references because the full nodes live on the homepage and the author page under the same @id values.

    {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Organization",
          "@id": "https://example.com/#organization",
          "name": "Example Co",
          "url": "https://example.com/"
        },
        {
          "@type": "Person",
          "@id": "https://example.com/team/jane/#person",
          "name": "Jane Doe",
          "worksFor": { "@id": "https://example.com/#organization" }
        },
        {
          "@type": "Article",
          "@id": "https://example.com/blog/example-post/#article",
          "headline": "Example headline",
          "datePublished": "2026-04-02",
          "dateModified": "2026-05-28",
          "author": { "@id": "https://example.com/team/jane/#person" },
          "publisher": { "@id": "https://example.com/#organization" },
          "mainEntityOfPage": "https://example.com/blog/example-post/"
        }
      ]
    }

## Validation routine

1. https://validator.schema.org for syntax and vocabulary.
2. https://search.google.com/test/rich-results for Google eligibility. Both free, no API key.
3. curl the production URL after deploy and confirm the block survived the build server-side.
