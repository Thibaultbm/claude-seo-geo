#!/usr/bin/env python3
"""Audit an XML sitemap for its two readers: robots (valid, light, honest) and people (readable).

Follows a sitemap index into its child files and prints raw facts, then a list of findings.
Pure standard library, Python 3.9+, read only, no API key.

Usage:
  python3 sitemap_audit.py https://example.com/sitemap.xml
  python3 sitemap_audit.py https://example.com            (reads robots.txt, falls back to /sitemap.xml)
  python3 sitemap_audit.py https://example.com/sitemap.xml --json report.json --max-children 200

Checks:
  people   xml-stylesheet instruction, XSL on the same origin, reachable, right content type,
           xslt-polyfill loaded (Chrome removes native XSLT on 17 November 2026), HTML sitemap page
  robots   status, content type, size and URL limits, sitemap index and segmentation,
           duplicates, other hosts, http URLs, lastmod coverage and honesty,
           priority and changefreq (ignored by Google), hreflang weight, URLs per language
"""

import argparse
import collections
import gzip
import json
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0 Safari/537.36 sitemap-audit"
XSL_TYPES = ("text/xsl", "application/xslt+xml", "application/xml", "text/xml")
HTML_SITEMAP_PATHS = ("/plan-du-site", "/plan-du-site/", "/sitemap", "/sitemap/", "/site-map", "/sitemap.html", "/html-sitemap")
MAX_URLS = 50000
MAX_BYTES = 50 * 1024 * 1024


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            if r.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz"):
                try:
                    body = gzip.decompress(body)
                except OSError:
                    pass
            return r.status, (r.headers.get("Content-Type") or "").lower(), body, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, (e.headers.get("Content-Type") or "").lower(), b"", url
    except Exception as e:  # network error: report it, do not crash the audit
        return 0, "{}: {}".format(type(e).__name__, e), b"", url


def origin(url):
    p = urlparse(url)
    return (p.scheme, p.hostname, p.port)


def find_sitemap(start):
    p = urlparse(start)
    if p.path and p.path not in ("", "/"):
        return start
    base = "{}://{}".format(p.scheme or "https", p.netloc or p.path)
    status, _, body, _ = fetch(urljoin(base, "/robots.txt"))
    if status == 200:
        found = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", body.decode("utf-8", "replace"))
        if found:
            return found[0]
    return urljoin(base, "/sitemap.xml")


def stylesheet_of(xml):
    m = re.search(r"<\?xml-stylesheet\b([^?]*)\?>", xml[:2000])
    if not m:
        return None
    attrs = dict(re.findall(r'(\w+)\s*=\s*["\']([^"\']*)["\']', m.group(1)))
    return attrs


def check_people(url, xml, cache):
    """Human readability of one sitemap file."""
    out = {"stylesheet": None}
    attrs = stylesheet_of(xml)
    if not attrs:
        return out
    href = urljoin(url, attrs.get("href", ""))
    out["stylesheet"] = href
    out["stylesheet_type"] = attrs.get("type", "")
    out["stylesheet_same_origin"] = origin(href) == origin(url)
    if href not in cache:
        status, ctype, body, _ = fetch(href)
        cache[href] = {"status": status, "content_type": ctype,
                       "is_xslt": b"XSL/Transform" in body[:4000]}
    out["stylesheet_fetch"] = cache[href]
    m = re.search(r'<script\b[^>]*src=["\']([^"\']*xslt-polyfill[^"\']*)["\']', xml[:5000])
    if m:
        src = urljoin(url, m.group(1))
        out["polyfill"] = src
        out["polyfill_same_origin"] = origin(src) == origin(url)
        if src not in cache:
            status, ctype, _, _ = fetch(src)
            cache[src] = {"status": status, "content_type": ctype}
        out["polyfill_fetch"] = cache[src]
    else:
        out["polyfill"] = None
    return out


def first_segment(path):
    return path.strip("/").split("/")[0] if path.strip("/") else ""


def analyse_urlset(url, xml, size):
    locs = [l.strip() for l in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml)]
    host = urlparse(url).hostname
    lastmods = re.findall(r"<lastmod>\s*([^<]+?)\s*</lastmod>", xml)
    days = collections.Counter(l[:10] for l in lastmods)
    alt_bytes = sum(len(m) for m in re.findall(r"<xhtml:link\b[^>]*/>", xml))
    # Language of a URL: its self-referencing hreflang alternate.
    per_lang = collections.Counter()
    for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>\s*([^<]+?)\s*</loc>", block)
        if not loc:
            continue
        for lang, href in re.findall(r'hreflang="([^"]+)"\s+href="([^"]+)"', block):
            if lang != "x-default" and href.strip() == loc.group(1).strip():
                per_lang[lang] += 1
                break
    sections = collections.Counter(first_segment(urlparse(l).path) for l in locs)
    return {
        "url": url,
        "bytes": size,
        "urls": len(locs),
        "duplicates": len(locs) - len(set(locs)),
        "other_hosts": sum(1 for l in locs if urlparse(l).hostname != host),
        "http_urls": sum(1 for l in locs if l.startswith("http://")),
        "lastmod_coverage": round(len(lastmods) / len(locs), 3) if locs else 0,
        "lastmod_top_day": days.most_common(1)[0] if days else None,
        "lastmod_top_day_share": round(days.most_common(1)[0][1] / len(lastmods), 3) if lastmods else 0,
        "lastmod_days": len(days),
        "has_priority": "<priority>" in xml,
        "has_changefreq": "<changefreq>" in xml,
        "hreflang_links": xml.count("<xhtml:link"),
        "hreflang_share_of_bytes": round(alt_bytes / size, 3) if size else 0,
        "per_language": dict(per_lang.most_common()),
        "sections": dict(sections.most_common()),
    }


