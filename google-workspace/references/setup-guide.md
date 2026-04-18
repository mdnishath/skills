# Setup Guide

One-time setup, takes ~3 minutes. After this, Claude can read/write any of your Google Sheets without browser prompts.

## 1. Install Python dependencies

```bash
python -m pip install gspread google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## 2. Create Google Cloud credentials

1. Go to https://console.cloud.google.com/
2. **Create a new project** (or select an existing one). Name it anything — "claude-sheets" works.
3. **Enable two APIs** (one link each — click "Enable"):
   - Google Sheets API → https://console.cloud.google.com/apis/library/sheets.googleapis.com
   - Google Drive API  → https://console.cloud.google.com/apis/library/drive.googleapis.com
4. **Create OAuth credentials:**
   - Go to **APIs & Services → Credentials**
   - Click **+ Create credentials → OAuth client ID**
   - If prompted to configure a consent screen first:
     - User type: **External**
     - App name: "Claude Sheets" (anything)
     - Support email + dev contact: your email
     - Save & continue past the scope/test-users steps (you can add yourself as a test user, that's fine for personal use)
   - Back on the Create OAuth Client ID page:
     - Application type: **Desktop app**
     - Name: "claude-desktop"
     - Click **Create** → download the JSON (or click the download icon)

## 3. Run the setup script

From the skill folder:

```bash
python scripts/setup.py --creds "/path/to/downloaded/client_secret_xxx.json"
```

Or copy the JSON to `~/.google_sheets_skill/credentials.json` first, then just run `python scripts/setup.py`.

A browser tab will open → sign in with the Google account whose sheets you want to edit → click **Allow** on the permission screen. The script saves `~/.google_sheets_skill/gsheet_token.json` and does a smoke test (lists your first 5 spreadsheets). If you see that list, you're done.

## 4. (Optional) Test from Claude

In a new Claude session, just say "list my google sheets". Claude will load the skill and run `list_all_spreadsheets()`.

## Troubleshooting

### `Error 403: access_denied` in the browser
Your app is in "testing" mode and Google is blocking non-test-users. Fix: go to **APIs & Services → OAuth consent screen → Test users → + Add user** → add your Gmail. Re-run setup.

### `Google Sheets API has not been used` / `SERVICE_DISABLED`
The Sheets (or Drive) API isn't enabled in that project. Go back to step 2.3 and enable both APIs.

### `invalid_grant` later, in regular use
Your token expired or was revoked. Re-run `python scripts/setup.py` to refresh.

### Re-authorizing with a different Google account
Delete `~/.google_sheets_skill/gsheet_token.json`, then re-run `setup.py`. The browser will prompt for a fresh sign-in.

### Using existing credentials from another project
If you already have an OAuth client JSON from a previous Google Cloud project, you can point to it:

```bash
GSHEETS_CREDS=/path/to/my-creds.json python scripts/setup.py
```

Or copy it to `~/.google_sheets_skill/credentials.json` manually.
