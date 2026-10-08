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
# Search-index bots: blocking these removes you from AI answers (GEO impact).
AI_SEARCH_BOTS = ["OAI-SearchBot", "Claude-SearchBot", "PerplexityBot", "DuckAssistBot"]
# User-fetch agents: they load a page on a user's explicit request; robots.txt is
# not a reliable control for ChatGPT-User and Perplexity-User (see ai-crawlers.md).
AI_USER_FETCH_BOTS = ["ChatGPT-User", "Claude-User", "Perplexity-User", "MistralAI-User"]
# Training bots: blocking these keeps you out of future model knowledge (brand tradeoff).
AI_TRAINING_BOTS = ["GPTBot", "ClaudeBot", "anthropic-ai", "CCBot", "Google-Extended",
                    "Applebot-Extended", "Meta-ExternalAgent", "Amazonbot",
                    "Bytespider", "cohere-ai"]
AI_BOTS = AI_SEARCH_BOTS + AI_USER_FETCH_BOTS + AI_TRAINING_BOTS

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


def weight_url(img):
    """Pick the file a browser is most likely to actually download, and a note.

    Responsive images (Webflow especially) put the FULL-RESOLUTION original in
    `src` and the resized, actually-served files in `srcset`. Measuring `src`
    therefore over-reports weight for any image displayed small -- a 30px icon
    whose original is 3000px wide gets flagged as "too heavy" even though the
    browser never downloads it. That is the main false positive in the weight
    check.

    Heuristic: when `srcset` carries width descriptors AND `sizes` pins a fixed
    pixel width, measure the variant that width would select (x2 for retina)
    instead of the original. When `sizes` is viewport-relative (e.g. 100vw) or
    absent we keep `src`, because such images really can ship a near-full-size
    variant -- so a heavy result there is a real finding, not a false positive.
    Returns (url, note)."""
    src = img.get("src") or ""
    cands = []
    for part in (img.get("srcset") or "").split(","):
        bits = part.strip().split()
        if len(bits) >= 2 and bits[-1].endswith("w"):
            try:
                cands.append((int(bits[-1][:-1]), bits[0]))
            except ValueError:
                pass
    if not cands:
        return src, ""
    cands.sort()
    # Keep only the slot lengths, not the "(max-width: NNNpx)" media conditions.
    slots = re.sub(r"\([^)]*\)", "", img.get("sizes") or "")
    px = [int(n) for n in re.findall(r"(\d+)px", slots)]
    if not px:
        return src, "full-res src measured (sizes is viewport-based, so a large variant ships)"
    target = max(px) * 2  # assume retina display
    for w, url in cands:
        if w >= target:
            return url, "{}w variant (src is the {}w original)".format(w, cands[-1][0])
    w, url = cands[-1]
    return url, "{}w variant (largest available)".format(w)


