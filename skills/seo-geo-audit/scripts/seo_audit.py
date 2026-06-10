#!/usr/bin/env python3
"""On-page fact collector for SEO + GEO audits.

Fetches the raw HTML of one or more URLs (no JavaScript rendering), plus
robots.txt, sitemap and llms.txt, and prints the raw facts an audit needs:
title, meta description, heading hierarchy, images without alt text, image
weight, Open Graph, canonical, structured data, text volume, link counts,
and AI crawler access rules.

Zero external dependencies (standard library only, Python 3.9+). Output is
a readable text report followed by a JSON block a model can parse. The
JUDGMENT (verdict, prioritization, tone) belongs to the model guided by
references/audit-checklist.md; this script only measures.

Usage:
    python3 seo_audit.py https://example.com
    python3 seo_audit.py https://example.com /about /services   # extra pages
    python3 seo_audit.py https://example.com --no-images        # skip image weight checks
"""

import argparse
import gzip
import json
import re
import ssl
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# AI crawlers, split by what blocking them costs you.
# Search/assistant bots: blocking these removes you from AI answers (GEO impact).
AI_SEARCH_BOTS = ["OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User",
                  "PerplexityBot", "Perplexity-User", "DuckAssistBot", "MistralAI-User"]
# Training bots: blocking these keeps you out of future model knowledge (brand tradeoff).
AI_TRAINING_BOTS = ["GPTBot", "ClaudeBot", "anthropic-ai", "CCBot", "Google-Extended",
                    "Applebot-Extended", "Meta-ExternalAgent", "Amazonbot",
                    "Bytespider", "cohere-ai"]
AI_BOTS = AI_SEARCH_BOTS + AI_TRAINING_BOTS

MAX_IMG_CHECK = 15      # max number of images whose weight is verified (HEAD)
IMG_WEIGHT_KB = 200     # field threshold: 200 KB max per image
TIMEOUT = 15


