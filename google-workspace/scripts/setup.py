"""Interactive setup for the google-sheets Claude skill.

Runs a guided wizard that:
  - Checks Python deps, installs them if missing
  - Opens the Google Cloud console pages for you (one step at a time)
  - Auto-detects a downloaded credentials JSON in your Downloads folder
  - Authorizes OAuth in the browser
  - Smoke-tests the connection

Profile support (switch between Google accounts easily):
  python setup.py                    # default profile
  python setup.py --profile work     # named profile
  python setup.py --list             # list profiles
  python setup.py --use work         # set a profile as active
  python setup.py --revoke           # delete tokens/credentials for current profile
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

CFG_DIR = Path.home() / ".google_sheets_skill"
PROFILES_DIR = CFG_DIR / "profiles"
ACTIVE_FILE = CFG_DIR / "active_profile"
DEFAULT_PROFILE = "default"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]

REQUIRED_PACKAGES = [
    "google-auth",
    "google-auth-oauthlib",
    "google-auth-httplib2",
    "google-api-python-client",
]


# ---------------- profile helpers ----------------

def _active_profile() -> str:
    if ACTIVE_FILE.exists():
        return ACTIVE_FILE.read_text().strip() or DEFAULT_PROFILE
    return DEFAULT_PROFILE


def _profile_dir(name: str) -> Path:
    d = PROFILES_DIR / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def _list_profiles() -> list[str]:
    if not PROFILES_DIR.exists():
        return []
    return sorted([p.name for p in PROFILES_DIR.iterdir() if p.is_dir()])


def _set_active(name: str) -> None:
    CFG_DIR.mkdir(exist_ok=True)
    ACTIVE_FILE.write_text(name)


# ---------------- UI helpers ----------------

def step(n: int, total: int, title: str) -> None:
    print(f"\n\033[1;36m[{n}/{total}] {title}\033[0m")


def ok(msg: str) -> None:
    print(f"  \033[32m✓\033[0m {msg}")


def warn(msg: str) -> None:
    print(f"  \033[33m!\033[0m {msg}")


def err(msg: str) -> None:
    print(f"  \033[31m✗\033[0m {msg}", file=sys.stderr)


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"  {prompt}{suffix}: ").strip()
    return val or (default or "")


def wait(prompt: str = "Press Enter to continue...") -> None:
    try:
        input(f"  \033[90m{prompt}\033[0m")
    except EOFError:
        pass


# ---------------- actual steps ----------------

def check_deps() -> bool:
    missing = []
    for pkg in REQUIRED_PACKAGES:
        mod = pkg.replace("-", "_")
        # Special cases: google.auth etc.
        check_name = {
            "google-auth": "google.auth",
            "google-auth-oauthlib": "google_auth_oauthlib",
            "google-auth-httplib2": "google_auth_httplib2",
            "google-api-python-client": "googleapiclient",
        }.get(pkg, mod)
        try:
            __import__(check_name)
        except ImportError:
            missing.append(pkg)
    if missing:
        warn(f"Missing: {', '.join(missing)}")
        if ask("Install them now?", "y").lower().startswith("y"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            ok("Installed.")
        else:
            err("Cannot continue without dependencies.")
            return False
    else:
        ok("All Python dependencies present.")
    return True


def guide_create_creds(profile: Path) -> Path | None:
    """Guide user through Google Cloud console + detect downloaded JSON."""
    creds_target = profile / "credentials.json"
    if creds_target.exists():
        if ask(f"Credentials already exist for this profile ({creds_target}). Re-use?", "y").lower().startswith("y"):
            return creds_target
        creds_target.unlink()

    print("""
  This skill needs an OAuth client-secret JSON from your Google Cloud project.
  If you already have one, skip the guided steps and paste the path below.
""")

    # Ask if they already have creds
    existing = ask("Path to an existing credentials.json (leave blank to create one)", "")
    if existing:
        p = Path(existing).expanduser()
        if not p.exists():
            err(f"File not found: {p}")
            return None
        shutil.copy(p, creds_target)
        ok(f"Copied → {creds_target}")
        return creds_target

    # Guided creation
    print("\n  Guided setup — we'll open the pages for you one by one.\n")
    steps_urls = [
        ("1. Create (or open) a Google Cloud project",
         "https://console.cloud.google.com/projectcreate"),
        ("2. Enable Google Sheets API",
         "https://console.cloud.google.com/apis/library/sheets.googleapis.com"),
        ("3. Enable Google Drive API",
         "https://console.cloud.google.com/apis/library/drive.googleapis.com"),
        ("4. Configure OAuth consent screen (choose External, add yourself as Test user)",
         "https://console.cloud.google.com/apis/credentials/consent"),
        ("5. Create OAuth Client ID — type: Desktop app. Download the JSON.",
         "https://console.cloud.google.com/apis/credentials"),
    ]
    for label, url in steps_urls:
        print(f"  {label}")
        print(f"    Opening: {url}")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        wait("Complete this step, then press Enter...")

    # Auto-detect downloaded JSON
    print("\n  Looking for the downloaded JSON in your Downloads folder...")
    downloads = Path.home() / "Downloads"
    candidates = []
    if downloads.exists():
        for pattern in ("client_secret*.json", "credentials*.json"):
            candidates.extend(sorted(downloads.glob(pattern), key=lambda p: -p.stat().st_mtime))

    chosen = None
    if candidates:
        print(f"  Found {len(candidates)} candidate(s):")
        for i, p in enumerate(candidates[:5], 1):
            print(f"    {i}. {p.name}  ({time.strftime('%Y-%m-%d %H:%M', time.localtime(p.stat().st_mtime))})")
        pick = ask("Pick a number (or press Enter to paste a custom path)", "1")
        if pick.isdigit() and 1 <= int(pick) <= len(candidates):
            chosen = candidates[int(pick) - 1]

    if not chosen:
        manual = ask("Full path to the downloaded JSON")
        if not manual:
            err("No path given.")
            return None
        chosen = Path(manual).expanduser()
        if not chosen.exists():
            err(f"File not found: {chosen}")
            return None

    # Validate it's a Desktop OAuth client JSON
    try:
        data = json.loads(chosen.read_text())
        if "installed" not in data and "web" not in data:
            warn("JSON doesn't look like an OAuth client file. Continuing anyway.")
    except Exception as e:
        warn(f"Couldn't parse JSON ({e}). Continuing anyway.")

    shutil.copy(chosen, creds_target)
    ok(f"Copied credentials → {creds_target}")
    return creds_target


def run_oauth(profile: Path) -> bool:
    """Run OAuth flow in browser, save token.json in profile dir."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds_file = profile / "credentials.json"
    token_file = profile / "gsheet_token.json"

    if not creds_file.exists():
        err(f"Missing {creds_file}")
        return False

    print("\n  Opening browser for Google sign-in...")
    flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True)
    token_file.write_text(creds.to_json())
    ok(f"Token saved → {token_file}")
    return True


