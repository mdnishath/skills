# Usage Examples

Copy-paste recipes for common Google Workspace tasks using this skill.

Every example assumes you've run the import preamble:
```python
import sys, os
SKILL = os.path.join(os.path.expanduser("~"), ".claude", "skills", "google-workspace", "scripts")
if SKILL not in sys.path: sys.path.insert(0, SKILL)
```

---

## Drive

### List all files in a specific folder
```python
from gdrive_api import GDrive
gd = GDrive()
files = gd.list_files(parent="<folder_id>", limit=200)
for f in files:
    print(f["name"], f["mimeType"])
```

### Find a file by name (any type)
```python
gd.find("Q3 plan")                    # any type
gd.find("Invoice", mime="pdf")
gd.find("Budget", mime="spreadsheet", exact=True)
```

### Export a Google Sheet as PDF
```python
gd.export("<sheet_id>", "pdf", "/path/to/out.pdf")
```

### Upload a local xlsx and convert to a Google Sheet
```python
new_id = gd.upload_as_google_sheet("/path/local.xlsx", title="Synced")
print(f"https://docs.google.com/spreadsheets/d/{new_id}")
```

### Move a file to a folder (or create folder first)
```python
folder_id = gd.create_folder("Client Reports")
gd.move("<file_id>", folder_id)
```

### Share a file (add collaborators in bulk)
```python
for email in ["alice@co.com", "bob@co.com"]:
    gd.share("<file_id>", email, role="writer", notify=False)
```

### Revoke sharing
```python
for perm in gd.list_permissions("<file_id>"):
    if perm.get("emailAddress") == "old@co.com":
        gd.svc.permissions().delete(fileId="<file_id>", permissionId=perm["id"]).execute()
```

---

## Sheets

### Read a whole tab
```python
from gsheet_api import GSheet
gs = GSheet("<sheet_id>")
rows = gs.read("Data", "A1:Z")
for r in rows:
    print(r)
```

### Bulk update many cells in one call
```python
gs.svc.spreadsheets().values().batchUpdate(
    spreadsheetId=gs.id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "'Data'!A2", "values": [["Alice"]]},
            {"range": "'Data'!B2", "values": [["alice@co.com"]]},
            {"range": "'Data'!C2", "values": [[42]]},
        ],
    },
).execute()
```

### Find a row by a column value
```python
rows = gs.read("Orders", "A:Z")
header = rows[0]
idx = header.index("Order ID")
target = [r for r in rows[1:] if len(r) > idx and r[idx] == "ORD-042"]
```

### Append rows to the end
```python
gs.append("Log", "A:D", [
    ["2026-04-18", "nishath", "created task", "OK"],
    ["2026-04-18", "nishath", "closed task", "OK"],
])
```

### Add a dropdown (data validation) on a column
```python
sid = gs.find_sheet_id("Data")
gs.batch_update([{
    "setDataValidation": {
        "range": {"sheetId": sid, "startRowIndex": 1, "startColumnIndex": 2, "endColumnIndex": 3},
        "rule": {
            "condition": {"type": "ONE_OF_LIST", "values": [
                {"userEnteredValue": "Pending"},
                {"userEnteredValue": "Live"},
                {"userEnteredValue": "Done"},
            ]},
            "strict": True, "showCustomUi": True,
        },
    }
}])
```

### Conditional format: color cells red when Status is "Rejected"
```python
sid = gs.find_sheet_id("Data")
gs.batch_update([{
    "addConditionalFormatRule": {
        "rule": {
            "ranges": [{"sheetId": sid, "startColumnIndex": 4, "endColumnIndex": 5, "startRowIndex": 1}],
            "booleanRule": {
                "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "Rejected"}]},
                "format": {"backgroundColor": {"red": 1.0, "green": 0.85, "blue": 0.85}},
            },
        },
        "index": 0,
    }
}])
```

### Sort a tab by a column
```python
sid = gs.find_sheet_id("Data")
gs.batch_update([{
    "sortRange": {
        "range": {"sheetId": sid, "startRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 10},
        "sortSpecs": [{"dimensionIndex": 3, "sortOrder": "DESCENDING"}],  # col D desc
    }
}])
```

