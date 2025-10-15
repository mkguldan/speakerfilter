"""
Simple script to check CSV format and suggest event names.
Run this to debug why you're getting 0 results.
"""
import pandas as pd
import sys

def check_csv(filepath):
    """Check CSV format and suggest event names."""
    print(f"\n{'='*60}")
    print(f"🔍 Analyzing CSV: {filepath}")
    print(f"{'='*60}\n")
    
    try:
        # Read CSV
        df = pd.read_csv(filepath)
        
        # Basic info
        print(f"✅ CSV loaded successfully!")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}\n")
        
        # Column names
        print(f"📋 Columns in your CSV:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")
        
        # Check critical columns
        print(f"\n🎯 Critical Column Check:")
        required_cols = {
            'Workshops': 'Workshops',
            'Name': 'Name',
        }
        
        missing = []
        for display_name, col_name in required_cols.items():
            if col_name in df.columns:
                print(f"   ✅ '{col_name}' column found")
            else:
                print(f"   ❌ '{col_name}' column MISSING")
                missing.append(col_name)
        
        if missing:
            print(f"\n⚠️  WARNING: Missing critical columns: {', '.join(missing)}")
            print(f"   The filtering won't work without these columns!")
            
            # Suggest similar columns
            print(f"\n💡 Did you mean one of these?")
            for col in df.columns:
                for miss in missing:
                    if miss.lower() in col.lower():
                        print(f"   - '{col}' (close to '{miss}')")
        
        # Analyze Workshops column if exists
        if 'Workshops' in df.columns:
            print(f"\n🔍 Analyzing 'Workshops' column:")
            
            # Get unique values
            workshops_data = df['Workshops'].dropna().unique()
            
            if len(workshops_data) == 0:
                print(f"   ⚠️  Workshops column is EMPTY!")
            else:
                print(f"   Found {len(workshops_data)} unique tag patterns:\n")
                
                # Extract potential event names
                event_names = set()
                for entry in workshops_data[:20]:  # Show first 20
                    entry_str = str(entry)
                    print(f"   - {entry_str[:80]}")
                    
                    # Try to extract event name (text before Confirmed/Intended/Endorsed)
                    for keyword in ['Confirmed', 'Intended', 'Endorsed']:
                        if keyword in entry_str:
                            event_name = entry_str.split(keyword)[0].strip()
                            if event_name:
                                event_names.add(event_name)
                
                # Suggest event names
                if event_names:
                    print(f"\n💡 Suggested Event Names:")
                    print(f"   Based on your data, try entering one of these:")
                    for event_name in sorted(event_names):
                        print(f"   📌 \"{event_name}\"")
                else:
                    print(f"\n⚠️  Could not detect standard event name patterns!")
                    print(f"   Expected format: '[EventName] Confirmed' or '[EventName] Intended'")
        
        # Show sample data
        print(f"\n📊 Sample Data (first 3 rows):")
        print(f"\n{df.head(3).to_string()}\n")
        
        # Count potential matches for common patterns
        if 'Workshops' in df.columns:
            print(f"\n📈 Tag Distribution:")
            for keyword in ['Confirmed', 'Intended', 'Endorsed']:
                count = df['Workshops'].astype(str).str.contains(keyword, case=False, na=False).sum()
                print(f"   {keyword:12s}: {count} rows")
        
        print(f"\n{'='*60}")
        print(f"✅ Analysis complete!")
        print(f"{'='*60}\n")
        
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {filepath}")
        print(f"   Make sure the file path is correct.")
    except pd.errors.EmptyDataError:
        print(f"❌ ERROR: CSV file is empty!")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n" + "="*60)
        print("CSV Format Checker for Speaker Filter Tool")
        print("="*60)
        print("\nUsage:")
        print("  python check_csv_format.py <path_to_csv_file>")
        print("\nExample:")
        print("  python check_csv_format.py speakertestcsv.csv")
        print("  python check_csv_format.py \"C:\\Users\\Name\\Downloads\\speakers.csv\"")
        print("\n" + "="*60 + "\n")
    else:
        check_csv(sys.argv[1])

