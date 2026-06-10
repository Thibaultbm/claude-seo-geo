# AI crawlers: canonical reference

Single source of truth for AI crawler behavior across this repository. Other skills (seo-geo-audit, geo-visibility, geo-tracking, seo-schema-markup, content skills) link here instead of duplicating bot facts. Scope: who crawls, what each bot feeds, whether robots.txt holds, how to verify identity, and which robots.txt to ship.

## The three bot roles

Confusing these roles produces wrong robots.txt decisions, because blocking each role has a different cost.

| Role | What it feeds | Cost of blocking it |
|---|---|---|
| Training crawler | Future model weights | Brand knowledge inside the model: recommendations that happen without any web search |
| Search-index crawler | The engine's live retrieval index | Citations and visibility in answers, lost within days |
| User-fetch agent | One page load on a user's explicit request | Mostly unblockable via robots.txt by design |

## Crawler table

| User-agent | Operator | Role | Obeys robots.txt | Identity verification |
|---|---|---|---|---|
| GPTBot | OpenAI | Training | Yes | https://openai.com/gptbot.json |
| OAI-SearchBot | OpenAI | Search index (ChatGPT search citations) | Yes | https://openai.com/searchbot.json |
| ChatGPT-User | OpenAI | User fetch | No (acts on direct user requests) | https://openai.com/chatgpt-user.json |
| ClaudeBot | Anthropic | Training | Yes, supports Crawl-delay | https://claude.com/crawling/bots.json |
| Claude-SearchBot | Anthropic | Search index | Yes | https://claude.com/crawling/bots.json |
| Claude-User | Anthropic | User fetch | Yes | https://claude.com/crawling/bots.json |
| PerplexityBot | Perplexity | Search index | Yes | https://www.perplexity.com/perplexitybot.json |
| Perplexity-User | Perplexity | User fetch | Generally no | https://www.perplexity.com/perplexity-user.json |
| Googlebot | Google | Search, AI Overviews, AI Mode grounding | Yes | Reverse DNS plus https://developers.google.com/search/apis/ipranges/googlebot.json |
| Google-Extended | Google | Control token (Gemini training and grounding), not a crawler | Yes (as a token) | Not applicable: fetches arrive via Google infrastructure |
| Bingbot | Microsoft | Bing, Copilot, supplies ChatGPT search | Yes | Reverse DNS (search.msn.com) |
| CCBot | Common Crawl | Open datasets reused for training by many labs | Yes | https://commoncrawl.org/ccbot |
| Applebot-Extended | Apple | Control token for Apple Intelligence training (the crawler is Applebot) | Yes (as a token) | https://support.apple.com/en-us/119829 |
| Meta-ExternalAgent | Meta | Training | Declared yes | https://developers.facebook.com/docs/sharing/webmasters/web-crawlers |
| Amazonbot | Amazon | Alexa and AI answers | Yes | https://developer.amazon.com/amazonbot |
| DuckAssistBot | DuckDuckGo | DuckAssist answers | Yes | https://duckduckgo.com/duckduckgo-help-pages/results/duckassistbot/ |
| MistralAI-User | Mistral | User fetch (Le Chat) | Declared yes | No published IP list; judge by behavior |
| Bytespider | ByteDance | Training | Reputed non-compliant | No published list; enforce at CDN or WAF |

## Behavioral facts that change decisions

1. None of them execute JavaScript. Measured across 500M+ fetches by Vercel and MERJ: GPTBot, ClaudeBot, PerplexityBot, and Meta-ExternalAgent sometimes download JavaScript files (11.5 percent of ChatGPT fetches, 23.8 percent of Claude fetches) and execute none of it. Content must live in the raw HTML (https://vercel.com/blog/the-rise-of-the-ai-crawler).
2. Googlebot is the only renderer. Gemini, AI Overviews, and AI Mode can see client-side rendered content; ChatGPT, Claude, and Perplexity cannot (https://www.gsqi.com/marketing-blog/ai-search-javascript-rendering/).
3. Google-Extended does not control AI Overviews. It only opts out of Gemini training and grounding. AI Overviews and AI Mode are fed by standard Googlebot crawling; the only opt-outs (nosnippet, max-snippet, noindex) also reduce classic search snippets (https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers).
4. Bing is a gateway to ChatGPT search. Being indexed in Bing (Bing Webmaster Tools plus IndexNow) is part of ChatGPT visibility (https://yoast.com/chatgpt-search/).
5. User-fetch agents follow users, not robots. ChatGPT-User and Perplexity-User load a page when a human asks for it; robots.txt is not a reliable control for them. A page that must stay private needs authentication, not a robots rule.
6. Bytespider has a reputation for ignoring robots.txt. When blocking it matters, enforce at the CDN or WAF, not in robots.txt alone.

## robots.txt recipes

### Strategy 1: maximum AI visibility (default for brands, SaaS, lead-gen, e-commerce)

Rationale: presence in training data means the model itself knows the brand and can recommend it even when the answer runs without web search. Citations additionally require the search-index bots. Both are wanted, so nothing is blocked.

    # Allow all crawlers, including AI training and search bots
    User-agent: *
    Allow: /

    Sitemap: https://www.example.com/sitemap.xml

No per-bot rules are needed: the absence of Disallow allows everything.

### Strategy 2: defensive publisher (content is the product)

Rationale: keep every live answer surface that cites and links back, refuse to feed training sets and open datasets.

    # Search and citation surfaces: allowed
    User-agent: OAI-SearchBot
    Allow: /

    User-agent: Claude-SearchBot
    Allow: /

    User-agent: PerplexityBot
    Allow: /

    # Training and datasets: blocked
    User-agent: GPTBot
    Disallow: /

    User-agent: ClaudeBot
    Disallow: /

    User-agent: CCBot
    Disallow: /

    User-agent: Google-Extended
    Disallow: /

    User-agent: Applebot-Extended
    Disallow: /

    User-agent: meta-externalagent
    Disallow: /

    User-agent: Bytespider
    Disallow: /

    Sitemap: https://www.example.com/sitemap.xml

Notes:

- Googlebot and Bingbot stay allowed (no rule means allowed): blocking them removes classic search, AI Overviews, Copilot, and the Bing-to-ChatGPT path at once.
- robots.txt is a request, not a wall. Compliant bots honor it; Bytespider reportedly does not. Hard enforcement happens at the CDN or WAF layer.
- After switching strategies, re-test citations with the geo-tracking skill: training opt-outs show no immediate effect, search-bot blocks show within days.

## Anti-spoofing: verify before trusting

User-agent strings are trivially forged; scrapers impersonate GPTBot to bypass paywalls and they skew log analyses. Before whitelisting a bot at the WAF or counting it in a crawl report:

1. Check the source IP against the operator's published ranges (URLs in the crawler table above).
2. For Googlebot and Bingbot, run reverse DNS, then forward-confirm:

       host 66.249.66.1
       # expect a *.googlebot.com name, then resolve that name back to the same IP

3. Treat unverifiable "AI bots" as scrapers: rate-limit rather than whitelist.

## Sources

- https://vercel.com/blog/the-rise-of-the-ai-crawler
- https://www.gsqi.com/marketing-blog/ai-search-javascript-rendering/
- https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers
- https://developers.google.com/search/docs/appearance/ai-features
- https://yoast.com/chatgpt-search/
- Operator bot pages: linked per row in the crawler table
