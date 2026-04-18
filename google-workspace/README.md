# google-workspace — Claude skill

Full Google Workspace control — **Drive, Sheets, Docs, Slides** — from Claude (or any Python environment). One-time OAuth setup, then read/write/create anything in your Google Drive.

## What you get

- **Drive** — list/search files, upload/download, create folders, move, rename, copy, delete, share, export Google-native → PDF/xlsx/docx
- **Sheets** — read/write cells and ranges, create/rename/delete/move tabs, formatting, conditional formatting, data validation, batch updates
- **Docs** — read text, append/insert text, headings, images, find & replace, batch updates
- **Slides** — add/delete/duplicate slides, text boxes, images, find & replace across deck, batch updates

Separate Python modules — use only what you need:
```
scripts/
├── gdrive_api.py     # Drive file operations
├── gsheet_api.py     # Sheets
├── gdoc_api.py       # Docs
├── gslide_api.py     # Slides
└── setup.py          # Interactive OAuth setup (supports multiple accounts)
```

## Install

### Option 1 — as a Claude skill
```bash
git clone https://github.com/mdnishath/skills.git ~/claude-skills
cp -r ~/claude-skills/google-workspace ~/.claude/skills/google-workspace
```

### Option 2 — standalone (any Python project)
```bash
git clone https://github.com/mdnishath/skills.git
cd skills/google-workspace
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## First-time setup (2–3 minutes)

```bash
python scripts/setup.py
```

The interactive wizard:
1. Checks and installs Python deps if missing
2. Opens Google Cloud console pages one at a time (create project, enable Sheets/Docs/Slides/Drive APIs, create OAuth client)
3. Auto-detects the downloaded credentials JSON in your Downloads folder
4. Opens the browser for OAuth authorization
5. Smoke-tests the connection

Full walkthrough in [references/setup-guide.md](google-workspace/references/setup-guide.md).

### Multiple Google accounts
```bash
python scripts/setup.py --profile personal    # set up personal account
python scripts/setup.py --profile work        # set up work account
python scripts/setup.py --list                # show all profiles
python scripts/setup.py --use work            # switch active profile
```

## Use from Claude

Once installed, Claude picks up the skill automatically. Example prompts:

- "List all my Google Sheets"
- "Open my 'Q3 Report' doc and add a heading 'Key Takeaways'"
- "Create a new presentation with 3 slides for Acme Corp"
- "Export the Dashboard sheet as PDF"
- "Share this sheet with alice@example.com as editor"
- "Find all sheets modified in the last week"

Claude will use the relevant module under the hood — you don't need to know the API.

## Use from Python directly

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/google-workspace/scripts"))

from gdrive_api import GDrive
from gsheet_api import GSheet, find_spreadsheet
from gdoc_api import GDoc, create_doc
from gslide_api import GSlide, create_presentation

# Find a sheet, read cells
sid = find_spreadsheet("Quarterly Report")[0]["id"]
rows = GSheet(sid).read("Data", "A1:D10")

# Create a new doc
GDoc(create_doc("Meeting Notes")).append_text("Agenda:\n")

# Export any file as PDF
GDrive().export(sid, "pdf", "report.pdf")
```

See [references/usage-examples.md](google-workspace/references/usage-examples.md) for 25+ ready-to-paste recipes.

## Security notes

- OAuth token is stored locally at `~/.google_sheets_skill/gsheet_token.json`. Never commit this to git.
- Each profile's credentials/token live under `~/.google_sheets_skill/profiles/<name>/`.
- Scopes requested: `spreadsheets`, `documents`, `presentations`, `drive` — i.e., full read/write on files you own or have been shared.
- To revoke access entirely: `python scripts/setup.py --revoke` + revoke the app in your Google account settings.

## License

MIT — use, modify, redistribute freely.
