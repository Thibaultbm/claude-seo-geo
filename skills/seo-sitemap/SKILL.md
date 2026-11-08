---
name: seo-sitemap
description: "Build an XML sitemap that is clean for robots (valid, light, segmented, honest lastmod) and elegant for people who open it: pretty-printed raw XML, one element per line, two-space indentation, a fixed order inside every entry, no stylesheet, no script, no HTML. Input: a site or its sitemap URL. Output: an audit by sitemap_audit.py (pretty-print, leftover XSL or polyfill, size, segmentation, duplicates, lastmod honesty, priority and changefreq, hreflang weight, URLs per language), the build (a sitemap index split by section and language when the site is large, every file pretty-printed by the bundled formatter or xmllint --format), and a scripted acceptance test. Use when a sitemap looks messy or minified when opened, sits on one line, carries an XSL stylesheet or Chrome's XSLT removal warning, is one huge file, or when building or auditing any sitemap."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "2.0.0"
---

# Elegant sitemaps: pretty-printed raw XML

A sitemap has two readers. Robots (Googlebot, Bingbot, the AI crawlers) need a valid, light, honest file. People open it too: the client checking that the site is complete, the developer, the agency during an audit. What they should see is **the raw XML, printed elegantly**: one element per line, a consistent indentation, the same order inside every entry, nothing else. No stylesheet, no CSS, no HTML layer, no script. Opened in a browser, view-source, `curl` or an editor, the file reads cleanly and is exactly what the robots get.

Technical crawl rules for sitemaps (robots.txt line, Search Console submission, IndexNow, the dead ping endpoint) live in seo-technical, Step 2. This skill owns the file's format and structure.

## Hard rules

1. **Raw XML only.** No `<?xml-stylesheet?>` instruction, no XSL file, no xslt-polyfill or any `<script>` inside the sitemap, no HTML served at the sitemap address, no response that changes by user agent. The browser's own XML view ("This XML file does not appear to have any style information" followed by the tree) is the expected and correct rendering: it is not a defect to fix.
2. **Pretty-printed, always.** Every sitemap file, index and children, is formatted exactly as `xmllint --format` would print it: XML declaration on line 1, one element per line, two spaces per nesting level, text-only elements on one line (`<loc>…</loc>`), no blank lines, no trailing spaces, LF line endings, a final newline. A minified or single-line sitemap is valid for robots but fails this skill.
3. **Same order everywhere.** Inside each `<url>`: `loc`, `lastmod`, then the `xhtml:link` alternates in a fixed language order with `x-default` last, then `image:image`. Across the file: home first, then sections in a stable order, each page's language versions next to each other.
4. **Remove what exists.** A site that already ships an XSL view: delete the processing instruction from every file, delete the XSL and any polyfill file, and keep the pretty-printed XML. Chrome removes native XSLT on 17 November 2026 and already shows a red warning above styled sitemaps; the decoration is not worth that risk.
5. **One source of truth.** The XML sitemap, the hreflang tags in the pages and any HTML sitemap page are generated from the same page inventory, so their counts match.

## Phase 1: Spec

| ID | Requirement | Source |
|---|---|---|
| SMP-01 | Served with HTTP 200 and Content-Type application/xml, UTF-8, at the address declared on the robots.txt `Sitemap:` line | Official |
| SMP-02 | Max 50,000 URLs and 50 MB uncompressed per file; above that Google rejects the whole file | Official |
| SMP-03 | Above about 500 URLs, a sitemap index with child files split by section (pages, blog, case studies, location pages, products) and, on multilingual sites, by language. Search Console then reports indexation per template, and each file stays short enough to read | Field rule |
| SMP-04 | Only canonical, indexable, 200 URLs on the sitemap's own host, in https, no duplicates | Official |
| SMP-05 | lastmod present on every URL and equal to the date of the last real content change. A date shared by a large share of URLs (build, import or generation date) is a lie Google learns to ignore | Official (Google ignores inaccurate lastmod) |
| SMP-06 | No priority, no changefreq: Google ignores both. They add weight and noise to the file | Official |
| SMP-07 | hreflang in the sitemap or in the page head, both allowed. When both, they must match exactly. On big multilingual sites, hreflang links often make most of the file's weight: segment by language | Official, field rule |
| SMP-08 | Multilingual: the same number of pages in every language (seo-technical, Step 2) | Field rule |
| SMP-09 | Pretty-printed: byte-identical to `xmllint --format` output (two-space indentation, one element per line, text-only elements inline, no blank lines, no trailing spaces, final newline) | Field rule |
| SMP-10 | Fixed element order inside each entry (loc, lastmod, alternates with x-default last, images) and a stable page order across the file | Field rule |
| SMP-11 | No xml-stylesheet instruction, no XSL, no script, no comment, no HTML anywhere in a sitemap file | Field rule |
| SMP-12 | Optional: an HTML sitemap page (`/plan-du-site`, `/sitemap`) linked from the footer, listing every indexable page by section with its title. It is a crawl hub for orphan-prone pages (seo-internal-linking), not a replacement for the XML file and never required by this skill | Field rule |

