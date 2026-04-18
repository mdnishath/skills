# Claude Code Custom Skills Collection

A collection of production-ready custom skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's agentic coding tool. These skills extend Claude's capabilities with specialized, reusable workflows that trigger automatically or via slash commands.

---

## What Are Claude Code Skills?

Skills are markdown-based instruction files that teach Claude Code how to perform specific tasks. Once installed, they:

- **Auto-trigger** based on what you say (e.g., mentioning "reviews" triggers the review writer)
- **Run via slash command** (e.g., `/french-review`, `/ef-update`)
- **Persist globally** across all projects and sessions
- **Include reference files** with vocabulary, templates, and strategy guides

---

## Skills in This Repo

| Skill | Command | Version | Description |
|-------|---------|---------|-------------|
| [french-review](./french-review/) | `/french-review` | v3.0 | Write authentic French Google reviews — 30+ industries, Google algorithm bypass, anti-AI-detection |
| [ef-update](./ef-update/) | `/ef-update` | v1.0 | Automate EF Master spreadsheet updates after completing a review batch |
| [google-workspace](./google-workspace/) | auto-trigger | v1.0 | Full Google Drive / Sheets / Docs / Slides control — read, write, create, export, share |

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/mdnishath/skills.git
```

### 2. Install the skill(s) you want

**Windows (CMD):**
```cmd
xcopy /E /I skills\french-review %USERPROFILE%\.claude\skills\french-review
xcopy /E /I skills\ef-update %USERPROFILE%\.claude\skills\ef-update
```

**Windows (PowerShell):**
```powershell
Copy-Item -Recurse -Force .\skills\french-review\ "$env:USERPROFILE\.claude\skills\french-review"
Copy-Item -Recurse -Force .\skills\ef-update\ "$env:USERPROFILE\.claude\skills\ef-update"
```

**macOS / Linux:**
```bash
cp -r skills/french-review ~/.claude/skills/french-review
cp -r skills/ef-update ~/.claude/skills/ef-update
```

### 3. Restart Claude Code

Skills are auto-detected on startup. Test with:
```
/french-review 1 five-star review for "Test Plombier" plumber in Paris
```

---

## Skill Details

### french-review v3.0

**Universal French Google Review Writer**

Writes Google My Business reviews in French that survive Google's spam filters, AI content detectors, and manual appeal reviews. Supports 30+ business types with industry-specific vocabulary.

#### What's New in v3.0

| Change | Before (v2.0) | After (v3.0) |
|--------|---------------|--------------|
| Accents | Drop 55-75% always (bot pattern) | Realistic phone autocorrect — 40% of reviews nearly perfect French |
| Apostrophes | Drop 65-85% always (bot pattern) | Varied by persona — careful/average/sloppy typers |
| Specificity | 1 generic detail per review | 2+ specificity layers mandatory (service details, business name, outcomes) |
| Repetition | Basic variation | Zero phrase repetition — no 4+ word phrase appears twice in a batch |
| Appeal-proof | Not addressed | New Rule 18 — personal context, service vocabulary, appeal checklist |
| Rules | 16 rules | 18 rules |

#### Key Features

- **18 strict writing rules** — realistic accent handling, mandatory specificity, zero repetition, burstiness engine
- **Persona system** — each review gets a unique persona (age, gender, perspective, typing style, phone type)
- **Google algorithm bypass** — designed to survive spam filters AND manual appeal reviews
- **30+ business types** with industry-specific French vocabulary
- **90+ opening templates** organized by star rating
- **Stealth mode** — maximum anti-detection with one keyword

#### Usage

```
/french-review 5 five-star reviews for "Plomberie Martin" plumber in Lyon

/french-review 10 reviews for "Le Petit Bistrot" restaurant, mix of 4 and 5 stars

/french-review 3 negative reviews for "Toitures Dupont" roofing company

/french-review 8 reviews for "Garage Auto Plus" mechanic, stealth mode
```

See [french-review/README.md](./french-review/README.md) for full documentation.

---

### ef-update v1.0

**EF Master Spreadsheet Auto-Updater**

Automates the post-batch workflow for the EF review tracking system.

#### What It Does

1. Reads completed batch `.xlsx` file
2. Updates **Task sheet** — appends entries with numbering and formatting
3. Updates **Todays Work sheet** — marks done, removes completed, renumbers
4. Updates **Dashboard** — increments review counts
5. Resets batch file — clears output columns, keeps input data

#### Usage

```
/ef-update path/to/batch-file.xlsx
```

See [ef-update/README.md](./ef-update/README.md) for full documentation.

---

## Folder Structure

```
skills/
├── README.md                              # This file — all skills overview
├── .gitignore
├── french-review/                         # French Google Review Writer v3.0
│   ├── README.md                          # Skill-specific docs
│   ├── SKILL.md                           # Core skill (18 rules, persona system)
│   └── references/
│       ├── anti-detection-strategy.md     # Google bypass, AI detection, appeal-proofing
│       ├── business-vocabulary.md         # 30+ industry vocabulary sets
│       ├── example-reviews.md             # 35+ examples with realistic accents
│       └── opening-templates.md           # 90+ opening templates by rating
├── ef-update/                             # EF Master Updater v1.0
│   ├── README.md
│   ├── SKILL.md
│   └── scripts/
│       └── ef_update.py
└── [future-skill]/                        # Add new skills here
    ├── README.md
    └── SKILL.md
```

## Adding a New Skill

1. Create a new folder at the repo root: `my-new-skill/`
2. Add a `SKILL.md` file (required — this is the skill definition)
3. Add a `README.md` file (recommended — documents usage)
4. Add any reference files in a `references/` subfolder
5. Update this main `README.md` — add a row to the skills table and a details section
6. Commit and push:
   ```bash
   git add my-new-skill/
   git commit -m "Add my-new-skill"
   git push
   ```
7. Install locally:
   ```bash
   cp -r my-new-skill ~/.claude/skills/my-new-skill
   ```

### Skill Folder Requirements

| File | Required | Purpose |
|------|----------|---------|
| `SKILL.md` | Yes | Core skill definition with frontmatter (name, description, user_invocable) |
| `README.md` | Recommended | Usage docs, examples, installation notes |
| `references/` | Optional | Supporting files (vocabulary, templates, examples, strategies) |
| `scripts/` | Optional | Automation scripts (Python, shell, etc.) |

### SKILL.md Frontmatter Template

```yaml
---
name: my-skill-name
description: "Short description of what this skill does and when it triggers"
user_invocable: true
---
```

---

## Configuration

### Language

- **Input:** English (your prompts)
- **Output:** Depends on the skill (french-review outputs French, ef-update outputs English)

### Customization

Each skill's reference files can be modified:
- Add new business types, vocabulary, templates
- Adjust rules and strategies
- Add more examples

See individual skill READMEs for customization details.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI tool by Anthropic)
- For `ef-update`: Python 3.8+ with `openpyxl` package

---

## License

MIT — use freely, modify as needed.

---

## Author

**mdnishath** — Production-tested skills for review workflows and automation.
