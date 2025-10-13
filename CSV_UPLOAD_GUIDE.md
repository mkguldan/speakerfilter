# 📤 CSV Upload Guide - Speaker Prospect Filtering Tool

## ✅ What Changed

The application now accepts **CSV file uploads** instead of connecting to Airtable!

### Why CSV Upload?
- ✅ **Quick Start** - No Airtable setup needed
- ✅ **Flexible** - Use any data source (export from Airtable, Excel, Google Sheets, etc.)
- ✅ **Large Files** - Supports up to **1GB** CSV files
- ✅ **Offline** - No external API dependencies

---

## 📋 CSV Requirements

### Required Columns

Your CSV must have these columns (exact names, case-sensitive):

| Column Name | Description | Example |
|------------|-------------|---------|
| `Name` | Speaker name | John Doe |
| `Workshops` | Event tags | "2511 Barclays Confirmed" |
| `Axel's rating` | Numeric rating | 94 |
| `Notes speaker calls` | Call notes with "In sum" | See below |
| `Jelena's comments` | Comments with rating | "INsum 4.5: Great speaker..." |
| `Abstract` | Speaker abstract | "Expert in..." |
| `Company` | Speaker's company | TechCorp Inc |
| `Region` | Geographic region | Europe, Asia, US |
| `IR Speaking engagement` | IR ratings | 4.2 |
| `Activity notes` | Activity log | Recent activities |

### Optional Columns
All other columns will be ignored but won't cause errors.

---

## 📤 How to Upload

### 1. **Export from Airtable**

```
1. Open your Airtable base
2. Click on the view you want to export
3. Click "..." menu → "Download CSV"
4. Save the file
```

### 2. **Export from Excel/Google Sheets**

**Excel:**
- File → Save As → Choose "CSV (Comma delimited)" format

**Google Sheets:**
- File → Download → Comma-separated values (.csv)

### 3. **Ensure Column Names Match**

Open your CSV in a text editor or Excel and verify the first row has exact column names as listed above.

---

## 🎯 Using the Application

### Step 1: Upload CSV

1. Open the web application
2. **Drag and drop** your CSV file into the upload box
3. Or **click to browse** and select your file
4. You'll see a green confirmation with file name and size

### Step 2: Filter Speakers

1. Enter **Event Name** (e.g., "2511 Barclays")
2. Optionally enter **Event Title** for better analysis
3. Click **"Filter Speakers"**
4. Wait for results (large files may take a moment)

### Step 3: View Results

Results are organized in three tabs:
- **Confirmed** - Speakers with "Event Name Confirmed" tag
- **Intended** - Speakers with filtering applied
- **Endorsed** - Endorsed speakers with filtering

### Step 4: Export

Click any export button to download:
- **CSV** - Spreadsheet format
- **JSON** - Structured data
- **TXT** - Human-readable report

---

## 📊 File Size Limits

| Limit | Value |
|-------|-------|
| Maximum file size | **1GB** |
| Maximum rows | No hard limit (memory dependent) |
| Typical file size | 5-50MB (thousands of rows) |
| Processing time | ~1-5 seconds for typical files |

### Performance Tips
- ✅ Files under 100MB process instantly
- ✅ 100MB-500MB files take 2-10 seconds
- ✅ 500MB-1GB files may take 10-30 seconds
- ⚠️ Very large files (>500MB) are best processed locally

---

## 🔍 Example CSV Format

```csv
Name,Workshops,Axel's rating,Notes speaker calls,Jelena's comments,Abstract,Company,Region,IR Speaking engagement,Activity notes
John Doe,"2511 Barclays Confirmed",95,"Call on 2024-01-15. In sum: Excellent speaker with deep expertise.","INsum 4.5: Highly recommended","Expert in digital transformation",TechCorp,Europe,4.2,"Recent keynote at..."
Jane Smith,"2511 Barclays Intended",92,"In sum: Strong candidate","INsum 4.0: Good fit","Leadership expert",FinanceInc,US,3.9,"Spoke at..."
```

---

## ⚠️ Common Issues

### "File must be a CSV file"
- Ensure file has `.csv` extension
- Don't use `.xlsx`, `.xls`, or other formats
- Convert to CSV first

### "File size exceeds 1GB limit"
- Your file is too large
- Try exporting only needed rows
- Or split into multiple files

### "CSV file is empty"
- File has no data rows
- Check file in text editor
- Ensure it's not corrupted

### "No records found in CSV file"
- File might be empty after header
- Check for at least one data row
- Verify CSV is properly formatted

### "Column not found" errors
- Column names must match exactly
- Check capitalization (case-sensitive)
- Remove extra spaces in column names
- See "Required Columns" section above

---

## 🎨 UI Features

### Drag & Drop
- Drag CSV file directly onto upload area
- Visual feedback when dragging
- Hover effect shows it's ready to drop

### File Preview
- Shows file name and size after upload
- Green checkmark indicates file is ready
- Click X to remove and upload different file

### Status Indicators
- **Green**: File uploaded successfully
- **Loading**: Processing your file
- **Success**: Results ready!
- **Error**: Problem occurred (see error message)

---

## 🔒 Privacy & Security

### Your Data
- ✅ Files are processed **in memory** only
- ✅ Nothing is stored on the server
- ✅ Files are discarded immediately after processing
- ✅ No data is sent to third parties

### Best Practices
- Don't upload files with sensitive PII if concerned
- Use secure HTTPS connection (automatic in production)
- Clear your browser after using shared computers

---

## 🚀 Quick Start Example

1. **Export your Airtable view as CSV**
   ```
   Airtable → View → Download CSV
   ```

2. **Open the web app**
   ```
   https://your-app-url.web.app
   ```

3. **Upload CSV**
   - Drag file to upload box

4. **Filter speakers**
   - Event Name: `2511 Barclays`
   - Click "Filter Speakers"

5. **Done!** 🎉
   - View results in tabs
   - Export as needed

---

## 💡 Pro Tips

### Tip 1: Prepare Your CSV
Before uploading, verify:
- Column names match exactly
- No extra columns (they're fine but ignored)
- Data is clean (no corrupt rows)

### Tip 2: Event Names
Event names must match your "Workshops" column exactly:
- Correct: `2511 Barclays`
- Wrong: `2511 barclays` (case matters!)
- Wrong: `2511Barclays` (space matters!)

### Tip 3: Multiple Events
Want to process multiple events?
- Upload once
- Filter different event names
- Results update each time

### Tip 4: Keep File Handy
- Bookmark/save your CSV export
- Can reuse same file multiple times
- Upload again if you close browser

---

## 📞 Still Need Help?

**File too large?**
- Export fewer rows from source
- Split into multiple files
- Process locally instead (see CLI tool)

**Columns don't match?**
- Update CSV column headers
- Or ask developer to update column mapping

**Processing too slow?**
- Normal for large files (>100MB)
- Consider using smaller exports
- Or use CLI tool for batch processing

---

## 🎓 From Airtable to CSV

Since you were planning to use Airtable, here's how to export:

### One-Time Export
1. Open Airtable base
2. Go to your "Status View"
3. Click grid menu (...)
4. "Download CSV"
5. Use that file in the app!

### Regular Updates
- Export weekly/monthly from Airtable
- Upload latest CSV to filter speakers
- No integration needed!

---

**Ready to filter speakers? Upload your CSV and get started!** 🎤

