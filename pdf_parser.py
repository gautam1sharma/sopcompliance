import PyPDF2
import re
from typing import List, Dict

class PDFParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
    def extract_text(self) -> str:
        """Extract text from PDF file."""
        try:
            with open(self.filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return self._clean_text(text)
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text by removing extra spaces and special characters."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:!?-]', '', text)
        return text.strip()
    
    def extract_sections(self) -> Dict[str, str]:
        """Extract sections from the document based on headings."""
        text = self.extract_text()
        sections = {}
        
        # Common section patterns in SOPs
        section_patterns = [
            r'(?i)section\s+\d+[.:]\s*([^\n]+)',
            r'(?i)chapter\s+\d+[.:]\s*([^\n]+)',
            r'(?i)\d+\.\s*([^\n]+)'
        ]
        
        # Find all potential section headers
        section_headers = []
        for pattern in section_patterns:
            matches = re.finditer(pattern, text)
            section_headers.extend([(m.start(), m.group(1).strip()) for m in matches])
        
        # Sort sections by position in document
        section_headers.sort(key=lambda x: x[0])
        
        # Extract content between sections
        for i in range(len(section_headers)):
            start = section_headers[i][0]
            end = section_headers[i + 1][0] if i + 1 < len(section_headers) else len(text)
            section_title = section_headers[i][1]
            section_content = text[start:end].strip()
            sections[section_title] = section_content
            
        return sections 