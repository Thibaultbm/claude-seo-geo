# Using these skills outside Claude Code

Every skill in this repository is plain markdown that follows the open Agent Skills format (https://agentskills.io). Nothing here depends on Claude Code internals, so the same files work in any agent that can read instructions from disk.

## Claude Code

Install as a plugin (recommended):

```
/plugin marketplace add Thibaultbm/claude-seo-geo
/plugin install claude-seo-geo@sorank
```

Or copy skills manually:

```
git clone --depth 1 https://github.com/Thibaultbm/claude-seo-geo.git
cp -r claude-seo-geo/skills/* ~/.claude/skills/
```

## Cursor, Codex, Gemini CLI, Cline, Aider and others

1. Clone the repository somewhere stable.
2. Point your agent at the skill you need: paste the relevant `SKILL.md` into context, or reference its path in your rules file (`.cursorrules`, `AGENTS.md`, `GEMINI.md`, etc).
3. The `references/` files inside each skill are meant to be loaded on demand: load them when the SKILL.md says so, not upfront.
4. The executables in the repository are `skills/seo-geo-audit/scripts/seo_audit.py`, `skills/seo-page-sections/scripts/section_audit.py`, `skills/seo-ai-site-builders/scripts/render_check.py`, and the two vault-audit scripts in `skills/obsidian-brain/scripts/` (`link_graph.py`, `person_matches.py`). All are pure Python standard library (Python 3.9+), read only, no packages to install, no API keys.

## Skill map

| Skill | Use it for |
|---|---|
| obsidian-brain | Build and maintain the knowledge vault (architecture, importing docs and WhatsApp, link audit) that every skill reads first and logs to after |
| seo-geo-audit | Full site audit (SEO + AI visibility), prioritized action plan |
| seo-technical | Crawlability, indexation, speed, JS rendering, AI crawler access |
| seo-keyword-research | Keywords, search intent, AI prompt research |
| seo-content-blog | Blog articles that rank and get cited |
| seo-content-product-page | E-commerce product pages |
| seo-content-service-page | Service and landing pages |
| seo-content-collection-page | E-commerce category and collection pages |
| seo-content-comparison-page | Comparison, alternatives, best-for and customer segment pages |
| seo-page-sections | Which sections a page is missing, and the content to fill each gap |
| seo-ai-site-builders | Sites built by AI generators (Lovable, Base44, Bolt, v0, Bubble and others): turn the JavaScript app into served HTML so it can be indexed and cited |
| seo-internal-linking | Internal links, silos, orphan pages |
| seo-schema-markup | Structured data that still matters in 2026 |
| seo-backlinks | Link building, ninja linking, brand mentions |
| seo-local | Google Business Profile, reviews, local pages |
| social-amplification | Repurpose and distribute content to drive branded search and feed AI citation surfaces |
| geo-visibility | Getting cited by ChatGPT, Perplexity, AI Overviews |
| geo-tracking | Measuring AI traffic, citations and share of voice |