class Page(HTMLParser):
    """Single-pass collector. Everything the checks below need is gathered
    here so the HTML is parsed once per page."""

    CONTAINER_TEXT = ("p", "li", "td", "th", "blockquote", "dd", "figcaption")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.meta_description = None
        self.meta_robots = None
        self.viewport = None
        self.charset = None
        self.canonical = None
        self.favicon = False
        self.meta_refresh = None
        self.og = {}
        self.twitter = {}
        self.article_meta = {}      # article:published_time etc.
        self.hreflang = []          # (lang, href)
        self.headings = []          # (level, text, id)
        self.heading_ids = set()
        self.all_ids = set()
        self._cur_h = None
        self._cur_h_id = None
        self._cur_h_text = []
        self.images = []            # {src, alt, loading, width, height, srcset}
        self.links = []             # {href, rel, text, in_main}
        self._a = None
        self.jsonld_types = []
        self.jsonld_objects = []    # parsed top-level JSON-LD payloads
        self.jsonld_errors = 0
        self._skip = 0              # depth inside script/style/noscript
        self._text = []
        self._main_text = []
        self._main_depth = 0        # inside <main> or <article>
        self._chrome_depth = 0      # inside header / nav / footer / aside
        self.has_main = False
        self._in_jsonld = False
        self._jsonld_buf = []
        self.bold = []              # text of strong / b
        self._bold_depth = 0
        self._bold_buf = []
        self.italic = 0
        self.paragraphs = []        # text of each <p>
        self._p_depth = 0
        self._p_buf = []
        self.lists = 0
        self.list_items = 0
        self.tables = 0
        self.tables_with_th = 0
        self._table_has_th = []
        self.blockquotes = 0
        self.details = 0
        self.tokens = []            # class / id / itemprop / rel tokens, lowercased
        self.times = 0
        self.iframes = []
        self.elements = 0           # DOM size proxy
        self.resource_urls = []     # src / href of loaded resources (mixed content)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in ("strong", "b") and self._bold_depth:
            self._bold_depth -= 1

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.elements += 1
        if tag in ("script", "style", "noscript", "template"):
            if tag == "script" and a.get("src"):
                self.resource_urls.append(a["src"])
            self._skip += 1
            if tag == "script" and "ld+json" in (a.get("type") or "").lower():
                self._in_jsonld = True
                self._jsonld_buf = []
            return
        # Anything inside script/style/noscript/template is not rendered: a
        # <noscript> fallback copy or a hidden <template> must not inflate the
        # image / link / heading counts (a common source of phantom "lazy"
        # images, since lazy-load libraries stash a duplicate <img> there).
        if self._skip:
            return
        for key in ("class", "id", "itemprop", "rel", "aria-label"):
            v = a.get(key)
            if v:
                self.tokens.append(v.lower())
        if a.get("id"):
            self.all_ids.add(a["id"])
        if tag in ("main", "article"):
            self._main_depth += 1
            self.has_main = True
        elif tag in ("header", "nav", "footer", "aside"):
            self._chrome_depth += 1
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (a.get("name") or "").lower()
            prop = (a.get("property") or "").lower()
            content = a.get("content", "")
            if a.get("charset"):
                self.charset = a["charset"]
            elif (a.get("http-equiv") or "").lower() == "content-type" and "charset" in content.lower():
                self.charset = content
            elif (a.get("http-equiv") or "").lower() == "refresh":
                self.meta_refresh = content
            if name == "description":
                self.meta_description = content
            elif name == "robots":
                self.meta_robots = content
            elif name == "viewport":
                self.viewport = content
            elif name.startswith("twitter:"):
                self.twitter[name] = content
            elif prop.startswith("og:"):
                self.og[prop] = content
            elif prop.startswith("twitter:"):
                self.twitter[prop] = content
            elif prop.startswith("article:"):
                self.article_meta[prop] = content
        elif tag == "link":
            rel = (a.get("rel") or "").lower().split()
            if "canonical" in rel:
                self.canonical = a.get("href")
            if "icon" in rel or "apple-touch-icon" in rel:
                self.favicon = True
            if "alternate" in rel and a.get("hreflang"):
                self.hreflang.append((a["hreflang"], a.get("href") or ""))
            if "stylesheet" in rel and a.get("href"):
                self.resource_urls.append(a["href"])
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._cur_h = int(tag[1])
            self._cur_h_id = a.get("id")
            self._cur_h_text = []
        elif tag == "img":
            src = a.get("src") or a.get("data-src") or ""
            self.images.append({
                "src": src,
                "srcset": a.get("srcset") or a.get("data-srcset") or "",
                "sizes": a.get("sizes") or "",
                "alt": a.get("alt"),
                "loading": (a.get("loading") or "").lower(),
                "width": a.get("width"),
                "height": a.get("height"),
                "in_link": self._a is not None,
            })
            if a.get("src"):
                self.resource_urls.append(a["src"])
            if self._a is not None and a.get("alt"):
                self._a["text_parts"].append(a["alt"])
        elif tag == "a" and a.get("href") is not None:
            self._a = {"href": a["href"], "rel": (a.get("rel") or "").lower(),
                       "text_parts": [], "in_main": self._main_depth > 0,
                       "in_chrome": self._chrome_depth > 0,
                       "aria": a.get("aria-label") or a.get("title") or ""}
        elif tag in ("strong", "b"):
            self._bold_depth += 1
            if self._bold_depth == 1:
                self._bold_buf = []
        elif tag in ("em", "i") and not a.get("class"):
            self.italic += 1
        elif tag == "p":
            self._p_depth += 1
            if self._p_depth == 1:
                self._p_buf = []
        elif tag in ("ul", "ol"):
            self.lists += 1
        elif tag == "li":
            self.list_items += 1
        elif tag == "table":
            self.tables += 1
            self._table_has_th.append(False)
        elif tag == "th" and self._table_has_th:
            self._table_has_th[-1] = True
        elif tag == "blockquote" or tag == "q":
            self.blockquotes += 1
        elif tag == "details":
            self.details += 1
        elif tag == "time":
            self.times += 1
        elif tag == "iframe":
            self.iframes.append(a.get("src") or a.get("data-src") or "")
            if a.get("src"):
                self.resource_urls.append(a["src"])

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "template"):
            self._skip = max(0, self._skip - 1)
            if tag == "script" and self._in_jsonld:
                self._in_jsonld = False
                try:
                    data = json.loads("".join(self._jsonld_buf))
                    self.jsonld_objects.append(data)
                    self._walk_jsonld(data)
                except Exception:
                    self.jsonld_errors += 1
            return
        if self._skip:
            return
        if tag in ("main", "article"):
            self._main_depth = max(0, self._main_depth - 1)
        elif tag in ("header", "nav", "footer", "aside"):
            self._chrome_depth = max(0, self._chrome_depth - 1)
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._cur_h:
            text = " ".join("".join(self._cur_h_text).split())
            self.headings.append((self._cur_h, text, self._cur_h_id))
            if self._cur_h_id:
                self.heading_ids.add(self._cur_h_id)
            self._cur_h = None
        elif tag == "a" and self._a is not None:
            self._a["text"] = " ".join(" ".join(self._a.pop("text_parts")).split())
            self.links.append(self._a)
            self._a = None
        elif tag in ("strong", "b") and self._bold_depth:
            self._bold_depth -= 1
            if self._bold_depth == 0:
                t = " ".join("".join(self._bold_buf).split())
                if t:
                    self.bold.append(t)
        elif tag == "p" and self._p_depth:
            self._p_depth -= 1
            if self._p_depth == 0:
                t = " ".join("".join(self._p_buf).split())
                if t:
                    self.paragraphs.append(t)
        elif tag == "table" and self._table_has_th:
            if self._table_has_th.pop():
                self.tables_with_th += 1

    def _walk_jsonld(self, node):
        # Recursive: WordPress/Yoast, RankMath and most CMS wrap everything in
        # {"@graph": [...]}, and types can nest arbitrarily deep.
        if isinstance(node, dict):
            t = node.get("@type")
            if isinstance(t, str):
                self.jsonld_types.append(t)
            elif isinstance(t, list):
                self.jsonld_types.extend(x for x in t if isinstance(x, str))
            for v in node.values():
                self._walk_jsonld(v)
        elif isinstance(node, list):
            for v in node:
                self._walk_jsonld(v)

    def handle_data(self, data):
        if self._in_jsonld:
            self._jsonld_buf.append(data)
            return
        if self._skip:
            return
        if self._in_title:
            self.title = (self.title or "") + data
            return
        if self._cur_h is not None:
            self._cur_h_text.append(data)
        if self._a is not None:
            self._a["text_parts"].append(data)
        if self._bold_depth:
            self._bold_buf.append(data)
        if self._p_depth:
            self._p_buf.append(data)
        self._text.append(data)
        if self._main_depth:
            self._main_text.append(data)

    def word_count(self):
        return len(re.findall(r"\b\w+\b", " ".join(self._text)))

    def content_text(self):
        """Main content when the page marks it up (<main> / <article>), else
        the whole visible text. Keyword and readability metrics use this so
        menus and footers repeated on every page do not skew them."""
        main = " ".join(self._main_text)
        everything = " ".join(self._text)
        n_main = len(re.findall(r"\b\w+\b", main))
        # A <main> that holds a fraction of the page (a pricing widget, a
        # hero) is not the content; fall back to the whole visible text.
        if n_main >= 150 and n_main >= 0.4 * len(re.findall(r"\b\w+\b", everything)):
            return main
        return everything


# ---------------------------------------------------------------------------
# Deep on-page checks. Thresholds mirror the Sorank SEO Analyzer extension so
# the script and the extension agree on the same page. Each rule cites why in
# references/audit-checklist.md (sections 2, 3, 6, 15).
# ---------------------------------------------------------------------------

STOPWORDS = set("""
a an and are as at be been but by can do does for from has have how i if in into is it its
just more most my no not of on or our out so than that the their them then there these they
this to too up us was we what when where which who why will with you your yours about after
all also any because before being both each few here him his her its me once only other own
same she should some such through under until very were while would could own off over again
au aux avec ce ces cet cette dans de des du elle elles en est et eux il ils je la le les leur
leurs lui ma mais me meme mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se
ses son sont sur ta te tes toi ton tu un une vos votre vous y ete etre avoir fait plus tout
tous toute toutes comme peut sans aussi bien tres entre alors donc car ainsi cela ceci celui
dont quand chez sous vers deja encore faire faut avez avons sera sont ont ai as etait leur
""".split())

GENERIC_ANCHORS = {
    "click here", "here", "read more", "learn more", "more", "link", "this", "this page",
    "see more", "details", "continue", "go", "en savoir plus", "cliquez ici", "ici", "lire la suite",
    "voir plus", "plus", "lien", "cette page", "suite", "decouvrir", "en lire plus",
}

SOCIAL_HOSTS = ("linkedin.com", "twitter.com", "x.com", "instagram.com", "youtube.com",
                "facebook.com", "tiktok.com", "pinterest.com", "threads.net", "twitch.tv",
                "discord.gg", "discord.com")

AUTHOR_PATH_RE = re.compile(r"/(auteur|author|authors|auteurs|a-propos|about|equipe|team|"
                            r"mon-parcours|qui-suis-je|who-we-are|notre-equipe|profil|profile)\b", re.I)
LEGAL_PATH_RE = re.compile(r"(cgv|cgu|mentions|legal|privacy|confidentialite|cookies|terms|"
                           r"conditions|rgpd|gdpr|login|connexion|signin|sign-in|account|compte)", re.I)
TOC_TOKEN_RE = re.compile(r"\b(toc|table-of-contents|tableofcontents|sommaire|fs-toc\w*|"
                          r"ez-toc\w*|rank-math-toc\w*|wp-block-table-of-contents|lwptoc\w*)\b")
