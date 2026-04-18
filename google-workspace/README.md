# google-workspace — Claude Code skill

A Claude Code skill that gives Claude **direct read/write access to your entire Google Drive** — Sheets, Docs, Slides, folders, sharing, exports. Set it up once, then just tell Claude what you want in plain language.

> **TL;DR for users:** install the skill → run `setup.py` → answer the browser prompt → start saying things like *"list my sheets"*, *"add a Summary tab to my Q3 Report sheet"*, *"export this doc as PDF"*. Claude does the rest.

---

## What this skill can do

### 📂 Drive (any file type)
- List, search, get metadata
- Download binary files, export Google-native files to PDF / docx / xlsx / csv
- Upload local files (with optional auto-convert to Google Sheet)
- Create folders, move, rename, copy, delete (trash or permanent), restore
- Share files with collaborators, list/revoke permissions

### 📊 Sheets
- Read/write individual cells or ranges
- Append rows, clear ranges
- Add / delete / rename / move / color tabs
- Formatting: bold, italic, font color, cell background, size, alignment
- Raw `batchUpdate` for advanced ops: conditional formatting, data validation dropdowns, sorts, freeze rows, merges, charts

### 📝 Docs
- Read full document text
- Append / insert text at any index
- Headings (H1–H6), find & replace, insert image from URL
- Clear document, raw `batchUpdate` for advanced styling

### 🎞 Slides
- Create / delete / duplicate slides with chosen layouts
- Add text boxes, images
- Find & replace across entire deck
- Raw `batchUpdate` for animations, transitions, theming

---

## Install (one-time)

### Step 1 — clone this repo
```bash
git clone https://github.com/mdnishath/skills.git
```

### Step 2 — copy the `google-workspace` folder into your Claude skills dir

**Windows (PowerShell):**
```powershell
Copy-Item -Recurse -Force .\skills\google-workspace\ "$env:USERPROFILE\.claude\skills\google-workspace"
```

**Windows (CMD):**
```cmd
xcopy /E /I skills\google-workspace %USERPROFILE%\.claude\skills\google-workspace
```

**macOS / Linux:**
```bash
cp -r skills/google-workspace ~/.claude/skills/google-workspace
```

### Step 3 — first-time authorization

Run the interactive setup wizard once:

```bash
python "~/.claude/skills/google-workspace/scripts/setup.py"
```

