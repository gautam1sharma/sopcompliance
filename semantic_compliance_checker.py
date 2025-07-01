import re
import json
import os
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
from sentence_transformers import SentenceTransformer, CrossEncoder
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
        
        print("Loading sentence transformer models...")
        self.bi_encoder_name = 'Qwen/Qwen3-Embedding-0.6B'
        self.cross_encoder_name = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
        self.bi_encoder = SentenceTransformer(self.bi_encoder_name, trust_remote_code=True)
        self.cross_encoder = CrossEncoder(self.cross_encoder_name)
        print("Models loaded successfully!")
        
        self.control_keywords = self._load_control_keywords()
        self._precompute_control_embeddings()
        
    def _load_iso_standards(self) -> Dict:
        cached_standards = get_cached_iso_standards()
        if cached_standards:
            print("Loaded ISO standards from cache.")
            return cached_standards
        
        print("Loading ISO standards from JSON file...")
        standards_path = os.path.join('iso_standards', 'iso27002.json')
        try:
            with open(standards_path, 'r') as f:
                data = json.load(f)
                standards = {k: v for k, v in data.items() if k != 'metadata'}
                cache_iso_standards(standards)
                print("Cached ISO standards for future use.")
                return standards
        except FileNotFoundError:
            print("Warning: ISO standards file not found, using basic fallback controls")
            return self._get_fallback_standards()

    def _get_fallback_standards(self) -> Dict:
        return {
            "5.1": {"name": "Information security policies", "keywords": ["policy", "policies", "information security"]},
            "5.2": {"name": "Information security roles and responsibilities", "keywords": ["roles", "responsibilities"]},
        }

    def _load_control_keywords(self) -> Dict[str, List[str]]:
        control_keywords = {}
        for control_id, control_data in self.standards.items():
            if isinstance(control_data, dict) and 'keywords' in control_data:
                control_keywords[control_id] = control_data['keywords']
            else:
                control_name = control_data.get('name', '') if isinstance(control_data, dict) else str(control_data)
                control_keywords[control_id] = self._generate_keywords_from_name(control_name)
        return control_keywords

    def _generate_keywords_from_name(self, name: str) -> List[str]:
        words = name.lower().split()
        stop_words = {'of', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
        return [word for word in words if word not in stop_words and len(word) > 2]

    def _precompute_control_embeddings(self):
        print("Precomputing control embeddings...")
        self.control_embeddings = {}
        for control_id, control_info in self.standards.items():
            control_name = control_info.get('name', '')
            control_description = control_info.get('description', '')
            keywords = self.control_keywords.get(control_id, [])
            combined_text = f"{control_name} {control_description} {' '.join(keywords)}"
            
            text_hash = get_content_hash(combined_text)
            cached_embedding = get_cached_model_embeddings(self.bi_encoder_name, text_hash)

            if cached_embedding is not None:
                embedding = cached_embedding
            else:
                embedding = self.bi_encoder.encode([combined_text])
                cache_model_embeddings(self.bi_encoder_name, text_hash, embedding)

            self.control_embeddings[control_id] = {
                'embedding': embedding[0],
                'text': combined_text,
                'name': control_name,
                'keywords': keywords
            }
        print("Control embeddings precomputed successfully!")

    def _remove_boilerplate(self, text: str) -> str:
        patterns = [
            r"^(confidential|internal use only|property of).*",
            r"^page\s+\d+\s+of\s+\d+",
            r"^document\s+version:\s+\d+",
            r"^revision\s+history",
            r"^author(s)?:.*",
            r"^date\s+of\s+issue:.*",
        ]
        
        cleaned_text = text
        for pattern in patterns:
            cleaned_text = re.sub(pattern, "", cleaned_text, flags=re.IGNORECASE | re.MULTILINE)
            
        return cleaned_text.strip()

    def _create_text_chunks(self, text: str, chunk_size: int = 3, overlap: int = 1) -> List[str]:
        sentences = re.split(r'[.!?]+\s+(?=[A-Z])', text)
        
        chunks = []
        for i in range(0, len(sentences) - chunk_size + 1, chunk_size - overlap):
            chunk = " ".join(sentences[i:i+chunk_size])
            if len(chunk.split()) > 10:
                chunks.append(chunk)
        
        return chunks

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,;:!?\-(")]', ' ', text)
        text = re.sub(r'\b(\w)\s+(\w)\b', r'\1\2', text)
        return text.strip()

    def check_compliance(self, content: str) -> Dict:
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
            'method': 'Hybrid Re-ranking (Bi-Encoder + Cross-Encoder)'
        }
        
        content_no_boilerplate = self._remove_boilerplate(content)
        content_clean = self._clean_text(content_no_boilerplate)
        chunks = self._create_text_chunks(content_clean)
        
        if not chunks:
            return results

        content_hash = get_content_hash(content_clean)
        chunk_embeddings = get_cached_document_embeddings(self.bi_encoder_name, content_hash)
        if chunk_embeddings is None:
            print("Creating document embeddings...")
            chunk_embeddings = self.bi_encoder.encode(chunks)
            cache_document_embeddings(self.bi_encoder_name, content_hash, chunk_embeddings)
        else:
            print("Loaded document embeddings from cache.")

        for control_id, control_info in self.standards.items():
            control_name = control_info.get('name', '')
            
            score, evidence = self._calculate_semantic_score(
                control_id, 
                chunks, 
                chunk_embeddings
            )
            
            if score > 0.8:
                status, confidence = 'High Confidence', 'high'
                results['summary']['high_confidence'] += 1
            elif score > 0.5:
                status, confidence = 'Medium Confidence', 'medium'
                results['summary']['medium_confidence'] += 1
            elif score > 0.3:
                status, confidence = 'Low Confidence', 'low'
                results['summary']['low_confidence'] += 1
            else:
                status, confidence = 'Non-compliant', 'none'
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
        
        total_controls = results['summary']['total_controls']
        matched_controls = results['summary']['matched_controls']
        if total_controls > 0:
            results['compliance_score'] = float((matched_controls / total_controls) * 100)
        
        print("Semantic compliance analysis completed!")
        return results

    def _calculate_semantic_score(self, control_id: str, chunks: List[str], 
                                 chunk_embeddings: np.ndarray) -> Tuple[float, List[str]]:
        if control_id not in self.control_embeddings:
            return 0.0, []
        
        control_embedding = self.control_embeddings[control_id]['embedding']
        control_text = self.control_embeddings[control_id]['text']

        # Stage 1: Fast Retrieval (Bi-Encoder)
        similarities = cosine_similarity(np.array([control_embedding]), chunk_embeddings)[0]
        top_k_indices = np.argsort(similarities)[-10:][::-1] # Get top 10 candidates

        if not top_k_indices.any():
            return 0.0, []

        # Stage 2: Accurate Re-ranking (Cross-Encoder)
        cross_encoder_pairs = [(control_text, chunks[i]) for i in top_k_indices]
        cross_encoder_scores = self.cross_encoder.predict(cross_encoder_pairs, convert_to_numpy=True)
        
        # Apply sigmoid scaling to normalize scores to a 0-1 range
        scaled_scores = 1 / (1 + np.exp(-cross_encoder_scores))
        
        # Combine scores and find the best match
        final_score = np.max(scaled_scores) if len(scaled_scores) > 0 else 0.0
        best_chunk_index = top_k_indices[np.argmax(scaled_scores)] if len(scaled_scores) > 0 else -1

        evidence = []
        if best_chunk_index != -1:
            evidence.append(f"(Score: {final_score:.2f}) {chunks[best_chunk_index]}")

        return final_score, evidence