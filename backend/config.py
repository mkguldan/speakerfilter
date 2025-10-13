"""
Configuration module for the Speaker Prospect Filtering Tool.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Airtable Configuration
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

# Column names in Airtable
COLUMNS = {
    'workshops': 'Workshops',
    'axel_rating': "Axel's rating",
    'notes_speaker_calls': 'Notes speaker calls',
    'jelena_comments': "Jelena's comments",
    'region': 'Region',
    'abstract': 'Abstract',
    'company': 'Company',
    'ir_speaking_engagement': 'IR Speaking engagement',
    'activity_notes': 'Activity notes',
    'speaker_name': 'Name'  # Adjust this to match your actual name column
}

# Rating thresholds
AXEL_RATING_GOOD = 94
AXEL_RATING_LOWER = 92
IR_RATING_THRESHOLD = 3.8

# Region filters for Intended/Endorsed
EXCLUDED_REGIONS = ['Asia', 'US']


