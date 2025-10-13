"""
Main application for Speaker Prospect Filtering Tool.
"""
import argparse
import sys
from datetime import datetime
from airtable_fetcher import AirtableFetcher
from filters import SpeakerFilter
from output_generator import OutputGenerator


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Speaker Prospect Filtering Tool - Filter and organize speaker prospects from Airtable'
    )
    parser.add_argument(
        'event_name',
        help='Event name tag (e.g., "2511 Barclays")'
    )
    parser.add_argument(
        '--event-title',
        default='',
        help='Full event title for content fit analysis'
    )
    parser.add_argument(
        '--output',
        default='speaker_report',
        help='Output file name (without extension)'
    )
    parser.add_argument(
        '--format',
        choices=['csv', 'json', 'text', 'all'],
        default='all',
        help='Output format (default: all)'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("Speaker Prospect Filtering Tool")
    print("="*60)
    print(f"Event: {args.event_name}")
    print(f"Output: {args.output}")
    print(f"Format: {args.format}")
    print("-"*60)
    
    try:
        # Step 1: Fetch data from Airtable
        print("\n[1/4] Fetching data from Airtable...")
        fetcher = AirtableFetcher()
        records = fetcher.get_records_dict()
        print(f"✓ Fetched {len(records)} records")
        
        # Step 2: Filter speakers into categories
        print("\n[2/4] Filtering speakers into categories...")
        speaker_filter = SpeakerFilter(args.event_name)
        
        confirmed = speaker_filter.filter_confirmed(records)
        print(f"✓ Found {len(confirmed)} confirmed speakers")
        
        intended = speaker_filter.filter_intended(records)
        print(f"✓ Found {len(intended)} intended speakers")
        
        endorsed = speaker_filter.filter_endorsed(records)
        print(f"✓ Found {len(endorsed)} endorsed speakers")
        
        # Step 3: Generate output
        print("\n[3/4] Generating output files...")
        generator = OutputGenerator(args.event_name, args.event_title)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_base = f"{args.output}_{timestamp}"
        
        if args.format in ['csv', 'all']:
            csv_file = f"{output_base}.csv"
            generator.generate_csv(confirmed, intended, endorsed, csv_file)
        
        if args.format in ['json', 'all']:
            json_file = f"{output_base}.json"
            generator.generate_json(confirmed, intended, endorsed, json_file)
        
        if args.format in ['text', 'all']:
            text_file = f"{output_base}.txt"
            generator.generate_text(confirmed, intended, endorsed, text_file)
        
        # Step 4: Summary
        print("\n[4/4] Complete!")
        print("-"*60)
        print("Summary:")
        print(f"  Confirmed: {len(confirmed)}")
        print(f"  Intended: {len(intended)}")
        print(f"  Endorsed: {len(endorsed)}")
        print(f"  Total: {len(confirmed) + len(intended) + len(endorsed)}")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())




