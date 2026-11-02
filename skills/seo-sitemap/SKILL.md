---
name: seo-sitemap
description: "Build an XML sitemap that serves its two readers: robots (valid, light, segmented, honest lastmod) and people (a clean, readable page in the browser instead of a raw XML tree). Input: a site or its sitemap URL. Output: an audit by sitemap_audit.py (stylesheet, polyfill, size, segmentation, duplicates, lastmod honesty, priority and changefreq, hreflang weight, URLs per language), then the build: a sitemap index split by section and language, the bundled sitemap.xsl readable view with the xslt-polyfill that keeps it working after Chrome removes XSLT (17 November 2026), an HTML sitemap page, and a scripted acceptance test. Use when a sitemap looks ugly or unreadable in the browser, shows 'This XML file does not appear to have any style information', shows Chrome's XSLT removal warning, is one huge file, or when building or auditing any sitemap."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Readable sitemaps (for robots and for people)

A sitemap has two readers. Robots (Googlebot, Bingbot, the AI crawlers) need a valid, light, honest file. People open it too: the client checking that the site is complete, the developer, the agency during an audit, a prospect. Opened in a browser, a plain sitemap is a raw XML tree that nobody can read, and the client concludes it is broken. This skill delivers both: the same file stays exactly what robots expect, and the browser shows a clean page with counts, sections, languages and a filter.

Technical crawl rules for sitemaps (robots.txt line, Search Console submission, IndexNow, the dead ping endpoint) live in seo-technical, Step 2. This skill owns the file's format, structure and human view.

## Hard rules

1. **Never trade robot validity for looks.** The readable view is a layer on top: an `xml-stylesheet` processing instruction that search engines ignore. Never serve HTML at the sitemap address, never change the response by user agent or Accept header (Googlebot would receive the HTML and the sitemap would fail).
2. **Same origin.** The stylesheet and the polyfill are served from the sitemap's own domain. Browsers refuse a cross-origin XSL and show nothing.
3. **No stylesheet without the polyfill, from now on.** Chrome removes native XSLT on 17 November 2026 (Chrome 158; Chrome 156 already shows a red removal warning above every styled sitemap). A sitemap that calls a stylesheet in a browser without XSLT renders as one block of run-together text, worse than the raw tree. Firefox and WebKit have announced the same removal without a date. The official polyfill fixes all of them (measured: Chrome 156 with XSLT disabled, see Phase 3).
4. **Every sitemap file is styled**, the index and each child: people click from the index into the children.
5. **One source of truth.** The XML sitemap, the HTML sitemap page and the hreflang tags in the pages are generated from the same page inventory, so their counts match.

## Phase 1: Spec