def audit(start, max_children):
    url = find_sitemap(start)
    report = {"sitemap": url, "files": [], "people": [], "index": None}
    cache = {}
    status, ctype, body, final = fetch(url)
    report["status"], report["content_type"] = status, ctype
    if status != 200 or not body:
        report["error"] = "sitemap not reachable (HTTP {})".format(status)
        return report
    xml = body.decode("utf-8", "replace")
    report["people"].append(dict(file=url, **check_people(url, xml, cache)))
    if "<sitemapindex" in xml:
        children = [c.strip() for c in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml)]
        report["index"] = {"children": len(children), "read": min(len(children), max_children)}
        for child in children[:max_children]:
            s, ct, b, _ = fetch(child)
            if s != 200 or not b:
                report["files"].append({"url": child, "error": "HTTP {}".format(s)})
                continue
            cx = b.decode("utf-8", "replace")
            report["people"].append(dict(file=child, **check_people(child, cx, cache)))
            f = analyse_urlset(child, cx, len(b))
            f["content_type"] = ct
            report["files"].append(f)
    else:
        f = analyse_urlset(url, xml, len(body))
        f["content_type"] = ctype
        report["files"].append(f)
    base = "{0.scheme}://{0.netloc}".format(urlparse(url))
    report["html_sitemap"] = []
    for path in HTML_SITEMAP_PATHS:
        s, ct, b, final = fetch(urljoin(base, path))
        if s == 200 and "html" in ct and b"<a " in b:
            report["html_sitemap"].append({"url": final, "links": b.count(b"<a ")})
            break
    return report