AUTHOR_TOKEN_RE = re.compile(r"(author|auteur|byline|post-meta__author|writer|redacteur|bio)")
CTA_TOKEN_RE = re.compile(r"(\bcta\b|cta[-_]|[-_]cta|call-to-action|btn|button|bouton)")

STAT_RE = re.compile(r"\b\d+(?:[.,]\d+)?\s?(?:%|percent|pour ?cent|x\b|fois\b|€|\$|£|k€|m€|"
                     r"millions?|milliards?|billion|thousand)", re.I)
DEFINITION_RE = re.compile(r"\b[A-Z][\w' -]{1,40}\s(?:is|are|refers to|means|est|sont|désigne|"
                           r"signifie|correspond à)\s(?:a|an|the|un|une|le|la|les|l')\b")

# Required (and empty-string-sensitive) properties for the JSON-LD types that
# still drive a Google feature or an AI entity graph. A property present but
# set to "" counts as missing: CMS templates often ship empty FAQ questions.
SCHEMA_REQUIRED = {
    "Organization": ["name", "url"],
    "LocalBusiness": ["name", "address"],
    "Person": ["name"],
    "WebSite": ["name", "url"],
    "Article": ["headline", "author", "datePublished", "image"],
    "BlogPosting": ["headline", "author", "datePublished", "image"],
    "NewsArticle": ["headline", "author", "datePublished", "image"],
    "Product": ["name", "offers|review|aggregateRating"],
    "Offer": ["price", "priceCurrency"],
    "Course": ["name", "description", "provider"],
    "FAQPage": ["mainEntity"],
    "Question": ["name", "acceptedAnswer"],
    "Answer": ["text"],
    "BreadcrumbList": ["itemListElement"],
    "VideoObject": ["name", "thumbnailUrl", "uploadDate"],
    "AggregateRating": ["ratingValue", "reviewCount|ratingCount"],
    "Review": ["author", "reviewRating|reviewBody"],
    "Event": ["name", "startDate", "location"],
    "Service": ["name", "provider|areaServed"],
}

# Severity weights used by the extension's displayed score (100 minus the sum).
SEVERITY_POINTS = {"critical": 12.5, "high": 6, "medium": 3, "low": 1.5}


def _norm(s):
    s = s.lower()
    for a, b in (("à", "a"), ("â", "a"), ("ä", "a"), ("é", "e"), ("è", "e"), ("ê", "e"),
                 ("ë", "e"), ("î", "i"), ("ï", "i"), ("ô", "o"), ("ö", "o"), ("ù", "u"),
                 ("û", "u"), ("ü", "u"), ("ç", "c"), ("’", "'")):
        s = s.replace(a, b)
    return s


def _words(text):
    return re.findall(r"[a-zA-ZÀ-ɏ0-9]+(?:'[a-zA-ZÀ-ɏ]+)?", text)


def _content_terms(text):
    return [w for w in (_norm(x) for x in _words(text)) if len(w) > 2 and w not in STOPWORDS
            and not w.isdigit()]


def _syllables(word):
    groups = re.findall(r"[aeiouyàâäéèêëîïôöùûü]+", word.lower())
    n = len(groups)
    if word.lower().endswith("e") and n > 1:
        n -= 1
    return max(1, n)


def readability(text, lang):
    """Sentence-length buckets and a Flesch score (Kandel-Moles for French,
    original Flesch for English). Same buckets as the extension."""
    sentences = [s for s in re.split(r"(?<=[.!?…])\s+|\n+", text) if len(_words(s)) >= 3]
    if not sentences:
        return {"sentences": 0}
    lens = [len(_words(s)) for s in sentences]
    words = [w for s in sentences for w in _words(s)]
    asl = sum(lens) / len(lens)
    asw = sum(_syllables(w) for w in words) / max(1, len(words))
    if (lang or "").lower().startswith("fr"):
        flesch = 207 - 1.015 * asl - 73.6 * asw
    else:
        flesch = 206.835 - 1.015 * asl - 84.6 * asw
    buckets = {"<=10": 0, "11-20": 0, "21-30": 0, "31+": 0}
    for n in lens:
        if n <= 10:
            buckets["<=10"] += 1
        elif n <= 20:
            buckets["11-20"] += 1
        elif n <= 30:
            buckets["21-30"] += 1
        else:
            buckets["31+"] += 1
    pct_long = 100.0 * (buckets["21-30"] + buckets["31+"]) / len(lens)
    pct_very_long = 100.0 * buckets["31+"] / len(lens)
    return {
        "sentences": len(lens),
        "avg_sentence_words": round(asl, 1),
        "buckets": buckets,
        "pct_over_20_words": round(pct_long, 1),
        "pct_over_30_words": round(pct_very_long, 1),
        "flesch": round(max(0, min(100, flesch)), 1),
        "score": round(max(0, 100 - 0.5 * pct_long - 1.5 * pct_very_long)),
    }


def keyword_analysis(p, final, content):
    """Top terms with density, stuffing alerts, and the placement matrix for
    the terms the page itself targets (title + H1)."""
    terms = _content_terms(content)
    total = max(1, len(terms))
    freq = {}
    for t in terms:
        freq[t] = freq.get(t, 0) + 1
    top = sorted(freq.items(), key=lambda kv: -kv[1])[:15]
    top_out = [{"term": t, "count": n, "density": round(100.0 * n / total, 2)} for t, n in top]
    bigrams = {}
    for a, b in zip(terms, terms[1:]):
        bigrams[a + " " + b] = bigrams.get(a + " " + b, 0) + 1
    top_bi = [{"term": t, "count": n} for t, n in sorted(bigrams.items(), key=lambda kv: -kv[1])[:10]
              if n >= 2]
    stuffing = [x for x in top_out if x["count"] >= 5 and x["density"] > 2.5]

    title_terms = _content_terms(p.title or "")
    h1_terms = _content_terms(" ".join(t for lvl, t, _ in p.headings if lvl == 1))
    targets = []
    for t in title_terms + h1_terms:
        if t not in targets:
            targets.append(t)
    targets = targets[:6]
    # The intro is read from the paragraphs, not the raw text, so a menu or a
    # hero label at the top of the DOM does not count as the first 100 words.
    intro_src = " ".join(p.paragraphs) or content
    first100 = " ".join(_norm(w) for w in _words(intro_src)[:100])
    zones = {
        "title": _norm(p.title or ""),
        "h1": _norm(" ".join(t for lvl, t, _ in p.headings if lvl == 1)),
        "h2_h6": _norm(" ".join(t for lvl, t, _ in p.headings if lvl > 1)),
        "meta_description": _norm(p.meta_description or ""),
        "url": _norm(urlparse(final).path.replace("-", " ").replace("_", " ")),
        "first_100_words": first100,
        "bold": _norm(" ".join(p.bold)),
        "image_alt": _norm(" ".join(i["alt"] or "" for i in p.images)),
    }
    matrix = {}
    for t in targets:
        matrix[t] = {z: (re.search(r"\b" + re.escape(t) + r"\b", txt) is not None)
                     for z, txt in zones.items()}
    coverage = 0.0
    if matrix:
        coverage = sum(sum(v.values()) / len(v) for v in matrix.values()) / len(matrix)
    return {"top_terms": top_out, "top_bigrams": top_bi, "stuffing": stuffing,
            "target_terms": targets, "placement": matrix,
            "placement_coverage": round(100 * coverage)}


