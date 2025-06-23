import re
import json
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import time

class SentenceSimilarityScorer:
    """
    Enhanced sentence-by-sentence similarity scorer for SOP compliance checking.
    Compares each sentence in ISO chunks with each sentence in SOP files.
    """
    
    def __init__(self, model_name: str = 'all-roberta-large-v1'):
        """
        Initialize the scorer with a sentence transformer model.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        print(f"Loading sentence transformer model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully!")
        
        # Load ISO chunks
        self.iso_chunks = self._load_iso_chunks()
        print(f"Loaded {len(self.iso_chunks)} ISO control sections")
        
        # Preprocess ISO chunks into sentences
        self._preprocess_iso_chunks()
        
    def _load_iso_chunks(self) -> Dict:
        """Load ISO 27002 chunked data from JSON file."""
        try:
            with open('../iso27002_chunked_100.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: ISO chunks file not found, using fallback data")
            return self._get_fallback_iso_data()
    
    def _get_fallback_iso_data(self) -> Dict:
        """Provide fallback ISO data if main file is not available."""
        return {
            "5.1": {
                "Clause Name": "Policies for information security",
                "Chunks": [
                    "Information security policy and topic-specific policies should be defined, approved by management.",
                    "Management should require all personnel to apply information security in accordance with policies.",
                    "The organization should establish and maintain contact with relevant authorities."
                ]
            },
            "5.2": {
                "Clause Name": "Information security roles and responsibilities", 
                "Chunks": [
                    "Information security roles and responsibilities should be defined and allocated according to organizational needs.",
                    "Conflicting duties and conflicting areas of responsibility should be segregated."
                ]
            }
        }
    
    def _preprocess_iso_chunks(self):
        """Preprocess ISO chunks into individual sentences and create embeddings."""
        print("Preprocessing ISO chunks into sentences...")
        self.iso_sentences = {}
        self.iso_sentence_embeddings = {}
        
        for control_id, control_data in self.iso_chunks.items():
            if isinstance(control_data, dict) and 'Chunks' in control_data:
                clause_name = self._clean_clause_name(control_data.get('Clause Name', ''))
                chunks = control_data['Chunks']
                
                # Extract sentences from all chunks
                all_sentences = []
                for chunk in chunks:
                    sentences = self._split_into_sentences(chunk)
                    all_sentences.extend(sentences)
                
                # Remove duplicates and filter meaningful sentences
                unique_sentences = self._filter_sentences(all_sentences)
                
                # Store sentences and create embeddings
                self.iso_sentences[control_id] = {
                    'clause_name': clause_name,
                    'sentences': unique_sentences
                }
                
                if unique_sentences:
                    print(f"  Control {control_id}: {len(unique_sentences)} sentences")
                    # Create embeddings for all sentences
                    embeddings = self.model.encode(unique_sentences)
                    self.iso_sentence_embeddings[control_id] = embeddings
                else:
                    print(f"  Control {control_id}: No valid sentences found")
                    self.iso_sentence_embeddings[control_id] = np.array([])
        
        total_sentences = sum(len(data['sentences']) for data in self.iso_sentences.values())
        print(f"ISO chunk preprocessing completed! Total sentences: {total_sentences}")
    
    def _clean_clause_name(self, clause_name: str) -> str:
        """Clean clause name by removing extra spaces and formatting issues."""
        if not clause_name:
            return "Unknown Clause"
        
        # Remove extra whitespace and normalize
        cleaned = re.sub(r'\s+', ' ', clause_name.strip())
        
        # Fix specific formatting issues seen in the data
        cleaned = re.sub(r'P olicies', 'Policies', cleaned)
        cleaned = re.sub(r'S egregation', 'Segregation', cleaned) 
        cleaned = re.sub(r'Information secur ity', 'Information security', cleaned)
        cleaned = re.sub(r'Management r esponsibilities', 'Management responsibilities', cleaned)
        cleaned = re.sub(r'C ontact', 'Contact', cleaned)
        cleaned = re.sub(r'Thr eat', 'Threat', cleaned)
        cleaned = re.sub(r'In ventory', 'Inventory', cleaned)
        cleaned = re.sub(r'A cceptable', 'Acceptable', cleaned)
        cleaned = re.sub(r'R eturn', 'Return', cleaned)
        cleaned = re.sub(r'A ccess', 'Access', cleaned)
        cleaned = re.sub(r'A uthentication', 'Authentication', cleaned)
        cleaned = re.sub(r'A ddressing', 'Addressing', cleaned)
        cleaned = re.sub(r'Monit oring', 'Monitoring', cleaned)
        cleaned = re.sub(r'R esponse', 'Response', cleaned)
        cleaned = re.sub(r'C ollection', 'Collection', cleaned)
        cleaned = re.sub(r'ICT r eadiness', 'ICT readiness', cleaned)
        cleaned = re.sub(r'Leg al', 'Legal', cleaned)
        cleaned = re.sub(r'Int ellectual', 'Intellectual', cleaned)
        cleaned = re.sub(r'Pr otection', 'Protection', cleaned)
        cleaned = re.sub(r'Pri vacy', 'Privacy', cleaned)
        cleaned = re.sub(r'Independent r eview', 'Independent review', cleaned)
        cleaned = re.sub(r'C ompliance', 'Compliance', cleaned)
        cleaned = re.sub(r'Document ed', 'Documented', cleaned)
        cleaned = re.sub(r'T erms', 'Terms', cleaned)
        cleaned = re.sub(r'Disciplinary pr ocess', 'Disciplinary process', cleaned)
        cleaned = re.sub(r'R esponsibilities', 'Responsibilities', cleaned)
        cleaned = re.sub(r'R emote', 'Remote', cleaned)
        cleaned = re.sub(r'Ph ysical', 'Physical', cleaned)
        cleaned = re.sub(r'W orking', 'Working', cleaned)
        cleaned = re.sub(r'E quipment', 'Equipment', cleaned)
        cleaned = re.sub(r'S ecurity', 'Security', cleaned)
        cleaned = re.sub(r'St orage', 'Storage', cleaned)
        cleaned = re.sub(r'User endpoint de vices', 'User endpoint devices', cleaned)
        cleaned = re.sub(r'Pri vileged', 'Privileged', cleaned)
        cleaned = re.sub(r'S ecure', 'Secure', cleaned)
        cleaned = re.sub(r'Capacity managem ent', 'Capacity management', cleaned)
        cleaned = re.sub(r'Management of t echnical', 'Management of technical', cleaned)
        cleaned = re.sub(r'Information deleti on', 'Information deletion', cleaned)
        cleaned = re.sub(r'Data leakage pr evention', 'Data leakage prevention', cleaned)
        cleaned = re.sub(r'Information back up', 'Information backup', cleaned)
        cleaned = re.sub(r'R edundancy', 'Redundancy', cleaned)
        cleaned = re.sub(r'Monit oring', 'Monitoring', cleaned)
        cleaned = re.sub(r'Clock s ynchronization', 'Clock synchronization', cleaned)
        cleaned = re.sub(r'Use of pri vileged', 'Use of privileged', cleaned)
        cleaned = re.sub(r'Installation of soft ware', 'Installation of software', cleaned)
        cleaned = re.sub(r'Netw orks', 'Networks', cleaned)
        cleaned = re.sub(r'S egregation', 'Segregation', cleaned)
        cleaned = re.sub(r'Use of crypt ography', 'Use of cryptography', cleaned)
        cleaned = re.sub(r'A pplication', 'Application', cleaned)
        cleaned = re.sub(r'S ecure system', 'Secure system', cleaned)
        cleaned = re.sub(r'S ecure coding', 'Secure coding', cleaned)
        cleaned = re.sub(r'Outsour ced', 'Outsourced', cleaned)
        cleaned = re.sub(r'S eparation', 'Separation', cleaned)
        cleaned = re.sub(r'Change manageme nt', 'Change management', cleaned)
        cleaned = re.sub(r'T est', 'Test', cleaned)
        
        # Remove tab characters and other formatting artifacts
        cleaned = re.sub(r'\t', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Advanced sentence splitting with better handling of technical documents.
        
        Args:
            text: Input text to split into sentences
            
        Returns:
            List of individual sentences
        """
        # Clean the text first
        text = self._clean_text(text)
        
        # Split on sentence endings but preserve context
        sentences = re.split(r'[.!?]+\s+(?=[A-Z])', text)
        
        # Also split on "type Information" patterns which seem to be chunk separators
        all_sentences = []
        for sentence in sentences:
            # Split further on "type Information" patterns
            parts = re.split(r'\s+type\s+Information\s+', sentence)
            all_sentences.extend(parts)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in all_sentences:
            sentence = sentence.strip()
            # Keep sentences that are meaningful (not just numbers or single words)
            if len(sentence) > 20 and len(sentence.split()) > 4:
                # Remove artifacts like "type Information" repetitions
                sentence = re.sub(r'\btype\s+Information\b', '', sentence)
                sentence = re.sub(r'\s+', ' ', sentence).strip()
                # Remove sentences that are just control references or metadata
                if not re.match(r'^(name\s+)*according to ISO/IEC', sentence, re.IGNORECASE):
                    if sentence and len(sentence) > 15:
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
        # Remove repeated "type Information" patterns
        text = re.sub(r'\btype\s+Information\b', '', text)
        return text.strip()
    
    def _filter_sentences(self, sentences: List[str]) -> List[str]:
        """
        Filter out duplicate and low-quality sentences.
        
        Args:
            sentences: List of sentences to filter
            
        Returns:
            Filtered list of unique, high-quality sentences
        """
        unique_sentences = []
        seen = set()
        
        for sentence in sentences:
            # Normalize for comparison
            normalized = sentence.lower().strip()
            
            # Skip if too short, too long, or already seen
            if (len(normalized) < 20 or 
                len(normalized) > 800 or 
                normalized in seen or
                len(sentence.split()) < 5):
                continue
            
            # Skip sentences with too many repeated words
            words = normalized.split()
            if len(set(words)) / len(words) < 0.4:  # Less than 40% unique words
                continue
            
            # Skip sentences that are mostly metadata or control references
            if re.search(r'according to iso|name name|according to ISO/IEC', sentence, re.IGNORECASE):
                continue
                
            # Skip sentences that start with common metadata patterns
            if re.match(r'^(To\s+ensure|To\s+protect|To\s+maintain|To\s+reduce|To\s+prevent)', sentence):
                # These are good - purpose statements, keep them
                pass
            elif re.match(r'^(name\s+)+', sentence, re.IGNORECASE):
                continue
            
            seen.add(normalized)
            unique_sentences.append(sentence)
        
        return unique_sentences
    
    def analyze_sop_document(self, sop_content: str, 
                           similarity_threshold: float = 0.3,
                           top_matches_per_sentence: int = 3) -> Dict[str, Any]:
        """
        Analyze a SOP document by comparing each sentence with ISO sentences.
        
        Args:
            sop_content: Content of the SOP document
            similarity_threshold: Minimum similarity score to consider a match
            top_matches_per_sentence: Number of top matches to return per sentence
            
        Returns:
            Detailed analysis results with sentence-by-sentence scores
        """
        print("Starting SOP document analysis...")
        start_time = time.time()
        
        # Split SOP content into sentences
        sop_sentences = self._split_into_sentences(sop_content)
        sop_sentences = self._filter_sentences(sop_sentences)
        
        if not sop_sentences:
            return {
                'error': 'No valid sentences found in SOP document',
                'analysis_time': time.time() - start_time
            }
        
        print(f"Found {len(sop_sentences)} sentences in SOP document")
        
        # Create embeddings for SOP sentences
        print("Creating SOP sentence embeddings...")
        sop_embeddings = self.model.encode(sop_sentences)
        
        # Initialize results structure
        results = {
            'overall_score': 0.0,
            'total_sop_sentences': len(sop_sentences),
            'control_analysis': {},
            'sentence_analysis': [],
            'compliance_summary': {
                'compliant_controls': 0,
                'total_controls': len(self.iso_sentences),
                'average_similarity': 0.0
            },
            'analysis_time': 0.0
        }
        
        all_similarities = []
        
        # Analyze each ISO control
        for control_id, iso_data in self.iso_sentences.items():
            iso_sentences_list = iso_data['sentences']
            clause_name = iso_data['clause_name']
            
            if not iso_sentences_list or control_id not in self.iso_sentence_embeddings:
                print(f"Skipping control {control_id}: No sentences or embeddings")
                continue
            
            iso_embeddings = self.iso_sentence_embeddings[control_id]
            
            # Calculate similarities between all SOP and ISO sentences for this control
            control_similarities = cosine_similarity(sop_embeddings, iso_embeddings)
            
            # Analyze this control
            control_result = self._analyze_control_similarity(
                control_id, clause_name, sop_sentences, iso_sentences_list,
                control_similarities, similarity_threshold, top_matches_per_sentence
            )
            
            results['control_analysis'][control_id] = control_result
            all_similarities.extend(control_result['sentence_matches'])
            
            # Check if control is compliant
            if control_result['max_similarity'] > similarity_threshold:
                results['compliance_summary']['compliant_controls'] += 1
        
        # Calculate overall metrics
        if all_similarities:
            results['compliance_summary']['average_similarity'] = np.mean(all_similarities)
            results['overall_score'] = (results['compliance_summary']['compliant_controls'] / 
                                      results['compliance_summary']['total_controls']) * 100
        
        results['analysis_time'] = time.time() - start_time
        print(f"Analysis completed in {results['analysis_time']:.2f} seconds")
        
        return results
    
    def _analyze_control_similarity(self, control_id: str, clause_name: str,
                                   sop_sentences: List[str], iso_sentences: List[str],
                                   similarities: np.ndarray, threshold: float,
                                   top_matches: int) -> Dict[str, Any]:
        """
        Analyze similarity between SOP sentences and a specific ISO control.
        
        Args:
            control_id: ISO control identifier
            clause_name: Name of the ISO clause
            sop_sentences: List of SOP sentences
            iso_sentences: List of ISO sentences for this control
            similarities: Similarity matrix (sop_sentences x iso_sentences)
            threshold: Similarity threshold for matches
            top_matches: Number of top matches to include
            
        Returns:
            Analysis results for this control
        """
        # Find best matches for each SOP sentence
        sentence_matches = []
        
        for sop_idx, sop_sentence in enumerate(sop_sentences):
            sentence_similarities = similarities[sop_idx]
            
            # Get top matches above threshold
            top_indices = np.argsort(sentence_similarities)[-top_matches:][::-1]
            
            matches = []
            for iso_idx in top_indices:
                similarity_score = sentence_similarities[iso_idx]
                if similarity_score > threshold:
                    matches.append({
                        'iso_sentence': iso_sentences[iso_idx],
                        'similarity_score': float(similarity_score),
                        'iso_sentence_index': int(iso_idx)
                    })
            
            if matches:  # Only include SOP sentences that have matches
                sentence_matches.append({
                    'sop_sentence': sop_sentence,
                    'sop_sentence_index': sop_idx,
                    'matches': matches,
                    'best_similarity': float(matches[0]['similarity_score'])
                })
        
        # Calculate control-level metrics
        all_scores = [match['best_similarity'] for match in sentence_matches]
        
        return {
            'control_id': control_id,
            'clause_name': clause_name,
            'total_iso_sentences': len(iso_sentences),
            'matching_sop_sentences': len(sentence_matches),
            'sentence_matches': [match['best_similarity'] for match in sentence_matches],
            'max_similarity': float(max(all_scores)) if all_scores else 0.0,
            'average_similarity': float(np.mean(all_scores)) if all_scores else 0.0,
            'coverage_percentage': (len(sentence_matches) / len(sop_sentences)) * 100,
            'detailed_matches': sentence_matches
        }
    
    def generate_detailed_report(self, analysis_results: Dict[str, Any],
                               min_similarity_for_report: float = 0.4) -> str:
        """
        Generate a detailed text report from analysis results.
        
        Args:
            analysis_results: Results from analyze_sop_document
            min_similarity_for_report: Minimum similarity to include in detailed report
            
        Returns:
            Formatted text report
        """
        if 'error' in analysis_results:
            return f"Analysis Error: {analysis_results['error']}"
        
        report = []
        report.append("="*80)
        report.append("SOP COMPLIANCE ANALYSIS REPORT")
        report.append("="*80)
        report.append("")
        
        # Overall summary
        summary = analysis_results['compliance_summary']
        report.append(f"Overall Compliance Score: {analysis_results['overall_score']:.1f}%")
        report.append(f"Compliant Controls: {summary['compliant_controls']}/{summary['total_controls']}")
        report.append(f"Average Similarity: {summary['average_similarity']:.3f}")
        report.append(f"Total SOP Sentences Analyzed: {analysis_results['total_sop_sentences']}")
        report.append(f"Analysis Time: {analysis_results['analysis_time']:.2f} seconds")
        report.append("")
        
        # Control-by-control analysis
        report.append("CONTROL-BY-CONTROL ANALYSIS:")
        report.append("-" * 50)
        
        for control_id, control_data in analysis_results['control_analysis'].items():
            report.append(f"\nControl {control_id}: {control_data['clause_name']}")
            report.append(f"  Max Similarity: {control_data['max_similarity']:.3f}")
            report.append(f"  Average Similarity: {control_data['average_similarity']:.3f}")
            report.append(f"  Coverage: {control_data['coverage_percentage']:.1f}% ({control_data['matching_sop_sentences']} matching sentences)")
            
            # Show top matches if similarity is high enough
            if control_data['max_similarity'] >= min_similarity_for_report:
                report.append("  Top Matches:")
                for match in control_data['detailed_matches'][:3]:  # Top 3 matches
                    if match['best_similarity'] >= min_similarity_for_report:
                        report.append(f"    • SOP: \"{match['sop_sentence'][:100]}...\"")
                        report.append(f"      ISO: \"{match['matches'][0]['iso_sentence'][:100]}...\"")
                        report.append(f"      Similarity: {match['best_similarity']:.3f}")
                        report.append("")
        
        return "\n".join(report)
    
    def batch_analyze_files(self, file_paths: List[str], 
                          output_dir: str = "analysis_results") -> Dict[str, Any]:
        """
        Analyze multiple SOP files in batch.
        
        Args:
            file_paths: List of file paths to analyze
            output_dir: Directory to save individual analysis results
            
        Returns:
            Batch analysis summary
        """
        os.makedirs(output_dir, exist_ok=True)
        
        batch_results = {
            'files_analyzed': 0,
            'total_files': len(file_paths),
            'results': {},
            'summary_stats': {
                'average_compliance_score': 0.0,
                'best_performing_file': '',
                'worst_performing_file': '',
                'total_analysis_time': 0.0
            }
        }
        
        all_scores = []
        
        for file_path in file_paths:
            try:
                print(f"\nAnalyzing file: {file_path}")
                
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Analyze the file
                analysis = self.analyze_sop_document(content)
                
                if 'error' not in analysis:
                    batch_results['results'][file_path] = analysis
                    all_scores.append(analysis['overall_score'])
                    batch_results['files_analyzed'] += 1
                    
                    # Save individual report
                    report = self.generate_detailed_report(analysis)
                    report_filename = os.path.join(output_dir, f"{os.path.basename(file_path)}_analysis.txt")
                    with open(report_filename, 'w', encoding='utf-8') as f:
                        f.write(report)
                    
                    batch_results['summary_stats']['total_analysis_time'] += analysis['analysis_time']
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {str(e)}")
                batch_results['results'][file_path] = {'error': str(e)}
        
        # Calculate summary statistics
        if all_scores:
            batch_results['summary_stats']['average_compliance_score'] = np.mean(all_scores)
            
            best_idx = np.argmax(all_scores)
            worst_idx = np.argmin(all_scores)
            
            file_list = [fp for fp, result in batch_results['results'].items() 
                        if 'error' not in result]
            
            if file_list:
                batch_results['summary_stats']['best_performing_file'] = file_list[best_idx]
                batch_results['summary_stats']['worst_performing_file'] = file_list[worst_idx]
        
        return batch_results


def main():
    """Example usage of the SentenceSimilarityScorer."""
    # Initialize the scorer
    scorer = SentenceSimilarityScorer()
    
    # Example SOP content
    example_sop = """
    Our organization has established comprehensive information security policies that are approved by management.
    All employees must comply with information security requirements and procedures.
    We conduct regular security awareness training for all personnel.
    Access to sensitive information is restricted based on job responsibilities.
    Physical security measures are implemented to protect our facilities and equipment.
    """
    
    # Analyze the example
    results = scorer.analyze_sop_document(example_sop)
    
    # Generate and print report
    report = scorer.generate_detailed_report(results)
    print(report)


if __name__ == "__main__":
    main() 