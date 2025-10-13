"""
Output generation for speaker filtering results.
"""
import csv
import json
from datetime import datetime
from text_extractor import TextExtractor


class OutputGenerator:
    """Generates output in various formats."""
    
    def __init__(self, event_name, event_title=""):
        """
        Initialize output generator.
        
        Args:
            event_name: Name of the event
            event_title: Full title of the event
        """
        self.event_name = event_name
        self.event_title = event_title
        self.text_extractor = TextExtractor()
    
    def generate_csv(self, confirmed, intended, endorsed, output_file):
        """
        Generate CSV output file.
        
        Args:
            confirmed: List of confirmed speakers
            intended: List of intended speakers
            endorsed: List of endorsed speakers
            output_file: Path to output CSV file
        """
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Category', 'Speaker Name', 'Company', 'Rating Flag', 
                           'Axel Rating', 'IR Rating', 'Analysis', 'Call Date', 
                           'In Sum', 'Jelena Rating', 'Jelena Comments', 
                           'Abstract Title', 'Region', 'IR Engagement Full'])
            
            # Write confirmed speakers
            for speaker in confirmed:
                writer.writerow([
                    speaker['category'],
                    speaker['speaker_name'],
                    speaker.get('company', ''),
                    '',  # No rating flag for confirmed
                    '',  # No detailed info for confirmed
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ])
            
            # Write intended speakers
            for speaker in intended:
                analysis = self._generate_analysis_text(speaker)
                writer.writerow([
                    speaker['category'],
                    speaker['speaker_name'],
                    speaker.get('company', ''),
                    speaker.get('rating_flag', ''),
                    speaker.get('axel_rating', ''),
                    speaker.get('ir_rating', ''),
                    analysis,
                    speaker.get('call_date', ''),
                    speaker.get('in_sum', ''),
                    speaker.get('jelena_rating', ''),
                    speaker.get('jelena_comments', ''),
                    speaker.get('abstract_title', ''),
                    speaker.get('region', ''),
                    speaker.get('ir_engagement', '')
                ])
            
            # Write endorsed speakers
            for speaker in endorsed:
                analysis = self._generate_analysis_text(speaker)
                writer.writerow([
                    speaker['category'],
                    speaker['speaker_name'],
                    speaker.get('company', ''),
                    speaker.get('rating_flag', ''),
                    speaker.get('axel_rating', ''),
                    speaker.get('ir_rating', ''),
                    analysis,
                    speaker.get('call_date', ''),
                    speaker.get('in_sum', ''),
                    speaker.get('jelena_rating', ''),
                    speaker.get('jelena_comments', ''),
                    speaker.get('abstract_title', ''),
                    speaker.get('region', ''),
                    speaker.get('ir_engagement', '')
                ])
        
        print(f"CSV file generated: {output_file}")
    
    def generate_json(self, confirmed, intended, endorsed, output_file):
        """
        Generate JSON output file.
        
        Args:
            confirmed: List of confirmed speakers
            intended: List of intended speakers
            endorsed: List of endorsed speakers
            output_file: Path to output JSON file
        """
        output_data = {
            'event_name': self.event_name,
            'event_title': self.event_title,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'confirmed_count': len(confirmed),
                'intended_count': len(intended),
                'endorsed_count': len(endorsed)
            },
            'confirmed_speakers': confirmed,
            'intended_speakers': [self._enhance_speaker_data(s) for s in intended],
            'endorsed_speakers': [self._enhance_speaker_data(s) for s in endorsed]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"JSON file generated: {output_file}")
    
    def generate_text(self, confirmed, intended, endorsed, output_file):
        """
        Generate human-readable text output.
        
        Args:
            confirmed: List of confirmed speakers
            intended: List of intended speakers
            endorsed: List of endorsed speakers
            output_file: Path to output text file
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("SPEAKER PROSPECT FILTERING REPORT\n")
            f.write(f"Event: {self.event_name}\n")
            if self.event_title:
                f.write(f"Title: {self.event_title}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            # Confirmed Speakers
            f.write("### CONFIRMED SPEAKERS ###\n")
            f.write("Count: {}\n\n".format(len(confirmed)))
            
            if confirmed:
                for i, speaker in enumerate(confirmed, 1):
                    f.write(f"{i}. {speaker['speaker_name']}")
                    if speaker.get('company'):
                        f.write(f" - {speaker['company']}")
                    f.write(f"\n   Tag: {speaker.get('tag', '')}\n\n")
            else:
                f.write("No confirmed speakers found.\n\n")
            
            f.write("\n" + "="*80 + "\n\n")
            
            # Intended Speakers
            f.write("### INTENDED SPEAKERS ###\n")
            f.write("Count: {}\n\n".format(len(intended)))
            
            if intended:
                for i, speaker in enumerate(intended, 1):
                    f.write(self._format_detailed_speaker(speaker, i))
            else:
                f.write("No intended speakers found.\n\n")
            
            f.write("\n" + "="*80 + "\n\n")
            
            # Endorsed Speakers
            f.write("### ENDORSED SPEAKERS ###\n")
            f.write(f"Count: {len(endorsed)}\n\n")
            
            if endorsed:
                for i, speaker in enumerate(endorsed, 1):
                    f.write(self._format_detailed_speaker(speaker, i))
            else:
                f.write("No endorsed speakers found.\n\n")
        
        print(f"Text file generated: {output_file}")
    
    def _format_detailed_speaker(self, speaker, index):
        """
        Format detailed speaker information for text output.
        
        Args:
            speaker: Speaker data dictionary
            index: Speaker index number
            
        Returns:
            str: Formatted speaker information
        """
        output = f"{index}. {speaker['speaker_name']}"
        if speaker.get('company'):
            output += f" - {speaker['company']}"
        output += "\n"
        
        if speaker.get('rating_flag'):
            output += f"   Rating: {speaker['rating_flag']}"
            if speaker.get('axel_rating'):
                output += f" (Axel: {speaker['axel_rating']})"
            output += "\n"
        
        # Call notes
        if speaker.get('in_sum') or speaker.get('call_date'):
            output += "\n   Call Notes:\n"
            if speaker.get('call_date'):
                output += f"   Date: {speaker['call_date']}\n"
            if speaker.get('in_sum'):
                output += f"   In Sum: {speaker['in_sum']}\n"
        
        # Jelena's comments
        if speaker.get('jelena_rating') or speaker.get('jelena_comments'):
            output += "\n   Jelena's Comments:\n"
            if speaker.get('jelena_rating'):
                output += f"   Rating: {speaker['jelena_rating']}\n"
            if speaker.get('jelena_comments'):
                output += f"   {speaker['jelena_comments']}\n"
        
        # Abstract title
        if speaker.get('abstract_title'):
            output += f"\n   Abstract Title: {speaker['abstract_title']}\n"
        
        # Content fit analysis
        analysis = self.text_extractor.generate_content_fit_analysis(
            speaker.get('full_abstract', ''), 
            self.event_title
        )
        output += f"\n   Content Fit Analysis:\n   {analysis}\n"
        
        # IR Speaking engagement
        if speaker.get('ir_engagement'):
            output += f"\n   IR Speaking Engagement: {speaker['ir_engagement']}\n"
        
        # Region
        if speaker.get('region'):
            output += f"   Region: {speaker['region']}\n"
        
        output += "\n" + "-"*80 + "\n\n"
        
        return output
    
    def _generate_analysis_text(self, speaker):
        """
        Generate brief analysis text for CSV output.
        
        Args:
            speaker: Speaker data dictionary
            
        Returns:
            str: Analysis text
        """
        return self.text_extractor.generate_content_fit_analysis(
            speaker.get('full_abstract', ''),
            self.event_title,
            max_words=50
        )
    
    def _enhance_speaker_data(self, speaker):
        """
        Enhance speaker data with analysis for JSON output.
        
        Args:
            speaker: Speaker data dictionary
            
        Returns:
            dict: Enhanced speaker data
        """
        enhanced = speaker.copy()
        enhanced['content_fit_analysis'] = self._generate_analysis_text(speaker)
        return enhanced

