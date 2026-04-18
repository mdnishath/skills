"""Generic Google Sheets + Drive helper, used by the google-sheets Claude skill.

Config paths (resolved from env, with sensible defaults):
  credentials file: $GSHEETS_CREDS, else ~/.google_sheets_skill/credentials.json
  cached token:     $GSHEETS_TOKEN, else ~/.google_sheets_skill/gsheet_token.json

This module exposes:
  - GSheet(spreadsheet_id)                      — open one spreadsheet for read/write
  - list_all_spreadsheets(limit=30)             — all sheets in user's Drive
  - find_spreadsheet(name, exact=False)         — search by title
  - create_spreadsheet(title)                   — make a new one, returns id

See SKILL.md and references/ for the full API and common-task recipes.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def _config_dir() -> Path:
    p = Path.home() / ".google_sheets_skill"
    p.mkdir(exist_ok=True)
    return p


def _active_profile_dir() -> Path | None:
    """If the user ran setup.py, an active profile is set. Return its folder, else None."""
    active_file = _config_dir() / "active_profile"
    if active_file.exists():
        name = active_file.read_text().strip()
        if name:
            d = _config_dir() / "profiles" / name
            if d.exists():
                return d
    return None


def _creds_path() -> Path:
    if env := os.environ.get("GSHEETS_CREDS"):
        return Path(env)
    prof = _active_profile_dir()
    if prof and (prof / "credentials.json").exists():
        return prof / "credentials.json"
    return _config_dir() / "credentials.json"


def _token_path() -> Path:
    if env := os.environ.get("GSHEETS_TOKEN"):
        return Path(env)
    prof = _active_profile_dir()
    if prof and (prof / "gsheet_token.json").exists():
        return prof / "gsheet_token.json"
    return _config_dir() / "gsheet_token.json"


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]


def _ensure_creds() -> Credentials:
    token = _token_path()
    creds: Credentials | None = None
    if token.exists():
        creds = Credentials.from_authorized_user_file(str(token), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_file = _creds_path()
            if not creds_file.exists():
                raise FileNotFoundError(
                    f"Google OAuth credentials not found at {creds_file}.\n"
                    f"Run: python {Path(__file__).parent / 'setup.py'!s}\n"
                    "See SKILL.md / references/setup-guide.md."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
            creds = flow.run_local_server(port=0, open_browser=True)
        token.write_text(creds.to_json())
    return creds


def _hex_to_rgb(hex_color: str) -> dict:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return {"red": r / 255, "green": g / 255, "blue": b / 255}


# ---------- Drive-level helpers ----------

def list_all_spreadsheets(limit: int = 30) -> list[dict]:
    """List all spreadsheets in the user's Drive, most recently modified first."""
    drive = build("drive", "v3", credentials=_ensure_creds())
    resp = drive.files().list(
        q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
        fields="files(id,name,modifiedTime,webViewLink)",
        pageSize=limit,
        orderBy="modifiedTime desc",
    ).execute()
    return [
        {"id": f["id"], "title": f["name"], "modifiedTime": f["modifiedTime"], "url": f.get("webViewLink")}
        for f in resp.get("files", [])
    ]


def find_spreadsheet(name: str, exact: bool = False) -> list[dict]:
    """Find spreadsheets by title. Partial match by default; pass exact=True for equality."""
    drive = build("drive", "v3", credentials=_ensure_creds())
    op = "=" if exact else "contains"
    q = (
        f"mimeType='application/vnd.google-apps.spreadsheet' "
        f"and name {op} '{name}' and trashed=false"
    )
    resp = drive.files().list(
        q=q,
        fields="files(id,name,modifiedTime,webViewLink)",
        pageSize=50,
        orderBy="modifiedTime desc",
    ).execute()
    return [
        {"id": f["id"], "title": f["name"], "modifiedTime": f["modifiedTime"], "url": f.get("webViewLink")}
        for f in resp.get("files", [])
    ]


def create_spreadsheet(title: str) -> str:
    """Create a brand-new Google Sheet in the user's Drive root and return its ID."""
    svc = build("sheets", "v4", credentials=_ensure_creds())
    resp = svc.spreadsheets().create(body={"properties": {"title": title}}).execute()
    return resp["spreadsheetId"]


# ---------- Spreadsheet-scoped helper ----------

