# Faceted Navigation Playbook

Platform-specific parameter patterns, robots.txt examples, and the monitoring loop for controlling filter URL explosions on collection pages. Companion to SKILL.md section 4.

## Decision flow

For each parameter or facet pattern the template can emit, walk this sequence:

1. Does the facet term have real search demand AND distinct inventory AND its own unique content? Yes: make it an indexable landing page (self-canonical, unique title, H1, intro, ideally its own bottom block). No: continue.
2. Is the pattern already indexed in volume? Yes: meta robots noindex, leave it crawlable until the URLs drop out of the index, only consider robots.txt afterwards. No: continue.
3. Is the pattern crawled in volume (crawl stats, server logs)? Yes: robots.txt Disallow on the pattern, plus rel=canonical to the clean collection URL on the pages themselves. No: rel=canonical to the clean collection URL is enough.

Never do both robots.txt Disallow and noindex on the same URLs at the same time: a blocked URL is never fetched, so its noindex is never seen.

Keep sort orders, view modes, and session parameters (?sort=, ?view=, ?page-size=) permanently out of the crawl: they never deserve indexing.

## robots.txt patterns

Adapt to the real parameter names of the store; verify with the Search Console robots.txt report and a live URL Inspection test before shipping (Google retired the standalone robots.txt Tester in December 2023). Examples:

```
# Block filter combinations (two or more filters)
Disallow: /*?*filter*&*filter*

# Block sort and display parameters anywhere in the query string
Disallow: /*?*sort=
Disallow: /*&sort=
Disallow: /*?*view=
Disallow: /*&view=
```

Warnings:

- robots.txt removes crawling, not indexing. Already-indexed URLs stay indexed (without content) until they decay. For removal, use noindex first.
- Over-blocking is the classic failure: a pattern like `Disallow: /*?` also kills legitimate parameter URLs (search pages, tracking variants you canonicalized). List what each rule matches before shipping.
- Google retired the Search Console URL Parameters tool in 2022 (https://developers.google.com/search/blog/2022/03/url-parameters-tool-deprecated). robots.txt, canonicals, and noindex are the only levers left.

## Platform notes

Verify each claim against the live store with curl: themes and apps override defaults constantly.

### Shopify

- Filter URLs from Search & Discovery look like `?filter.v.option.color=red` or `?filter.p.product_type=...`; sort is `?sort_by=price-ascending`.
- Tag filtering also exists at the path level: `/collections/dresses/red`. Check the canonical your theme outputs on tag URLs: many themes self-canonicalize them, which makes every tag an indexable near-duplicate. Decide per the 3-test exception.
- robots.txt is editable since 2021 via `robots.txt.liquid`; default Shopify robots.txt already blocks some patterns (`+`, `%2B` combinations, sort_by). Read the live file before adding rules.
- Smart collections multiply easily; audit for 0-2 product collections quarterly.

### WooCommerce

- Layered nav widgets emit `?filter_color=red&query_type_color=or`; sorting emits `?orderby=price`.
- Product attribute archives (`/color/red/`) exist when "Enable archives" is on for the attribute; treat each enabled archive as a facet landing page candidate, noindex the rest via the SEO plugin.
- SEO plugins (Yoast, Rank Math) can set canonicals and noindex per archive type; confirm what the theme actually renders with curl, plugins conflict.

### Magento (Adobe Commerce)

- Layered navigation emits numeric parameters (`?color=58&price=50-100`).
- Stock configuration offers canonical meta tags for category pages; layered nav indexing control usually requires an extension or custom logic. Audit which filter URLs return self-canonicals.

### BigCommerce and PrestaShop

- BigCommerce faceted search emits `?color=red` style parameters and brand/facet pages; PrestaShop layered navigation emits `?facets=` style URLs (version-dependent).
- Same decision flow applies; both platforms need template-level edits or apps for noindex on facets, so default state is usually "everything crawlable". Check before assuming.

## Monitoring loop

Check monthly in Search Console:

| Report | What to watch |
|---|---|
| Page indexing > Why pages are not indexed | "Discovered, currently not indexed" and "Duplicate without user-selected canonical" trending up = parameter leak |
| Page indexing > "Alternate page with proper canonical tag" | This is the healthy bucket for filtered URLs; growth here is fine |
| Page indexing > "Excluded by noindex tag" | Filter URLs you noindexed land here; once stable, you may move the pattern to robots.txt |
| Crawl stats (Settings > Crawl stats) | Share of crawl spent on parameter URLs; new-product discovery delay |

Server logs beat Search Console for facet diagnosis when available: count Googlebot hits per parameter pattern, then prioritize the patterns eating the most budget.

## Pagination quick reference

| Pattern | Verdict |
|---|---|
| `/collections/shoes?page=2` with self-canonical | Correct |
| Page 2 canonical to page 1 | Wrong: deep products lose their crawl path |
| `<a href="?page=3">` links | Required: crawlers do not click JS buttons or scroll |
| Infinite scroll only | Wrong without a paginated `<a href>` fallback |
| rel=prev/next | Ignored by Google since 2019; harmless, never a fix |
| Title "Shoes - Page 3 \| Brand" | Correct: keeps paginated titles unique |

Source: https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading
