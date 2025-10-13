"""
Filtering logic for categorizing speakers.
"""
from config import (
    COLUMNS, 
    AXEL_RATING_GOOD, 
    AXEL_RATING_LOWER, 
    IR_RATING_THRESHOLD
)
from text_extractor import TextExtractor


class SpeakerFilter:
    """Handles filtering and categorization of speaker records."""
    
    def __init__(self, event_name):
        """
        Initialize filter with event name.
        
        Args:
            event_name: Name of the event (e.g., "2511 Barclays")
        """
        self.event_name = event_name
        self.text_extractor = TextExtractor()
    
    def filter_confirmed(self, records):
        """
        Filter confirmed speakers.
        
        Args:
            records: List of all speaker records
            
        Returns:
            list: Confirmed speakers with relevant fields
        """
        confirmed = []
        confirmed_tag = f"{self.event_name} Confirmed"
        
        for record in records:
            workshops = record.get(COLUMNS['workshops'], '')
            if not workshops:
                continue
            
            # Check if workshops contains the confirmed tag
            if isinstance(workshops, list):
                workshops_str = ' '.join(str(w) for w in workshops)
            else:
                workshops_str = str(workshops)
            
            if confirmed_tag.lower() in workshops_str.lower():
                confirmed.append({
                    'speaker_name': record.get(COLUMNS['speaker_name'], 'Unknown'),
                    'tag': confirmed_tag,
                    'company': record.get(COLUMNS['company'], ''),
                    'category': 'Confirmed'
                })
        
        return confirmed
    
    def filter_intended(self, records):
        """
        Filter intended speakers with sub-filtering by ratings.
        
        Args:
            records: List of all speaker records
            
        Returns:
            list: Intended speakers with detailed information
        """
        intended = []
        intended_tag = f"{self.event_name} Intended"
        not_reached_tag = f"{self.event_name} not reached"
        not_available_tag = f"{self.event_name} not available"
        
        for record in records:
            workshops = record.get(COLUMNS['workshops'], '')
            if not workshops:
                continue
            
            # Convert to string for checking
            if isinstance(workshops, list):
                workshops_str = ' '.join(str(w) for w in workshops)
            else:
                workshops_str = str(workshops)
            
            workshops_lower = workshops_str.lower()
            
            # Check if intended but not "not reached" or "not available"
            if intended_tag.lower() in workshops_lower:
                if not_reached_tag.lower() in workshops_lower or not_available_tag.lower() in workshops_lower:
                    continue
                
                # Check activity notes for DON'T CONTACT
                activity_notes = record.get(COLUMNS['activity_notes'], '')
                if activity_notes:
                    activity_lower = str(activity_notes).lower()
                    if "don't contact" in activity_lower or "do not contact" in activity_lower:
                        continue
                
                # Apply rating filters
                if self._passes_rating_filter(record):
                    intended_speaker = self._build_detailed_speaker_info(record, 'Intended')
                    intended.append(intended_speaker)
        
        return intended
    
    def filter_endorsed(self, records):
        """
        Filter endorsed speakers with sub-filtering by ratings.
        
        Args:
            records: List of all speaker records
            
        Returns:
            list: Endorsed speakers with detailed information
        """
        endorsed = []
        endorsed_tag = f"{self.event_name} Endorsed"
        
        for record in records:
            workshops = record.get(COLUMNS['workshops'], '')
            if not workshops:
                continue
            
            # Convert to string for checking
            if isinstance(workshops, list):
                workshops_str = ' '.join(str(w) for w in workshops)
            else:
                workshops_str = str(workshops)
            
            if endorsed_tag.lower() in workshops_str.lower():
                # Check activity notes for DON'T CONTACT
                activity_notes = record.get(COLUMNS['activity_notes'], '')
                if activity_notes:
                    activity_lower = str(activity_notes).lower()
                    if "don't contact" in activity_lower or "do not contact" in activity_lower:
                        continue
                
                # Apply rating filters
                if self._passes_rating_filter(record):
                    endorsed_speaker = self._build_detailed_speaker_info(record, 'Endorsed')
                    endorsed.append(endorsed_speaker)
        
        return endorsed
    
    def _passes_rating_filter(self, record):
        """
        Check if record passes rating filters.
        
        Args:
            record: Speaker record
            
        Returns:
            bool: True if passes filter
        """
        axel_rating = record.get(COLUMNS['axel_rating'])
        ir_engagement = record.get(COLUMNS['ir_speaking_engagement'])
        
        # Try to get numeric Axel rating
        axel_numeric = None
        if axel_rating is not None:
            try:
                axel_numeric = float(axel_rating)
            except (ValueError, TypeError):
                pass
        
        # Check Axel's rating
        if axel_numeric is not None and axel_numeric >= AXEL_RATING_LOWER:
            return True
        
        # Check IR speaking engagement rating
        ir_rating = self.text_extractor.extract_ir_rating(ir_engagement)
        if ir_rating is not None and ir_rating >= IR_RATING_THRESHOLD:
            return True
        
        return False
    
    def _get_rating_flag(self, record):
        """
        Get rating flag for speaker.
        
        Args:
            record: Speaker record
            
        Returns:
            str: Rating flag ("Good option", "Lower rating", or "")
        """
        axel_rating = record.get(COLUMNS['axel_rating'])
        
        axel_numeric = None
        if axel_rating is not None:
            try:
                axel_numeric = float(axel_rating)
            except (ValueError, TypeError):
                pass
        
        if axel_numeric is not None:
            if axel_numeric >= AXEL_RATING_GOOD:
                return "Good option"
            elif axel_numeric in [92, 93]:
                return "Lower rating"
        
        return ""
    
    def _build_detailed_speaker_info(self, record, category):
        """
        Build detailed speaker information for Intended/Endorsed categories.
        
        Args:
            record: Speaker record
            category: Category name
            
        Returns:
            dict: Detailed speaker information
        """
        # Extract all necessary information
        speaker_name = record.get(COLUMNS['speaker_name'], 'Unknown')
        company = record.get(COLUMNS['company'], '')
        notes = record.get(COLUMNS['notes_speaker_calls'], '')
        jelena_comments = record.get(COLUMNS['jelena_comments'], '')
        abstract = record.get(COLUMNS['abstract'], '')
        region = record.get(COLUMNS['region'], '')
        ir_engagement = record.get(COLUMNS['ir_speaking_engagement'], '')
        axel_rating = record.get(COLUMNS['axel_rating'], '')
        
        # Extract structured information
        in_sum, call_date = self.text_extractor.extract_in_sum_section(notes)
        jelena_rating, jelena_lines = self.text_extractor.extract_jelena_comments(jelena_comments)
        abstract_title = self.text_extractor.extract_abstract_title(abstract)
        
        # Build speaker info dictionary
        speaker_info = {
            'speaker_name': speaker_name,
            'company': company,
            'category': category,
            'rating_flag': self._get_rating_flag(record),
            'axel_rating': axel_rating,
            'in_sum': in_sum,
            'call_date': call_date,
            'full_notes': notes,
            'jelena_rating': jelena_rating,
            'jelena_comments': jelena_lines,
            'abstract_title': abstract_title,
            'full_abstract': abstract,
            'region': region,
            'ir_engagement': ir_engagement,
            'ir_rating': self.text_extractor.extract_ir_rating(ir_engagement)
        }
        
        return speaker_info

