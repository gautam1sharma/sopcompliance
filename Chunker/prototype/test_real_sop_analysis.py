#!/usr/bin/env python3
"""
Real SOP Analysis Test: InformationSecurityPolicy-godfreyphillips.pdf
Test the SentenceSimilarityScorer prototype with a real SOP document.
"""

import sys
import os
import time
import json
from datetime import datetime

# Add parent directory to path to import the PDF parser
sys.path.append('..')
from pdf_parser import PDFParser
from sentence_similarity_scorer import SentenceSimilarityScorer

def extract_sop_content(pdf_path: str) -> str:
    """Extract text content from the SOP PDF file."""
    print(f"Extracting content from: {pdf_path}")
    
    try:
        parser = PDFParser(pdf_path)
        
        # Check if PDF is readable
        if not parser.is_pdf_loadable():
            raise Exception("PDF file is corrupted or cannot be loaded")
        
        # Extract text content
        content = parser.extract_text()
        
        if not content or len(content.strip()) < 100:
            raise Exception("Insufficient content extracted from PDF")
        
        print(f"✓ Successfully extracted {len(content)} characters from PDF")
        print(f"✓ Content preview: {content[:200]}...")
        
        return content
        
    except Exception as e:
        print(f"✗ Error extracting PDF content: {str(e)}")
        return None