def fetch(url, method="GET"):
    """Return (final_url, status, headers, body_bytes). Handles redirects, gzip, lax TLS."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = Request(url, method=method, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            try:
                raw = gzip.decompress(raw)
            except OSError:
                pass
        return resp.geturl(), resp.status, dict(resp.headers), raw


def head_size(url):
    """Size in KB via HEAD (Content-Length), or None if unavailable."""
    try:
        _, _, headers, _ = fetch(url, method="HEAD")
        cl = headers.get("Content-Length")
        return round(int(cl) / 1024) if cl else None
    except Exception:
        return None


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.meta_description = None
        self.meta_robots = None
        self.viewport = None
        self.canonical = None
        self.og = {}
        self.headings = []          # (level, text)
        self._cur_h = None
        self._cur_h_text = []
        self.images = []            # {src, alt, loading}
        self.links = []             # {href, rel}
        self.jsonld_types = []
        self._skip = 0              # depth inside script/style/noscript
        self._text = []
        self._in_jsonld = False
        self._jsonld_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript", "template"):
            self._skip += 1
            if tag == "script" and a.get("type") == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_buf = []
            return
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (a.get("name") or "").lower()
            prop = (a.get("property") or "").lower()
            content = a.get("content", "")
            if name == "description":
                self.meta_description = content
            elif name == "robots":
                self.meta_robots = content
            elif name == "viewport":
                self.viewport = content
            elif prop.startswith("og:"):
                self.og[prop] = content
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._cur_h = int(tag[1])
            self._cur_h_text = []
        elif tag == "img":
            self.images.append({
                "src": a.get("src") or a.get("data-src") or "",
                "alt": a.get("alt"),
                "loading": (a.get("loading") or "").lower(),
            })
        elif tag == "a" and a.get("href"):
            self.links.append({"href": a["href"], "rel": (a.get("rel") or "").lower()})

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "template"):
            self._skip = max(0, self._skip - 1)
            if tag == "script" and self._in_jsonld:
                self._in_jsonld = False
                try:
                    data = json.loads("".join(self._jsonld_buf))
                    for node in (data if isinstance(data, list) else [data]):
                        if isinstance(node, dict) and node.get("@type"):
                            t = node["@type"]
                            self.jsonld_types.extend(t if isinstance(t, list) else [t])
                except Exception:
                    pass
            return
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._cur_h:
            self.headings.append((self._cur_h, " ".join("".join(self._cur_h_text).split())))
            self._cur_h = None

    def handle_data(self, data):
        if self._in_jsonld:
            self._jsonld_buf.append(data)
            return
        if self._in_title:
            self.title = (self.title or "") + data
        if self._cur_h is not None:
            self._cur_h_text.append(data)
        if self._skip == 0:
            self._text.append(data)

    def word_count(self):
        return len(re.findall(r"\b\w+\b", " ".join(self._text)))


def analyse_page(url, do_images=True):
    out = {"url": url}
    try:
        final, status, headers, body = fetch(url)
    except (HTTPError, URLError, ssl.SSLError, Exception) as e:
        out["error"] = "{}: {}".format(type(e).__name__, e)
        return out

    html = body.decode("utf-8", errors="replace")
    p = Page()
    p.feed(html)

    out["final_url"] = final
    out["http_status"] = status
    out["https"] = final.startswith("https://")
    out["html_size_kb"] = round(len(body) / 1024)

    # Platform fingerprints (adapts the advice: WordPress, Shopify, client-rendered builders...)
    fw = []
    sig = html.lower()
    for name, pat in [("WordPress", "wp-content"), ("Shopify", "cdn.shopify"),
                      ("Webflow", "data-wf-"), ("Framer", "framerusercontent"),
                      ("Wix", "_wixcssimports"), ("Squarespace", "squarespace"),
                      ("Next.js", "__next_data__"), ("Lovable", "lovable-uploads")]:
        if pat in sig:
            fw.append(name)
    out["frameworks"] = fw

    # Title
    title = (p.title or "").strip()
    out["title"] = {"value": title, "length": len(title),
                    "generic": title.lower() in ("", "home", "homepage", "accueil",
                                                  "untitled", "new project", "welcome")}
    # Meta description
    md = p.meta_description
    out["meta_description"] = {"present": md is not None,
                               "length": len(md) if md else 0,
                               "too_long": bool(md and len(md) > 160),
                               "value": md}
    # Headings
    h1 = [t for lvl, t in p.headings if lvl == 1]
    jumps = []
    prev = 0
    for lvl, _ in p.headings:
        if prev and lvl > prev + 1:
            jumps.append("H{}->H{}".format(prev, lvl))
        prev = lvl
    out["headings"] = {
        "h1_count": len(h1), "h1_values": h1,
        "total": len(p.headings),
        "sequence": ["H{}".format(lvl) for lvl, _ in p.headings][:40],
        "level_jumps": jumps,
        "empty": sum(1 for _, t in p.headings if not t),
    }
    # Images
    no_alt = [i for i in p.images if i["alt"] is None]
    empty_alt = [i for i in p.images if i["alt"] == ""]
    lazy = [i for i in p.images if i["loading"] == "lazy"]
    out["images"] = {"total": len(p.images), "missing_alt": len(no_alt),
                     "empty_alt": len(empty_alt), "lazy": len(lazy)}
    # Image weight (sample)
    if do_images and p.images:
        heavy = []
        checked = 0
        for img in p.images:
            if checked >= MAX_IMG_CHECK:
                break
            src = img["src"]
            if not src or src.startswith("data:"):
                continue
            kb = head_size(urljoin(final, src))
            checked += 1
            if kb and kb > IMG_WEIGHT_KB:
                heavy.append({"src": src[:120], "kb": kb})
        out["images"]["checked"] = checked
        out["images"]["over_200kb"] = heavy

    # Internal vs external links
    host = urlparse(final).netloc
    internal = external = 0
    for l in p.links:
        h = l["href"]
        if h.startswith("#") or h.startswith("mailto:") or h.startswith("tel:"):
            continue
        netloc = urlparse(urljoin(final, h)).netloc
        if netloc == host:
            internal += 1
        else:
            external += 1
    out["links"] = {"internal": internal, "external": external}

    # Open Graph / canonical / schema / misc
    out["open_graph"] = {"present": bool(p.og), "keys": sorted(p.og.keys())}
    out["canonical"] = p.canonical
    out["schema_jsonld"] = sorted(set(p.jsonld_types))
    out["viewport"] = p.viewport
    out["lang"] = bool(re.search(r"<html[^>]*\blang=", html, re.I))
    out["word_count"] = p.word_count()
    out["meta_robots"] = p.meta_robots
    # JS rendering hint: very little text + client-side framework means the raw
    # HTML is probably incomplete. AI crawlers do not execute JavaScript, so
    # whatever is missing here is invisible to ChatGPT, Claude and Perplexity.
    out["likely_js_rendered"] = (out["word_count"] < 120 and
                                  any(f in fw for f in ("Framer", "Next.js", "Lovable", "Wix")))
    return out


def analyse_robots(base):
    out = {}
    try:
        final, status, _, body = fetch(urljoin(base, "/robots.txt"))
        txt = body.decode("utf-8", errors="replace")
        out["present"] = status == 200
        out["has_user_agent_rules"] = "user-agent" in txt.lower()
        out["sitemap_declared"] = bool(re.search(r"(?im)^\s*sitemap:", txt))
        out["sitemaps"] = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", txt)
        blocked_search, blocked_training = [], []
        for bot in AI_BOTS:
            # "User-agent: <bot>" group followed (before the next User-agent) by "Disallow: /"
            m = re.search(r"(?is)user-agent:\s*{}\s*(.*?)(?=user-agent:|\Z)".format(re.escape(bot)), txt)
            if m and re.search(r"(?im)^\s*disallow:\s*/\s*$", m.group(1)):
                if bot in AI_SEARCH_BOTS:
                    blocked_search.append(bot)
                else:
                    blocked_training.append(bot)
        out["ai_search_bots_blocked"] = blocked_search
        out["ai_training_bots_blocked"] = blocked_training
        out["raw_excerpt"] = txt[:600]
    except Exception as e:
        out["error"] = "{}: {}".format(type(e).__name__, e)
    return out


def analyse_llms_txt(base):
    """llms.txt presence. Note for the model: no major engine confirms reading it;
    report presence as a fact, never as a ranking or citation lever."""
    out = {}
    try:
        _, status, _, body = fetch(urljoin(base, "/llms.txt"))
        text = body.decode("utf-8", errors="replace")
        looks_html = "<html" in text[:500].lower()
        out["present"] = status == 200 and not looks_html
        if out["present"]:
            out["lines"] = text.count("\n") + 1
    except Exception:
        out["present"] = False
    return out


def analyse_sitemap(base, robots):
    out = {}
    candidates = robots.get("sitemaps") or [urljoin(base, "/sitemap.xml")]
    out["url"] = candidates[0]
    try:
        _, status, _, body = fetch(candidates[0])
        xml = body.decode("utf-8", errors="replace")
        if "<sitemapindex" in xml:
            children = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml)
            out["type"] = "index"
            out["child_sitemaps"] = len(children)
            total = 0
            for child in children[:10]:
                try:
                    _, _, _, b2 = fetch(child.strip())
                    total += len(re.findall(r"<loc>", b2.decode("utf-8", "replace")))
                except Exception:
                    pass
            out["url_count_estimate"] = total
            out["note"] = "estimate from the first 10 child sitemaps" if len(children) > 10 else "total"
        else:
            out["type"] = "urlset"
            out["url_count"] = len(re.findall(r"<loc>", xml))
    except Exception as e:
        out["error"] = "{}: {}".format(type(e).__name__, e)
    return out


def fmt(report):
    """Readable text report (raw facts; the verdict belongs to the model)."""
    L = []
    def line(s=""):
        L.append(s)
    base = report["base"]
    line("=" * 70)
    line("ON-PAGE FACT COLLECTION  {}".format(base))
    line("=" * 70)

    r = report["robots"]
    line("\n## robots.txt, sitemap, llms.txt")
    if r.get("error"):
        line("  robots.txt: error ({})".format(r["error"]))
    else:
        line("  robots.txt present         : {} (user-agent rules: {})".format(
            r.get("present"), r.get("has_user_agent_rules")))
        line("  sitemap declared in robots : {}  {}".format(
            r.get("sitemap_declared"), r.get("sitemaps") or ""))
        bs = r.get("ai_search_bots_blocked")
        bt = r.get("ai_training_bots_blocked")
        line("  AI SEARCH bots blocked     : {}".format(bs if bs else "none (good for AI visibility)"))
        line("  AI training bots blocked   : {}".format(bt if bt else "none"))
    s = report.get("sitemap", {})
    if s:
        cnt = s.get("url_count") or s.get("url_count_estimate")
        line("  sitemap                    : {} ({}, ~{} URLs)".format(
            s.get("url"), s.get("type"), cnt))
    lt = report.get("llms_txt", {})
    line("  llms.txt present           : {} (informational only; no engine confirms reading it)".format(
        lt.get("present")))

    for pg in report["pages"]:
        line("\n" + "-" * 70)
        line("## {}".format(pg["url"]))
        if pg.get("error"):
            line("  ERROR: {}".format(pg["error"]))
            continue
        line("  HTTP {} | https={} | HTML {} KB | platform={}".format(
            pg["http_status"], pg["https"], pg["html_size_kb"], pg["frameworks"] or "-"))
        if pg.get("likely_js_rendered"):
            line("  WARNING: HTML probably rendered client-side (very little text in raw HTML).")
            line("           AI crawlers will not see the missing content. Verify in a browser.")
        t = pg["title"]
        generic_flag = " [GENERIC]" if t["generic"] else ""
        line("  TITLE ({} chars){}: {!r}".format(t["length"], generic_flag, t["value"][:100]))
        m = pg["meta_description"]
        flag = " [TOO LONG >160]" if m["too_long"] else (" [MISSING]" if not m["present"] else "")
        line("  META DESC ({} chars){}: {!r}".format(m["length"], flag, (m["value"] or "")[:120]))
        h = pg["headings"]
        line("  H1 = {} {} | total headings={} | level jumps={} | empty={}".format(
            h["h1_count"], h["h1_values"][:3], h["total"], h["level_jumps"] or "-", h["empty"]))
        line("     sequence: {}".format(" ".join(h["sequence"])))
        im = pg["images"]
        line("  IMAGES total={} | missing alt={} | empty alt={} | lazy={}".format(
            im["total"], im["missing_alt"], im["empty_alt"], im["lazy"]))
        if im.get("over_200kb"):
            sizes = ["{}KB".format(x["kb"]) for x in im["over_200kb"]]
            line("     over 200KB ({}/{} checked): {}".format(
                len(im["over_200kb"]), im.get("checked"), sizes))
        line("  WORDS (visible text): {}".format(pg["word_count"]))
        line("  LINKS internal={} | external={}".format(
            pg["links"]["internal"], pg["links"]["external"]))
        og = pg["open_graph"]
        line("  Open Graph: {}".format("yes " + str(og["keys"]) if og["present"] else "NO"))
        line("  canonical: {} | schema: {}".format(
            pg["canonical"] or "NO", pg["schema_jsonld"] or "none"))
        line("  viewport: {} | html lang: {} | meta robots: {}".format(
            "yes" if pg["viewport"] else "NO", "yes" if pg["lang"] else "NO",
            pg["meta_robots"] or "-"))

    line("\n" + "=" * 70)
    line("JSON (machine summary):")
    line(json.dumps(report, ensure_ascii=False))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="On-page fact collection for SEO + GEO audits")
    ap.add_argument("url", help="homepage URL (https://...)")
    ap.add_argument("pages", nargs="*", help="extra pages (absolute or relative)")
    ap.add_argument("--no-images", action="store_true", help="skip image weight checks")
    args = ap.parse_args()

    base = args.url if args.url.startswith("http") else "https://" + args.url
    robots = analyse_robots(base)
    sitemap = analyse_sitemap(base, robots)
    llms = analyse_llms_txt(base)

    urls = [base] + [urljoin(base, u) for u in args.pages]
    pages = [analyse_page(u, do_images=not args.no_images) for u in urls]

    report = {"base": base, "robots": robots, "sitemap": sitemap,
              "llms_txt": llms, "pages": pages}
    print(fmt(report))


if __name__ == "__main__":
    sys.exit(main())
