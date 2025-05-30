import re
import json
import os
import numpy as np
from typing import Dict, List, Tuple, Set
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticComplianceChecker:
    def __init__(self):
        self.standards = self._load_iso_standards()
        
        # Initialize the sentence transformer model
        print("Loading sentence transformer model...")
        self.model = SentenceTransformer('all-roberta-large-v1')
        print("Model loaded successfully!")
        
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
        
        # Create embeddings for control descriptions and keywords
        self._precompute_control_embeddings()
        
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
    
    def _precompute_control_embeddings(self):
        """Precompute embeddings for all control descriptions and keywords."""
        print("Precomputing control embeddings...")
        self.control_embeddings = {}
        
        for control_id, control_info in self.standards.items():
            if isinstance(control_info, dict):
                control_name = control_info.get('name', '')
                control_description = control_info.get('description', '')
            else:
                control_name = control_info
                control_description = ""
            
            # Combine control name, description, and keywords
            keywords = self.control_keywords.get(control_id, [])
            combined_text = f"{control_name} {control_description} {' '.join(keywords)}"
            
            # Create embedding
            embedding = self.model.encode([combined_text])
            self.control_embeddings[control_id] = {
                'embedding': embedding[0],
                'text': combined_text,
                'name': control_name,
                'keywords': keywords
            }
        print("Control embeddings precomputed successfully!")
    
    def extract_semantic_features(self, content: str) -> Dict[str, List[str]]:
        """Extract semantic features from document content using sentence transformers."""
        # Clean and prepare content
        content = self._clean_text(content)
        sentences = self._advanced_sentence_split(content)
        
        features = defaultdict(list)
        
        # Create embeddings for document sentences
        if sentences:
            sentence_embeddings = self.model.encode(sentences)
            
            # Define feature categories with their representative sentences
            feature_categories = {
                'policies': [
                    "Information security policy and procedures",
                    "Policy management and governance",
                    "Security standards and guidelines"
                ],
                'access_control': [
                    "User access management and authentication",
                    "Authorization and permission controls",
                    "Identity and access management"
                ],
                'asset_management': [
                    "Asset classification and inventory",
                    "Data protection and handling",
                    "Information asset management"
                ],
                'training': [
                    "Security awareness and training",
                    "Employee education programs",
                    "Competency development"
                ],
                'incident_management': [
                    "Security incident response",
                    "Breach management and reporting",
                    "Event monitoring and detection"
                ]
            }
            
            # Create embeddings for feature categories
            for category, descriptions in feature_categories.items():
                category_embeddings = self.model.encode(descriptions)
                
                # Find sentences similar to each category
                for i, sentence_embedding in enumerate(sentence_embeddings):
                    similarities = cosine_similarity(
                        [sentence_embedding], 
                        category_embeddings
                    )[0]
                    
                    # If any similarity is above threshold, add to category
                    if max(similarities) > 0.3:  # Threshold for semantic similarity
                        features[category].append(sentences[i])
        
        return dict(features)
    
    def _advanced_sentence_split(self, text: str) -> List[str]:
        """Advanced sentence splitting with better handling of technical documents."""
        # Split on sentence endings but preserve context
        sentences = re.split(r'[.!?]+\s+(?=[A-Z])', text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            # Keep sentences that are meaningful (not just numbers or single words)
            if len(sentence) > 20 and len(sentence.split()) > 3:
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
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
        """Enhanced compliance checking with semantic analysis using sentence transformers."""
        results = {
            'compliance_score': 0,
            'total_controls': len(self.standards),
            'matched_controls': 0,
            'details': [],
            'semantic_analysis': {},
            'method': 'Sentence Transformers (RoBERTa-Large)'
        }
        
        # Extract semantic features
        semantic_features = self.extract_semantic_features(content)
        results['semantic_analysis'] = {k: len(v) for k, v in semantic_features.items()}
        
        # Clean content for processing
        content_clean = self._clean_text(content)
        sentences = self._advanced_sentence_split(content_clean)
        
        if not sentences:
            return results
        
        # Create embeddings for document sentences
        print("Creating document embeddings...")
        sentence_embeddings = self.model.encode(sentences)
        
        for control_id, control_info in self.standards.items():
            if isinstance(control_info, dict):
                control_name = control_info.get('name', '')
            else:
                control_name = control_info
            
            # Calculate semantic similarity score
            score = self._calculate_semantic_score(
                control_id, 
                sentences, 
                sentence_embeddings, 
                semantic_features
            )
            
            results['details'].append({
                'control_id': control_id,
                'control_name': control_name,
                'score': float(score),  # Convert numpy float to Python float
                'status': 'Compliant' if score > 0.25 else 'Non-compliant',  # Lower threshold for semantic matching
                'evidence': self._find_semantic_evidence(control_id, sentences, sentence_embeddings)
            })
            
            if score > 0.25:
                results['matched_controls'] += 1
        
        # Calculate overall compliance score
        results['compliance_score'] = float((results['matched_controls'] / results['total_controls']) * 100)
        
        print("Semantic compliance analysis completed!")
        return results
    
    def _calculate_semantic_score(self, control_id: str, sentences: List[str], 
                                 sentence_embeddings: np.ndarray, semantic_features: Dict) -> float:
        """Calculate compliance score using semantic similarity."""
        if control_id not in self.control_embeddings:
            return 0.0
        
        control_embedding = self.control_embeddings[control_id]['embedding']
        
        # Calculate similarities between control and document sentences
        similarities = cosine_similarity([control_embedding], sentence_embeddings)[0]
        
        # Get top similarities
        top_similarities = np.sort(similarities)[-5:]  # Top 5 matches
        
        # Different scoring components
        scores = []
        
        # 1. Maximum similarity score (40% weight)
        max_similarity = np.max(similarities) if len(similarities) > 0 else 0
        scores.append(max_similarity * 0.4)
        
        # 2. Average of top similarities (30% weight)
        avg_top_similarity = np.mean(top_similarities) if len(top_similarities) > 0 else 0
        scores.append(avg_top_similarity * 0.3)
        
        # 3. Semantic feature matching (30% weight)
        semantic_score = self._semantic_match(control_id, semantic_features)
        scores.append(semantic_score * 0.3)
        
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
    
    def _find_semantic_evidence(self, control_id: str, sentences: List[str], 
                               sentence_embeddings: np.ndarray) -> List[str]:
        """Find specific evidence for a control using semantic similarity."""
        if control_id not in self.control_embeddings or len(sentences) == 0:
            return []
        
        control_embedding = self.control_embeddings[control_id]['embedding']
        
        # Calculate similarities
        similarities = cosine_similarity([control_embedding], sentence_embeddings)[0]
        
        # Get indices of top similar sentences
        top_indices = np.argsort(similarities)[-3:][::-1]  # Top 3, in descending order
        
        evidence = []
        for idx in top_indices:
            if similarities[idx] > 0.2:  # Only include if similarity is above threshold
                sentence = sentences[idx]
                # Truncate long sentences
                if len(sentence) > 200:
                    sentence = sentence[:200] + "..."
                evidence.append(sentence)
        
        return evidence 