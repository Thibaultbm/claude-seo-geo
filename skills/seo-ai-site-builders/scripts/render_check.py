#!/usr/bin/env python3
"""render_check.py: show what a JavaScript-less crawler actually sees.

AI website generators (Lovable, Base44, Bolt, Replit, Softr, Bubble and others)
usually ship a client-rendered single page app. Googlebot renders JavaScript on
a delay; no AI crawler renders it at all. This script fetches the raw HTML of one
or more URLs, exactly like a crawler that runs no JavaScript, and reports whether
real content is present in that response.

Zero dependencies, Python 3.9+, read only. It fetches pages, nothing else.

Usage:
    python3 render_check.py https://example.com
    python3 render_check.py https://example.com/ https://example.com/pricing
    python3 render_check.py --sitemap https://example.com/sitemap.xml --limit 10
    python3 render_check.py https://example.com --ua-compare
    python3 render_check.py https://example.com --json

Options:
    --sitemap URL   read URLs from a sitemap or sitemap index instead of argv
    --limit N       max URLs to check when reading a sitemap (default 10)
    --ua-compare    refetch each URL as Googlebot and as GPTBot and compare
    --soft404       probe a URL that cannot exist, to detect a 200 SPA fallback
    --timeout S     request timeout in seconds (default 20)
    --json          machine readable output

Exit code 0 if every page checked serves its content in the HTML, 1 otherwise.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import unescape

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
GOOGLEBOT_UA = (
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
)
GPTBOT_UA = "Mozilla/5.0 (compatible; GPTBot/1.2; +https://openai.com/gptbot)"

# Content in the raw HTML is the only thing every crawler can read.
WORDS_SERVER_RENDERED = 250
WORDS_SHELL = 60

COMMENT_RE = re.compile(r"(?s)<!--.*?-->")
BLOCK_RE = re.compile(r"(?is)<(script|style|noscript|svg|template)\b[^>]*>.*?</\1>")
TAG_RE = re.compile(r"(?s)<[^>]+>")
TITLE_RE = re.compile(r"(?is)<title[^>]*>(.*?)</title>")
H1_RE = re.compile(r"(?is)<h1\b[^>]*>(.*?)</h1>")
H2_RE = re.compile(r"(?is)<h2\b[^>]*>")
ANCHOR_RE = re.compile(r"(?is)<a\b[^>]*\shref=[\"\']([^\"\']*)[\"\']")
IMG_RE = re.compile(r"(?is)<img\b[^>]*\ssrc=[\"\'][^\"\']+[\"\']")
JSONLD_RE = re.compile(
    r"(?is)<script[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>"
)
MODULE_RE = re.compile(r"(?is)<script[^>]*type=[\"\']module[\"\']")
EMPTY_ROOT_RE = re.compile(
    r"(?is)<div[^>]*\sid=[\"\'](root|app|__next|___gatsby|__nuxt)[\"\'][^>]*>\s*</div>"
)
LOC_RE = re.compile(r"(?is)<loc>(.*?)</loc>")

# Fingerprints are matched against the lowercased raw HTML.
BUILDERS = [
    ("Lovable", ["gpteng.co", "lovable.dev", "lovable-tagger", ".lovable.app"]),
    ("Base44", ["base44.app", "base44.com", "base44"]),
    ("Bolt (StackBlitz)", ["bolt.new", "stackblitz"]),
    ("v0 (Vercel)", ["v0.dev", "v0.app"]),
    ("Replit", ["replit.dev", "repl.co", "replit.com"]),
    ("Framer", ["framerusercontent.com", "framer.com"]),
    ("Webflow", ["webflow.io", "wf-page", "assets.website-files.com"]),
    ("Wix", ["parastorage.com", "wixstatic.com", "wix.com"]),
    ("Squarespace", ["squarespace.com", "static1.squarespace.com"]),
    ("Bubble", ["bubble.io", "bubble_page_load", "meta.bubble.io"]),
    ("Softr", ["softr.io", "softr-"]),
    ("Glide", ["glideapps.com"]),
    ("Durable", ["durable.co"]),
    ("Dora", ["dora.run"]),
    ("Firebase Hosting or Studio", ["firebaseapp.com", "web.app"]),
    ("Hostinger Horizons", ["hostinger", "horizons."]),
    ("Shopify", ["cdn.shopify.com"]),
    ("WordPress", ["/wp-content/", "/wp-includes/"]),
]

FRAMEWORKS = [
    ("Next.js", ["__next_data__", "/_next/static"]),
    ("Nuxt", ["/_nuxt/", "__nuxt"]),
    ("Astro", ["astro-island", "/_astro/"]),
    ("SvelteKit", ["__sveltekit", "/_app/immutable"]),
    ("TanStack Start", ["tanstack", "__tsr"]),
    ("Remix or React Router framework", ["__remixcontext", "window.__reactrouter"]),
    ("Angular", ["ng-version", "<app-root"]),
    ("Vite single page app", ["/assets/index-", "type=\"module\" crossorigin"]),
]


def fetch(url, ua, timeout):
    """Return (status, final_url, html, error). Never raises."""
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(3_000_000)
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.status, resp.geturl(), raw.decode(charset, "replace"), None
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read(1_000_000).decode("utf-8", "replace")
        except Exception:
            pass
        return exc.code, url, body, None
    except Exception as exc:  # network, TLS, timeout, malformed URL
        return None, url, "", str(exc)


def visible_words(html):
    """Word count of the text a crawler can read without running JavaScript."""
    text = COMMENT_RE.sub(" ", html)
    text = BLOCK_RE.sub(" ", text)
    text = TAG_RE.sub(" ", text)
    return len([w for w in unescape(text).split() if any(c.isalnum() for c in w)])


def first_group(regex, html):
    match = regex.search(html)
    if not match:
        return None
    return unescape(TAG_RE.sub("", match.group(1))).strip() or None


def meta_content(html, attr, value):
    pattern = re.compile(
        r"(?is)<meta[^>]*\s%s=[\"\']%s[\"\'][^>]*\scontent=[\"\']([^\"\']*)[\"\']"
        % (attr, re.escape(value))
    )
    match = pattern.search(html)
    if match:
        return unescape(match.group(1)).strip() or None
    pattern_rev = re.compile(
        r"(?is)<meta[^>]*\scontent=[\"\']([^\"\']*)[\"\'][^>]*\s%s=[\"\']%s[\"\']"
        % (attr, re.escape(value))
    )
    match = pattern_rev.search(html)
    return unescape(match.group(1)).strip() if match else None


def link_href(html, rel):
    pattern = re.compile(
        r"(?is)<link[^>]*\srel=[\"\']%s[\"\'][^>]*\shref=[\"\']([^\"\']*)[\"\']" % rel
    )
    match = pattern.search(html)
    return match.group(1).strip() if match else None


def detect(html_lower, table):
    return [name for name, needles in table if any(n in html_lower for n in needles)]


def real_internal_links(html, base_url):
    host = urllib.parse.urlparse(base_url).netloc
    count = 0
    for href in ANCHOR_RE.findall(html):
        href = href.strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        parsed = urllib.parse.urlparse(urllib.parse.urljoin(base_url, href))
        if parsed.netloc == host:
            count += 1
    return count


def analyze(url, timeout, ua=BROWSER_UA):
    status, final_url, html, error = fetch(url, ua, timeout)
    report = {"url": url, "final_url": final_url, "status": status, "error": error}
    if error or not html:
        report["verdict"] = "ERROR"
        return report

    lower = html.lower()
    words = visible_words(html)
    h1s = [unescape(TAG_RE.sub("", h)).strip() for h in H1_RE.findall(html)]
    jsonld = JSONLD_RE.findall(html)
    valid_jsonld = 0
    for block in jsonld:
        try:
            json.loads(block.strip())
            valid_jsonld += 1
        except ValueError:
            pass

    report.update(
        {
            "builders": detect(lower, BUILDERS),
            "frameworks": detect(lower, FRAMEWORKS),
            "title": first_group(TITLE_RE, html),
            "meta_description": meta_content(html, "name", "description"),
            "meta_robots": meta_content(html, "name", "robots"),
            "og_title": meta_content(html, "property", "og:title"),
            "canonical": link_href(html, "canonical"),
            "words": words,
            "h1_count": len(h1s),
            "h1": h1s[0] if h1s else None,
            "h2_count": len(H2_RE.findall(html)),
            "internal_links": real_internal_links(html, final_url or url),
            "images": len(IMG_RE.findall(html)),
            "jsonld_blocks": len(jsonld),
            "jsonld_valid": valid_jsonld,
            "module_scripts": len(MODULE_RE.findall(html)),
            "empty_root_div": bool(EMPTY_ROOT_RE.search(html)),
            "bytes": len(html),
        }
    )

    if status is None or status >= 400:
        report["verdict"] = "ERROR"
    elif report["empty_root_div"] or words < WORDS_SHELL:
        report["verdict"] = "SHELL ONLY"
    elif words >= WORDS_SERVER_RENDERED and h1s:
        report["verdict"] = "SERVER RENDERED"
    else:
        report["verdict"] = "PARTIAL"
    return report


def issues(report):
    """Findings ordered by how much they cost, worst first."""
    out = []
    verdict = report.get("verdict")
    if verdict == "ERROR":
        out.append("fetch failed or non-200 status, nothing could be checked")
        return out
    if verdict == "SHELL ONLY":
        out.append(
            "no content in the HTML: every AI crawler sees an empty page, "
            "Google only after a delayed render pass"
        )
    elif verdict == "PARTIAL":
        out.append(
            "thin HTML (%d words): part of the page is injected by JavaScript"
            % report["words"]
        )
    if not report.get("title"):
        out.append("no title in the HTML")
    if not report.get("meta_description"):
        out.append("no meta description in the HTML")
    if report.get("h1_count", 0) == 0:
        out.append("no h1 in the HTML")
    elif report["h1_count"] > 1:
        out.append("%d h1 tags" % report["h1_count"])
    if not report.get("canonical"):
        out.append("no canonical link")
    if (report.get("meta_robots") or "").lower().find("noindex") >= 0:
        out.append("meta robots noindex is served on this URL")
    if report.get("internal_links", 0) < 3:
        out.append(
            "%d crawlable internal links: router links must be real a href anchors"
            % report.get("internal_links", 0)
        )
    if report.get("jsonld_blocks", 0) == 0:
        out.append("no JSON-LD in the HTML")
    elif report.get("jsonld_valid", 0) < report["jsonld_blocks"]:
        out.append("JSON-LD present but some blocks do not parse")
    if not report.get("og_title"):
        out.append("no og:title, link previews will be empty on social and chat apps")
    return out


def print_report(report, ua_compare=None):
    print("\n" + "=" * 72)
    print(report["url"])
    print("=" * 72)
    if report.get("error"):
        print("  ERROR  %s" % report["error"])
        return
    print("  Status          %s" % report["status"])
    if report.get("final_url") and report["final_url"] != report["url"]:
        print("  Redirected to   %s" % report["final_url"])
    print("  Verdict         %s" % report["verdict"])
    print("  Built with      %s" % (", ".join(report["builders"]) or "unknown"))
    print("  Framework       %s" % (", ".join(report["frameworks"]) or "unknown"))
    print("  Words in HTML   %d" % report["words"])
    print("  Title           %s" % (report["title"] or "MISSING"))
    print("  H1              %s" % (report["h1"] or "MISSING"))
    print(
        "  Structure       h2:%d  internal links:%d  img:%d  json-ld:%d/%d valid"
        % (
            report["h2_count"],
            report["internal_links"],
            report["images"],
            report["jsonld_valid"],
            report["jsonld_blocks"],
        )
    )
    print("  Canonical       %s" % (report["canonical"] or "MISSING"))
    print("  Meta robots     %s" % (report["meta_robots"] or "not set (indexable)"))
    if ua_compare:
        print("  Words by UA     %s" % ua_compare)
    found = issues(report)
    if found:
        print("  Findings")
        for item in found:
            print("    - %s" % item)
    else:
        print("  Findings        none, this page serves its content as HTML")


def read_sitemap(url, timeout, limit):
    """Return up to `limit` page URLs from a sitemap or sitemap index."""
    status, _, body, error = fetch(url, BROWSER_UA, timeout)
    if error or not body:
        print("Could not read sitemap %s (%s)" % (url, error or status))
        return []
    locs = [unescape(loc).strip() for loc in LOC_RE.findall(body)]
    pages, indexes = [], []
    for loc in locs:
        (indexes if loc.endswith((".xml", ".xml.gz")) else pages).append(loc)
    for index in indexes:
        if len(pages) >= limit:
            break
        _, _, child, child_error = fetch(index, BROWSER_UA, timeout)
        if child_error:
            continue
        pages.extend(
            unescape(loc).strip()
            for loc in LOC_RE.findall(child)
            if not loc.endswith((".xml", ".xml.gz"))
        )
    return pages[:limit]


def soft404_probe(url, timeout):
    parsed = urllib.parse.urlparse(url)
    probe = urllib.parse.urlunparse(
        (parsed.scheme, parsed.netloc, "/render-check-404-probe-zzz", "", "", "")
    )
    status, _, _, error = fetch(probe, BROWSER_UA, timeout)
    if error:
        return probe, None, "probe failed: %s" % error
    if status == 200:
        return probe, status, (
            "SPA fallback returns 200 for a URL that does not exist: every typo and "
            "dead link becomes a soft 404. Serve a real 404 status for unknown routes."
        )
    return probe, status, "correct: unknown routes return %s" % status


def main():
    parser = argparse.ArgumentParser(
        description="Check what a JavaScript-less crawler sees on an AI-generated site."
    )
    parser.add_argument("urls", nargs="*", help="page URLs to check")
    parser.add_argument("--sitemap", help="read URLs from this sitemap instead")
    parser.add_argument("--limit", type=int, default=10, help="max sitemap URLs")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--ua-compare", action="store_true",
                        help="refetch as Googlebot and GPTBot and compare word counts")
    parser.add_argument("--soft404", action="store_true",
                        help="probe a URL that cannot exist to detect a 200 fallback")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    urls = list(args.urls)
    if args.sitemap:
        urls.extend(read_sitemap(args.sitemap, args.timeout, args.limit))
    urls = [u if "://" in u else "https://" + u for u in dict.fromkeys(urls)]
    if not urls:
        parser.error("give at least one URL or a --sitemap")

    reports, payload = [], []
    for url in urls:
        report = analyze(url, args.timeout)
        compare = None
        if args.ua_compare and report.get("verdict") != "ERROR":
            counts = {"browser": report["words"]}
            for label, ua in (("googlebot", GOOGLEBOT_UA), ("gptbot", GPTBOT_UA)):
                counts[label] = analyze(url, args.timeout, ua).get("words", 0)
            report["words_by_ua"] = counts
            compare = "  ".join("%s:%d" % (k, v) for k, v in counts.items())
            spread = max(counts.values()) - min(counts.values())
            if spread > max(30, 0.3 * max(counts.values())):
                report.setdefault("notes", []).append(
                    "the HTML differs by user agent: a crawler-only prerender layer "
                    "is in place, verify it serves the same content to every bot"
                )
        reports.append((report, compare))
        payload.append(report)

    if args.as_json:
        out = {"pages": payload}
        if args.soft404 and urls:
            probe, status, note = soft404_probe(urls[0], args.timeout)
            out["soft404"] = {"url": probe, "status": status, "note": note}
        print(json.dumps(out, indent=2))
    else:
        for report, compare in reports:
            print_report(report, compare)
            for note in report.get("notes", []):
                print("    - %s" % note)
        if args.soft404 and urls:
            probe, status, note = soft404_probe(urls[0], args.timeout)
            print("\n" + "=" * 72)
            print("404 handling: %s" % probe)
            print("  %s" % note)
        counts = {}
        for report, _ in reports:
            counts[report["verdict"]] = counts.get(report["verdict"], 0) + 1
        print("\n" + "-" * 72)
        print("%d URLs checked: %s" % (
            len(reports),
            ", ".join("%d %s" % (v, k) for k, v in sorted(counts.items())),
        ))
        print("Only SERVER RENDERED pages are readable by ChatGPT, Claude and Perplexity.")

    return 0 if all(r["verdict"] == "SERVER RENDERED" for r, _ in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
