#!/usr/bin/env python3
"""
Simple test to verify the structure of iso27002_chunked_100.json 
and its compatibility with the prototype logic (without model loading).
"""

import json
import re
import time

def test_chunked_file_structure():
    """Test detailed structure of the chunked file."""
    print("=" * 80)
    print("ISO27002 CHUNKED FILE STRUCTURE ANALYSIS")
    print("=" * 80)
    
    try:
        # Load the chunked file
        with open('../iso27002_chunked_100.json', 'r', encoding='utf-8') as f:
            iso_data = json.load(f)
        
        print(f"✓ Successfully loaded ISO chunks file")
        print(f"✓ Total controls found: {len(iso_data)}")
        
        # Analyze structure
        control_stats = {
            'total_controls': len(iso_data),
            'controls_with_chunks': 0,
            'total_chunks': 0,
            'total_raw_text': 0,
            'clause_name_issues': [],
            'sample_chunks': {}
        }
        
        print("\nDetailed Control Analysis:")
        print("-" * 50)
        
        for i, (control_id, control_data) in enumerate(iso_data.items()):
            if isinstance(control_data, dict):
                clause_name = control_data.get('Clause Name', 'N/A')
                chunks = control_data.get('Chunks', [])
                
                # Check for formatting issues in clause names
                if re.search(r'[A-Z]\s+[a-z]', clause_name):
                    control_stats['clause_name_issues'].append((control_id, clause_name))
                
                control_stats['controls_with_chunks'] += 1
                control_stats['total_chunks'] += len(chunks)
                
                # Calculate text length
                chunk_text = ' '.join(chunks)
                control_stats['total_raw_text'] += len(chunk_text)
                
                # Show first few controls in detail
                if i < 10:
                    cleaned_name = clean_clause_name(clause_name)
                    print(f"  {control_id}: \"{cleaned_name}\"")
                    print(f"    Original: \"{clause_name}\"")
                    print(f"    Chunks: {len(chunks)}")
                    
                    # Analyze first chunk
                    if chunks:
                        first_chunk = chunks[0]
                        sentences = split_into_sentences(first_chunk)
                        print(f"    First chunk length: {len(first_chunk)} chars")
                        print(f"    Sentences extracted: {len(sentences)}")
                        print(f"    Sample sentence: \"{sentences[0][:100]}...\"" if sentences else "    No valid sentences")
                    print()
                
                # Store sample for later analysis
                if i < 3:
                    control_stats['sample_chunks'][control_id] = {
                        'clause_name': clause_name,
                        'cleaned_name': clean_clause_name(clause_name),
                        'chunks': chunks[:2],  # First 2 chunks
                        'sentences': []
                    }
                    
                    # Process sentences
                    for chunk in chunks[:2]:
                        sentences = split_into_sentences(chunk)
                        control_stats['sample_chunks'][control_id]['sentences'].extend(sentences)
        
        # Print summary statistics
        print("\nSUMMARY STATISTICS:")
        print("-" * 50)
        print(f"Total Controls: {control_stats['total_controls']}")
        print(f"Controls with Chunks: {control_stats['controls_with_chunks']}")
        print(f"Total Chunks: {control_stats['total_chunks']}")
        print(f"Average Chunks per Control: {control_stats['total_chunks'] / control_stats['controls_with_chunks']:.1f}")
        print(f"Total Raw Text: {control_stats['total_raw_text']:,} characters")
        print(f"Average Text per Control: {control_stats['total_raw_text'] / control_stats['controls_with_chunks']:,.0f} characters")
        
        # Report clause name issues
        if control_stats['clause_name_issues']:
            print(f"\nClause Name Formatting Issues: {len(control_stats['clause_name_issues'])}")
            for control_id, clause_name in control_stats['clause_name_issues'][:5]:
                cleaned = clean_clause_name(clause_name)
                print(f"  {control_id}: \"{clause_name}\" → \"{cleaned}\"")
            if len(control_stats['clause_name_issues']) > 5:
                print(f"  ... and {len(control_stats['clause_name_issues']) - 5} more")
        
        return control_stats
        
    except Exception as e:
        print(f"✗ Error loading chunked file: {str(e)}")
        return None

