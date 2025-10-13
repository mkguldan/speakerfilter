"""
Module for fetching data from Airtable.
"""
from pyairtable import Api
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME


class AirtableFetcher:
    """Handles fetching data from Airtable."""
    
    def __init__(self):
        """Initialize Airtable API connection."""
        if not AIRTABLE_API_KEY:
            raise ValueError("AIRTABLE_API_KEY not set in environment variables")
        if not AIRTABLE_BASE_ID:
            raise ValueError("AIRTABLE_BASE_ID not set in environment variables")
        if not AIRTABLE_TABLE_NAME:
            raise ValueError("AIRTABLE_TABLE_NAME not set in environment variables")
            
        self.api = Api(AIRTABLE_API_KEY)
        self.table = self.api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
    
    def fetch_all_records(self):
        """
        Fetch all records from the Airtable table.
        
        Returns:
            list: List of all records with their fields
        """
        try:
            records = self.table.all()
            return records
        except Exception as e:
            raise Exception(f"Error fetching records from Airtable: {str(e)}")
    
    def get_records_dict(self):
        """
        Get all records as a list of dictionaries with fields only.
        
        Returns:
            list: List of record fields
        """
        records = self.fetch_all_records()
        return [record['fields'] for record in records]


