# Speaker Prospect Filtering Tool

A comprehensive tool for filtering and organizing speaker prospects from Airtable for events. Categorizes speakers into Confirmed, Intended, and Endorsed groups with detailed analysis and multiple output formats.

## Features

- **Airtable Integration**: Fetches speaker data directly from your Airtable base
- **Smart Filtering**: Applies complex rating-based filters and exclusion rules
- **Multiple Categories**: Organizes speakers into Confirmed, Intended, and Endorsed
- **Detailed Analysis**: Extracts and analyzes call notes, ratings, and content fit
- **Multiple Output Formats**: Generates CSV, JSON, and human-readable text reports
- **Content Fit Analysis**: Automatically analyzes speaker-event alignment

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Airtable credentials:

```
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id_here
AIRTABLE_TABLE_NAME=your_table_name_here
```

### Getting Airtable Credentials

- **API Key**: Go to https://airtable.com/account → Generate API key
- **Base ID**: Found in your Airtable URL: `https://airtable.com/[BASE_ID]/...`
- **Table Name**: The exact name of your table (e.g., "2511 Barclays status view")

## Usage

### Basic Usage

```bash
python main.py "2511 Barclays"
```

### With Event Title (for better content fit analysis)

```bash
python main.py "2511 Barclays" --event-title "Digital Transformation in Finance"
```

### Specify Output Format

```bash
# Generate only CSV
python main.py "2511 Barclays" --format csv

# Generate only JSON
python main.py "2511 Barclays" --format json

# Generate only text report
python main.py "2511 Barclays" --format text

# Generate all formats (default)
python main.py "2511 Barclays" --format all
```

### Custom Output Filename

```bash
python main.py "2511 Barclays" --output my_report
```

## Filtering Logic

### Confirmed Speakers
- Contains event tag: `[Event Name] Confirmed`
- No additional filtering applied

### Intended Speakers
- Contains event tag: `[Event Name] Intended`
- Excludes: `[Event Name] not reached` or `[Event Name] not available`
- Excludes: Activity notes containing "DON'T CONTACT" or "DO NOT CONTACT"
- **Rating filters**:
  - Axel's rating ≥ 94: Marked as "Good option"
  - Axel's rating = 92 or 93: Included with "Lower rating" flag
  - Axel's rating < 92: Excluded UNLESS...
  - IR Speaking Engagement ≥ 3.8: Included regardless of Axel's rating

### Endorsed Speakers
- Contains event tag: `[Event Name] Endorsed`
- Same rating filters as Intended Speakers
- Same exclusion rules as Intended Speakers

## Output Information

### Confirmed Speakers Output
- Speaker Name
- Company
- Event Tag

### Intended & Endorsed Speakers Output
- Speaker Name and Company
- Rating flag (Good option / Lower rating)
- Call Notes:
  - "In sum" section
  - Date of call
  - First two lines below "In sum"
- Jelena's Comments:
  - INsum rating
  - First two lines of comments
- Abstract title
- Content fit analysis (up to 50 words)
- IR Speaking Engagement (full ratings if available)
- Axel's input (first line containing "25:" if present)
- Region

## Output Formats

### CSV Format
Tabular format with columns for all key information. Best for importing into Excel or other tools.

### JSON Format
Structured data format with:
- Event metadata
- Summary statistics
- Full speaker details in nested structure
- Content fit analysis included

### Text Format
Human-readable report with:
- Clear section headers
- Formatted speaker profiles
- Easy-to-scan layout
- All relevant information organized by category

## Column Mapping

The tool expects these columns in your Airtable table (can be customized in `config.py`):

- `Workshops`: Contains event tags
- `Axel's rating`: Numeric rating
- `Notes speaker calls`: Call notes with "In sum" sections
- `Jelena's comments`: Comments with ratings
- `Region`: Geographic region
- `Abstract`: Speaker abstract with title
- `Company`: Speaker's company
- `IR Speaking engagement`: IR ratings
- `Activity notes`: Activity log (checked for "DON'T CONTACT")
- `Name`: Speaker name (adjust column name in config.py)

## Customization

### Adjusting Rating Thresholds

Edit `config.py`:

```python
AXEL_RATING_GOOD = 94  # "Good option" threshold
AXEL_RATING_LOWER = 92  # Minimum Axel rating
IR_RATING_THRESHOLD = 3.8  # Minimum IR rating
```

### Changing Column Names

If your Airtable columns have different names, update the `COLUMNS` dictionary in `config.py`.

## Troubleshooting

### "AIRTABLE_API_KEY not set"
- Ensure `.env` file exists in project root
- Check that variable names match exactly
- Verify API key is valid

### "No records found"
- Verify table name matches exactly (case-sensitive)
- Check Base ID is correct
- Ensure API key has access to the base

### Missing speaker data
- Check that column names in `config.py` match your Airtable
- Verify records have data in the expected columns

## Requirements

- Python 3.7 or higher
- Internet connection (for Airtable API)
- Valid Airtable account and API key

## Support

For issues or questions:
1. Check that all Airtable credentials are correct
2. Verify column names match your table structure
3. Review the generated output files for any error messages

## License

This tool is provided as-is for internal use.




