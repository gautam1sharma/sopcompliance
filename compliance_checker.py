import re
from typing import Dict, List, Tuple
import json
import os

class ComplianceChecker:
    def __init__(self):
        self.standards = self._load_iso_standards()
        
    def _load_iso_standards(self) -> Dict:
        """Load ISO 27002 standards from JSON file."""
        standards_path = os.path.join('iso_standards', 'iso27002.json')
        try:
            with open(standards_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return basic structure if file doesn't exist
            return {
                "5.1": "Information security policies",
                "5.2": "Information security roles and responsibilities",
                "6.1": "Internal organization",
                "6.2": "Mobile device policy",
                "7.1": "Human resource security",
                "7.2": "During employment",
                "7.3": "Termination and change of employment",
                "8.1": "Asset management",
                "8.2": "Information classification",
                "8.3": "Media handling",
                "9.1": "Access control",
                "9.2": "User access management",
                "9.3": "User responsibilities",
                "9.4": "System and application access control",
                "10.1": "Cryptographic controls",
                "11.1": "Physical and environmental security",
                "12.1": "Operational security",
                "13.1": "Communications security",
                "14.1": "System acquisition, development and maintenance",
                "15.1": "Supplier relationships",
                "16.1": "Incident management",
                "17.1": "Business continuity management",
                "18.1": "Compliance"
            }
    
    def check_compliance(self, content: str) -> Dict:
        """Check document content against ISO 27002 standards."""
        results = {
            'compliance_score': 0,
            'total_controls': len(self.standards),
            'matched_controls': 0,
            'details': []
        }
        
        # Convert content to lowercase for case-insensitive matching
        content_lower = content.lower()
        
        for control_id, control_info in self.standards.items():
            if isinstance(control_info, dict):
                control_name = control_info.get('name', '')
            else:
                control_name = control_info
            # Create search patterns for the control
            patterns = self._generate_search_patterns(control_id, control_name)
            
            # Check if any pattern matches
            matches = []
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    matches.append(pattern)
            
            # Calculate score for this control
            control_score = len(matches) / len(patterns) if patterns else 0
            
            results['details'].append({
                'control_id': control_id,
                'control_name': control_name,
                'score': control_score,
                'matches': matches,
                'status': 'Compliant' if control_score > 0.5 else 'Non-compliant'
            })
            
            if control_score > 0.5:
                results['matched_controls'] += 1
        
        # Calculate overall compliance score
        results['compliance_score'] = (results['matched_controls'] / results['total_controls']) * 100
        
        return results
    
    def _generate_search_patterns(self, control_id: str, control_name: str) -> List[str]:
        """Generate search patterns for a given control."""
        patterns = []
        
        # Add control ID pattern
        patterns.append(rf'\b{control_id}\b')
        
        # Add control name pattern
        words = control_name.lower().split()
        if len(words) > 2:
            # Use trigrams for longer control names
            for i in range(len(words) - 2):
                pattern = r'\b' + r'\s+'.join(words[i:i+3]) + r'\b'
                patterns.append(pattern)
        else:
            # Use full control name for shorter ones
            patterns.append(r'\b' + r'\s+'.join(words) + r'\b')
        
        return patterns 