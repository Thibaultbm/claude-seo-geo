# Page skill standard: spec, audit, benchmark, build

Every skill that owns a page type (homepage, service, product, collection, comparison, blog, local, page sections) is a specification (cahier des charges) that runs in four phases. The same four phases, in the same order, with the same deliverable, in every page skill. A reader who knows one page skill knows them all.

| Phase | Question it answers | Tools | Output |
|---|---|---|---|
| 1. Spec | What must a page of this type contain? | The page skill's spec table + `skills/seo-geo-audit/references/common-page-spec.md` | The checklist, with IDs |
| 2. Audit | What does the existing page contain? | `seo_audit.py <url>`, `section_audit.py --type <type> <url>` | Every spec row marked Pass, Fail or Not verifiable |
| 3. Benchmark | What do the pages that rank (and that AI assistants cite) contain? | `page_benchmark.py --type <type> <client> <3-5 competitors>` | Block x competitor table, gaps, metrics below the median, the information gain to add |
| 4. Build | What do we write and change, and when is it done? | The page skill's wireframe, copy rules, schema templates | The finished page or the change list, then the scripts re-run as the acceptance test |

When no page exists yet, Phase 2 is skipped and Phase 3 sets the bar for the build.

## Required structure of a page skill SKILL.md

1. Frontmatter: `name`, `description` that says the skill runs spec, audit, competitor benchmark and build for its page type, `license`, `metadata`.
2. Title and a 2-4 line intro: what the page type is for and how it fails.
3. Company knowledge first (Obsidian): short, unchanged pattern.
4. When to use, and the routing table to adjacent skills.
5. `## Phase 1. The spec`: the page-specific requirements as a table with stable IDs (prefix per skill: HOME, SVC, PDP, COL, CMP, BLOG, LOC, SEC), columns `ID | Requirement | Threshold | Verified by | Why`, plus the line "Common requirements C-01 to C-26: skills/seo-geo-audit/references/common-page-spec.md". "Verified by" is a `seo_audit.py` finding code, a `section_audit.py` block, or "manual".
6. `## Phase 2. Audit the existing page`: the exact commands with the right `--type`, and how to map findings to spec IDs.
7. `## Phase 3. Benchmark the competitors`: how to pick them for this page type (the query, the SERP, the AI answers), the `page_benchmark.py` command, what to read in its output, and the information gain to define.
8. `## Phase 4. Build`: the wireframe or skeleton, copy rules, schema, metadata patterns, then the acceptance test (scripts re-run, finish line).
9. Reference sections kept from the original skill (rules and thresholds, GEO layer, special cases), each tied to spec IDs where they justify one.
10. `## Deliverable`: the standard four-part output (below).
11. Common mistakes, Sources.

## Standard deliverable

```markdown
## 1. Spec scorecard
| ID | Requirement | Status (Pass / Fail / Not verifiable) | Evidence |

## 2. Audit findings
(seo_audit.py scores and high or medium findings, section_audit.py blocks; or "new page")

## 3. Competitor benchmark
(page_benchmark.py table, blocks and schema types the client lacks, metrics below the median, the information gain chosen)

## 4. Build
(the copy, block by block, metadata, JSON-LD, internal links; placeholders {to confirm} for unverified facts)

## 5. Acceptance
(scripts re-run: remaining findings, each either fixed or a written owner decision)
```

## House rules that apply to every skill

- No em dashes or en dashes, no emoji (CI checks them).
- SKILL.md under 500 lines; long material goes to `references/` and is loaded on demand.
- Every number tagged as measured (with a source) or as a field heuristic.
- Never invent client facts: unknowns stay as `{to confirm}`.
