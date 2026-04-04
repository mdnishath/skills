# ef-update — EF Master Spreadsheet Auto-Updater

Automates the post-batch update workflow for the EF review tracking system. Takes a completed batch `.xlsx` file and updates the Task sheet, Todays Work sheet, and Dashboard in EF Master.xlsx.

## Quick Start

```
/ef-update path/to/batch-file.xlsx
```

## What It Does

1. Reads completed batch file (extracts Email, GMB Name, URL, Review Text, Share Links)
2. Updates **Task sheet** — appends entries with numbering and formatting
3. Updates **Todays Work sheet** — marks Done, removes completed rows, renumbers
4. Updates **Dashboard** — increments review counts
5. Resets batch file — clears output columns, keeps input data

## Requirements

- Python 3.8+
- `openpyxl` package (`pip install openpyxl`)

## Install

Copy this folder to `~/.claude/skills/ef-update/` and restart Claude Code.
