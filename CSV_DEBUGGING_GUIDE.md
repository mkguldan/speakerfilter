# CSV Upload Debugging Guide

## Why Am I Getting 0 Results?

Your CSV file needs to have specific columns and tags for the filtering to work.

### Required CSV Structure

Your CSV must have these columns (case-sensitive):

| Column Name | Description | Required? |
|------------|-------------|-----------|
| **Name** | Speaker's name | Yes |
| **Workshops** | Event tags (this is where filtering happens!) | **Critical** |
| **Company** | Speaker's company | Optional |
| **Axel's rating** | Numeric rating (e.g., 92, 94, 96) | For filtering |
| **IR Speaking engagement** | IR rating (e.g., 3.8, 4.0) | For filtering |
| **Notes speaker calls** | Call notes with "In sum" sections | Optional |
| **Jelena's comments** | Comments with ratings | Optional |
| **Abstract** | Speaker abstract | Optional |
| **Region** | Geographic region | Optional |
| **Activity notes** | Activity log | Optional |

### The Critical Part: Workshops Column

The **Workshops** column must contain tags matching your event name format:

**If your event name is: "2511 Barclays"**

Your Workshops column should have entries like:
- `2511 Barclays Confirmed`
- `2511 Barclays Intended`
- `2511 Barclays Endorsed`

**If your event name is: "speakertestcsv"**

Your Workshops column should have:
- `speakertestcsv Confirmed`
- `speakertestcsv Intended`
- `speakertestcsv Endorsed`

### Example CSV Format

```csv
Name,Workshops,Company,Axel's rating,IR Speaking engagement
"John Smith","2511 Barclays Confirmed","Acme Corp",95,4.2
"Jane Doe","2511 Barclays Intended","Tech Inc",93,3.9
"Bob Johnson","2511 Barclays Endorsed","Finance Co",91,4.5
"Alice Williams","2511 Barclays Intended, 2511 Barclays not reached","StartUp LLC",94,3.5
```

## How to Debug Your CSV

### Step 1: Check Your Columns

After uploading, the system shows you:
- Number of rows
- Number of columns
- Column names
- Sample data

**Look for:**
1. ✅ Is there a "Workshops" column?
2. ✅ Are the column names spelled exactly as expected?
3. ✅ Do you have a "Name" column?

### Step 2: Check Your Event Name

The event name you enter must **match the tags** in your Workshops column.

**Wrong:**
- Event name: `2511 Barclays`
- Workshops column: `Barclays Confirmed` ❌ (missing "2511")

**Right:**
- Event name: `2511 Barclays`
- Workshops column: `2511 Barclays Confirmed` ✅

### Step 3: Check Your Tags Format

The system looks for these exact patterns:
- `[EVENT_NAME] Confirmed`
- `[EVENT_NAME] Intended`
- `[EVENT_NAME] Endorsed`

**Case doesn't matter** - the system does case-insensitive matching.

## Common Issues & Solutions

### Issue 1: Wrong Event Name

❌ **Problem**: You entered "speakertestcsv" but your CSV has "2511 Barclays Confirmed"

✅ **Solution**: Enter "2511 Barclays" as the event name

### Issue 2: Missing Workshops Column

❌ **Problem**: Your CSV doesn't have a "Workshops" column

✅ **Solution**: 
- Add a "Workshops" column to your CSV
- Or rename your tags column to "Workshops"

### Issue 3: Wrong Tag Format

❌ **Problem**: Workshops column has just "Confirmed" instead of "EventName Confirmed"

✅ **Solution**: 
- Update your CSV to include the event name in each tag
- Format: `[EVENT_NAME] [STATUS]`

### Issue 4: Column Name Mismatch

❌ **Problem**: Your CSV has "Workshop" (singular) but system expects "Workshops" (plural)

✅ **Solution**: Rename the column to exactly "Workshops"

## How to Fix Your CSV

### Option 1: Update Your CSV File

1. Open your CSV in Excel or a text editor
2. Make sure you have a "Workshops" column
3. Add tags like: `speakertestcsv Confirmed`, `speakertestcsv Intended`, etc.
4. Save and re-upload

### Option 2: Find What Tags Exist

Look at the sample data shown after upload. Check what's actually in your "Workshops" column, then use that as your event name (minus the " Confirmed" part).

**Example:**
If your Workshops column shows: `"TestEvent Confirmed"`
Then enter event name as: `TestEvent`

## Testing Your CSV

### Create a Simple Test CSV

Save this as `test_speakers.csv`:

```csv
Name,Workshops,Company,Axel's rating,IR Speaking engagement
"Test Speaker 1","TestEvent Confirmed","Company A",95,4.0
"Test Speaker 2","TestEvent Intended","Company B",93,3.9
"Test Speaker 3","TestEvent Endorsed","Company C",92,4.2
```

Then:
1. Upload this file
2. Enter event name: `TestEvent`
3. Click "Filter Speakers"
4. You should get 3 results!

## What Gets Filtered?

### Confirmed Speakers
- ✅ **Includes**: Anyone with `[EVENT_NAME] Confirmed` tag
- ❌ **Excludes**: Nothing - all confirmed are included

### Intended Speakers
- ✅ **Includes**: `[EVENT_NAME] Intended` tag with:
  - Axel's rating ≥ 92, OR
  - IR Speaking engagement ≥ 3.8
- ❌ **Excludes**:
  - `[EVENT_NAME] not reached` tag
  - `[EVENT_NAME] not available` tag
  - Activity notes containing "DON'T CONTACT"

### Endorsed Speakers
- ✅ **Includes**: `[EVENT_NAME] Endorsed` tag with:
  - Axel's rating ≥ 92, OR
  - IR Speaking engagement ≥ 3.8
- ❌ **Excludes**:
  - Activity notes containing "DON'T CONTACT"

## Quick Checklist

Before clicking "Filter Speakers":

- [ ] CSV has "Workshops" column (exact spelling)
- [ ] CSV has "Name" column
- [ ] Workshops column contains tags like "[EventName] Confirmed"
- [ ] Event name you enter matches the tags in Workshops
- [ ] At least one row has the matching tag

## Need More Help?

### View Your Data

After uploading, look at the "sample_data" in the response. This shows you the first 3 rows of your CSV and helps you see:
- What columns you actually have
- What values are in the Workshops column
- What event name to use

### Check Backend Logs

If running locally, check the terminal where the backend is running. It will show any errors.

If on Cloud Run, check logs:
```bash
gcloud run services logs read speaker-filter-backend --region us-central1
```

## Real-World Example

Your Airtable (or CSV) might look like this:

| Name | Workshops | Company | Axel's rating |
|------|-----------|---------|---------------|
| John | 2511 Barclays Confirmed, 2601 Microsoft Intended | Acme | 95 |
| Jane | 2511 Barclays Intended | Tech Co | 93 |
| Bob | 2601 Microsoft Confirmed | Finance | 96 |

To filter **2511 Barclays** speakers:
- Enter event name: `2511 Barclays`
- Results: John (Confirmed), Jane (Intended)

To filter **2601 Microsoft** speakers:
- Enter event name: `2601 Microsoft`
- Results: John (Intended), Bob (Confirmed)

---

**The key**: Your event name must match the prefix of the tags in your Workshops column! 🔑