def smoke_test(profile: Path) -> bool:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    token_file = profile / "gsheet_token.json"
    if not token_file.exists():
        err("No token — authorization failed.")
        return False

    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    drive = build("drive", "v3", credentials=creds)
    resp = drive.files().list(
        q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
        fields="files(id,name)",
        pageSize=5,
        orderBy="modifiedTime desc",
    ).execute()
    files = resp.get("files", [])
    ok(f"Connected! Found {len(files)}+ spreadsheets. First 5:")
    for f in files[:5]:
        print(f"      - {f['name']}")
    return True


def write_active_symlinks(profile: Path) -> None:
    """Write the top-level credentials.json + gsheet_token.json that gsheet_api.py expects."""
    for name in ("credentials.json", "gsheet_token.json"):
        src = profile / name
        dst = CFG_DIR / name
        if src.exists():
            try:
                if dst.exists() or dst.is_symlink():
                    dst.unlink()
            except Exception:
                pass
            try:
                os.link(src, dst)
            except Exception:
                shutil.copy(src, dst)


# ---------------- main ----------------

def main() -> int:
    p = argparse.ArgumentParser(description="Interactive setup for google-sheets skill.")
    p.add_argument("--profile", default=None, help="Name of profile to set up (default: 'default')")
    p.add_argument("--creds", default=None, help="Path to existing OAuth client JSON (skip guided steps)")
    p.add_argument("--list", action="store_true", help="List all profiles")
    p.add_argument("--use", metavar="NAME", help="Set a profile as active")
    p.add_argument("--revoke", action="store_true", help="Delete credentials and token for the current profile")
    args = p.parse_args()

    CFG_DIR.mkdir(exist_ok=True)
    PROFILES_DIR.mkdir(exist_ok=True)

    if args.list:
        active = _active_profile()
        profiles = _list_profiles()
        if not profiles:
            print("No profiles yet. Run: python setup.py")
            return 0
        for name in profiles:
            marker = "*" if name == active else " "
            token_ok = (PROFILES_DIR / name / "gsheet_token.json").exists()
            print(f"  {marker} {name} {'(authorized)' if token_ok else '(not authorized)'}")
        return 0

    if args.use:
        if args.use not in _list_profiles():
            err(f"No profile named {args.use!r}. Run `python setup.py --list`.")
            return 1
        _set_active(args.use)
        write_active_symlinks(PROFILES_DIR / args.use)
        ok(f"Active profile: {args.use}")
        return 0

    profile_name = args.profile or _active_profile()
    profile = _profile_dir(profile_name)

    if args.revoke:
        for name in ("credentials.json", "gsheet_token.json"):
            f = profile / name
            if f.exists():
                f.unlink()
                ok(f"Deleted {f}")
        return 0

    print(f"\n\033[1m== google-sheets skill setup — profile: {profile_name!r} ==\033[0m")

    step(1, 4, "Check Python dependencies")
    if not check_deps():
        return 1

    step(2, 4, "Get Google Cloud OAuth credentials")
    if args.creds:
        src = Path(args.creds).expanduser()
        if not src.exists():
            err(f"Not found: {src}")
            return 1
        shutil.copy(src, profile / "credentials.json")
        ok(f"Copied → {profile / 'credentials.json'}")
    else:
        if not guide_create_creds(profile):
            return 1

    step(3, 4, "Authorize in browser")
    if not run_oauth(profile):
        return 1

    step(4, 4, "Verify connection")
    if not smoke_test(profile):
        return 1

    _set_active(profile_name)
    write_active_symlinks(profile)

    print("\n\033[1;32mSetup complete.\033[0m")
    print(f"Active profile: {profile_name}")
    print(f"To switch accounts later: `python setup.py --profile <name>` then `--use <name>`.")
    print("You can now ask Claude to read/write/create/manage any Google Sheet in this Drive.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
