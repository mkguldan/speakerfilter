"""
Test script to verify Airtable connection and data structure.
"""
import sys
from airtable_fetcher import AirtableFetcher
from config import COLUMNS


def test_connection():
    """Test Airtable connection and display sample data."""
    print("="*60)
    print("AIRTABLE CONNECTION TEST")
    print("="*60)
    
    try:
        print("\n[1] Testing Airtable connection...")
        fetcher = AirtableFetcher()
        print("✓ Connection successful")
        
        print("\n[2] Fetching records...")
        records = fetcher.get_records_dict()
        print(f"✓ Fetched {len(records)} records")
        
        if len(records) == 0:
            print("\n⚠ Warning: No records found in table")
            return
        
        print("\n[3] Analyzing data structure...")
        sample_record = records[0]
        
        print(f"\n✓ Sample record has {len(sample_record)} fields")
        print("\nAvailable columns in your Airtable:")
        print("-" * 60)
        for i, key in enumerate(sorted(sample_record.keys()), 1):
            sample_value = sample_record[key]
            if isinstance(sample_value, str) and len(sample_value) > 50:
                sample_value = sample_value[:50] + "..."
            print(f"{i:2}. {key:30} | Example: {sample_value}")
        
        print("\n" + "="*60)
        print("COLUMN MAPPING CHECK")
        print("="*60)
        print("\nChecking if configured columns exist in Airtable:\n")
        
        missing_columns = []
        for config_key, column_name in COLUMNS.items():
            if column_name in sample_record:
                print(f"✓ {column_name:30} (config key: {config_key})")
            else:
                print(f"✗ {column_name:30} (config key: {config_key}) - NOT FOUND")
                missing_columns.append((config_key, column_name))
        
        if missing_columns:
            print("\n⚠ WARNING: Missing columns detected!")
            print("\nPlease update config.py to match your Airtable columns:")
            print("\nCOLUMNS = {")
            for config_key, column_name in COLUMNS.items():
                if (config_key, column_name) in missing_columns:
                    print(f"    '{config_key}': 'YOUR_ACTUAL_COLUMN_NAME',  # Update this!")
                else:
                    print(f"    '{config_key}': '{column_name}',")
            print("}")
        else:
            print("\n✓ All configured columns found in Airtable!")
        
        print("\n[4] Testing workshop tags...")
        workshop_tags = set()
        for record in records:
            workshops = record.get(COLUMNS['workshops'], '')
            if workshops:
                if isinstance(workshops, list):
                    for tag in workshops:
                        workshop_tags.add(str(tag))
                else:
                    workshop_tags.add(str(workshops))
        
        if workshop_tags:
            print(f"\n✓ Found {len(workshop_tags)} unique workshop tags:")
            for tag in sorted(workshop_tags)[:10]:  # Show first 10
                print(f"   - {tag}")
            if len(workshop_tags) > 10:
                print(f"   ... and {len(workshop_tags) - 10} more")
        else:
            print("\n⚠ No workshop tags found")
        
        print("\n" + "="*60)
        print("✓ CONNECTION TEST COMPLETE")
        print("="*60)
        print("\nYou can now run the main tool with:")
        print('    python main.py "YOUR_EVENT_NAME"')
        
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("\nPlease check your .env file and ensure all required variables are set:")
        print("  - AIRTABLE_API_KEY")
        print("  - AIRTABLE_BASE_ID")
        print("  - AIRTABLE_TABLE_NAME")
        return 1
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Verify your API key is correct and has permission")
        print("2. Check that the Base ID is correct")
        print("3. Ensure the table name matches exactly (case-sensitive)")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(test_connection())




