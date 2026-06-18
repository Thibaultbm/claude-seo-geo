# Getting started: install Obsidian, connect the AI, first session (reference)

Load this when the user is starting from zero: Obsidian is not installed, the agent is not yet connected to a vault, or the user just wants the plain install-to-first-note path before any architecture or import work. Once Obsidian is open, the skill is loaded, and a vault folder exists, the rest of the skill takes over (architecture, the three protocols, import, audit). This file is the on-ramp, not the method.

The whole point of "guided by AI": the user does not design the folder structure or maintain the graph by hand. They install two free tools, point the agent at a folder, then feed raw material and confirm facts. Claude scaffolds the vault, routes the facts, and keeps it navigable. The user's job is to supply knowledge and answer questions, not to be a librarian.

## Step 1: Install Obsidian

1. Go to https://obsidian.md and download the app for the operating system (macOS, Windows, Linux). It is free for personal and commercial use.
2. Open it and choose "Create new vault". A vault is nothing more than a folder of plain markdown files on the disk; Obsidian is the browser and editor on top of it.
3. Name the vault (for example `company-vault`) and pick where it lives (for example `~/Documents/company-vault`). Note that path: it is the one thing the agent needs in order to read and write the notes.
4. No plugins are required to start. The default install reads and writes the markdown this skill produces.

Sync is optional and local-first by default. If the user wants the vault on more than one device, Obsidian Sync, iCloud or Dropbox on the folder, or a private git repo all work; none of them are needed to begin, and none change how the agent reads the files.

## Step 2: Connect the AI

A vault is only a second brain once an agent reads and writes it. Install Claude Code and add this kit so the obsidian-brain skill is available.

Plugin (recommended), from inside Claude Code:

```
/plugin marketplace add Thibaultbm/claude-seo-geo
/plugin install claude-seo-geo@sorank
```

Or with the skills CLI:

```
npx skills add Thibaultbm/claude-seo-geo
```

Or copy the skills manually:

```
git clone --depth 1 https://github.com/Thibaultbm/claude-seo-geo.git
cp -r claude-seo-geo/skills/* ~/.claude/skills/
```

Then give the agent access to the vault folder: start Claude Code from inside the vault directory, or tell it the path (`~/Documents/company-vault`) so it can read and write the notes. The agent needs filesystem access to that folder; nothing leaves the machine. The skills are plain markdown in the open Agent Skills format, so the same files work in Cursor, Codex, Gemini CLI and any agent that reads instructions from disk (see AGENTS.md).

## Step 3: First session (scaffold the vault)

With Obsidian open and the agent pointed at the folder, the first session builds the structure. A starter prompt the user can paste:

```
Set up an Obsidian second brain for my company in this folder.
We are [one line: what the business does, and for whom].
Scaffold the vault, draft what you can from what I tell you,
mark the gaps as TODO, and tell me what to dump in first.
```

The skill responds with the scaffolded tree (entry point, domain hubs, the `seo/` folder with `action-log.md`, `sources/`), the company and market notes drafted with TODO markers where facts are missing, and a prioritized dump plan. This is the documented scaffolding output; the shape and the rules behind it live in `references/vault-architecture.md`.

For a founder whose personal and business life are entangled, say so in the prompt: the skill creates two entry points (business and personal) that link to each other, instead of one.

## Step 4: First dump

The vault is empty structure until the user's real knowledge is in it. Hand the agent the pile and it converts and routes it (full procedure in `references/import-workflows.md`). Priority for the first dump:

1. Identity and product documents (who you are, what you sell, pricing): they ground every later output.
2. Sales and call transcripts, and WhatsApp chats with clients: the customer's own words, the highest-value and most-overlooked source.
3. Past SEO work and analytics, then everything else.

Each source becomes one note in `sources/`, and its facts are routed into the company, market and people notes, linked back. A dump is done when its facts are findable from the index, not when the file is converted.

## Step 5: The loop that compounds

From here the three protocols in SKILL.md run every session, and they are where the payoff comes:

- Read first: the agent reads the entry point and the notes a task needs before acting, so it stops asking for facts already written down.
- Capture: when the user states a durable fact, the agent writes it to the smallest correct note immediately, so it is never asked twice.
- Write back: at the end of a session that changed something, the agent appends a dated entry to `seo/action-log.md`, so the next session starts where this one ended.

The first session is install and scaffold; the value builds from session two onward, as the vault learns the business and the agent grounds every output in it.

## Beginner snags

| Snag | Fix |
|---|---|
| The agent cannot find or write the vault | Start it inside the vault folder, or give the exact path; confirm it has filesystem access to that directory |
| Not sure where the vault is | In Obsidian, the vault name and path show in the bottom left; that folder is the vault |
| Tempted to paste passwords, API keys or 2FA codes | Never put secrets in the vault; note that they exist and where they live (a password manager), never the value |
| Wants it on phone and laptop | Add sync after the vault exists (Obsidian Sync, iCloud, Dropbox or git); it is not needed to start |
| Vault feels messy after a big import | Run the link audit (`references/link-audit.md`) to find broken links, orphans and duplicate people, then fix in one pass |