class GSheet:
    def __init__(self, spreadsheet_id: str):
        if not spreadsheet_id:
            raise ValueError("spreadsheet_id is required. Use find_spreadsheet() to resolve a name to an ID.")
        self.id = spreadsheet_id
        self.creds = _ensure_creds()
        self.svc = build("sheets", "v4", credentials=self.creds)
        self._sheet_cache: dict[str, int] | None = None

    def _load_cache(self) -> dict[str, int]:
        meta = self.svc.spreadsheets().get(spreadsheetId=self.id).execute()
        self._sheet_cache = {
            s["properties"]["title"]: s["properties"]["sheetId"]
            for s in meta["sheets"]
        }
        return self._sheet_cache

    def title(self) -> str:
        meta = self.svc.spreadsheets().get(spreadsheetId=self.id).execute()
        return meta["properties"]["title"]

    def list_sheets(self) -> list[str]:
        return list(self._load_cache().keys())

    def find_sheet_id(self, title: str) -> int:
        cache = self._sheet_cache or self._load_cache()
        if title not in cache:
            cache = self._load_cache()
        if title not in cache:
            raise KeyError(f"Sheet tab not found: {title!r}. Available: {list(cache)[:5]}...")
        return cache[title]

    # ---- values read/write ----

    def read(self, sheet: str, a1_range: str) -> list[list[Any]]:
        resp = (
            self.svc.spreadsheets()
            .values()
            .get(spreadsheetId=self.id, range=f"'{sheet}'!{a1_range}")
            .execute()
        )
        return resp.get("values", [])

    def update(self, sheet: str, a1_range: str, values: Any) -> dict:
        if not isinstance(values, list):
            values = [[values]]
        elif values and not isinstance(values[0], list):
            values = [values]
        return (
            self.svc.spreadsheets()
            .values()
            .update(
                spreadsheetId=self.id,
                range=f"'{sheet}'!{a1_range}",
                valueInputOption="USER_ENTERED",
                body={"values": values},
            )
            .execute()
        )

    def append(self, sheet: str, a1_range: str, rows: list[list[Any]]) -> dict:
        return (
            self.svc.spreadsheets()
            .values()
            .append(
                spreadsheetId=self.id,
                range=f"'{sheet}'!{a1_range}",
                valueInputOption="USER_ENTERED",
                body={"values": rows},
            )
            .execute()
        )

    def clear(self, sheet: str, a1_range: str) -> dict:
        return (
            self.svc.spreadsheets()
            .values()
            .clear(spreadsheetId=self.id, range=f"'{sheet}'!{a1_range}", body={})
            .execute()
        )

    # ---- sheet tab management ----

    def add_sheet(
        self,
        title: str,
        index: int | None = None,
        rows: int = 1000,
        cols: int = 26,
        tab_color: str | None = None,
    ) -> int:
        props: dict[str, Any] = {
            "title": title,
            "gridProperties": {"rowCount": rows, "columnCount": cols},
        }
        if index is not None:
            props["index"] = index
        if tab_color:
            props["tabColor"] = _hex_to_rgb(tab_color)
        resp = self.svc.spreadsheets().batchUpdate(
            spreadsheetId=self.id,
            body={"requests": [{"addSheet": {"properties": props}}]},
        ).execute()
        self._sheet_cache = None
        return resp["replies"][0]["addSheet"]["properties"]["sheetId"]

    def delete_sheet(self, title: str) -> None:
        sid = self.find_sheet_id(title)
        self.svc.spreadsheets().batchUpdate(
            spreadsheetId=self.id,
            body={"requests": [{"deleteSheet": {"sheetId": sid}}]},
        ).execute()
        self._sheet_cache = None

    def move_sheet(self, title: str, new_index: int) -> None:
        sid = self.find_sheet_id(title)
        self.svc.spreadsheets().batchUpdate(
            spreadsheetId=self.id,
            body={"requests": [{
                "updateSheetProperties": {
                    "properties": {"sheetId": sid, "index": new_index},
                    "fields": "index",
                }
            }]},
        ).execute()

    def rename_sheet(self, old: str, new: str) -> None:
        sid = self.find_sheet_id(old)
        self.svc.spreadsheets().batchUpdate(
            spreadsheetId=self.id,
            body={"requests": [{
                "updateSheetProperties": {
                    "properties": {"sheetId": sid, "title": new},
                    "fields": "title",
                }
            }]},
        ).execute()
        self._sheet_cache = None

    # ---- formatting ----

    def set_cell_format(
        self,
        sheet: str,
        a1_range: str,
        *,
        bold: bool | None = None,
        italic: bool | None = None,
        font_color: str | None = None,
        bg: str | None = None,
        font_size: int | None = None,
        horizontal_align: str | None = None,
    ) -> None:
        sid = self.find_sheet_id(sheet)
        start, end = self._a1_to_grid(a1_range)
        cell_fmt: dict[str, Any] = {}
        text_fmt: dict[str, Any] = {}
        if bold is not None:
            text_fmt["bold"] = bold
        if italic is not None:
            text_fmt["italic"] = italic
        if font_size is not None:
            text_fmt["fontSize"] = font_size
        if font_color:
            text_fmt["foregroundColor"] = _hex_to_rgb(font_color)
        if text_fmt:
            cell_fmt["textFormat"] = text_fmt
        if bg:
            cell_fmt["backgroundColor"] = _hex_to_rgb(bg)
        if horizontal_align:
            cell_fmt["horizontalAlignment"] = horizontal_align
        fields = ",".join(f"userEnteredFormat.{k}" for k in cell_fmt.keys())
        self.svc.spreadsheets().batchUpdate(
            spreadsheetId=self.id,
            body={"requests": [{
                "repeatCell": {
                    "range": {
                        "sheetId": sid,
                        "startRowIndex": start[0],
                        "endRowIndex": end[0] + 1,
                        "startColumnIndex": start[1],
                        "endColumnIndex": end[1] + 1,
                    },
                    "cell": {"userEnteredFormat": cell_fmt},
                    "fields": fields,
                }
            }]},
        ).execute()

    # ---- raw batch for advanced use ----

    def batch_update(self, requests: list[dict]) -> dict:
        return self.svc.spreadsheets().batchUpdate(
            spreadsheetId=self.id, body={"requests": requests}
        ).execute()

    # ---- helpers ----

    @staticmethod
    def _a1_to_grid(a1: str) -> tuple[tuple[int, int], tuple[int, int]]:
        import re

        def parse(ref: str) -> tuple[int, int]:
            m = re.match(r"^([A-Z]+)(\d+)$", ref.upper())
            if not m:
                raise ValueError(f"Bad A1 ref: {ref!r}")
            col_s, row_s = m.groups()
            col = 0
            for ch in col_s:
                col = col * 26 + (ord(ch) - ord("A") + 1)
            return int(row_s) - 1, col - 1

        if ":" in a1:
            a, b = a1.split(":", 1)
            return parse(a), parse(b)
        p = parse(a1)
        return p, p


