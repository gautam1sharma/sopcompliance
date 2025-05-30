from pdf_parser import PDFParser
from enhanced_compliance_checker import EnhancedComplianceChecker
import json

def analyze_document(filepath):
    """Analyze a specific document to understand its structure and content."""
    print(f"Analyzing document: {filepath}")
    print("=" * 50)
    
    try:
        # Extract text
        parser = PDFParser(filepath)
        content = parser.extract_text()
        
        print(f"Document length: {len(content)} characters")
        print(f"First 500 characters:")
        print("-" * 30)
        print(content[:500])
        print("-" * 30)
        
        # Extract sections
        sections = parser.extract_sections()
        print(f"\nFound {len(sections)} sections:")
        for title, content in sections.items():
            print(f"- {title}: {len(content)} chars")
        
        # Run enhanced compliance check
        checker = EnhancedComplianceChecker()
        results = checker.check_compliance(content)
        
        print(f"\nCompliance Analysis:")
        print(f"Overall Score: {results['compliance_score']:.1f}%")
        print(f"Matched Controls: {results['matched_controls']}/{results['total_controls']}")
        
        print(f"\nSemantic Features Found:")
        for category, count in results['semantic_analysis'].items():
            print(f"- {category}: {count} instances")
        
        print(f"\nTop Compliant Controls:")
        compliant_controls = [detail for detail in results['details'] if detail['status'] == 'Compliant']
        compliant_controls.sort(key=lambda x: x['score'], reverse=True)
        
        for control in compliant_controls[:5]:
            print(f"- {control['control_id']}: {control['control_name']} (Score: {control['score']:.2f})")
            if control['evidence']:
                print(f"  Evidence: {control['evidence'][0][:100]}...")
        
        # Save detailed results
        with open('analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to analysis_results.json")
        
    except Exception as e:
        print(f"Error analyzing document: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Analyze the provided document
    analyze_document("InformationSecurityPolicy-godfreyphillips.pdf") 