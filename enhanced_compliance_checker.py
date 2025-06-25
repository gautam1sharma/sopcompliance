import re
import json
import os
from typing import Dict, List, Tuple, Set
from collections import defaultdict

class EnhancedComplianceChecker:
    def __init__(self):
        self.standards = self._load_iso_standards()
        
        # Load keywords from ISO standards file
        self.control_keywords = self._load_control_keywords()
        
    def _load_iso_standards(self) -> Dict:
        """Load ISO 27002 standards from JSON file."""
        standards_path = os.path.join('iso_standards', 'iso27002.json')
        try:
            with open(standards_path, 'r') as f:
                data = json.load(f)
                # Extract only the control data (excluding metadata)
                return {k: v for k, v in data.items() if k != 'metadata'}
        except FileNotFoundError:
            # Fallback with basic controls if file not found
            print("Warning: ISO standards file not found, using basic fallback controls")
            return self._get_fallback_standards()
    
    def _get_fallback_standards(self) -> Dict:
        """Provide fallback standards if main file is not available."""
        return {
            "5.1": {"name": "Information security policies", "keywords": ["policy", "policies", "information security"]},
            "5.2": {"name": "Information security roles and responsibilities", "keywords": ["roles", "responsibilities"]},
            "6.1": {"name": "Screening", "keywords": ["screening", "background", "employment"]},
            "7.1": {"name": "Physical security perimeters", "keywords": ["physical security", "perimeter"]},
            "8.1": {"name": "User endpoint devices", "keywords": ["endpoint", "devices", "user"]}
        }
    
    def _load_control_keywords(self) -> Dict[str, List[str]]:
        """Load control keywords from the standards data."""
        control_keywords = {}
        for control_id, control_data in self.standards.items():
            if isinstance(control_data, dict) and 'keywords' in control_data:
                control_keywords[control_id] = control_data['keywords']
            else:
                # Fallback: generate keywords from control name
                control_name = control_data.get('name', '') if isinstance(control_data, dict) else str(control_data)
                control_keywords[control_id] = self._generate_keywords_from_name(control_name)
        
        return control_keywords
    
    def _generate_keywords_from_name(self, name: str) -> List[str]:
        """Generate basic keywords from control name."""
        words = name.lower().split()
        # Remove common stop words and generate variations
        stop_words = {'of', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords
    
    def extract_semantic_features(self, content: str) -> Dict[str, List[str]]:
        """Extract semantic features from document content using simple string processing."""
        # Clean and prepare content
        content = self._clean_text(content)
        sentences = self._simple_sentence_split(content)
        
        features = defaultdict(list)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Look for policy-related patterns
            if any(word in sentence_lower for word in ['policy', 'procedure', 'guideline', 'standard']):
                features['policies'].append(sentence)
            
            # Look for access control patterns
            if any(word in sentence_lower for word in ['access', 'authorization', 'authentication', 'permission']):
                features['access_control'].append(sentence)
            
            # Look for asset management patterns
            if any(word in sentence_lower for word in ['asset', 'inventory', 'classification', 'data']):
                features['asset_management'].append(sentence)
            
            # Look for security awareness patterns
            if any(word in sentence_lower for word in ['training', 'awareness', 'education', 'employee']):
                features['training'].append(sentence)
            
            # Look for incident management patterns
            if any(word in sentence_lower for word in ['incident', 'breach', 'response', 'report']):
                features['incident_management'].append(sentence)
        
        return dict(features)
    
    def _simple_sentence_split(self, text: str) -> List[str]:
        """Simple sentence splitting without NLTK."""
        # Split on sentence endings
        sentences = re.split(r'[.!?]+', text)
        # Clean and filter
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _clean_text(self, text: str) -> str:
        """Enhanced text cleaning for real-world documents."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep sentence structure
        text = re.sub(r'[^\w\s.,;:!?\-\'\"()]', ' ', text)
        # Fix common OCR errors
        text = re.sub(r'\b(\w)\s+(\w)\b', r'\1\2', text)
        return text.strip()
    
    def check_compliance(self, content: str) -> Dict:
        """Enhanced compliance checking with semantic analysis."""
        results = {
            'compliance_score': 0,
            'summary': {
                'total_controls': len(self.standards),
                'matched_controls': 0,
                'high_confidence': 0,
                'medium_confidence': 0,
                'low_confidence': 0,
                'non_compliant': 0,
            },
            'details': [],
            'semantic_analysis': {},
            'method': 'Enhanced Analysis (String-based)'
        }
        
        # Extract semantic features
        semantic_features = self.extract_semantic_features(content)
        results['semantic_analysis'] = {k: len(v) for k, v in semantic_features.items()}
        
        # Convert content to lowercase for matching
        content_lower = content.lower()
        
        for control_id, control_info in self.standards.items():
            if isinstance(control_info, dict):
                control_name = control_info.get('name', '')
            else:
                control_name = control_info
            
            # Enhanced matching using multiple approaches
            score = self._calculate_enhanced_score(control_id, control_name, content_lower, semantic_features)
            
            # Determine confidence level and status
            if score > 0.6:
                status = 'High Confidence'
                confidence = 'high'
                results['summary']['high_confidence'] += 1
            elif score > 0.4:
                status = 'Medium Confidence'
                confidence = 'medium'
                results['summary']['medium_confidence'] += 1
            elif score > 0.25:
                status = 'Low Confidence'
                confidence = 'low'
                results['summary']['low_confidence'] += 1
            else:
                status = 'Non-compliant'
                confidence = 'none'
                results['summary']['non_compliant'] += 1
            
            results['details'].append({
                'id': control_id,
                'name': control_name,
                'score': float(score),
                'status': status,
                'confidence': confidence,
                'rationale': '\n'.join(self._find_evidence(control_id, content_lower))
            })
            
            if score > 0.25:
                results['summary']['matched_controls'] += 1
        
        # Calculate overall compliance score
        total_controls = results['summary']['total_controls']
        matched_controls = results['summary']['matched_controls']
        if total_controls > 0:
            results['compliance_score'] = float((matched_controls / total_controls) * 100)
        else:
            results['compliance_score'] = 0.0
        
        return results
    
    def _calculate_enhanced_score(self, control_id: str, control_name: str, content: str, semantic_features: Dict) -> float:
        """Calculate compliance score using multiple matching techniques."""
        scores = []
        
        # 1. Keyword matching
        keywords = self.control_keywords.get(control_id, [])
        keyword_matches = sum(1 for keyword in keywords if keyword.lower() in content)
        keyword_score = min(keyword_matches / max(len(keywords), 1), 1.0)
        scores.append(keyword_score * 0.4)  # 40% weight
        
        # 2. Control name matching
        control_words = control_name.lower().split()
        control_matches = sum(1 for word in control_words if word in content)
        control_score = control_matches / max(len(control_words), 1)
        scores.append(control_score * 0.3)  # 30% weight
        
        # 3. Semantic feature matching
        semantic_score = self._semantic_match(control_id, semantic_features)
        scores.append(semantic_score * 0.3)  # 30% weight
        
        return sum(scores)
    
    def _semantic_match(self, control_id: str, semantic_features: Dict) -> float:
        """Match controls based on semantic features."""
        # Map control IDs to semantic feature categories based on ISO 27002:2022
        semantic_mapping = {
            # Organizational controls (5.x) - Policies and governance
            "5.1": ["policies"], "5.2": ["policies"], "5.3": ["policies"], "5.4": ["policies"],
            "5.5": ["policies"], "5.6": ["policies"], "5.7": ["policies"], "5.8": ["policies"],
            "5.9": ["asset_management"], "5.10": ["asset_management"], "5.11": ["asset_management"],
            "5.12": ["asset_management"], "5.13": ["asset_management"], "5.14": ["asset_management"],
            "5.15": ["access_control"], "5.16": ["access_control"], "5.17": ["access_control"], "5.18": ["access_control"],
            "5.19": ["policies"], "5.20": ["policies"], "5.21": ["policies"], "5.22": ["policies"], "5.23": ["policies"],
            "5.24": ["incident_management"], "5.25": ["incident_management"], "5.26": ["incident_management"], 
            "5.27": ["incident_management"], "5.28": ["incident_management"],
            "5.29": ["policies"], "5.30": ["policies"], "5.31": ["policies"], "5.32": ["policies"],
            "5.33": ["policies"], "5.34": ["policies"], "5.35": ["policies"], "5.36": ["policies"], "5.37": ["policies"],
            
            # People controls (6.x) - Training and HR
            "6.1": ["training"], "6.2": ["training"], "6.3": ["training"], "6.4": ["training"],
            "6.5": ["training"], "6.6": ["policies"], "6.7": ["policies"], "6.8": ["incident_management"],
            
            # Physical controls (7.x) - Physical security
            "7.1": ["policies"], "7.2": ["policies"], "7.3": ["policies"], "7.4": ["policies"],
            "7.5": ["policies"], "7.6": ["policies"], "7.7": ["asset_management"], "7.8": ["policies"],
            "7.9": ["asset_management"], "7.10": ["asset_management"], "7.11": ["policies"], 
            "7.12": ["policies"], "7.13": ["policies"], "7.14": ["asset_management"],
            
            # Technological controls (8.x) - Technical controls
            "8.1": ["access_control"], "8.2": ["access_control"], "8.3": ["access_control"], "8.4": ["access_control"],
            "8.5": ["access_control"], "8.6": ["policies"], "8.7": ["policies"], "8.8": ["policies"],
            "8.9": ["policies"], "8.10": ["asset_management"], "8.11": ["asset_management"], "8.12": ["policies"],
            "8.13": ["asset_management"], "8.14": ["policies"], "8.15": ["incident_management"], "8.16": ["incident_management"],
            "8.17": ["policies"], "8.18": ["access_control"], "8.19": ["policies"], "8.20": ["policies"],
            "8.21": ["policies"], "8.22": ["policies"], "8.23": ["access_control"], "8.24": ["policies"],
            "8.25": ["policies"], "8.26": ["policies"], "8.27": ["policies"], "8.28": ["policies"],
            "8.29": ["policies"], "8.30": ["policies"], "8.31": ["policies"], "8.32": ["policies"],
            "8.33": ["policies"], "8.34": ["policies"]
        }
        
        relevant_categories = semantic_mapping.get(control_id, [])
        if not relevant_categories:
            return 0.0
        
        total_evidence = sum(len(semantic_features.get(cat, [])) for cat in relevant_categories)
        return min(total_evidence / 10.0, 1.0)  # Normalize to 0-1
    
    def _find_evidence(self, control_id: str, content: str) -> List[str]:
        """Find specific evidence for a control in the document."""
        evidence = []
        keywords = self.control_keywords.get(control_id, [])
        
        sentences = content.split('.')
        for sentence in sentences:
            if any(keyword.lower() in sentence.lower() for keyword in keywords):
                evidence.append(sentence.strip()[:200] + "..." if len(sentence) > 200 else sentence.strip())
        
        return evidence[:3]  # Return top 3 pieces of evidence 