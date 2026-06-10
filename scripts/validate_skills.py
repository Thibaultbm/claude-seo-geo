#!/usr/bin/env python3
"""Validate every skill in skills/ against the Agent Skills format and house rules.

Checks per skill:
  1. SKILL.md exists and starts with YAML frontmatter
  2. frontmatter has name (== folder name, lowercase, hyphens) and description (<= 1024 chars)
  3. body stays under 500 lines (soft limit, warning only above 460)
  4. evals/evals.json, when present, is valid JSON with a non-empty evals array
  5. no em dashes or en dashes anywhere (house style)
  6. no emoji anywhere (house style)

Exit code 0 if clean, 1 if any error. Stdlib only.
Usage: python3 scripts/validate_skills.py [repo_root]
"""

import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Characters are written as \u escapes so this file passes its own sweep.
DASH_RE = re.compile("[\\u2014\\u2013]")  # em dash, en dash
EMOJI_RE = re.compile(
    "[\\U0001F000-\\U0001FAFF\\u2600-\\u27BF\\U0001F1E6-\\U0001F1FF\\u2B00-\\u2BFF\\uFE0F]"
)
TEXT_EXTENSIONS = {".md", ".json", ".py", ".yml", ".yaml", ".txt"}


def parse_frontmatter(text):
    """Return (dict, body) from a SKILL.md. Minimal YAML: top-level key: value."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    block = text[3:end].strip("\n")
    body = text[end + 4:]
    data = {}
    current_key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and current_key:
            continue  # nested metadata, not validated here
        if ":" in line:
            key, _, value = line.partition(":")
            current_key = key.strip()
            data[current_key] = value.strip().strip('"')
    return data, body


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    errors, warnings = [], []

    skill_dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir())
    if not skill_dirs:
        errors.append("no skill directories found under skills/")

    for d in skill_dirs:
        skill_md = d / "SKILL.md"
        label = d.name
        if not skill_md.exists():
            errors.append(f"{label}: SKILL.md missing")
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{label}: missing or unterminated YAML frontmatter")
            continue
        name = fm.get("name", "")
        if name != d.name:
            errors.append(f"{label}: frontmatter name '{name}' != folder name")
        if not NAME_RE.match(name or ""):
            errors.append(f"{label}: name must be lowercase letters, digits and hyphens")
        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{label}: description missing")
        elif len(desc) > 1024:
            errors.append(f"{label}: description is {len(desc)} chars (max 1024)")
        # Unquoted "key: value: more" breaks strict YAML parsers (skills CLI, plugin loaders).
        for raw_line in text[:text.find("\n---", 3)].splitlines():
            if raw_line.startswith("description:"):
                raw_value = raw_line[len("description:"):].strip()
                if ": " in raw_value and not (raw_value.startswith('"') and raw_value.endswith('"')):
                    errors.append(f"{label}: description contains an unquoted colon-space; rephrase or quote the whole value")
        body_lines = body.count("\n") + 1
        if body_lines > 500:
            errors.append(f"{label}: SKILL.md body is {body_lines} lines (max 500)")
        elif body_lines > 460:
            warnings.append(f"{label}: SKILL.md body is {body_lines} lines (close to the 500 limit)")

        evals_file = d / "evals" / "evals.json"
        if evals_file.exists():
            try:
                payload = json.loads(evals_file.read_text(encoding="utf-8"))
                if not payload.get("evals"):
                    errors.append(f"{label}: evals.json has no evals")
            except json.JSONDecodeError as exc:
                errors.append(f"{label}: evals.json invalid JSON ({exc})")
        else:
            warnings.append(f"{label}: no evals/evals.json")

    # House style sweep over every text file in the repo (skills, README, scripts).
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_EXTENSIONS:
            continue
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root)
        for lineno, line in enumerate(text.splitlines(), 1):
            if DASH_RE.search(line):
                errors.append(f"{rel}:{lineno}: em/en dash found (use comma, colon or parentheses)")
            if EMOJI_RE.search(line):
                errors.append(f"{rel}:{lineno}: emoji found")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(skill_dirs)} skills checked, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