### Freeze header row
```python
sid = gs.find_sheet_id("Data")
gs.batch_update([{
    "updateSheetProperties": {
        "properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 1}},
        "fields": "gridProperties.frozenRowCount",
    }
}])
```

---

## Docs

### Fill a template doc
```python
from gdoc_api import GDoc, create_doc
from gdrive_api import GDrive

# Copy a template, then fill placeholders
new_id = GDrive().copy("<template_doc_id>", new_title="Invoice for Alice")
doc = GDoc(new_id)
doc.replace_all("{{client}}", "Alice")
doc.replace_all("{{amount}}", "$1,250")
doc.replace_all("{{date}}", "2026-04-18")
```

### Write a structured report
```python
doc_id = create_doc("Q2 Report")
doc = GDoc(doc_id)
doc.append_heading("Executive Summary", level=1)
doc.append_text("Overall revenue up 12%.\n\n")
doc.append_heading("Key Numbers", level=2)
doc.append_text("• Revenue: $1.2M\n• Customers: 342\n• Churn: 2.1%\n")
```

### Read a doc and analyse its text
```python
text = GDoc("<doc_id>").get_text()
print(f"Word count: {len(text.split())}")
```

---

## Slides

### Create a pitch deck from scratch
```python
from gslide_api import GSlide, create_presentation

pres_id = create_presentation("Product Pitch")
gp = GSlide(pres_id)

# Title slide
t = gp.add_slide(layout="TITLE")
# Bullet slide
b = gp.add_slide(layout="TITLE_AND_BODY")
gp.add_text_box(b, "Why us\n• Fast\n• Reliable\n• Affordable", x=50, y=100, w=500, h=300)
# Closing
gp.add_slide(layout="SECTION_HEADER")
```

### Fill a template deck
```python
from gdrive_api import GDrive
new_id = GDrive().copy("<template_pres_id>", new_title="Client: Acme")
gp = GSlide(new_id)
gp.replace_all("{{client_name}}", "Acme Corp")
gp.replace_all("{{date}}", "April 2026")
```

### Bulk-generate decks for a list of clients
```python
template_id = "<template_pres_id>"
gd = GDrive()
for client in ["Acme", "Beta", "Gamma"]:
    new_id = gd.copy(template_id, new_title=f"Deck — {client}")
    GSlide(new_id).replace_all("{{client_name}}", client)
    print(f"https://docs.google.com/presentation/d/{new_id}")
```

---

## Cross-service recipes

### Sheet → PDF → email-ready file
```python
from gsheet_api import GSheet
from gdrive_api import GDrive
gs = GSheet("<sheet_id>")
gs.svc.spreadsheets().values().update(
    spreadsheetId=gs.id, range="'Data'!Z1",
    valueInputOption="USER_ENTERED",
    body={"values": [[f'=TEXT(NOW(),"yyyy-mm-dd")']]},
).execute()
GDrive().export("<sheet_id>", "pdf", "report.pdf")
```

### Import Sheet data into a new Doc
```python
from gsheet_api import GSheet
from gdoc_api import create_doc, GDoc

rows = GSheet("<sheet_id>").read("Summary", "A1:D10")
doc = GDoc(create_doc("Sales Summary"))
doc.append_heading("Sales Summary", level=1)
for row in rows:
    doc.append_text(" | ".join(str(c) for c in row) + "\n")
```

### One Sheet row per slide
```python
from gsheet_api import GSheet
from gslide_api import GSlide, create_presentation

rows = GSheet("<sheet_id>").read("Clients", "A2:C")
deck = GSlide(create_presentation("All Clients"))
for name, industry, size in rows:
    s = deck.add_slide(layout="TITLE_AND_BODY")
    deck.add_text_box(s, f"{name}\nIndustry: {industry}\nSize: {size}", x=50, y=80, w=600, h=200)
```

### Bulk rename all files in a folder
```python
gd = GDrive()
for f in gd.list_files(parent="<folder_id>", limit=200):
    new_name = f["name"].replace("OLD-", "NEW-")
    if new_name != f["name"]:
        gd.rename(f["id"], new_name)
```