On Windows (if `~` doesn't expand):
```cmd
python "C:\Users\<YOU>\.claude\skills\google-workspace\scripts\setup.py"
```

The wizard will:
1. Check & install Python dependencies (`google-auth`, `google-api-python-client`, etc.)
2. Walk you through getting **Google Cloud OAuth credentials** (opens the correct console pages for you one by one)
3. Auto-detect the downloaded credentials JSON from your Downloads folder
4. Open your browser → you sign in → click **Allow**
5. Smoke-test: lists your first 5 spreadsheets to confirm connection

After this, the OAuth token is cached at `~/.google_sheets_skill/gsheet_token.json`. **No more browser prompts.**

> ⚠️ During step 2 you'll need to enable **four APIs** in your Cloud project: Sheets, Docs, Slides, Drive. The setup guide shows exactly where to click.

Full walkthrough with screenshots in [`references/setup-guide.md`](./references/setup-guide.md).

### Step 4 — restart Claude Code

Skills load at startup. Once restarted, Claude picks this up automatically whenever you mention anything Drive-related.

---

## How to USE it

### 🎯 Option A: Just talk to Claude (easiest)

Start any Claude Code session and say things like:

| You say | What Claude does |
|---|---|
| "List my 10 most recent sheets" | Uses `GDrive().list_files(mime="spreadsheet")` |
| "Open my Project_Management sheet and show me the Dashboard tab" | Finds the sheet → opens it → reads the Dashboard |
| "Add a new tab called 'Q2 Forecast' to my Budget sheet" | Searches for "Budget" → opens → `add_sheet` |
| "In the Orders tab, change row 5 status to Done" | Reads header row → finds "Status" col → writes to row 5 |
| "Create a new Google Doc titled 'April Report'" | `create_doc("April Report")` |
| "Export the Q3 Report doc as PDF to my desktop" | `GDrive().export(id, "pdf", "...")` |
| "Create a 10-slide pitch deck for Acme Corp" | `create_presentation(...)` + `add_slide` loop |
| "Share this sheet with alice@co.com as editor" | `GDrive().share(id, email, role="writer")` |
| "Find all my files in the 'Clients' folder" | `list_files(parent=folder_id)` |
| "Bulk-rename all PDFs in Downloads folder that start with 'OLD-' to start with 'NEW-'" | Full bulk workflow |

Claude will confirm what it's about to do before any destructive operation (delete, overwrite, etc.).

### 🐍 Option B: Use the Python modules directly (in your own scripts)

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/google-workspace/scripts"))

from gdrive_api import GDrive
from gsheet_api import GSheet, find_spreadsheet, create_spreadsheet
from gdoc_api import GDoc, create_doc
from gslide_api import GSlide, create_presentation

# Find a sheet by name, read a range
sid = find_spreadsheet("Quarterly Report")[0]["id"]
rows = GSheet(sid).read("Data", "A1:D10")

# Create a new doc, add content
doc = GDoc(create_doc("Meeting Notes"))
doc.append_heading("Agenda", level=1)
doc.append_text("• Item 1\n• Item 2\n")

# Export any sheet as PDF
GDrive().export(sid, "pdf", "/path/to/report.pdf")
```

See [`references/usage-examples.md`](./references/usage-examples.md) for **25+ ready-to-paste recipes**, including cross-service ones like "Sheet row → one slide per client", "Doc from Sheet data", bulk rename, etc.

### ⌨️ Option C: Command line

```bash
# List all your spreadsheets
python ~/.claude/skills/google-workspace/scripts/gsheet_api.py drive-list

# Search by name
python ~/.claude/skills/google-workspace/scripts/gsheet_api.py drive-find "Report"

# List tabs of a specific sheet
python ~/.claude/skills/google-workspace/scripts/gsheet_api.py list --id <spreadsheet_id>

# Read cells
python ~/.claude/skills/google-workspace/scripts/gsheet_api.py read --id <spreadsheet_id> Dashboard A1:D5

# Write a cell
python ~/.claude/skills/google-workspace/scripts/gsheet_api.py write --id <spreadsheet_id> Dashboard B5 "hello"

# Add / delete tabs
python ~/.claude/skills/google-workspace/scripts/gsheet_api.py add --id <spreadsheet_id> "New Tab"
python ~/.claude/skills/google-workspace/scripts/gsheet_api.py delete --id <spreadsheet_id> "Old Tab"
```

---

## Multiple Google accounts

Switch between personal/work/client accounts with named profiles:

```bash
# Set up additional accounts
python scripts/setup.py --profile work
python scripts/setup.py --profile client1

# See all profiles (the active one is marked with *)
python scripts/setup.py --list

# Switch active profile
python scripts/setup.py --use work

# Revoke a profile's token (forces re-auth next time)
python scripts/setup.py --revoke
```

Each profile has its own cached credentials + token under `~/.google_sheets_skill/profiles/<name>/`.

---

## How it works (under the hood)

```
~/.claude/skills/google-workspace/
├── SKILL.md              ← Instructions Claude reads when the skill triggers
├── README.md             ← This file (for humans)
├── scripts/
│   ├── gdrive_api.py    ← class GDrive — file/folder/share/export
│   ├── gsheet_api.py    ← class GSheet — cells/tabs/formatting
│   ├── gdoc_api.py      ← class GDoc   — text/headings/images
│   ├── gslide_api.py    ← class GSlide — slides/shapes/text boxes
│   └── setup.py         ← Interactive OAuth wizard
└── references/
    ├── setup-guide.md       ← Detailed Google Cloud setup walkthrough
    └── usage-examples.md    ← 25+ copy-paste recipes

~/.google_sheets_skill/       ← Auth state (never commit this!)
├── active_profile            ← Name of current profile
├── credentials.json          ← Hardlink to current profile's creds
├── gsheet_token.json         ← Hardlink to current profile's token
└── profiles/
    ├── default/
    │   ├── credentials.json  ← OAuth client-secret JSON
    │   └── gsheet_token.json ← OAuth refresh token
    └── work/ ...             ← Additional profiles
```

- The four Python modules share the **same OAuth token** — authorize once, use all services.
- `setup.py` handles everything automation-friendly: dependency install, guided Cloud console setup, browser OAuth, profile management.
- Token refresh is automatic via Google's `refresh_token` flow. You only re-auth if you revoke it or change scopes.

---

## Security & privacy

- **Token storage:** Local only, at `~/.google_sheets_skill/gsheet_token.json`. Never logged, never transmitted outside Google.
- **Scopes requested:** `spreadsheets`, `documents`, `presentations`, `drive`. This is full read/write on anything your Google account can access.
- **Don't commit** `~/.google_sheets_skill/` to git. A `.gitignore` at the skill root excludes it automatically.
- **Revoke access** at any time: `python scripts/setup.py --revoke` (local cleanup) + revoke the app at https://myaccount.google.com/permissions (server-side).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `SERVICE_DISABLED` / "Google Docs API has not been used" | Enable the missing API in Cloud console. Setup wizard tries to do this for you; if it missed one, open the URL in the error message and click Enable. |
| `invalid_grant` | Token expired or was revoked. Run `python scripts/setup.py` again to re-authorize. |
| `access_denied` during browser sign-in | App is in "testing" mode and your email isn't a test user. Add yourself: Cloud Console → APIs & Services → OAuth consent screen → Test users → Add user. |
| Setup can't find downloaded JSON | Paste the full path manually when prompted, or copy it to `~/.google_sheets_skill/credentials.json` first. |
| Want to switch Google accounts | `python setup.py --profile <new-name>` then `--use <new-name>`. |

---

## Contributing

Found a bug or want a new feature? Open an issue or PR at https://github.com/mdnishath/skills.

---

## License

MIT — use, modify, redistribute freely.
