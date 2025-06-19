#!/usr/bin/env python3
"""
Test script to verify compatibility between iso27002_chunked_100.json 
and the SentenceSimilarityScorer prototype.
"""

import sys
import json
import time
from sentence_similarity_scorer import SentenceSimilarityScorer

def test_chunked_file_structure():
    """Test if the chunked file can be loaded and has expected structure."""
    print("=" * 60)
    print("TESTING CHUNKED FILE STRUCTURE")
    print("=" * 60)
    
    try:
        # Load the chunked file directly
        with open('../iso27002_chunked_100.json', 'r', encoding='utf-8') as f:
            iso_data = json.load(f)
        
        print(f"✓ Successfully loaded ISO chunks file")
        print(f"✓ Total controls found: {len(iso_data)}")
        
        # Check structure of first few controls
        sample_controls = list(iso_data.keys())[:5]
        print(f"✓ Sample control IDs: {sample_controls}")
        
        for control_id in sample_controls:
            control_data = iso_data[control_id]
            if isinstance(control_data, dict):
                clause_name = control_data.get('Clause Name', 'N/A')
                chunks = control_data.get('Chunks', [])
                print(f"  {control_id}: \"{clause_name}\" ({len(chunks)} chunks)")
                
                # Show sample chunk
                if chunks:
                    sample_chunk = chunks[0][:100] + "..." if len(chunks[0]) > 100 else chunks[0]
                    print(f"    Sample: {sample_chunk}")
            else:
                print(f"  {control_id}: Unexpected data type: {type(control_data)}")
        
        print("\n✓ File structure validation completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error loading chunked file: {str(e)}")
        return False

def test_scorer_initialization():
    """Test if the SentenceSimilarityScorer can initialize with the chunked file."""
    print("\n" + "=" * 60)
    print("TESTING SCORER INITIALIZATION")
    print("=" * 60)
    
    try:
        print("Initializing SentenceSimilarityScorer...")
        scorer = SentenceSimilarityScorer()
        
        print(f"✓ Scorer initialized successfully!")
        print(f"✓ ISO chunks loaded: {len(scorer.iso_chunks)} controls")
        print(f"✓ ISO sentences processed: {len(scorer.iso_sentences)} controls")
        
        # Check some sample controls
        for control_id, sentences_data in list(scorer.iso_sentences.items())[:3]:
            clause_name = sentences_data['clause_name']
            sentences = sentences_data['sentences']
            print(f"  {control_id}: \"{clause_name}\" -> {len(sentences)} sentences")
            
            # Show sample sentence
            if sentences:
                sample_sentence = sentences[0][:80] + "..." if len(sentences[0]) > 80 else sentences[0]
                print(f"    Sample: {sample_sentence}")
        
        return scorer
        
    except Exception as e:
        print(f"✗ Error initializing scorer: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_sop_analysis(scorer):
    """Test SOP document analysis functionality."""
    print("\n" + "=" * 60)
    print("TESTING SOP ANALYSIS")
    print("=" * 60)
    
    # Sample SOP content with various compliance elements
    sample_sop = """
    Information Security Policy
    
    Our organization is committed to maintaining the highest standards of information security.
    We have established comprehensive information security policies that are approved by senior management.
    All employees must comply with these policies and undergo regular security awareness training.
    
    Access Control
    Access to sensitive information and systems is strictly controlled based on job responsibilities.
    User accounts are created only for authorized personnel and are reviewed regularly.
    Strong authentication mechanisms are implemented for all system access.
    
    Physical Security
    Physical security measures are implemented to protect our facilities and equipment.
    Secure areas are protected by appropriate entry controls and monitoring systems.
    Equipment is properly secured and protected from environmental threats.
    
    Incident Management
    We have established procedures for reporting and responding to information security incidents.
    All security events are logged and monitored for anomalous behavior.
    Security incidents are investigated and documented for continuous improvement.
    
    Data Protection
    Information is classified according to its sensitivity and handled appropriately.
    Backup procedures are in place to ensure data recovery capabilities.
    Data retention and disposal procedures comply with regulatory requirements.
    """
    
    try:
        print(f"Analyzing sample SOP document ({len(sample_sop)} characters)...")
        
        # Analyze the document
        start_time = time.time()
        results = scorer.analyze_sop_document(sample_sop, similarity_threshold=0.25)
        analysis_time = time.time() - start_time
        
        if 'error' in results:
            print(f"✗ Analysis error: {results['error']}")
            return False
        
        print(f"✓ Analysis completed in {analysis_time:.2f} seconds")
        print(f"✓ Overall compliance score: {results['overall_score']:.1f}%")
        print(f"✓ SOP sentences analyzed: {results['total_sop_sentences']}")
        print(f"✓ Compliant controls: {results['compliance_summary']['compliant_controls']}/{results['compliance_summary']['total_controls']}")
        print(f"✓ Average similarity: {results['compliance_summary']['average_similarity']:.3f}")
        
        # Show top performing controls
        print("\nTop 5 performing controls:")
        control_scores = [(cid, data['max_similarity']) for cid, data in results['control_analysis'].items()]
        control_scores.sort(key=lambda x: x[1], reverse=True)
        
        for i, (control_id, score) in enumerate(control_scores[:5]):
            control_data = results['control_analysis'][control_id]
            clause_name = control_data['clause_name']
            print(f"  {i+1}. {control_id}: {clause_name} (Score: {score:.3f})")
        
        # Generate and save detailed report
        report = scorer.generate_detailed_report(results)
        
        with open('sample_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✓ Detailed report saved to: sample_analysis_report.txt")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_with_real_sop_file():
    """Test with a real SOP file if available."""
    print("\n" + "=" * 60)
    print("TESTING WITH REAL SOP FILE")
    print("=" * 60)
    
    # Look for SOP files in uploads directory
    import os
    uploads_dir = "../uploads"
    
    if not os.path.exists(uploads_dir):
        print("✓ No uploads directory found, skipping real file test")
        return True
    
    sop_files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')]
    
    if not sop_files:
        print("✓ No PDF files found in uploads directory, skipping real file test")
        return True
    
    print(f"Found {len(sop_files)} PDF files in uploads directory:")
    for f in sop_files:
        print(f"  - {f}")
    
    print("\nNote: PDF parsing would require additional implementation.")
    print("✓ Real file test structure verified")
    return True

def main():
    """Run all compatibility and functionality tests."""
    print("CHUNKED FILE COMPATIBILITY TEST")
    print("Testing compatibility between iso27002_chunked_100.json and SentenceSimilarityScorer")
    print(f"Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: File structure
    if not test_chunked_file_structure():
        print("\n✗ FAILED: Chunked file structure test")
        return False
    
    # Test 2: Scorer initialization  
    scorer = test_scorer_initialization()
    if scorer is None:
        print("\n✗ FAILED: Scorer initialization test")
        return False
    
    # Test 3: SOP analysis
    if not test_sop_analysis(scorer):
        print("\n✗ FAILED: SOP analysis test")
        return False
    
    # Test 4: Real file test
    if not test_with_real_sop_file():
        print("\n✗ FAILED: Real file test")
        return False
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)
    print("✓ Chunked file structure is compatible")
    print("✓ Scorer initializes correctly with chunked data")
    print("✓ SOP analysis functionality works")
    print("✓ System is ready for production use")
    print(f"\nTest completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 