def schema_checks(objects):
    """Missing or empty required properties, per JSON-LD node."""
    problems = []

    def has(node, key):
        for k in key.split("|"):
            v = node.get(k)
            if v not in (None, "", [], {}):
                return True
        return False

    def walk(node, depth=0):
        if depth > 12:
            return
        if isinstance(node, dict):
            t = node.get("@type")
            types = t if isinstance(t, list) else [t]
            for ty in types:
                req = SCHEMA_REQUIRED.get(ty if isinstance(ty, str) else "")
                # Nested references ({"@id": ...} only) are pointers, not nodes.
                if req and not (len(node) <= 2 and "@id" in node):
                    missing = [k for k in req if not has(node, k)]
                    if missing:
                        problems.append({"type": ty, "missing_or_empty": missing})
            for v in node.values():
                walk(v, depth + 1)
        elif isinstance(node, list):
            for v in node:
                walk(v, depth + 1)

    for o in objects:
        walk(o)
    # Collapse duplicates (ten empty FAQ questions are one finding).
    seen = {}
    for pr in problems:
        key = (pr["type"], tuple(pr["missing_or_empty"]))
        seen[key] = seen.get(key, 0) + 1
    return [{"type": k[0], "missing_or_empty": list(k[1]), "count": n} for k, n in seen.items()]


def page_kind(final, p, types):
    path = urlparse(final).path.rstrip("/")
    segs = [s for s in path.split("/") if s]
    if not segs or (len(segs) == 1 and len(segs[0]) == 2):
        return "homepage"
    blogish = ("blog", "articles", "article", "actualites", "news", "guides", "guide",
               "magazine", "journal", "ressources", "resources", "insights")
    last = segs[-1].lower()
    if "Blog" in types or last in blogish or last.startswith("blog"):
        return "blog_hub"
    if any(t in types for t in ("Article", "BlogPosting", "NewsArticle")):
        return "article"
    for s in segs[:-1]:
        if s.lower() in blogish or s.lower().startswith("blog"):
            return "article"
    if "Product" in types:
        return "product"
    return "page"


def deep_checks(p, html, final, headers, out):
    host = urlparse(final).netloc
    path = urlparse(final).path
    content = p.content_text()
    types = set(p.jsonld_types)
    kind = page_kind(final, p, types)
    out["page_kind"] = kind
    lang_m = re.search(r"<html[^>]*\blang=[\"']?([\w-]+)", html, re.I)
    lang = lang_m.group(1) if lang_m else ""
    out["lang_value"] = lang

    # Head tags
    out["head"] = {
        "charset": bool(p.charset or "charset" in (headers.get("Content-Type") or "").lower()),
        "favicon": p.favicon,
        "twitter_card": p.twitter.get("twitter:card"),
        "og_missing": [k for k in ("og:title", "og:description", "og:image", "og:url")
                       if not p.og.get(k)],
        "meta_refresh": p.meta_refresh,
        "x_robots_tag": headers.get("X-Robots-Tag") or headers.get("x-robots-tag"),
    }
    canon = p.canonical
    if canon:
        cabs = urljoin(final, canon)
        out["canonical_self"] = cabs.rstrip("/") == final.split("#")[0].split("?")[0].rstrip("/")
        out["canonical_absolute"] = canon.startswith("http")
    # Robots directives that cap AI and snippet use
    robots = (p.meta_robots or "").lower() + "," + (out["head"]["x_robots_tag"] or "").lower()
    msn = re.search(r"max-snippet\s*:\s*(-?\d+)", robots)
    out["robots_directives"] = {
        "noindex": "noindex" in robots, "nofollow": "nofollow" in robots.split(",")[0],
        "nosnippet": "nosnippet" in robots, "max_snippet": int(msn.group(1)) if msn else None,
        "noindex_with_canonical_elsewhere": "noindex" in robots and canon is not None
        and not out.get("canonical_self", True),
    }
    # Hreflang
    if p.hreflang:
        codes = [c for c, _ in p.hreflang]
        bad = [c for c in codes if c.lower() != "x-default"
               and not re.match(r"^[a-zA-Z]{2,3}(-[a-zA-Z]{2,4})?$", c)]
        hrefs = [urljoin(final, h).rstrip("/") for _, h in p.hreflang]
        out["hreflang"] = {"count": len(codes), "x_default": "x-default" in [c.lower() for c in codes],
                           "self_reference": final.rstrip("/") in hrefs,
                           "invalid_codes": bad,
                           "duplicates": sorted({c for c in codes if codes.count(c) > 1})}
    # URL hygiene
    out["url_checks"] = {"length": len(final), "uppercase": path != path.lower(),
                         "underscores": "_" in path, "depth": len([s for s in path.split("/") if s]),
                         "params": bool(urlparse(final).query)}
    # Mixed content
    if final.startswith("https://"):
        out["mixed_content"] = sorted({u[:100] for u in p.resource_urls if u.startswith("http://")})[:10]
    # Size ratios
    text_len = len(" ".join(p._text))
    out["text_html_ratio"] = round(100.0 * text_len / max(1, len(html)), 1)
    out["dom_elements"] = p.elements

    # Formatting and readability
    content_words = len(_words(content))
    bold_words = sum(len(_words(b)) for b in p.bold)
    out["formatting"] = {
        "bold_count": len(p.bold), "bold_words": bold_words,
        "bold_samples": p.bold[:8], "italic_count": p.italic,
        "lists": p.lists, "list_items": p.list_items, "tables": p.tables,
        "tables_with_header": p.tables_with_th, "blockquotes": p.blockquotes,
        "details": p.details, "paragraphs": len(p.paragraphs),
        "long_paragraphs_over_150_words": sum(1 for x in p.paragraphs if len(_words(x)) > 150),
        "content_words": content_words,
    }
    out["readability"] = readability(content, lang)
    out["keywords"] = keyword_analysis(p, final, content)

    # Citability signals (counted, not judged)
    q_heads = [t for lvl, t, _ in p.headings if lvl in (2, 3) and t.strip().endswith("?")]
    snippable = sum(1 for x in p.paragraphs if 20 <= len(_words(x)) <= 80)
    out["citability"] = {
        "statistics": len(STAT_RE.findall(content)),
        "definitions": len(DEFINITION_RE.findall(content)),
        "quotes": p.blockquotes,
        "question_headings": len(q_heads),
        "snippable_paragraphs": snippable,
        "first_paragraph_words": len(_words(p.paragraphs[0])) if p.paragraphs else 0,
    }

    # Links: rel quality, anchors, social, author, CTA, sources
    internal, external, nofollow_internal, nofollow_all = [], [], 0, 0
    empty_anchor, generic_anchor, social, social_placeholder = 0, [], set(), []
    rels = {"nofollow": 0, "sponsored": 0, "ugc": 0}
    for l in p.links:
        h = l["href"].strip()
        if not h or h.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        absu = urljoin(final, h)
        u = urlparse(absu)
        is_int = u.netloc == host
        # Body link: inside <main>/<article> when the page marks them up,
        # otherwise anything outside header, nav, footer and aside.
        l["in_main"] = l["in_main"] if p.has_main else not l["in_chrome"]
        for r in rels:
            if r in l["rel"]:
                rels[r] += 1
        if "nofollow" in l["rel"]:
            nofollow_all += 1
            if is_int:
                nofollow_internal += 1
        text = l.get("text", "")
        if not text and not l.get("aria"):
            empty_anchor += 1
        elif _norm(text).strip(" .>→»") in GENERIC_ANCHORS:
            generic_anchor.append(text)
        if is_int:
            internal.append((u.path or "/", l["in_main"], text))
        else:
            external.append((absu, l["in_main"]))
            bare = re.sub(r"^(www\.|m\.|mobile\.)", "", u.netloc.lower())
            if any(bare == s or bare.endswith("." + s) for s in SOCIAL_HOSTS):
                social.add(bare)
                if u.path.strip("/") in ("", "@", "in", "company", "channel", "user"):
                    social_placeholder.append(absu)
    out["link_quality"] = {
        "rel_counts": rels, "nofollow_internal": nofollow_internal,
        "nofollow_share": round(100.0 * nofollow_all / max(1, len(internal) + len(external))),
        "empty_anchors": empty_anchor, "generic_anchors": generic_anchor[:8],
        "unique_internal_targets": len({x[0] for x in internal}),
    }
    out["social_links"] = {"networks": sorted(social), "placeholders": social_placeholder[:6]}

    blog_prefix = "/" + (path.strip("/").split("/")[0] if path.strip("/") else "") + "/"
    money = sorted({x[0] for x in internal
                    if x[0] not in ("/", "") and not x[0].startswith(blog_prefix)
                    and not re.match(r"^/[a-z]{2}(?:-[a-z]{2})?/?$", x[0])
                    and not re.match(r"^/(?:[a-z]{2}/)?(blog|articles?|actualites|news|guides?|magazine)\b", x[0])
                    and not LEGAL_PATH_RE.search(x[0]) and not AUTHOR_PATH_RE.search(x[0])})
    money_in_body = sorted({x[0] for x in internal if x[1] and x[0] in money})
    tokens = " ".join(p.tokens)
    toc_links = sum(1 for l in p.links if l["href"].startswith("#") and len(l["href"]) > 1
                    and l["href"][1:] in p.all_ids)
    author_links = sorted({x[0] for x in internal if AUTHOR_PATH_RE.search(x[0])})
    jsonld_author = any(isinstance(o, (dict, list)) and '"author"' in json.dumps(o)
                        for o in p.jsonld_objects)
    author_img = any(AUTHOR_TOKEN_RE.search(_norm(i["alt"] or "") + " " + i["src"].lower())
                     for i in p.images)
    out["template"] = {
        "toc_detected": bool(TOC_TOKEN_RE.search(tokens)) or toc_links >= 3,
        "toc_anchor_links": toc_links,
        "author_block_markup": bool(AUTHOR_TOKEN_RE.search(tokens)),
        "author_page_links": author_links[:5],
        "author_in_jsonld": jsonld_author,
        "author_photo_hint": author_img,
        "dates": {"time_tags": p.times,
                  "jsonld_datePublished": "datePublished" in json.dumps(p.jsonld_objects),
                  "jsonld_dateModified": "dateModified" in json.dumps(p.jsonld_objects),
                  "article_meta": sorted(p.article_meta.keys())},
        "breadcrumb": "BreadcrumbList" in types or "breadcrumb" in tokens or "fil-ariane" in tokens,
        "cta_markup": len(CTA_TOKEN_RE.findall(tokens)),
        "money_page_links": money[:15],
        "money_page_links_in_body": money_in_body[:15],
        "external_sources_in_body": len([e for e in external if e[1]
                                         and not any(s in e[0] for s in SOCIAL_HOSTS)]),
        "video_embeds": [s for s in p.iframes if "youtube" in s or "vimeo" in s or "wistia" in s][:5],
    }
    if kind == "blog_hub":
        posts = {x[0] for x in internal
                 if x[0].startswith(path.rstrip("/") + "/") and x[0].rstrip("/") != path.rstrip("/")
                 and "/page/" not in x[0] and "/category/" not in x[0]}
        linked_imgs = sum(1 for i in p.images if i["in_link"])
        out["template"]["hub_posts_linked"] = len(posts)
        out["template"]["hub_card_images"] = linked_imgs

    # Images: format, dimensions, above-the-fold lazy, alt quality
    fmts = {}
    for i in p.images:
        ext = urlparse(i["src"]).path.rsplit(".", 1)[-1].lower() if "." in i["src"] else "?"
        fmts[ext] = fmts.get(ext, 0) + 1
    alts = [i["alt"] for i in p.images if i["alt"]]
    out["image_quality"] = {
        "formats": fmts,
        "legacy_format": sum(n for e, n in fmts.items() if e in ("jpg", "jpeg", "png", "gif", "bmp")),
        "no_dimensions": sum(1 for i in p.images if not (i["width"] and i["height"])),
        "no_srcset": sum(1 for i in p.images if not i["srcset"]),
        "first_image_lazy": bool(p.images and p.images[0]["loading"] == "lazy"),
        "alt_too_long": sum(1 for a in alts if len(a) > 125),
        "alt_generic": sum(1 for a in alts if _norm(a).strip() in
                           ("image", "photo", "img", "picture", "logo", "icon", "banner", "untitled")
                           or re.match(r"^(img|image|dsc|screenshot)[-_ ]?\d*(\.\w+)?$", _norm(a))),
        "alt_duplicates": len(alts) - len(set(alts)),
    }
    out["schema_problems"] = schema_checks(p.jsonld_objects)
    out["jsonld_parse_errors"] = p.jsonld_errors
    return out