## Phase 2: Audit

```
python3 skills/seo-sitemap/scripts/sitemap_audit.py https://example.com
python3 skills/seo-sitemap/scripts/sitemap_audit.py https://example.com/sitemap_index.xml --json sitemap.json
```

Given a domain, the script reads robots.txt to find the sitemap (fallback `/sitemap.xml`), follows an index into its children (`--max-children`, default 100) and prints, per file: URL count, size, line count, whether the file is pretty-printed (and the first offending line when it is not), leftover stylesheet or script, hreflang links and their share of the bytes, lastmod coverage and the most frequent date, priority and changefreq, URLs per language, URLs per section. Then findings ranked BLOCKER, PRIORITY, FIX, WATCH, MINOR, each mapped to a spec row. Exit code 1 on any BLOCKER or PRIORITY.

Then check by eye: open the sitemap with view-source (or `curl -s URL | head -30`). You should see one element per line, indented by two spaces, the same shape repeated for every entry. One long line, tabs mixed with spaces, blank lines between entries, or a stylesheet line at the top: SMP-09 or SMP-11 fails.

Field case (a 5-language agency site, November 2026): one 1.4 MB file of 1762 URLs written on a handful of lines, 10500 hreflang links making 80% of the bytes (and duplicated in the page heads), priority and changefreq on every URL, 710 generated city pages all dated on the day they were generated, 41 blog posts without lastmod. The client opened it and thought the sitemap was broken. It was valid; it was unreadable and heavier than needed.

## Phase 3: Build

1. **Structure (SMP-01 to SMP-08).** Generate one file for a small site, or a sitemap index plus one child per section and language above about 500 URLs, for example `sitemap-pages-fr.xml`, `sitemap-blog-en.xml`. Drop priority and changefreq. Take lastmod from the content's real update date (CMS updated_at, git commit date of the content file), never the build date. Keep hreflang in one place when possible; if both the heads and the sitemap carry it, generate both from the same table. Declare the index in robots.txt and submit it in Search Console and Bing Webmaster Tools.
2. **Order (SMP-10).** Emit entries in a stable order (home, then sections, then pages; language versions of a page side by side) and the children of each entry in the fixed order. A generator that iterates over an unordered set produces a different file on every build, which makes diffs useless.
3. **Pretty-print (SMP-09, SMP-11).** Format every file as the last build step, then check it:

```
python3 skills/seo-sitemap/scripts/sitemap_audit.py --format public/sitemap.xml      # rewrites the file in place
xmllint --format public/sitemap.xml | diff -q - public/sitemap.xml && echo "pretty"     # independent check (libxml2, built into macOS and most Linux)
```

The bundled formatter strips any `xml-stylesheet` instruction, `<script>` element and comment, and prints the canonical layout. Expected shape:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/fr/</loc>
    <lastmod>2026-11-08</lastmod>
    <xhtml:link rel="alternate" hreflang="fr" href="https://example.com/fr/"/>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/en/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/fr/"/>
  </url>
</urlset>
```

Platforms that do not let you edit the sitemap (Shopify, Wix, Squarespace) generate their own layout: record it as an exception, do not add a stylesheet to compensate.

4. **Clean up an existing XSL view (SMP-11).** Remove the processing instruction from every file, delete `sitemap.xsl` and any `xslt-polyfill` file, and redeploy. Nothing changes for robots: they ignored the stylesheet.

## Acceptance

1. `sitemap_audit.py` exits 0: no BLOCKER, no PRIORITY; any remaining FIX is written down with its reason.
2. `xmllint --format FILE | diff -q - FILE` reports no difference for the index and every child.
3. The live file opened with view-source shows one element per line, two-space indentation, no stylesheet line.
4. In Search Console, each submitted sitemap reads "Success" and the discovered URL count equals the generated count.
5. URLs per language are equal, or the gaps are written down as exceptions.

## Sources

- Google, build and submit a sitemap (priority and changefreq ignored, lastmod accuracy): https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google, large sitemaps and sitemap index files: https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps
- Google, localized versions (hreflang in sitemaps): https://developers.google.com/search/docs/specialty/international/localized-versions
- Chrome, removing XSLT (why a stylesheet is now a liability): https://developer.chrome.com/docs/web-platform/deprecating-xslt
- libxml2 xmllint (the `--format` reference layout): https://gnome.pages.gitlab.gnome.org/libxml2/xmllint.html
