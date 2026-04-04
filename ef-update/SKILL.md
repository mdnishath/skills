---
name: ef-update
description: "Automates the EF Master update workflow after a batch of reviews is completed. Use this skill whenever the user mentions updating EF Master, adding completed batch results to Task sheet, syncing review data, or says /ef-update. Triggers when user has a completed batch .xlsx file (like 80.xlsx, 100.xlsx, etc.) and wants to update their EF Master tracking spreadsheet. Also trigger when user says things like 'update master file', 'add these to task', 'sync batch results', 'update dashboard with completed work', or references the EF review workflow."
---

# EF Master Update Workflow

This skill automates the full post-batch update process for the EF review system. It takes a completed batch file and updates all three sheets in EF Master.xlsx, then resets the batch file for reuse.

## How to invoke

The user will say `/ef-update <path-to-batch-file>` or something like "update EF master with this batch file".

If no batch file path is provided, ask the user for it.

## What it does

Run the Python script at `scripts/ef_update.py` to perform all updates in one go:

```bash
python "<skill-dir>/scripts/ef_update.py" "<batch-file-path>" "<ef-master-path>"
```

- `<batch-file-path>`: The completed batch .xlsx file (e.g., `C:\Users\nisha\OneDrive\Desktop\80.xlsx`)
- `<ef-master-path>`: Defaults to `C:\Users\nisha\OneDrive\Desktop\EF New\EF Master.xlsx`

The script handles everything:

1. **Reads the batch file** and extracts: Email, GMB Name, GMB URL, Review Text, and R6 Share Link from the Operations Done column.

2. **Updates Task sheet** in EF Master:
   - Appends entries after the last numbered row
   - Format: # | GMB Name | GMB Link | Review Text | Done | Email | Date (dd/mm/yyyy) | Notes (Share Link)
   - Copies formatting from existing rows
   - Updates the "Last Updated" merged header

3. **Updates Todays Work sheet**:
   - Changes header date to today
   - Marks matching entries (by GMB Link) as Done with email and date
   - Removes all Done rows entirely
   - Renumbers remaining Pending entries

4. **Updates Dashboard sheet**:
   - Increments Curr Reviews (+1) for each matching GMB Link
   - Total Posted and Remaining auto-recalculate via formulas

5. **Resets the batch file**:
   - Clears output columns: Status, Error Message, Operations Done, Share Link, Date, Op1-Op8, Live Check Status, and Unnamed columns
   - Keeps all input data (Name, Email, Password, TOTP, etc.) intact

## Output

The script prints a summary like:
```
=== EF Master Update Summary ===
Batch file: 80.xlsx
Entries processed: 80
Share links recovered: 80
Task sheet: Added #184 to #263
Todays Work: 80 marked Done, 80 removed, 18 remaining
Dashboard: 80 Curr Reviews updated
Batch file: Reset (output columns cleared)
```

## Important notes

- If the EF Master file is open in Excel, the save will fail. Ask the user to close it and retry.
- The Dashboard formulas (Total Posted, Remaining) recalculate automatically when the file is opened in Excel.
- Always run the script BEFORE clearing the batch file, because the share links come from the Operations Done column.