def recommendations(pg, site):
    """Turn the facts into prioritized findings. Severity drives the score the
    same way the extension does: 100 minus critical 12.5, high 6, medium 3,
    low 1.5, computed separately for SEO and GEO findings."""
    R = []
    kind = pg.get("page_kind", "page")
    content_page = kind in ("article", "homepage", "page", "product", "blog_hub")

    def add(sev, pillar, code, msg):
        R.append({"severity": sev, "pillar": pillar, "code": code, "message": msg})

    t = pg["title"]
    if not t["value"]:
        add("high", "seo", "title_missing", "No <title>.")
    elif t["length"] < 30:
        add("medium", "seo", "title_short", "Title {} chars, aim for 30-60.".format(t["length"]))
    elif t["length"] > 60:
        add("medium", "seo", "title_long", "Title {} chars, Google truncates past about 60.".format(t["length"]))
    m = pg["meta_description"]
    if not m["present"]:
        add("high", "seo", "meta_missing", "No meta description.")
    elif m["length"] > 160:
        add("medium", "seo", "meta_long", "Meta description {} chars, aim for 120-160.".format(m["length"]))
    elif m["length"] < 120:
        add("low", "seo", "meta_short", "Meta description {} chars, aim for 120-160.".format(m["length"]))
    h = pg["headings"]
    if h["h1_count"] == 0:
        add("high", "seo", "h1_missing", "No H1.")
    elif h["h1_count"] > 1:
        add("medium", "seo", "h1_multiple", "{} H1 on the page.".format(h["h1_count"]))
    if h["level_jumps"]:
        add("medium", "seo", "heading_jumps", "Heading levels skipped: {}.".format(", ".join(h["level_jumps"][:4])))
    if h["empty"]:
        add("medium", "seo", "heading_empty", "{} empty heading(s).".format(h["empty"]))
    wc = pg["word_count"]
    if content_page and wc < 300:
        add("high", "seo", "thin_content", "{} words of content, under the 300 floor.".format(wc))
    elif kind == "article" and wc < 800:
        add("medium", "seo", "article_short", "Article at {} words; benchmark the SERP (usually 1200+).".format(wc))
    f = pg["formatting"]
    if kind != "blog_hub" and content_page and wc >= 250 and f["bold_count"] == 0:
        add("medium", "seo", "no_bold", "No bold text: bold the main keyword in the first paragraph and key facts in the body.")
    kw = pg["keywords"]
    for s in kw["stuffing"][:2]:
        sev = "high" if s["density"] > 7 else "medium"
        add(sev, "seo", "keyword_stuffing", "'{}' at {}% density (alert above 2.5%, stuffing above 7%).".format(s["term"], s["density"]))
    if kw["target_terms"] and content_page:
        miss_first = [k for k, v in kw["placement"].items() if not v["first_100_words"]]
        miss_bold = [k for k, v in kw["placement"].items() if not v["bold"]]
        if len(miss_first) == len(kw["placement"]):
            add("medium", "seo", "kw_not_in_intro", "None of the title terms appear in the first 100 words.")
        if f["bold_count"] and len(miss_bold) == len(kw["placement"]):
            add("low", "seo", "kw_not_bold", "Bold is used but never on the title terms.")
        if kw["placement_coverage"] < 40:
            add("medium", "seo", "kw_placement_low", "Title terms cover {}% of the placement zones (title, H1, H2, meta, URL, intro, bold, alt).".format(kw["placement_coverage"]))
    rd = pg["readability"]
    if rd.get("sentences", 0) >= 10 and rd.get("score", 100) < 60:
        add("low", "seo", "readability", "Readability {} / 100: {}% of sentences over 20 words.".format(rd["score"], rd["pct_over_20_words"]))
    if f["long_paragraphs_over_150_words"]:
        add("low", "geo", "long_paragraphs", "{} paragraph(s) over 150 words; split into 40-80 word blocks.".format(f["long_paragraphs_over_150_words"]))

    im = pg["images"]
    iq = pg["image_quality"]
    if im["missing_alt"]:
        add("high", "seo", "alt_missing", "{} image(s) without an alt attribute.".format(im["missing_alt"]))
    if iq["alt_generic"] or iq["alt_too_long"]:
        add("low", "seo", "alt_quality", "{} generic and {} overlong (125+ chars) alt texts.".format(iq["alt_generic"], iq["alt_too_long"]))
    if iq["first_image_lazy"]:
        add("medium", "seo", "lcp_lazy", "First image is lazy-loaded: likely the LCP image, load it eagerly.")
    if im.get("over_200kb"):
        add("medium", "seo", "image_weight", "{} image(s) over 200 KB.".format(len(im["over_200kb"])))
    if iq["legacy_format"] >= 2:
        add("low", "seo", "image_format", "{} JPG/PNG/GIF images; serve WebP or AVIF.".format(iq["legacy_format"]))
    if iq["no_dimensions"] >= 3:
        add("low", "seo", "image_dimensions", "{} images without width/height (layout shift).".format(iq["no_dimensions"]))

    lq = pg["link_quality"]
    if lq["nofollow_internal"]:
        add("high", "seo", "internal_nofollow", "{} internal link(s) in nofollow.".format(lq["nofollow_internal"]))
    if lq["nofollow_share"] > 50:
        add("medium", "seo", "nofollow_share", "{}% of links are nofollow.".format(lq["nofollow_share"]))
    if lq["empty_anchors"]:
        add("medium", "seo", "empty_anchor", "{} link(s) with no anchor text or label.".format(lq["empty_anchors"]))
    if lq["generic_anchors"]:
        add("medium", "seo", "generic_anchor", "Generic anchors: {}.".format(", ".join(sorted(set(lq["generic_anchors"]))[:5])))
    sl = pg["social_links"]
    if sl["placeholders"]:
        add("medium", "geo", "social_placeholder", "Social links point to a network homepage, not a profile: {}.".format(", ".join(sl["placeholders"][:4])))
    elif not sl["networks"] and kind in ("homepage", "article"):
        add("low", "geo", "social_missing", "No link to the brand or author social profiles (entity consistency, sameAs).")

    hd = pg["head"]
    if not pg["viewport"]:
        add("high", "seo", "viewport_missing", "No meta viewport (mobile-first indexing).")
    if not pg["lang"]:
        add("medium", "seo", "lang_missing", "No <html lang>.")
    if not hd["charset"]:
        add("low", "seo", "charset_missing", "No charset declaration.")
    if not hd["favicon"]:
        add("low", "seo", "favicon_missing", "No favicon link (shown next to the result on mobile).")
    if not pg["canonical"]:
        add("medium", "seo", "canonical_missing", "No canonical tag.")
    elif pg.get("canonical_self") is False:
        add("medium", "seo", "canonical_other", "Canonical points to another URL: {}.".format(pg["canonical"]))
    if "og:title" in hd["og_missing"] or "og:description" in hd["og_missing"]:
        add("medium", "seo", "og_missing", "Open Graph incomplete: missing {}.".format(", ".join(hd["og_missing"])))
    elif "og:image" in hd["og_missing"]:
        add("low", "seo", "og_image_missing", "No og:image (blank link previews).")
    if not hd["twitter_card"]:
        add("low", "seo", "twitter_missing", "No twitter:card.")
    if hd["meta_refresh"]:
        add("medium", "seo", "meta_refresh", "Meta refresh redirect: {}.".format(hd["meta_refresh"]))
    rb = pg["robots_directives"]
    if rb["noindex"]:
        add("critical", "seo", "noindex", "Page is noindex.")
    if rb["nosnippet"] or (rb["max_snippet"] is not None and 0 <= rb["max_snippet"] < 50):
        add("high", "geo", "snippet_capped", "nosnippet / max-snippet under 50 keeps the page out of AI Overviews and snippets.")
    if pg.get("mixed_content"):
        add("high", "seo", "mixed_content", "{} HTTP resource(s) on an HTTPS page.".format(len(pg["mixed_content"])))
    hl = pg.get("hreflang")
    if hl and (not hl["x_default"] or not hl["self_reference"] or hl["invalid_codes"] or hl["duplicates"]):
        add("medium", "seo", "hreflang", "Hreflang issues: x-default {}, self-reference {}, invalid {}, duplicates {}.".format(
            hl["x_default"], hl["self_reference"], hl["invalid_codes"] or "-", hl["duplicates"] or "-"))
    uc = pg["url_checks"]
    if uc["length"] > 100 or uc["uppercase"] or uc["underscores"]:
        add("low", "seo", "url_hygiene", "URL: {} chars, uppercase {}, underscores {}.".format(uc["length"], uc["uppercase"], uc["underscores"]))
    if pg["text_html_ratio"] < 10:
        add("low", "seo", "text_ratio", "Text is {}% of the HTML.".format(pg["text_html_ratio"]))
    if pg["dom_elements"] > 1500:
        add("low", "seo", "dom_size", "{} DOM elements (over 1500).".format(pg["dom_elements"]))
    if pg["html_size_kb"] > 1500:
        add("medium", "seo", "html_size", "HTML {} KB.".format(pg["html_size_kb"]))
    if pg.get("em_dashes", {}).get("body", 0) >= 4:
        add("medium", "geo", "em_dashes", "{} em/en dashes in the copy (AI-writing tell).".format(pg["em_dashes"]["body"]))

    # Structured data
    types = set(pg["schema_jsonld"])
    if pg["jsonld_parse_errors"]:
        add("high", "seo", "jsonld_invalid", "{} JSON-LD block(s) fail to parse.".format(pg["jsonld_parse_errors"]))
    if not types:
        add("high", "geo", "schema_none", "No JSON-LD at all.")
    else:
        if kind == "homepage" and not (types & {"Organization", "LocalBusiness", "Person", "ProfessionalService",
                                                 "Corporation", "OnlineStore", "EducationalOrganization"}):
            add("medium", "geo", "schema_entity", "Homepage without Organization or Person schema.")
        if kind == "article" and not (types & {"Article", "BlogPosting", "NewsArticle"}):
            add("medium", "geo", "schema_article", "Article without Article / BlogPosting schema.")
    for sp in pg["schema_problems"][:5]:
        add("medium", "geo", "schema_fields", "{} x{}: missing or empty {}.".format(sp["type"], sp["count"], ", ".join(sp["missing_or_empty"])))

    # Page templates (the blocks an article and a blog hub must ship)
    tp = pg["template"]
    if kind == "article":
        if not tp["toc_detected"]:
            add("medium", "geo", "toc_missing", "No table of contents (anchor links to the H2s, sticky in a sidebar on desktop).")
        if not (tp["author_block_markup"] or tp["author_in_jsonld"]):
            add("high", "geo", "author_missing", "No visible author block (name, photo, role, link to the author page, social profiles).")
        if not tp["author_page_links"]:
            add("medium", "geo", "author_page_link", "No link to an author or about page.")
        d = tp["dates"]
        if not (d["time_tags"] or d["jsonld_datePublished"] or d["article_meta"]):
            add("high", "geo", "date_missing", "No publication or update date.")
        if not tp["money_page_links_in_body"]:
            add("medium", "seo", "no_cta_money", "No link from the article body to a commercial page (offer, product, service, contact).")
        if not tp["breadcrumb"]:
            add("low", "seo", "breadcrumb_missing", "No breadcrumb.")
        if tp["external_sources_in_body"] < 3:
            add("medium", "geo", "few_sources", "{} external source(s) in the body; cite 3-5 authoritative sources.".format(tp["external_sources_in_body"]))
        cit = pg["citability"]
        if cit["statistics"] == 0:
            add("low", "geo", "no_stats", "No statistics in the text.")
        if cit["question_headings"] == 0:
            add("low", "geo", "no_question_h2", "No question-form H2/H3.")
        if f["tables"] == 0 and wc > 800:
            add("low", "geo", "no_table", "No table on an 800+ word page.")
    if kind == "blog_hub":
        n, imgs = tp.get("hub_posts_linked", 0), tp.get("hub_card_images", 0)
        if n >= 3 and imgs < n / 2:
            add("medium", "seo", "hub_no_covers", "{} posts listed but only {} linked image(s): give each card its cover image.".format(n, imgs))
    if kind == "homepage":
        if not tp["money_page_links"]:
            add("medium", "seo", "home_no_money_links", "Homepage links to no offer, product or service page.")
        if f["lists"] == 0 and f["tables"] == 0:
            add("low", "geo", "home_no_structure", "No list or table on the homepage.")

    # Site-level AI access (counted once, on the first page)
    if site and site.get("ai_search_bots_blocked"):
        add("high", "geo", "ai_bots_blocked", "AI search bots blocked in robots.txt: {}.".format(", ".join(site["ai_search_bots_blocked"])))

    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    R.sort(key=lambda r: order[r["severity"]])
    seo = max(0, 100 - sum(SEVERITY_POINTS[r["severity"]] for r in R if r["pillar"] == "seo"))
    geo = max(0, 100 - sum(SEVERITY_POINTS[r["severity"]] for r in R if r["pillar"] == "geo"))
    pg["recommendations"] = R
    pg["score"] = {"seo": round(seo), "geo": round(geo), "grade": _grade(min(seo, geo))}
    return pg