# ---------------- CLI ----------------
def _cli(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        print("\nCommands:")
        print("  drive-list                         List all spreadsheets")
        print("  drive-find <name>                  Search spreadsheets by name")
        print("  drive-new <title>                  Create a new spreadsheet")
        print("  list --id <sheet_id>               List tabs in a spreadsheet")
        print("  read --id <sheet_id> <tab> <A1>    Read cells")
        print("  write --id <sheet_id> <tab> <A1> <val>   Write a cell")
        print("  add --id <sheet_id> <tab_title> [index]  Add a new tab")
        print("  delete --id <sheet_id> <tab_title>       Delete a tab")
        return 0
    cmd = argv[1]
    if cmd == "drive-list":
        for f in list_all_spreadsheets(50):
            print(f"{f['id']}\t{f['title']}")
        return 0
    if cmd == "drive-find":
        for f in find_spreadsheet(argv[2]):
            print(f"{f['id']}\t{f['title']}")
        return 0
    if cmd == "drive-new":
        sid = create_spreadsheet(argv[2])
        print(f"Created: {sid}")
        return 0

    if "--id" not in argv:
        print("--id <spreadsheet_id> required for sheet-scoped commands")
        return 1
    i = argv.index("--id")
    sid_override = argv[i + 1]
    argv = argv[:i] + argv[i + 2:]
    gs = GSheet(sid_override)

    if cmd == "list":
        for name in gs.list_sheets():
            print(name)
    elif cmd == "read":
        tab, rng = argv[2], argv[3]
        for row in gs.read(tab, rng):
            print("\t".join(str(c) for c in row))
    elif cmd == "write":
        tab, rng, val = argv[2], argv[3], argv[4]
        gs.update(tab, rng, val)
        print(f"Wrote {val!r} to '{tab}'!{rng}")
    elif cmd == "add":
        title = argv[2]
        idx = int(argv[3]) if len(argv) > 3 else None
        sid = gs.add_sheet(title, index=idx)
        print(f"Created '{title}' (sheetId={sid}, index={idx})")
    elif cmd == "delete":
        gs.delete_sheet(argv[2])
        print(f"Deleted '{argv[2]}'")
    else:
        print(f"Unknown command: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