| ID | Requirement | Source |
|---|---|---|
| SMP-01 | Served with HTTP 200 and Content-Type application/xml, UTF-8, at the address declared on the robots.txt `Sitemap:` line | Official |
| SMP-02 | Max 50,000 URLs and 50 MB uncompressed per file; above that Google rejects the whole file | Official |
| SMP-03 | Above about 500 URLs, a sitemap index with child files split by section (pages, blog, case studies, location pages, products) and, on multilingual sites, by language. Search Console then reports indexation per template, and each file stays readable | Field rule |
| SMP-04 | Only canonical, indexable, 200 URLs on the sitemap's own host, in https, no duplicates | Official |
| SMP-05 | lastmod present on every URL and equal to the date of the last real content change. A date shared by a large share of URLs (build, import or generation date) is a lie Google learns to ignore | Official (Google ignores inaccurate lastmod) |
| SMP-06 | No priority, no changefreq: Google ignores both. They add weight and noise to the file and the view | Official |
| SMP-07 | hreflang in the sitemap or in the page head, both allowed. When both, they must match exactly. On big multilingual sites, hreflang links often make most of the file's weight: segment by language | Official, field rule |
| SMP-08 | Multilingual: the same number of pages in every language (seo-technical, Step 2) | Field rule |
| SMP-09 | Second line of every file: `<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>`, the XSL on the same origin, served as text/xsl or application/xml | Field rule (WordPress core and the main SEO plugins ship the same mechanism) |
| SMP-10 | First child of the root element of every styled file: the self-hosted, pinned xslt-polyfill script (Build, step 3) | Official (Chrome's migration guidance) |
| SMP-11 | The readable view shows: site, number of pages, number of languages, sections with counts, a filter, one row per page with its path as a link, its language versions, its last update. Labels in the site's language. Readable on a phone, light and dark | Field rule |
| SMP-12 | An HTML sitemap page (`/plan-du-site`, `/sitemap`, localized slug per language) linked from the footer, listing every indexable page by section with its title, server-rendered | Field rule |

## Phase 2: Audit

```
python3 skills/seo-sitemap/scripts/sitemap_audit.py https://example.com
python3 skills/seo-sitemap/scripts/sitemap_audit.py https://example.com/sitemap_index.xml --json sitemap.json
```

Given a domain, the script reads robots.txt to find the sitemap (fallback `/sitemap.xml`), follows an index into its children (`--max-children`, default 100) and prints, per file: URL count, size, hreflang links and their share of the bytes, lastmod coverage and the most frequent date, priority and changefreq, URLs per language, URLs per section. Then the people side: stylesheet, same origin, content type, polyfill, HTML sitemap page. Then findings ranked BLOCKER, PRIORITY, FIX, WATCH, MINOR, each mapped to a spec row. Exit code 1 on any BLOCKER or PRIORITY.

Then check by eye: open the sitemap in Chrome. Raw tree with "This XML file does not appear to have any style information": SMP-09 missing. Red banner about XSLT removal: SMP-10 missing. Run-together text: stylesheet broken or XSLT unavailable without polyfill.

Field case (a 5-language agency site, November 2026): one 1.4 MB file of 1762 URLs, no stylesheet, 10500 hreflang links making 80% of the bytes (and duplicated in the page heads), priority and changefreq on every URL, 710 generated city pages all dated on the day they were generated, 41 blog posts without lastmod. The client opened it in a browser and thought the sitemap was broken. It was valid; it was unreadable and heavier than needed.

## Phase 3: Build

1. **Structure (SMP-01 to SMP-08).** Generate a sitemap index plus one child per section and language, for example `sitemap-pages-fr.xml`, `sitemap-blog-en.xml`, `sitemap-locations-es.xml`. Drop priority and changefreq. Take lastmod from the content's real update date (CMS updated_at, git commit date of the content file), never the build date. Keep hreflang in one place when possible; if both the heads and the sitemap carry it, generate both from the same table. Declare the index in robots.txt and submit it in Search Console and Bing Webmaster Tools.
2. **Stylesheet (SMP-09, SMP-11).** Copy `assets/sitemap.xsl` to the site root (or the static folder) so it serves at `/sitemap.xsl`. Translate the labels at the top of the file into the site's language (a single language for the file: the one of the main market). Add the processing instruction on the second line of every sitemap file, index included. The view handles a sitemap index (list of files) and a urlset (stats, sections, language chips, filter, table), sitemap image extensions included. It sets `noindex` on itself.
3. **Polyfill (SMP-10).** Download a pinned version of the official polyfill (npm package `xslt-polyfill`, maintained by a Chrome engineer; version 1.0.34 measured on 2 November 2026) and serve it at `/xslt-polyfill.min.js`:

```
curl -o public/xslt-polyfill.min.js https://cdn.jsdelivr.net/npm/xslt-polyfill@1.0.34/xslt-polyfill.min.js
```

Then emit it as the first child of the root element of every styled file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <script src="/xslt-polyfill.min.js" xmlns="http://www.w3.org/1999/xhtml"></script>
  <url>...</url>
</urlset>
```

Measured in Chrome 156: with the polyfill, the view renders identically with XSLT disabled (the state of every Chrome from 17 November 2026), and the removal warning disappears with XSLT enabled. Without it, the same file shows as run-together text with XSLT disabled. The script element is in the XHTML namespace, the same namespace sitemaps already use for hreflang links, and crawlers skip elements they do not know; confirm it on the first deploy with acceptance step 3. The file is about 1.4 MB, downloaded only by browsers that open a sitemap. Platforms that do not let you edit the sitemap (Shopify, Wix, Squarespace): skip steps 2 and 3, the HTML page of step 4 is the readable version.

4. **HTML sitemap page (SMP-12).** One server-rendered page per language, linked from the footer ("Plan du site", "Sitemap"), generated from the same inventory: sections as headings, each page as a link with its title (not its URL), city or product lists in columns, paginated by section above about 500 links per page. It is the durable human version (it does not depend on any browser feature) and a crawl hub that helps orphan-prone pages (seo-internal-linking).
5. **Preview before deploy.** `xsltproc assets/sitemap.xsl sitemap.xml > preview.html` (built into macOS and most Linux) renders the view locally from the generated file.

## Acceptance

1. `sitemap_audit.py` exits 0: no BLOCKER, no PRIORITY; any remaining FIX is written down with its reason.
2. In a browser, the index and two children open as the readable view, phone width included, with no XSLT warning. Test once with XSLT disabled (`--disable-blink-features=XSLT`, or Chrome 158 and later): same view.
3. In Search Console, each submitted sitemap reads "Success" and the discovered URL count equals the generated count. Check after the first deploy, before closing the task.
4. URLs per language are equal, or the gaps are written down as exceptions.

## Not verified

- Google's written position on a polyfill script element inside a sitemap: none published. Acceptance step 3 is the check; on any parsing warning, keep the stylesheet, remove the script element, and rely on the HTML page for Chrome users.
- Firefox and Safari removal dates: announced, not dated.

## Sources

- Chrome, removing XSLT (timeline, polyfill, migration options): https://developer.chrome.com/docs/web-platform/deprecating-xslt
- xslt-polyfill: https://github.com/mfreed7/xslt_polyfill
- Google, build and submit a sitemap (priority and changefreq ignored, lastmod accuracy): https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google, large sitemaps and sitemap index files: https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps
- Google, localized versions (hreflang in sitemaps): https://developers.google.com/search/docs/specialty/international/localized-versions