def _grade(s):
    return "A" if s >= 90 else "B" if s >= 80 else "C" if s >= 70 else "D" if s >= 60 else "F"


def analyse_page(url, do_images=True):
    out = {"url": url}
    try:
        final, status, headers, body = fetch(url)
    except (HTTPError, URLError, ssl.SSLError, Exception) as e:
        out["error"] = "{}: {}".format(type(e).__name__, e)
        return out

    # Honor the declared charset (ISO-8859-1 and windows-1252 sites otherwise
    # come out as mojibake in title, meta description and headings).
    charset = "utf-8"
    m = re.search(r"charset=([\w-]+)", headers.get("Content-Type", ""), re.I)
    if m:
        charset = m.group(1)
    try:
        html = body.decode(charset, errors="replace")
    except LookupError:
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
    h1 = [t for lvl, t, _ in p.headings if lvl == 1]
    jumps = []
    prev = 0
    for lvl, _, _ in p.headings:
        if prev and lvl > prev + 1:
            jumps.append("H{}->H{}".format(prev, lvl))
        prev = lvl
    out["headings"] = {
        "h1_count": len(h1), "h1_values": h1,
        "total": len(p.headings),
        "sequence": ["H{}".format(lvl) for lvl, _, _ in p.headings][:40],
        "level_jumps": jumps,
        "empty": sum(1 for _, t, _ in p.headings if not t),
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
            url, note = weight_url(img)
            if not url or url.startswith("data:"):
                continue
            kb = head_size(urljoin(final, url))
            checked += 1
            if kb and kb > IMG_WEIGHT_KB:
                heavy.append({"src": url[:120], "kb": kb, "note": note})
        out["images"]["checked"] = checked
        out["images"]["over_200kb"] = heavy

    # Internal vs external links
    host = urlparse(final).netloc
    internal = external = 0
    for l in p.links:
        h = l["href"]
        if h.startswith(("#", "mailto:", "tel:", "javascript:")):
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
    # AI-writing tell: em dashes and en dashes in the copy the visitor reads.
    # Characters are written as escapes so this file passes the repo dash sweep.
    dash_re = re.compile("[\\u2014\\u2013]")
    body_text = re.sub(r"\s+", " ", " ".join(p._text))
    samples = []
    for m in list(dash_re.finditer(body_text))[:5]:
        samples.append(body_text[max(0, m.start() - 40):m.end() + 40].strip())
    title_dashes = len(dash_re.findall(title))
    out["em_dashes"] = {
        "body": len(dash_re.findall(body_text)),
        "title": title_dashes,
        "meta_description": len(dash_re.findall(md or "")),
        "headings": sum(len(dash_re.findall(t)) for _, t, _ in p.headings),
        "samples": samples,
    }
    # JS rendering hint: very little text + client-side framework means the raw
    # HTML is probably incomplete. AI crawlers do not execute JavaScript, so
    # whatever is missing here is invisible to ChatGPT, Claude and Perplexity.
    out["likely_js_rendered"] = (out["word_count"] < 120 and
                                  any(f in fw for f in ("Framer", "Next.js", "Lovable", "Wix")))
    deep_checks(p, html, final, headers, out)
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
        # Parse robots.txt by group: one or more consecutive User-agent lines
        # share the rule block that follows them, and "*" applies to every bot.
        blocked_search, blocked_user_fetch, blocked_training = [], [], []
        all_bots_blocked = False
        blocks = re.findall(
            r"(?im)((?:^\s*user-agent:[^\n]*\n)+)((?:^(?!\s*user-agent:)[^\n]*\n?)*)", txt)
        for agents_raw, rules in blocks:
            agents = {a.strip().lower() for a in
                      re.findall(r"(?im)^\s*user-agent:\s*([^\n#]+)", agents_raw)}
            if re.search(r"(?im)^\s*disallow:\s*/\s*$", rules):
                if "*" in agents:
                    all_bots_blocked = True
                for bot in AI_BOTS:
                    if bot.lower() in agents or "*" in agents:
                        if bot in AI_SEARCH_BOTS:
                            blocked_search.append(bot)
                        elif bot in AI_USER_FETCH_BOTS:
                            blocked_user_fetch.append(bot)
                        else:
                            blocked_training.append(bot)
        out["ai_search_bots_blocked"] = sorted(set(blocked_search))
        out["ai_user_fetch_bots_blocked"] = sorted(set(blocked_user_fetch))
        out["ai_training_bots_blocked"] = sorted(set(blocked_training))
        out["all_bots_blocked_via_wildcard"] = all_bots_blocked
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
            oversized = []
            for child in children[:10]:
                try:
                    _, _, _, b2 = fetch(child.strip())
                    n = len(re.findall(r"<loc>", b2.decode("utf-8", "replace")))
                    total += n
                    if n > 50000:
                        oversized.append(child.strip())
                except Exception:
                    pass
            out["url_count_estimate"] = total
            out["note"] = "estimate from the first 10 child sitemaps" if len(children) > 10 else "total"
            if oversized:
                out["children_over_50k"] = oversized
        else:
            out["type"] = "urlset"
            out["url_count"] = len(re.findall(r"<loc>", xml))
            if out["url_count"] > 50000:
                out["over_50k"] = True
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
        bu = r.get("ai_user_fetch_bots_blocked")
        if bu:
            line("  AI user-fetch agents ruled : {} (robots.txt is not a reliable control for ChatGPT-User and Perplexity-User)".format(bu))
        line("  AI training bots blocked   : {}".format(bt if bt else "none"))
        if r.get("all_bots_blocked_via_wildcard"):
            line("  WARNING: 'User-agent: *' with 'Disallow: /' blocks EVERY crawler, AI and Google alike.")
    s = report.get("sitemap", {})
    if s.get("error"):
        line("  sitemap                    : {} (error: {})".format(s.get("url"), s["error"]))
    elif s:
        cnt = s.get("url_count") or s.get("url_count_estimate")
        line("  sitemap                    : {} ({}, ~{} URLs)".format(
            s.get("url"), s.get("type"), cnt))
        if s.get("over_50k") or s.get("children_over_50k"):
            line("  WARNING: a sitemap file exceeds the 50,000 URL limit; Google rejects the whole file. Split it into child sitemaps under a sitemap index.")
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
            line("     over 200KB ({}/{} checked):".format(
                len(im["over_200kb"]), im.get("checked")))
            for x in im["over_200kb"]:
                note = " -- {}".format(x["note"]) if x.get("note") else ""
                line("       {}KB  {}{}".format(x["kb"], x["src"], note))
        line("  WORDS (visible text): {}".format(pg["word_count"]))
        ed = pg.get("em_dashes") or {}
        total_ed = ed.get("body", 0) + ed.get("title", 0) + ed.get("meta_description", 0)
        if total_ed:
            line("  EM/EN DASHES: {} in body, {} in title, {} in meta description"
                 " [AI-writing tell, replace with commas]".format(
                     ed.get("body", 0), ed.get("title", 0), ed.get("meta_description", 0)))
            for s in ed.get("samples", [])[:3]:
                line("       ...{}...".format(s[:110]))
        line("  LINKS internal={} | external={}".format(
            pg["links"]["internal"], pg["links"]["external"]))
        og = pg["open_graph"]
        line("  Open Graph: {}".format("yes " + str(og["keys"]) if og["present"] else "NO"))
        line("  canonical: {} | schema: {}".format(
            pg["canonical"] or "NO", pg["schema_jsonld"] or "none"))
        line("  viewport: {} | html lang: {} | meta robots: {}".format(
            "yes" if pg["viewport"] else "NO", "yes" if pg["lang"] else "NO",
            pg["meta_robots"] or "-"))
        fm, kw, rd = pg["formatting"], pg["keywords"], pg["readability"]
        line("  PAGE KIND: {} | SCORE seo={} geo={} grade={}".format(
            pg["page_kind"], pg["score"]["seo"], pg["score"]["geo"], pg["score"]["grade"]))
        line("  BOLD {} ({} words) {} | italic {} | lists {} | tables {} ({} with header) | quotes {}".format(
            fm["bold_count"], fm["bold_words"], fm["bold_samples"][:4], fm["italic_count"],
            fm["lists"], fm["tables"], fm["tables_with_header"], fm["blockquotes"]))
        line("  KEYWORDS top: {}".format(", ".join(
            "{} {}%".format(x["term"], x["density"]) for x in kw["top_terms"][:8])))
        if kw["placement"]:
            zones = list(next(iter(kw["placement"].values())).keys())
            line("  PLACEMENT ({}% coverage)  zones: {}".format(kw["placement_coverage"], " ".join(zones)))
            for term, z in kw["placement"].items():
                line("     {:<18} {}".format(term[:18], " ".join("x" if z[k] else "." for k in zones)))
        if rd.get("sentences"):
            line("  READABILITY score={} flesch={} avg sentence={} words | >20 words {}% | >30 words {}%".format(
                rd["score"], rd["flesch"], rd["avg_sentence_words"], rd["pct_over_20_words"], rd["pct_over_30_words"]))
        ci = pg["citability"]
        line("  CITABILITY stats={} definitions={} quotes={} question H2/H3={} snippable paragraphs={}".format(
            ci["statistics"], ci["definitions"], ci["quotes"], ci["question_headings"], ci["snippable_paragraphs"]))
        tp = pg["template"]
        line("  TEMPLATE toc={} author block={} author page links={} dates={} breadcrumb={} money links in body={}".format(
            tp["toc_detected"], tp["author_block_markup"] or tp["author_in_jsonld"], tp["author_page_links"] or "none",
            bool(tp["dates"]["time_tags"] or tp["dates"]["jsonld_datePublished"] or tp["dates"]["article_meta"]),
            tp["breadcrumb"], len(tp["money_page_links_in_body"])))
        if "hub_posts_linked" in tp:
            line("  BLOG HUB posts linked={} card images={}".format(tp["hub_posts_linked"], tp["hub_card_images"]))
        sl = pg["social_links"]
        line("  SOCIAL {} | placeholders: {}".format(sl["networks"] or "none", sl["placeholders"] or "-"))
        if pg["schema_problems"]:
            line("  SCHEMA FIELDS: {}".format("; ".join("{} x{} missing {}".format(
                s["type"], s["count"], "/".join(s["missing_or_empty"])) for s in pg["schema_problems"][:6])))
        line("  FINDINGS ({}):".format(len(pg["recommendations"])))
        for r in pg["recommendations"]:
            line("     [{:<8}] {:<3} {}".format(r["severity"], r["pillar"].upper(), r["message"]))

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
    for i, pg in enumerate(pages):
        if not pg.get("error"):
            recommendations(pg, robots if i == 0 else None)

    report = {"base": base, "robots": robots, "sitemap": sitemap,
              "llms_txt": llms, "pages": pages}
    print(fmt(report))
    return 1 if all(p.get("error") for p in pages) else 0


if __name__ == "__main__":
    sys.exit(main())
