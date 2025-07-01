import re
import json
import os
import numpy as np
from typing import Dict, List, Tuple, Set
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.cache_manager import (
    get_content_hash,
    cache_model_embeddings,
    get_cached_model_embeddings,
    cache_document_embeddings,
    get_cached_document_embeddings,
    cache_iso_standards,
    get_cached_iso_standards,
)

class SemanticComplianceChecker:
    def __init__(self):
        self.standards = self._load_iso_standards()
        
        # Initialize the sentence transformer model
        print("Loading sentence transformer model...")
        self.model_name = 'Qwen/Qwen3-Embedding-0.6B'
        self.model = SentenceTransformer(self.model_name, trust_remote_code=True)
        print("Model loaded successfully!")
        
        # Load keywords from ISO standards file
        self.control_keywords = self._load_control_keywords()
        
        # Create embeddings for control descriptions and keywords
        self._precompute_control_embeddings()
        
    def _load_iso_standards(self) -> Dict:
        """Load ISO 27002 standards from cache or JSON file."""
        # Try to load from cache first
        cached_standards = get_cached_iso_standards()
        if cached_standards:
            print("Loaded ISO standards from cache.")
            return cached_standards
        
        # If not in cache, load from JSON file
        print("Loading ISO standards from JSON file...")
        standards_path = os.path.join('iso_standards', 'iso27002.json')
        try:
            with open(standards_path, 'r') as f:
                data = json.load(f)
                standards = {k: v for k, v in data.items() if k != 'metadata'}
                
                # Cache the loaded standards
                cache_iso_standards(standards)
                print("Cached ISO standards for future use.")
                
                return standards
        except FileNotFoundError:
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
            
            # Check cache for embedding
            text_hash = get_content_hash(combined_text)
            cached_embedding = get_cached_model_embeddings(self.model_name, text_hash)

            if cached_embedding is not None:
                embedding = cached_embedding
            else:
                # Create embedding
                embedding = self.model.encode([combined_text])
                cache_model_embeddings(self.model_name, text_hash, embedding)

            self.control_embeddings[control_id] = {
                'embedding': embedding[0],
                'text': combined_text,
                'name': control_name,
                'keywords': keywords
            }
        print("Control embeddings precomputed successfully!")
    
    def extract_semantic_features(self, chunks: List[str], chunk_embeddings: np.ndarray) -> Dict[str, List[str]]:
        """Extract semantic features from document content using sentence transformers."""
        features = defaultdict(list)
        
        if not chunks:
            return dict(features)

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
            
            # Find chunks similar to each category
            for i, chunk_embedding in enumerate(chunk_embeddings):
                similarities = cosine_similarity(
                    np.expand_dims(chunk_embedding, axis=0), 
                    category_embeddings
                )[0]
                
                # If any similarity is above threshold, add to category
                if max(similarities) > 0.3:  # Threshold for semantic similarity
                    features[category].append(chunks[i])
        
        return dict(features)
    
    def _create_text_chunks(self, text: str, chunk_size: int = 3, overlap: int = 1) -> List[str]:
        """Create overlapping text chunks from the document."""
        sentences = re.split(r'[.!?]+\s+(?=[A-Z])', text)
        
        chunks = []
        for i in range(0, len(sentences) - chunk_size + 1, chunk_size - overlap):
            chunk = " ".join(sentences[i:i+chunk_size])
            if len(chunk.split()) > 10:  # Filter out very short chunks
                chunks.append(chunk)
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Enhanced text cleaning for real-world documents."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep sentence structure
        text = re.sub(r'[^\w\s.,;:!?\-\'"()]', ' ', text)
        # Fix common OCR errors
        text = re.sub(r'\b(\w)\s+(\w)\b', r'\1\2', text)
        return text.strip()

    def _remove_boilerplate(self, text: str) -> str:
        """Remove boilerplate text such as headers, footers, and revision tables."""
        # Patterns for common boilerplate content
        patterns = [
            r"(confidential|internal use only|property of).*",
            r"page\s+\d+\s+of\s+\d+",
            r"document\s+version:\s+\d+",
            r"revision\s+history",
            r"author(s)?:.*",
            r"date\s+of\s+issue:.*",
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)
            
        return text
    
    def check_compliance(self, content: str) -> Dict:
        """Enhanced compliance checking with semantic analysis using sentence transformers."""
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
            'method': 'Sentence Transformers (Qwen3-Embedding-0.6B) with Two-Stage Scoring'
        }
        
        # Clean content for processing
        content_no_boilerplate = self._remove_boilerplate(content)
        content_clean = self._clean_text(content_no_boilerplate)
        chunks = self._create_text_chunks(content_clean)
        
        if not chunks:
            return results

        # Get document embeddings (from cache or by encoding)
        content_hash = get_content_hash(content_clean)
        chunk_embeddings = get_cached_document_embeddings(self.model_name, content_hash)
        if chunk_embeddings is None:
            print("Creating document embeddings...")
            chunk_embeddings = self.model.encode(chunks)
            cache_document_embeddings(self.model_name, content_hash, chunk_embeddings)
        else:
            print("Loaded document embeddings from cache.")

        # Extract semantic features
        semantic_features = self.extract_semantic_features(chunks, chunk_embeddings)
        results['semantic_analysis'] = {k: len(v) for k, v in semantic_features.items()}
        
        for control_id, control_info in self.standards.items():
            if isinstance(control_info, dict):
                control_name = control_info.get('name', '')
            else:
                control_name = control_info
            
            # Calculate semantic similarity score
            score, evidence = self._calculate_semantic_score(
                control_id, 
                chunks, 
                chunk_embeddings, 
                semantic_features
            )
            
            # Determine confidence level and status
            if score > 0.7:
                status = 'High Confidence'
                confidence = 'high'
                results['summary']['high_confidence'] += 1
            elif score > 0.5:
                status = 'Medium Confidence'
                confidence = 'medium'
                results['summary']['medium_confidence'] += 1
            elif score > 0.3:
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
                'rationale': '\n'.join(evidence)
            })
            
            if score > 0.3:
                results['summary']['matched_controls'] += 1
        
        # Calculate overall compliance score
        total_controls = results['summary']['total_controls']
        matched_controls = results['summary']['matched_controls']
        if total_controls > 0:
            results['compliance_score'] = float((matched_controls / total_controls) * 100)
        else:
            results['compliance_score'] = 0.0
        
        print("Semantic compliance analysis completed!")
        return results
    
    def _calculate_semantic_score(self, control_id: str, chunks: List[str], 
                                 chunk_embeddings: np.ndarray, semantic_features: Dict) -> Tuple[float, List[str]]:
        """Calculate compliance score using a two-stage filtering and scoring model."""
        if control_id not in self.control_embeddings:
            return 0.0, []
        
        control_embedding = self.control_embeddings[control_id]['embedding']
        control_keywords = self.control_embeddings[control_id]['keywords']

        # --- Keyword Pre-filtering ---
        keyword_candidate_indices = []
        for i, chunk in enumerate(chunks):
            if any(keyword.lower() in chunk.lower() for keyword in control_keywords):
                keyword_candidate_indices.append(i)

        if not keyword_candidate_indices:
            return 0.0, []

        # Filter chunks and embeddings based on keyword matches
        keyword_filtered_chunks = [chunks[i] for i in keyword_candidate_indices]
        keyword_filtered_embeddings = chunk_embeddings[keyword_candidate_indices]
        
        # Calculate similarities between control and document chunks
        similarities = cosine_similarity(np.array([control_embedding]), keyword_filtered_embeddings)[0]
        
        # --- Stage 1: Filtering ---
        baseline_threshold = 0.3
        candidate_indices = np.where(similarities > baseline_threshold)[0]
        
        if len(candidate_indices) == 0:
            return 0.0, []
            
        candidate_similarities = similarities[candidate_indices]
        candidate_chunks = [chunks[i] for i in candidate_indices]

        # --- Stage 2: Scoring ---
        # 1. Maximum similarity score (primary factor)
        max_similarity = np.max(candidate_similarities)
        
        # 2. Density score (rewards multiple strong pieces of evidence)
        high_confidence_threshold = 0.6
        high_confidence_count = np.sum(candidate_similarities > high_confidence_threshold)
        density_score = min(high_confidence_count / 5.0, 1.0) # Normalize, capped at 5 pieces of evidence
        
        # 3. Semantic feature matching (contextual bonus)
        semantic_feature_score = self._semantic_match(control_id, semantic_features)
        
        # Combine scores: max_similarity is the main driver, density provides a boost
        score = (max_similarity * 0.7) + (density_score * 0.2) + (semantic_feature_score * 0.1)
        
        # Find evidence from the candidate chunks
        evidence = self._find_semantic_evidence(control_id, candidate_chunks, candidate_similarities)

        return min(score, 1.0), evidence
    
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
    
    def _find_semantic_evidence(self, control_id: str, chunks: List[str], 
                               similarities: np.ndarray) -> List[str]:
        """Find specific evidence for a control from candidate chunks."""
        if len(chunks) == 0:
            return []
        
        # Get indices of top similar chunks
        top_indices = np.argsort(similarities)[-3:][::-1]  # Top 3, in descending order
        
        evidence = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Only include if similarity is above threshold
                chunk = chunks[idx]
                # Truncate long chunks
                if len(chunk) > 300:
                    chunk = chunk[:300] + "..."
                evidence.append(chunk)
        
        return evidence