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

# Column names in Airtable/CSV
# These map to the actual column names in your data
COLUMNS = {
    'workshops': 'Workshops 25',  # Updated to match CSV format
    'axel_rating': "Axel Input",  # Updated to match CSV format
    'notes_speaker_calls': 'Notes Speaker Call',  # Updated to match CSV format
    'jelena_comments': "Scout Comments",  # Updated to match CSV format
    'region': 'Region',
    'abstract': 'Abstract',
    'company': 'Company',
    'ir_speaking_engagement': 'IR Speaking Engagements (Title and Event)',  # Updated
    'activity_notes': 'Activity Notes',  # Updated
    'speaker_name': 'Record Identifier'  # Updated to match CSV format
}

# Rating thresholds
AXEL_RATING_GOOD = 94
AXEL_RATING_LOWER = 92
IR_RATING_THRESHOLD = 3.8

# Region filters for Intended/Endorsed
EXCLUDED_REGIONS = ['Asia', 'US']


