"""
Text extraction utilities for parsing notes and comments.
"""
import re


class TextExtractor:
    """Utilities for extracting specific sections from text fields."""
    
    @staticmethod
    def extract_in_sum_section(notes_text):
        """
        Extract 'In sum' section and the first two lines after it from call notes.
        
        Args:
            notes_text: Text containing call notes
            
        Returns:
            tuple: (in_sum_section, date_of_call) or (None, None)
        """
        if not notes_text:
            return None, None
        
        # Look for "In sum" section (case insensitive)
        in_sum_pattern = r'In sum[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)'
        match = re.search(in_sum_pattern, notes_text, re.IGNORECASE | re.DOTALL)
        
        in_sum_content = None
        if match:
            in_sum_content = match.group(1).strip()
            # Get first two lines after "In sum"
            lines = in_sum_content.split('\n')
            if len(lines) > 2:
                in_sum_content = '\n'.join(lines[:2])
        
        # Try to extract date (various formats)
        date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|[A-Z][a-z]+ \d{1,2},? \d{4})'
        date_match = re.search(date_pattern, notes_text)
        date_of_call = date_match.group(1) if date_match else None
        
        return in_sum_content, date_of_call
    
    @staticmethod
    def extract_jelena_comments(jelena_text):
        """
        Extract rating and first two lines from Jelena's comments.
        
        Args:
            jelena_text: Text from Jelena's comments column
            
        Returns:
            tuple: (rating, first_two_lines) or (None, None)
        """
        if not jelena_text:
            return None, None
        
        # Look for "INsum" or "In sum" with rating (number)
        rating_pattern = r'[Ii]n?\s*sum[:\s]*(\d+(?:\.\d+)?)'
        rating_match = re.search(rating_pattern, jelena_text)
        rating = rating_match.group(1) if rating_match else None
        
        # Get first two lines
        lines = jelena_text.strip().split('\n')
        first_two_lines = '\n'.join(lines[:2]) if lines else None
        
        return rating, first_two_lines
    
    @staticmethod
    def extract_abstract_title(abstract_text):
        """
        Extract title from the Abstract column.
        
        Args:
            abstract_text: Text from Abstract column
            
        Returns:
            str: Extracted title or first line
        """
        if not abstract_text:
            return None
        
        # Try to find a title pattern (first line or text before colon/newline)
        lines = abstract_text.strip().split('\n')
        if lines:
            # If first line looks like a title (short, capitalized)
            first_line = lines[0].strip()
            if len(first_line) < 200:  # Reasonable title length
                return first_line
        
        return abstract_text[:200] + "..." if len(abstract_text) > 200 else abstract_text
    
    @staticmethod
    def extract_axel_25_line(axel_input_text):
        """
        Extract first line from Axel's input if it contains '25:'.
        
        Args:
            axel_input_text: Text from Axel's input column
            
        Returns:
            str: First line containing '25:' or None
        """
        if not axel_input_text:
            return None
        
        lines = axel_input_text.strip().split('\n')
        for line in lines:
            if '25:' in line or '25 ' in line:
                return line.strip()
        
        return None
    
    @staticmethod
    def extract_ir_rating(ir_engagement_text):
        """
        Extract IR speaking engagement rating (looking for 3.8 or above).
        
        Args:
            ir_engagement_text: Text or number from IR Speaking engagement column
            
        Returns:
            float: Rating value or None
        """
        if not ir_engagement_text:
            return None
        
        # If it's already a number
        if isinstance(ir_engagement_text, (int, float)):
            return float(ir_engagement_text)
        
        # Try to extract number from text
        rating_pattern = r'(\d+\.\d+|\d+)'
        match = re.search(rating_pattern, str(ir_engagement_text))
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        
        return None
    
    @staticmethod
    def generate_content_fit_analysis(abstract_text, event_title, max_words=50):
        """
        Generate a brief analysis of content fit (placeholder - can be enhanced with AI).
        
        Args:
            abstract_text: Speaker's abstract
            event_title: Event title
            max_words: Maximum words for analysis
            
        Returns:
            str: Brief analysis
        """
        if not abstract_text or not event_title:
            return "Content fit analysis not available due to missing information."
        
        # Simple keyword matching analysis (can be enhanced with NLP/AI)
        abstract_lower = abstract_text.lower()
        event_lower = event_title.lower()
        
        # Extract key terms from event title (words longer than 3 chars)
        event_keywords = [word for word in re.findall(r'\b\w+\b', event_lower) 
                         if len(word) > 3 and word not in ['this', 'that', 'with', 'from', 'will']]
        
        # Check for keyword matches
        matches = [kw for kw in event_keywords if kw in abstract_lower]
        
        if len(matches) >= 2:
            return f"Strong content fit: Speaker's expertise aligns with event focus on {', '.join(matches[:3])}. Abstract demonstrates relevant experience."
        elif len(matches) == 1:
            return f"Moderate fit: Abstract touches on {matches[0]}, relevant to event theme. May need to confirm specific angle."
        else:
            return "Content fit requires review: Abstract covers different focus area. Recommend verifying alignment with event objectives."


