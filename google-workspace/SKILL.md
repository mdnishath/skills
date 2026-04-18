---
name: google-workspace
description: Full Google Workspace control — Drive, Sheets, Docs, Slides — from Claude. Use when the user wants to read, edit, create, delete, move, share, or export files of any Google type (spreadsheets, documents, presentations), search their Drive by name, manage folders, upload/download files, or do any task involving their Google Drive. Triggers on "my sheet", "my doc", "my slide", "drive e ...", "sheets / docs / slides / presentation", "export as pdf", "share with X", and similar requests. Supports multiple Google accounts via named profiles.
user_invocable: true
---

# Google Workspace Manager

You manage the user's **entire Google Drive** — Sheets, Docs, Slides, Forms, PDFs, folders, sharing, everything — through Python helpers backed by Google Workspace APIs and a cached OAuth token.

## Check setup before doing anything

```bash
ls ~/.google_sheets_skill/gsheet_token.json
```

Exists → go to "Using the skill". Missing → run setup:

```bash
python "$CLAUDE_SKILL_DIR/scripts/setup.py"
```

The setup is an interactive wizard — it guides the user through Google Cloud console, enables APIs, opens the browser for authorization, and can manage multiple accounts via named profiles (`--profile work`, `--use work`, `--list`). Full walkthrough in `references/setup-guide.md`.

## The 4 modules

Each service has its own module. Use only what you need for the task.

| Module | What it does | Class / functions |
|---|---|---|
| `gdrive_api.py`  | File-level Drive ops across all types | `GDrive()`, list/find/get/download/export/upload/create_folder/move/rename/delete/share |
| `gsheet_api.py`  | Spreadsheet cells, tabs, formatting    | `GSheet(id)`, `find_spreadsheet`, `list_all_spreadsheets`, `create_spreadsheet` |
| `gdoc_api.py`    | Document text + structure              | `GDoc(id)`, `create_doc` |
| `gslide_api.py`  | Presentation slides + shapes + text    | `GSlide(id)`, `create_presentation` |

They share a single cached OAuth token — authorize once, use all four.

## Import preamble (put in every script)

```python
import sys, os
SKILL = os.path.join(os.path.expanduser("~"), ".claude", "skills", "google-workspace", "scripts")
if SKILL not in sys.path:
    sys.path.insert(0, SKILL)
```

Then import whatever you need:
```python
from gdrive_api import GDrive
from gsheet_api import GSheet, find_spreadsheet, list_all_spreadsheets, create_spreadsheet
from gdoc_api import GDoc, create_doc
from gslide_api import GSlide, create_presentation
```

## Resolving what file the user means

| User says | Do this |
|---|---|
| Full URL (`docs.google.com/.../d/<ID>/edit`) | Extract `<ID>` between `/d/` and `/edit`. |
| "my sheet named Sanjid Email" | `GDrive().find("Sanjid Email", mime="spreadsheet")` → pick best match |
| "my doc called Q3 Plan" | `GDrive().find("Q3 Plan", mime="document")` |
| "my slides" | `GDrive().list_files(mime="presentation")` |
| Vague ("my sheet") | `GDrive().list_files(mime="spreadsheet")[0]` **and** confirm with user before writing |
| Multiple matches | Show the list with titles + modified time, ask which |

## Sheets operations — `GSheet`

```python
gs = GSheet("1abc...xyz")                 # by spreadsheet ID
gs.list_sheets()                          # tab names
gs.read("Dashboard", "A1:D10")            # → list of rows
gs.update("Dashboard", "B5", "hello")     # single cell
gs.update("Dashboard", "B5:D5", [[1,2,3]])# range (list-of-lists)
gs.append("Dashboard", "A:A", [["new"]])  # append after last used row
gs.clear("Dashboard", "B5:D10")

gs.add_sheet("NewTab", index=0, tab_color="#F59E0B")
gs.delete_sheet("OldTab")
gs.move_sheet("Dashboard", 0)
gs.rename_sheet("Old", "New")

gs.set_cell_format("Dashboard", "A1:B2", bold=True, bg="#FEF3C7", font_color="#1F2A44")
gs.batch_update([...])                    # raw Sheets API requests
```

## Docs operations — `GDoc`

```python
doc_id = create_doc("My Report")
gd = GDoc(doc_id)
gd.get_text()                             # full plain text
gd.append_text("Hello world.\n")
gd.insert_text(1, "Intro: ")              # at index 1
gd.append_heading("Section 2", level=1)
gd.replace_all("{{name}}", "Nishath")     # find & replace
gd.insert_image("https://...png")         # from URL
gd.clear()                                # erase everything
gd.batch_update([...])                    # raw Docs API
```

## Slides operations — `GSlide`

```python
pres_id = create_presentation("Client Deck")
gp = GSlide(pres_id)
gp.list_slides()
s_id = gp.add_slide(layout="TITLE_AND_BODY")
gp.add_text_box(s_id, "Hello", x=50, y=60, w=400, h=60)
gp.add_image(s_id, "https://...jpg", x=60, y=150, w=300, h=200)
gp.replace_all("{{client}}", "Acme Corp")
gp.duplicate_slide(s_id)
gp.delete_slide(s_id)
gp.batch_update([...])                    # raw Slides API
```

## Drive operations — `GDrive`

```python
gd = GDrive()
gd.list_files(limit=20)                   # all files, newest first
gd.list_files(mime="document")            # only Docs
gd.list_files(mime="spreadsheet", parent="<folder_id>")
gd.find("Quarterly", mime="presentation")

meta = gd.get_metadata(file_id)
gd.download(file_id, "local.pdf")         # binary download (any file)
gd.export(file_id, "pdf", "out.pdf")      # Google-native → pdf/docx/xlsx/csv
gd.upload("local.xlsx")
gd.upload_as_google_sheet("local.xlsx", title="Converted")

gd.create_folder("My Folder", parent=None)
gd.move(file_id, folder_id)
gd.rename(file_id, "new name")
gd.copy(file_id, new_title="Copy")
gd.delete(file_id)                        # → trash
gd.delete(file_id, permanent=True)        # unrecoverable
gd.restore(file_id)

gd.share(file_id, "user@example.com", role="writer")
gd.list_permissions(file_id)
```

## Rules (follow every time)

1. **Read before overwrite.** If editing existing cells/text, read them first and show the diff. Brand-new tabs/files are fine.
2. **Preserve manual edits.** Never regenerate from defaults when the user may have corrected cells.
3. **Destructive ops confirm first.** Delete, clear, permanent delete, revoke sharing → quote what will be affected and wait for "yes".
4. **Batch writes >10 updates.** Use `batch_update`, not loops of single updates.
5. **Verify after write.** Read back and show the result.
6. **Sheet name quoting.** Always wrap in single quotes in A1 refs: `"'My Sheet'!A1"`. Helpers do this for you.
7. **Ask when ambiguous.** Multiple matches, unclear intent → list options, wait.

## Common gotchas

- Docs/Slides indexes are character-based, starting at `1`. Index `0` is the body-start marker.
- Drive `share()` sends an email by default. Pass `notify=False` to skip.
- `gd.export()` = Google-native → pdf/xlsx/docx/csv. `gd.download()` = any binary file.
- Permanent delete (`permanent=True`) skips trash, unrecoverable.
- Uploaded xlsx stays as xlsx unless you use `upload_as_google_sheet()` which converts.

See `references/usage-examples.md` for 25+ ready-to-paste recipes covering cross-service tasks.