def findings(r):
    F = []
    def add(level, who, text):
        F.append((level, who, text))
    if r.get("error"):
        add("BLOCKER", "robots", r["error"])
        return F
    files = [f for f in r["files"] if "urls" in f]
    total = sum(f["urls"] for f in files)
    # People
    styled = [p for p in r["people"] if p.get("stylesheet")]
    if not styled:
        add("FIX", "people", "No xml-stylesheet instruction: browsers show the raw XML tree, readable by robots only. Install assets/sitemap.xsl (Build, step 2).")
    else:
        if len(styled) < len(r["people"]):
            add("FIX", "people", "{} of {} sitemap files call no stylesheet: every file, index and children, needs the instruction.".format(len(r["people"]) - len(styled), len(r["people"])))
        seen = set()
        for p in styled:  # one finding per distinct stylesheet or polyfill, not per file
            fx = p.get("stylesheet_fetch", {})
            if p["stylesheet"] not in seen:
                seen.add(p["stylesheet"])
                if not p["stylesheet_same_origin"]:
                    add("FIX", "people", "Stylesheet on another origin ({}): browsers refuse it and show nothing. Serve it from the sitemap's own domain.".format(p["stylesheet"]))
                if fx.get("status") != 200 or not fx.get("is_xslt"):
                    add("FIX", "people", "Stylesheet {} unreachable or not XSLT (HTTP {}).".format(p["stylesheet"], fx.get("status")))
                elif not any(t in fx.get("content_type", "") for t in XSL_TYPES):
                    add("FIX", "people", "Stylesheet served as '{}': use text/xsl or application/xml.".format(fx.get("content_type")))
            if p.get("polyfill") and p["polyfill"] not in seen:
                seen.add(p["polyfill"])
                pf = p.get("polyfill_fetch", {})
                if pf.get("status") != 200:
                    add("FIX", "people", "Polyfill {} unreachable (HTTP {}).".format(p["polyfill"], pf.get("status")))
                if not p.get("polyfill_same_origin"):
                    add("WATCH", "people", "Polyfill loaded from another origin: self-host a pinned copy so a CDN change cannot break the view.")
        bare = [p["file"] for p in styled if not p.get("polyfill")]
        if bare:
            add("PRIORITY", "people", "{} sitemap file(s) call a stylesheet without xslt-polyfill. Chrome shows a removal warning today and drops native XSLT on 17 November 2026 (Chrome 158): the files then render as one block of run-together text, worse than no stylesheet. Add the polyfill (Build, step 3).".format(len(bare)))
    if not r.get("html_sitemap"):
        add("WATCH", "people", "No HTML sitemap page found at the usual addresses (/plan-du-site, /sitemap, /site-map): the durable human version, linked from the footer (Build, step 4).")
    # Robots
    ctype = r.get("content_type", "")
    if "xml" not in ctype:
        add("FIX", "robots", "Sitemap served as '{}': use application/xml.".format(ctype))
    for f in files:
        if f["urls"] > MAX_URLS or f["bytes"] > MAX_BYTES:
            add("BLOCKER", "robots", "{} exceeds 50,000 URLs or 50 MB: Google rejects the whole file.".format(f["url"]))
        if f["duplicates"]:
            add("FIX", "robots", "{} duplicate URLs in {}.".format(f["duplicates"], f["url"]))
        if f["other_hosts"]:
            add("FIX", "robots", "{} URLs on another host in {}: a sitemap lists its own host only.".format(f["other_hosts"], f["url"]))
        if f["http_urls"]:
            add("FIX", "robots", "{} http:// URLs in {}: list the final https URLs.".format(f["http_urls"], f["url"]))
        if f["lastmod_coverage"] < 1 and f["urls"]:
            add("WATCH", "robots", "lastmod on {:.0%} of URLs in {}.".format(f["lastmod_coverage"], f["url"]))
        if f["lastmod_top_day_share"] >= 0.4 and f["urls"] >= 50:
            day, n = f["lastmod_top_day"]
            add("FIX", "robots", "{} URLs ({:.0%}) share lastmod {} in {}: a build or import date, not a content date. Google ignores lastmod it finds inaccurate. Use the date of the last real content change.".format(n, f["lastmod_top_day_share"], day, f["url"]))
        if f["has_priority"] or f["has_changefreq"]:
            add("MINOR", "robots", "priority and changefreq in {}: Google ignores both. Remove them to lighten the file and the view.".format(f["url"]))
        if f["hreflang_share_of_bytes"] >= 0.5:
            add("WATCH", "robots", "hreflang links are {:.0%} of {} ({} links). Valid, but heavy: keep them only if the pages do not already carry the same hreflang tags, and segment the file.".format(f["hreflang_share_of_bytes"], f["url"], f["hreflang_links"]))
        langs = f["per_language"]
        if len(langs) > 1 and len(set(langs.values())) > 1:
            add("FIX", "robots", "URLs per language differ in {}: {}. Find the pages missing in some languages (seo-technical, Step 2).".format(f["url"], langs))
    if r.get("index") is None and total >= 500:
        add("FIX", "robots", "One single file for {} URLs: split by section and language under a sitemap index, so Search Console reports indexation per template and each file stays readable.".format(total))
    return F


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url")
    ap.add_argument("--max-children", type=int, default=100)
    ap.add_argument("--json", help="write the full report to this file")
    a = ap.parse_args()
    r = audit(a.url, a.max_children)
    F = findings(r)
    print("=" * 70)
    print("SITEMAP AUDIT  {}".format(r["sitemap"]))
    print("=" * 70)
    print("HTTP {}  {}".format(r.get("status"), r.get("content_type")))
    if r.get("index"):
        print("sitemap index: {children} child files ({read} read)".format(**r["index"]))
    for f in r["files"]:
        if "error" in f:
            print("  {}  ERROR {}".format(f["url"], f["error"]))
            continue
        print("\n  {}".format(f["url"]))
        print("    URLs {}  size {:.2f} MB  hreflang links {} ({:.0%} of bytes)".format(
            f["urls"], f["bytes"] / 1048576, f["hreflang_links"], f["hreflang_share_of_bytes"]))
        print("    lastmod: {:.0%} coverage, {} distinct days, most frequent {}".format(
            f["lastmod_coverage"], f["lastmod_days"], f["lastmod_top_day"]))
        print("    priority {}  changefreq {}".format(f["has_priority"], f["has_changefreq"]))
        if f["per_language"]:
            print("    per language: {}".format(", ".join("{} {}".format(k, v) for k, v in f["per_language"].items())))
        top = list(f["sections"].items())[:12]
        print("    sections: {}".format(", ".join("/{} {}".format(k, v) for k, v in top)))
    p = r["people"][0] if r["people"] else {}
    print("\n  people view: stylesheet {}  polyfill {}".format(p.get("stylesheet"), p.get("polyfill")))
    print("  HTML sitemap page: {}".format(r.get("html_sitemap") or "not found"))
    print("\nFINDINGS")
    if not F:
        print("  none: readable by people, clean for robots")
    for level, who, text in F:
        print("  [{}] ({}) {}".format(level, who, text))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"report": r, "findings": F}, fh, indent=2, ensure_ascii=False)
    return 1 if any(l in ("BLOCKER", "PRIORITY") for l, _, _ in F) else 0


if __name__ == "__main__":
    sys.exit(main())
