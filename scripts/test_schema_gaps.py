#!/usr/bin/env python3
"""Offline regression test for the structured data gap detector of seo_audit.py.

Each case is a small HTML page served from memory (no network): the codes the
detector must raise, and the codes it must not raise. Run it after any change
to schema_gaps() or to the regexes it uses:

    python3 scripts/test_schema_gaps.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "seo-geo-audit", "scripts"))
import seo_audit as S  # noqa: E402

PAGES = {}


def fake_fetch(url, method="GET"):
    return url, 200, {"Content-Type": "text/html; charset=utf-8"}, PAGES[url].encode("utf-8")


S.fetch = fake_fetch


def page(body, jsonld=None, head=""):
    ld = ""
    for block in jsonld or []:
        ld += '<script type="application/ld+json">{}</script>'.format(block)
    return ("<!doctype html><html lang='en'><head><title>Test page title here</title>"
            "<meta name='viewport' content='width=device-width'>{}{}</head><body>{}</body></html>"
            ).format(head, ld, body)


FILLER = "<p>" + ("Plain descriptive sentence about the topic of this page. " * 30) + "</p>"

CASES = [
    {
        "name": "product page, reviews, breadcrumb and video, no markup",
        "url": "https://shop.test/products/blue-shoe",
        "html": page(
            "<nav aria-label='breadcrumb'><a href='/'>Home</a> <a href='/collections/shoes'>Shoes</a></nav>"
            "<main><h1>Blue shoe</h1><p class='price'>49,90 €</p><button class='add-to-cart'>Add to cart</button>"
            + FILLER +
            "<section class='product-reviews'><h2>Customer reviews</h2><p>4.8/5 based on 132 reviews</p>"
            "<div class='review-card'>Great shoe</div><div class='review-card'>Comfortable</div></section>"
            "<iframe src='https://www.youtube.com/embed/abc123'></iframe></main>"),
        "expect": {"schema_gap_product", "schema_gap_reviews", "schema_gap_breadcrumb", "schema_gap_video"},
        "forbid": {"schema_gap_offer"},
        "severity": {"schema_gap_reviews": "high", "schema_gap_product": "high"},
    },
    {
        "name": "same product page, fully marked up",
        "url": "https://shop.test/products/blue-shoe-ok",
        "html": page(
            "<nav aria-label='breadcrumb'><a href='/'>Home</a></nav>"
            "<main><h1>Blue shoe</h1><p class='price'>49,90 €</p><button class='add-to-cart'>Add to cart</button>"
            + FILLER +
            "<section class='product-reviews'><h2>Customer reviews</h2><p>4.8/5 based on 132 reviews</p>"
            "<div class='review-card'>Great shoe</div></section>"
            "<iframe src='https://www.youtube.com/embed/abc123'></iframe></main>",
            ['{"@context":"https://schema.org","@graph":['
             '{"@type":"Product","name":"Blue shoe","image":"https://shop.test/a.jpg",'
             '"offers":{"@type":"Offer","price":"49.90","priceCurrency":"EUR"},'
             '"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"132"}},'
             '{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home"}]},'
             '{"@type":"VideoObject","name":"Shoe","thumbnailUrl":"https://shop.test/t.jpg","uploadDate":"2026-01-01"}]}']),
        "expect": set(),
        "forbid": {"schema_gap_product", "schema_gap_reviews", "schema_gap_breadcrumb", "schema_gap_video",
                   "schema_rating_mismatch", "schema_review_host"},
    },
    {
        "name": "rating in markup differs from the page",
        "url": "https://shop.test/products/red-shoe",
        "html": page(
            "<main><h1>Red shoe</h1><p class='price'>$59</p><button>Add to cart</button>" + FILLER +
            "<p>Rated 4.8 out of 5 stars, 90 reviews</p></main>",
            ['{"@context":"https://schema.org","@type":"Product","name":"Red shoe",'
             '"offers":{"@type":"Offer","price":"59","priceCurrency":"USD"},'
             '"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.5","reviewCount":"90"}}']),
        "expect": {"schema_rating_mismatch"},
        "forbid": {"schema_gap_reviews", "schema_gap_product"},
    },
    {
        "name": "local business homepage: map, hours, testimonials, social links",
        "url": "https://plombier.test/",
        "html": page(
            "<header><a href='tel:+33100000000'>01 00 00 00 00</a></header>"
            "<main><h1>Plombier a Lyon</h1>" + FILLER +
            "<h2>Avis clients</h2><blockquote>Intervention rapide, merci</blockquote>"
            "<h2>Horaires d'ouverture</h2><p>Lundi au vendredi, 8h a 19h</p>"
            "<iframe src='https://www.google.com/maps/embed?pb=xyz'></iframe></main>"
            "<footer><a href='https://www.facebook.com/plombierlyon'>Facebook</a>"
            "<a href='https://www.instagram.com/plombierlyon'>Instagram</a></footer>",
            ['{"@context":"https://schema.org","@type":"Organization","name":"Plombier Lyon","url":"https://plombier.test/"}']),
        "expect": {"schema_gap_local", "schema_gap_reviews", "schema_gap_sameas", "schema_gap_website"},
        "forbid": {"schema_gap_product", "schema_gap_offer"},
        "severity": {"schema_gap_reviews": "low"},
    },
    {
        "name": "self-serving rating on LocalBusiness",
        "url": "https://salon.test/",
        "html": page(
            "<main><h1>Salon</h1>" + FILLER + "<h2>Reviews</h2><p>4.9/5 from 210 reviews</p></main>",
            ['{"@context":"https://schema.org","@graph":[{"@type":"WebSite","name":"Salon","url":"https://salon.test/"},'
             '{"@type":"HairSalon","name":"Salon","address":{"@type":"PostalAddress","streetAddress":"1 rue"},'
             '"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"210"}}]}']),
        "expect": {"schema_review_host"},
        "forbid": {"schema_gap_reviews", "schema_rating_mismatch"},
    },
    {
        "name": "blog article: no false reviews, author as a string",
        "url": "https://blog.test/blog/how-to-write-a-brief",
        "html": page(
            "<main><article><h1>How to write a brief</h1><div class='author-box'>By Jane Doe</div>" + FILLER +
            "<h2>Can I review my draft before it goes live?</h2><p>4 out of 5 marketers skip this. "
            "We tested 10 reviews tools and $1500 a month agencies.</p>"
            "<h2>Localo review: what it does</h2><p>Text.</p></article></main>",
            ['{"@context":"https://schema.org","@type":"BlogPosting","headline":"How to write a brief",'
             '"author":"Jane Doe","datePublished":"2026-03-01","image":"https://blog.test/c.jpg"}']),
        "expect": {"schema_author_string"},
        "forbid": {"schema_gap_reviews", "schema_gap_offer", "schema_gap_product", "schema_gap_author"},
    },
    {
        "name": "SaaS pricing page, plans and testimonials, no markup",
        "url": "https://saas.test/pricing",
        "html": page(
            "<main><h1>Pricing</h1>" + FILLER +
            "<div class='plan-card'><span class='price'>$29</span>/month</div>"
            "<div class='plan-card'><span class='price'>$99</span>/month</div>"
            "<a href='/signup'>Start free trial</a>"
            "<div class='testimonial'>Doubled our traffic</div><div class='testimonial'>Great tool</div></main>"),
        "expect": {"schema_gap_offer", "schema_gap_reviews"},
        "forbid": {"schema_gap_product"},
        "severity": {"schema_gap_reviews": "medium"},
    },
    {
        "name": "reviews in microdata count as markup",
        "url": "https://shop.test/products/green-shoe",
        "html": page(
            "<main><div itemscope itemtype='https://schema.org/Product'><h1 itemprop='name'>Green shoe</h1>"
            "<p class='price'>$45</p><button>Add to cart</button>" + FILLER +
            "<div itemprop='aggregateRating' itemscope itemtype='https://schema.org/AggregateRating'>"
            "4.6/5 from 40 reviews</div></div></main>"),
        "expect": set(),
        "forbid": {"schema_gap_reviews", "schema_gap_product"},
    },
    {
        "name": "Trustpilot widget only (reviews rendered by JavaScript)",
        "url": "https://brand.test/",
        "html": page(
            "<main><h1>Brand</h1>" + FILLER +
            "<div class='trustpilot-widget' data-template-id='x'></div></main>",
            ['{"@context":"https://schema.org","@type":"Organization","name":"Brand","url":"https://brand.test/"}'],
            head="<script src='https://widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js'></script>"),
        "expect": {"schema_gap_reviews"},
        "forbid": {"schema_gap_product"},
    },
    {
        "name": "author page without Person",
        "url": "https://blog.test/author/jane-doe",
        "html": page("<main><h1>Jane Doe</h1>" + FILLER + "</main>",
                     ['{"@context":"https://schema.org","@type":"WebPage","name":"Jane Doe"}']),
        "expect": {"schema_gap_profile"},
        "forbid": set(),
    },
    {
        "name": "sitewide rating badge in footer and in a Webflow navbar div",
        "url": "https://agency.test/services/seo",
        "html": page(
            "<div class='navbar w-nav' role='banner'><span class='hero-rating'>Google 5/5</span></div>"
            "<main><h1>SEO service</h1>" + FILLER + "</main>"
            "<footer><div class='rating'>Rated 4.9/5 on Google, 120 reviews</div></footer>",
            ['{"@context":"https://schema.org","@type":"Service","name":"SEO","provider":{"@id":"https://agency.test/#org"}}']),
        "expect": set(),
        "forbid": {"schema_gap_reviews", "schema_gap_aggregate"},
    },
    {
        "name": "collection page and background video",
        "url": "https://shop.test/collections/shoes",
        "html": page(
            "<main><h1>Shoes</h1><video autoplay muted loop playsinline src='/bg.mp4'></video>" + FILLER +
            "".join("<div class='card'><p class='price'>${}</p><button>Add to cart</button></div>".format(20 + i)
                    for i in range(12)) + "</main>",
            ['{"@context":"https://schema.org","@type":"CollectionPage","name":"Shoes"}']),
        "expect": set(),
        "forbid": {"schema_gap_product", "schema_gap_video", "schema_gap_offer"},
    },
]


def main():
    failures = 0
    for case in CASES:
        PAGES[case["url"]] = case["html"]
        pg = S.analyse_page(case["url"], do_images=False)
        if pg.get("error"):
            print("FAIL  {}: {}".format(case["name"], pg["error"]))
            failures += 1
            continue
        codes = {g["code"] for g in pg["schema_gaps"]}
        missing = case["expect"] - codes
        wrong = case["forbid"] & codes
        sev = {g["code"]: g["severity"] for g in pg["schema_gaps"]}
        bad_sev = ["{} is {}, expected {}".format(c, sev.get(c), v)
                   for c, v in case.get("severity", {}).items() if sev.get(c) != v]
        if missing or wrong or bad_sev:
            failures += 1
            print("FAIL  {}".format(case["name"]))
            if missing:
                print("      not raised: {}".format(", ".join(sorted(missing))))
            if wrong:
                print("      raised by mistake: {}".format(", ".join(sorted(wrong))))
            for b in bad_sev:
                print("      severity: {}".format(b))
            print("      got: {}".format(", ".join(sorted(codes)) or "nothing"))
        else:
            print("ok    {}  [{}]".format(case["name"], ", ".join(sorted(codes)) or "no gap"))
    print("\n{} case(s), {} failure(s)".format(len(CASES), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
