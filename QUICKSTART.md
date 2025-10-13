# Quick Start Guide

Get up and running with the Speaker Prospect Filtering Tool in 5 minutes!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set Up Airtable Credentials

Create a file named `.env` in this directory:

```
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id_here
AIRTABLE_TABLE_NAME=your_table_name_here
```

### Where to Find These Values:

- **API Key**: https://airtable.com/account → Generate API key
- **Base ID**: From your Airtable URL: `https://airtable.com/[BASE_ID]/...`
- **Table Name**: Exact name of your table (e.g., "2511 Barclays status view")

## 3. Test Your Connection

```bash
python test_connection.py
```

This will:
- ✓ Verify your Airtable credentials work
- ✓ Show you all available columns
- ✓ Check if column names match
- ✓ Display sample workshop tags

## 4. Run the Tool

```bash
python main.py "2511 Barclays"
```

This generates three files:
- `speaker_report_[timestamp].csv` - Spreadsheet format
- `speaker_report_[timestamp].json` - Structured data
- `speaker_report_[timestamp].txt` - Human-readable report

## 5. Advanced Usage

### Add Event Title for Better Analysis

```bash
python main.py "2511 Barclays" --event-title "Digital Transformation in Finance"
```

### Choose Specific Output Format

```bash
python main.py "2511 Barclays" --format csv      # CSV only
python main.py "2511 Barclays" --format json     # JSON only
python main.py "2511 Barclays" --format text     # Text only
```

### Custom Output Name

```bash
python main.py "2511 Barclays" --output barclays_speakers
```

## What Gets Filtered?

### ✅ Confirmed Speakers
- Tag: `[Event Name] Confirmed`
- All confirmed speakers included

### ✅ Intended Speakers
- Tag: `[Event Name] Intended`
- Must have Axel's rating ≥ 92 OR IR rating ≥ 3.8
- Excludes "not reached" and "not available"
- Excludes "DON'T CONTACT" in activity notes

### ✅ Endorsed Speakers
- Tag: `[Event Name] Endorsed`
- Same filters as Intended Speakers

## Troubleshooting

### "AIRTABLE_API_KEY not set"
→ Check `.env` file exists and has correct format

### "No records found"
→ Verify Base ID and Table Name are correct

### Missing columns
→ Run `python test_connection.py` to see column mapping

### No speakers found
→ Check that event name matches exactly (case matters!)

## Need More Help?

- 📖 Full documentation: `README.md`
- 📋 Detailed setup: `setup_instructions.txt`
- 🔧 Test connection: `python test_connection.py`

---

**That's it!** You're ready to filter speaker prospects! 🎉