def analyze_sop_with_prototype(content: str) -> dict:
    """Analyze the SOP content using the SentenceSimilarityScorer prototype."""
    print("\n" + "="*80)
    print("INITIALIZING SENTENCE SIMILARITY SCORER")
    print("="*80)
    
    try:
        # Initialize the scorer (this will download the model if needed)
        scorer = SentenceSimilarityScorer()
        
        print("\n" + "="*80)
        print("ANALYZING SOP DOCUMENT")
        print("="*80)
        
        # Run the analysis
        results = scorer.analyze_sop_document(
            content, 
            similarity_threshold=0.25,  # Lower threshold for comprehensive analysis
            top_matches_per_sentence=3
        )
        
        if 'error' in results:
            print(f"✗ Analysis error: {results['error']}")
            return None
        
        print(f"✓ Analysis completed successfully!")
        print(f"✓ Overall compliance score: {results['overall_score']:.1f}%")
        print(f"✓ Analysis time: {results['analysis_time']:.2f} seconds")
        
        return results
        
    except Exception as e:
        print(f"✗ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def generate_comprehensive_report(results: dict, content: str) -> str:
    """Generate a comprehensive analysis report."""
    
    if not results:
        return "Analysis failed - no results to report"
    
    report_lines = []
    
    # Header
    report_lines.append("="*100)
    report_lines.append("COMPREHENSIVE SOP COMPLIANCE ANALYSIS REPORT")
    report_lines.append("InformationSecurityPolicy-godfreyphillips.pdf vs ISO 27002 Controls")
    report_lines.append("="*100)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Executive Summary
    report_lines.append("EXECUTIVE SUMMARY")
    report_lines.append("-" * 50)
    summary = results['compliance_summary']
    report_lines.append(f"Overall Compliance Score: {results['overall_score']:.1f}%")
    report_lines.append(f"Compliant Controls: {summary['compliant_controls']}/{summary['total_controls']}")
    report_lines.append(f"Compliance Rate: {(summary['compliant_controls']/summary['total_controls']*100):.1f}%")
    report_lines.append(f"Average Similarity Score: {summary['average_similarity']:.3f}")
    report_lines.append(f"SOP Sentences Analyzed: {results['total_sop_sentences']}")
    report_lines.append(f"Analysis Processing Time: {results['analysis_time']:.2f} seconds")
    report_lines.append("")
    
    # Document Statistics
    report_lines.append("DOCUMENT STATISTICS")
    report_lines.append("-" * 50)
    report_lines.append(f"Document Length: {len(content):,} characters")
    report_lines.append(f"Estimated Pages: {len(content) // 2000}")  # Rough estimate
    report_lines.append(f"Sentences Extracted: {results['total_sop_sentences']}")
    report_lines.append(f"Average Sentence Length: {len(content) // results['total_sop_sentences']:.0f} characters")
    report_lines.append("")
    
    # Top Performing Controls
    control_scores = [(cid, data['max_similarity']) for cid, data in results['control_analysis'].items()]
    control_scores.sort(key=lambda x: x[1], reverse=True)
    
    report_lines.append("TOP 10 PERFORMING CONTROLS")
    report_lines.append("-" * 50)
    for i, (control_id, score) in enumerate(control_scores[:10]):
        control_data = results['control_analysis'][control_id]
        report_lines.append(f"{i+1:2d}. {control_id}: {control_data['clause_name']}")
        report_lines.append(f"    Max Similarity: {score:.3f} | Avg: {control_data['average_similarity']:.3f} | Coverage: {control_data['coverage_percentage']:.1f}%")
    report_lines.append("")
    
    # Bottom Performing Controls
    report_lines.append("BOTTOM 10 PERFORMING CONTROLS (Need Attention)")
    report_lines.append("-" * 50)
    for i, (control_id, score) in enumerate(control_scores[-10:]):
        control_data = results['control_analysis'][control_id]
        report_lines.append(f"{i+1:2d}. {control_id}: {control_data['clause_name']}")
        report_lines.append(f"    Max Similarity: {score:.3f} | Avg: {control_data['average_similarity']:.3f} | Coverage: {control_data['coverage_percentage']:.1f}%")
    report_lines.append("")
    
    # Detailed Control Analysis
    report_lines.append("DETAILED CONTROL-BY-CONTROL ANALYSIS")
    report_lines.append("-" * 50)
    
    # Group controls by performance
    excellent = []  # > 0.5
    good = []       # 0.35 - 0.5
    fair = []       # 0.25 - 0.35
    poor = []       # < 0.25
    
    for control_id, data in results['control_analysis'].items():
        score = data['max_similarity']
        if score > 0.5:
            excellent.append((control_id, data))
        elif score > 0.35:
            good.append((control_id, data))
        elif score > 0.25:
            fair.append((control_id, data))
        else:
            poor.append((control_id, data))
    
    report_lines.append(f"EXCELLENT COMPLIANCE (>0.5): {len(excellent)} controls")
    for control_id, data in excellent[:5]:  # Show top 5
        report_lines.append(f"  • {control_id}: {data['clause_name']} (Score: {data['max_similarity']:.3f})")
    if len(excellent) > 5:
        report_lines.append(f"    ... and {len(excellent) - 5} more")
    report_lines.append("")
    
    report_lines.append(f"GOOD COMPLIANCE (0.35-0.5): {len(good)} controls")
    for control_id, data in good[:5]:  # Show top 5
        report_lines.append(f"  • {control_id}: {data['clause_name']} (Score: {data['max_similarity']:.3f})")
    if len(good) > 5:
        report_lines.append(f"    ... and {len(good) - 5} more")
    report_lines.append("")
    
    report_lines.append(f"FAIR COMPLIANCE (0.25-0.35): {len(fair)} controls")
    for control_id, data in fair[:5]:  # Show top 5
        report_lines.append(f"  • {control_id}: {data['clause_name']} (Score: {data['max_similarity']:.3f})")
    if len(fair) > 5:
        report_lines.append(f"    ... and {len(fair) - 5} more")
    report_lines.append("")
    
    report_lines.append(f"POOR COMPLIANCE (<0.25): {len(poor)} controls")
    for control_id, data in poor:  # Show all poor performing
        report_lines.append(f"  • {control_id}: {data['clause_name']} (Score: {data['max_similarity']:.3f})")
    report_lines.append("")
    
    # Evidence Examples
    report_lines.append("EVIDENCE EXAMPLES (Top Matches)")
    report_lines.append("-" * 50)
    
    # Show detailed evidence for top 3 performing controls
    for i, (control_id, score) in enumerate(control_scores[:3]):
        control_data = results['control_analysis'][control_id]
        report_lines.append(f"\n{i+1}. {control_id}: {control_data['clause_name']}")
        report_lines.append(f"   Max Similarity: {score:.3f}")
        
        if control_data['detailed_matches']:
            for j, match in enumerate(control_data['detailed_matches'][:2]):  # Top 2 matches
                if match['best_similarity'] > 0.3:
                    report_lines.append(f"   Match {j+1} (Similarity: {match['best_similarity']:.3f}):")
                    report_lines.append(f"     SOP: \"{match['sop_sentence'][:120]}...\"")
                    report_lines.append(f"     ISO: \"{match['matches'][0]['iso_sentence'][:120]}...\"")
                    report_lines.append("")
    
    # Recommendations
    report_lines.append("RECOMMENDATIONS")
    report_lines.append("-" * 50)
    
    compliance_rate = (summary['compliant_controls']/summary['total_controls']*100)
    
    if compliance_rate >= 80:
        report_lines.append("✓ EXCELLENT: Your SOP demonstrates strong ISO 27002 compliance!")
        report_lines.append("  - Consider minor improvements in lower-scoring controls")
        report_lines.append("  - Review and strengthen weak areas identified above")
    elif compliance_rate >= 60:
        report_lines.append("△ GOOD: Your SOP shows good compliance but has room for improvement")
        report_lines.append("  - Focus on addressing poor compliance controls")
        report_lines.append("  - Consider adding more detailed procedures for low-scoring areas")
    elif compliance_rate >= 40:
        report_lines.append("⚠ FAIR: Your SOP needs significant improvements for ISO 27002 compliance")
        report_lines.append("  - Priority focus on controls scoring below 0.25")
        report_lines.append("  - Consider comprehensive policy review and enhancement")
    else:
        report_lines.append("✗ POOR: Your SOP requires major revisions for ISO 27002 compliance")
        report_lines.append("  - Comprehensive policy rewrite recommended")
        report_lines.append("  - Consider professional compliance consultation")
    
    report_lines.append("")
    report_lines.append("Specific Actions:")
    report_lines.append(f"1. Address {len(poor)} controls with poor compliance scores")
    report_lines.append(f"2. Enhance {len(fair)} controls with fair compliance")
    report_lines.append(f"3. Maintain {len(excellent)} controls with excellent compliance")
    report_lines.append("")
    
    # Technical Details
    report_lines.append("TECHNICAL ANALYSIS DETAILS")
    report_lines.append("-" * 50)
    report_lines.append(f"Analysis Method: Sentence-by-sentence semantic similarity")
    report_lines.append(f"ML Model: all-roberta-large-v1 sentence transformer")
    report_lines.append(f"Similarity Threshold: 0.25 (configurable)")
    report_lines.append(f"ISO Controls Analyzed: {summary['total_controls']}")
    report_lines.append(f"Total ISO Sentences: {sum(len(data['sentences']) for data in [])}")  # Would need scorer instance
    report_lines.append("")
    
    # Footer
    report_lines.append("="*100)
    report_lines.append("End of Report")
    report_lines.append("="*100)
    
    return "\n".join(report_lines)

def save_results(results: dict, report: str):
    """Save analysis results and report to files."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save JSON results
    json_filename = f"godfrey_phillips_analysis_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✓ Detailed results saved to: {json_filename}")
    
    # Save text report
    report_filename = f"godfrey_phillips_report_{timestamp}.txt"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ Comprehensive report saved to: {report_filename}")
    
    return json_filename, report_filename

def main():
    """Main analysis workflow."""
    print("="*100)
    print("REAL SOP ANALYSIS: InformationSecurityPolicy-godfreyphillips.pdf")
    print("Testing SentenceSimilarityScorer prototype with ISO 27002 compliance")
    print("="*100)
    print(f"Analysis started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Extract PDF content
    pdf_path = "InformationSecurityPolicy-godfreyphillips.pdf"
    if not os.path.exists(pdf_path):
        print(f"✗ PDF file not found: {pdf_path}")
        print("Please ensure the file is in the current directory.")
        return False
    
    content = extract_sop_content(pdf_path)
    if not content:
        print("✗ Failed to extract PDF content")
        return False
    
    # Step 2: Run analysis
    results = analyze_sop_with_prototype(content)
    if not results:
        print("✗ Failed to analyze SOP document")
        return False
    
    # Step 3: Generate comprehensive report
    print("\n" + "="*80)
    print("GENERATING COMPREHENSIVE REPORT")
    print("="*80)
    
    report = generate_comprehensive_report(results, content)
    
    # Step 4: Save results
    json_file, report_file = save_results(results, report)
    
    # Step 5: Display summary
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - SUMMARY")
    print("="*80)
    print(f"Overall Compliance Score: {results['overall_score']:.1f}%")
    print(f"Compliant Controls: {results['compliance_summary']['compliant_controls']}/{results['compliance_summary']['total_controls']}")
    print(f"Analysis Time: {results['analysis_time']:.2f} seconds")
    print(f"Files Generated:")
    print(f"  - {json_file} (detailed data)")
    print(f"  - {report_file} (comprehensive report)")
    print("")
    print("Next Steps:")
    print("1. Review the comprehensive report for detailed findings")
    print("2. Focus on improving controls with low compliance scores")
    print("3. Use the detailed evidence to understand specific gaps")
    print(f"\nAnalysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 