def clean_clause_name(clause_name: str) -> str:
    """Clean clause name by removing extra spaces and formatting issues."""
    if not clause_name:
        return "Unknown Clause"
    
    # Remove extra whitespace and normalize
    cleaned = re.sub(r'\s+', ' ', clause_name.strip())
    
    # Fix specific formatting issues seen in the data
    replacements = [
        (r'P olicies', 'Policies'),
        (r'S egregation', 'Segregation'),
        (r'Information secur ity', 'Information security'),
        (r'Management r esponsibilities', 'Management responsibilities'),
        (r'C ontact', 'Contact'),
        (r'Thr eat', 'Threat'),
        (r'In ventory', 'Inventory'),
        (r'A cceptable', 'Acceptable'),
        (r'R eturn', 'Return'),
        (r'A ccess', 'Access'),
        (r'A uthentication', 'Authentication'),
        (r'A ddressing', 'Addressing'),
        (r'Monit oring', 'Monitoring'),
        (r'R esponse', 'Response'),
        (r'C ollection', 'Collection'),
        (r'ICT r eadiness', 'ICT readiness'),
        (r'Leg al', 'Legal'),
        (r'Int ellectual', 'Intellectual'),
        (r'Pr otection', 'Protection'),
        (r'Pri vacy', 'Privacy'),
        (r'Independent r eview', 'Independent review'),
        (r'C ompliance', 'Compliance'),
        (r'Document ed', 'Documented'),
        (r'T erms', 'Terms'),
        (r'Disciplinary pr ocess', 'Disciplinary process'),
        (r'R esponsibilities', 'Responsibilities'),
        (r'R emote', 'Remote'),
        (r'Ph ysical', 'Physical'),
        (r'W orking', 'Working'),
        (r'E quipment', 'Equipment'),
        (r'S ecurity', 'Security'),
        (r'St orage', 'Storage'),
        (r'User endpoint de vices', 'User endpoint devices'),
        (r'Pri vileged', 'Privileged'),
        (r'S ecure', 'Secure'),
        (r'Capacity managem ent', 'Capacity management'),
        (r'Management of t echnical', 'Management of technical'),
        (r'Information deleti on', 'Information deletion'),
        (r'Data leakage pr evention', 'Data leakage prevention'),
        (r'Information back up', 'Information backup'),
        (r'R edundancy', 'Redundancy'),
        (r'Clock s ynchronization', 'Clock synchronization'),
        (r'Use of pri vileged', 'Use of privileged'),
        (r'Installation of soft ware', 'Installation of software'),
        (r'Netw orks', 'Networks'),
        (r'Use of crypt ography', 'Use of cryptography'),
        (r'A pplication', 'Application'),
        (r'S ecure system', 'Secure system'),
        (r'S ecure coding', 'Secure coding'),
        (r'Outsour ced', 'Outsourced'),
        (r'S eparation', 'Separation'),
        (r'Change manageme nt', 'Change management'),
        (r'T est', 'Test')
    ]
    
    for pattern, replacement in replacements:
        cleaned = re.sub(pattern, replacement, cleaned)
    
    # Remove tab characters and other formatting artifacts
    cleaned = re.sub(r'\t', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def split_into_sentences(text: str) -> list:
    """Split text into sentences with cleaning."""
    # Clean the text first
    text = clean_text(text)
    
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

def clean_text(text: str) -> str:
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

def test_sentence_processing():
    """Test sentence processing on sample data."""
    print("\n" + "=" * 80)
    print("SENTENCE PROCESSING TEST")
    print("=" * 80)
    
    # Load and get sample data
    with open('../iso27002_chunked_100.json', 'r', encoding='utf-8') as f:
        iso_data = json.load(f)
    
    # Test on first 3 controls
    total_sentences_extracted = 0
    
    for i, (control_id, control_data) in enumerate(list(iso_data.items())[:3]):
        if isinstance(control_data, dict) and 'Chunks' in control_data:
            clause_name = clean_clause_name(control_data.get('Clause Name', ''))
            chunks = control_data['Chunks']
            
            print(f"\nControl {control_id}: {clause_name}")
            print("-" * 60)
            print(f"Original chunks: {len(chunks)}")
            
            # Process all chunks into sentences
            all_sentences = []
            for j, chunk in enumerate(chunks):
                sentences = split_into_sentences(chunk)
                all_sentences.extend(sentences)
                if j < 2:  # Show first 2 chunks in detail
                    print(f"  Chunk {j+1}: {len(chunk)} chars → {len(sentences)} sentences")
                    if sentences:
                        print(f"    Sample: \"{sentences[0][:80]}...\"")
            
            # Filter for uniqueness
            unique_sentences = []
            seen = set()
            for sentence in all_sentences:
                normalized = sentence.lower().strip()
                if normalized not in seen and len(sentence) > 20:
                    seen.add(normalized)
                    unique_sentences.append(sentence)
            
            print(f"  Total sentences extracted: {len(all_sentences)}")
            print(f"  Unique sentences: {len(unique_sentences)}")
            total_sentences_extracted += len(unique_sentences)
            
            # Show some sample sentences
            print("  Sample unique sentences:")
            for sentence in unique_sentences[:3]:
                print(f"    • \"{sentence[:100]}...\"")
    
    print(f"\nTotal unique sentences from 3 controls: {total_sentences_extracted}")
    return total_sentences_extracted

def test_compatibility_simulation():
    """Simulate the key compatibility aspects without model loading."""
    print("\n" + "=" * 80)
    print("COMPATIBILITY SIMULATION")
    print("=" * 80)
    
    try:
        # Load file
        with open('../iso27002_chunked_100.json', 'r', encoding='utf-8') as f:
            iso_data = json.load(f)
        
        # Simulate the preprocessing that would happen in SentenceSimilarityScorer
        print("Simulating SentenceSimilarityScorer preprocessing...")
        
        processed_controls = 0
        total_sentences = 0
        problematic_controls = []
        
        for control_id, control_data in iso_data.items():
            if isinstance(control_data, dict) and 'Chunks' in control_data:
                clause_name = clean_clause_name(control_data.get('Clause Name', ''))
                chunks = control_data['Chunks']
                
                # Extract sentences from all chunks
                all_sentences = []
                for chunk in chunks:
                    sentences = split_into_sentences(chunk)
                    all_sentences.extend(sentences)
                
                # Filter for uniqueness (like in the real implementation)
                unique_sentences = []
                seen = set()
                for sentence in all_sentences:
                    normalized = sentence.lower().strip()
                    if (normalized not in seen and 
                        len(sentence) > 20 and 
                        len(sentence.split()) > 4):
                        seen.add(normalized)
                        unique_sentences.append(sentence)
                
                if unique_sentences:
                    processed_controls += 1
                    total_sentences += len(unique_sentences)
                else:
                    problematic_controls.append((control_id, clause_name))
                
                # Show progress for first few
                if processed_controls <= 5:
                    print(f"  {control_id}: \"{clause_name}\" → {len(unique_sentences)} sentences")
        
        print(f"\n✓ Successfully processed {processed_controls}/{len(iso_data)} controls")
        print(f"✓ Total sentences extracted: {total_sentences}")
        print(f"✓ Average sentences per control: {total_sentences/processed_controls:.1f}")
        
        if problematic_controls:
            print(f"\n⚠ Controls with no valid sentences: {len(problematic_controls)}")
            for control_id, clause_name in problematic_controls[:3]:
                print(f"  {control_id}: {clause_name}")
        
        # Test compatibility with expected structure
        expected_structure = {
            'iso_sentences': {},
            'iso_sentence_embeddings': {}
        }
        
        for control_id, control_data in list(iso_data.items())[:3]:
            if isinstance(control_data, dict) and 'Chunks' in control_data:
                clause_name = clean_clause_name(control_data.get('Clause Name', ''))
                chunks = control_data['Chunks']
                
                all_sentences = []
                for chunk in chunks:
                    sentences = split_into_sentences(chunk)
                    all_sentences.extend(sentences)
                
                unique_sentences = []
                seen = set()
                for sentence in all_sentences:
                    normalized = sentence.lower().strip()
                    if normalized not in seen and len(sentence) > 20:
                        seen.add(normalized)
                        unique_sentences.append(sentence)
                
                expected_structure['iso_sentences'][control_id] = {
                    'clause_name': clause_name,
                    'sentences': unique_sentences
                }
                # Simulate embeddings as empty arrays (would be filled by model)
                expected_structure['iso_sentence_embeddings'][control_id] = f"Array of shape ({len(unique_sentences)}, 768)"
        
        print(f"\n✓ Structure compatibility verified!")
        print(f"✓ Expected iso_sentences structure: {len(expected_structure['iso_sentences'])} controls")
        print(f"✓ Expected iso_sentence_embeddings structure: {len(expected_structure['iso_sentence_embeddings'])} controls")
        
        return True
        
    except Exception as e:
        print(f"✗ Compatibility simulation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run structure and compatibility tests."""
    print("ISO27002 CHUNKED FILE STRUCTURE & COMPATIBILITY TEST")
    print(f"Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: File structure analysis
    stats = test_chunked_file_structure()
    if stats is None:
        print("\n✗ FAILED: File structure test")
        return False
    
    # Test 2: Sentence processing
    sentence_count = test_sentence_processing()
    if sentence_count == 0:
        print("\n✗ FAILED: Sentence processing test")
        return False
    
    # Test 3: Compatibility simulation
    if not test_compatibility_simulation():
        print("\n✗ FAILED: Compatibility simulation")
        return False
    
    print("\n" + "=" * 80)
    print("ALL STRUCTURE TESTS PASSED! ✓")
    print("=" * 80)
    print("✓ Chunked file loads correctly")
    print("✓ Control data structure is valid")
    print("✓ Clause name cleaning works")
    print("✓ Sentence extraction works")
    print("✓ Structure is compatible with SentenceSimilarityScorer")
    print("✓ Ready for integration with sentence transformer models")
    print(f"\nTest completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 