import re
import json
import os
from typing import Dict, List, Tuple, Set
from collections import defaultdict

class EnhancedComplianceChecker:
    def __init__(self):
        self.standards = self._load_iso_standards()
        
        # Extended keyword mapping for ISO 27002 controls
        self.control_keywords = {
            "5.1": ["policy", "policies", "information security", "governance", "management approval", "document"],
            "5.2": ["roles", "responsibilities", "confidentiality", "agreement", "authorities", "contact"],
            "6.1": ["organization", "internal", "framework", "management", "segregation", "duties"],
            "6.2": ["mobile", "device", "bring your own", "byod", "smartphone", "tablet", "registration"],
            "7.1": ["human resource", "hr", "screening", "background check", "employment", "hiring"],
            "7.2": ["training", "awareness", "education", "disciplinary", "employee", "contractor"],
            "7.3": ["termination", "resignation", "return assets", "access removal", "exit process"],
            "8.1": ["asset", "inventory", "classification", "ownership", "acceptable use", "protection"],
            "8.2": ["classification", "labeling", "handling", "confidential", "public", "restricted"],
            "8.3": ["media", "removable", "disposal", "transfer", "secure deletion", "usb", "cd", "dvd"],
            "9.1": ["access control", "authentication", "authorization", "user management", "privilege"],
            "9.2": ["user registration", "provisioning", "deprovisioning", "access review", "privilege management"],
            "9.3": ["password", "authentication", "user responsibility", "login", "session"],
            "9.4": ["system access", "application", "secure logon", "utility programs", "source code"],
            "10.1": ["cryptography", "encryption", "key management", "digital signature", "pki"],
            "11.1": ["physical security", "perimeter", "entry control", "secure area", "environmental"],
            "12.1": ["operational", "procedures", "change management", "capacity", "backup", "logging"],
            "13.1": ["network", "communication", "segregation", "firewall", "monitoring", "transfer"],
            "14.1": ["system development", "security requirements", "testing", "vulnerability", "application security"],
            "15.1": ["supplier", "vendor", "third party", "outsourcing", "service delivery", "contract"],
            "16.1": ["incident", "event", "reporting", "response", "forensics", "evidence", "breach"],
            "17.1": ["business continuity", "disaster recovery", "availability", "resilience", "backup"],
            "18.1": ["compliance", "legal", "regulatory", "audit", "intellectual property", "privacy", "gdpr"]
        }
        
    def _load_iso_standards(self) -> Dict:
        """Load ISO 27002 standards from JSON file."""
        standards_path = os.path.join('iso_standards', 'iso27002.json')
        try:
            with open(standards_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "5.1": {"name": "Information security policies"},
                "5.2": {"name": "Information security roles and responsibilities"},
                "6.1": {"name": "Internal organization"},
                "6.2": {"name": "Mobile device policy"},
                "7.1": {"name": "Human resource security"},
                "7.2": {"name": "During employment"},
                "7.3": {"name": "Termination and change of employment"},
                "8.1": {"name": "Asset management"},
                "8.2": {"name": "Information classification"},
                "8.3": {"name": "Media handling"},
                "9.1": {"name": "Access control"},
                "9.2": {"name": "User access management"},
                "9.3": {"name": "User responsibilities"},
                "9.4": {"name": "System and application access control"},
                "10.1": {"name": "Cryptographic controls"},
                "11.1": {"name": "Physical and environmental security"},
                "12.1": {"name": "Operational security"},
                "13.1": {"name": "Communications security"},
                "14.1": {"name": "System acquisition, development and maintenance"},
                "15.1": {"name": "Supplier relationships"},
                "16.1": {"name": "Incident management"},
                "17.1": {"name": "Business continuity management"},
                "18.1": {"name": "Compliance"}
            }
    
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
            'total_controls': len(self.standards),
            'matched_controls': 0,
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
            
            results['details'].append({
                'control_id': control_id,
                'control_name': control_name,
                'score': float(score),  # Ensure Python float type
                'status': 'Compliant' if score > 0.3 else 'Non-compliant',  # Lower threshold for real-world docs
                'evidence': self._find_evidence(control_id, content_lower)
            })
            
            if score > 0.3:
                results['matched_controls'] += 1
        
        # Calculate overall compliance score
        results['compliance_score'] = float((results['matched_controls'] / results['total_controls']) * 100)
        
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
        # Map control IDs to semantic feature categories
        semantic_mapping = {
            "5.1": ["policies"],
            "5.2": ["policies"],
            "9.1": ["access_control"],
            "9.2": ["access_control"],
            "9.3": ["access_control"],
            "9.4": ["access_control"],
            "8.1": ["asset_management"],
            "8.2": ["asset_management"],
            "7.2": ["training"],
            "16.1": ["incident_management"]
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