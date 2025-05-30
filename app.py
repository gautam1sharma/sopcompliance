from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from pdf_parser import PDFParser
from enhanced_compliance_checker import EnhancedComplianceChecker
from semantic_compliance_checker import SemanticComplianceChecker
import traceback

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

# Initialize checkers - Semantic checker will be initialized lazily
enhanced_checker = EnhancedComplianceChecker()
semantic_checker = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_semantic_checker():
    """Lazy initialization of semantic checker due to model loading time."""
    global semantic_checker
    if semantic_checker is None:
        semantic_checker = SemanticComplianceChecker()
    return semantic_checker

@app.route('/')
def index():
    """Landing page with model explanation and call-to-action."""
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    """Analysis page with upload functionality."""
    return render_template('analyze.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        method = request.form.get('method', 'enhanced')  # Default to enhanced method
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the PDF
            parser = PDFParser(filepath)
            content = parser.extract_text()
            
            if not content.strip():
                return jsonify({'error': 'No text could be extracted from the PDF'}), 400
            
            # Check compliance with selected method
            if method == 'semantic':
                print("Using Semantic Compliance Checker (Sentence Transformers)")
                checker = get_semantic_checker()
            else:
                print("Using Enhanced Compliance Checker (String-based)")
                checker = enhanced_checker
            
            compliance_results = checker.check_compliance(content)
            
            return jsonify({
                'message': 'File processed successfully',
                'results': compliance_results,
                'document_length': len(content),
                'filename': filename,
                'method_used': method
            })
        
        return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
    
    except Exception as e:
        # Log the full traceback for debugging
        print("Error in upload_file:")
        print(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/export', methods=['POST'])
def export_report():
    data = request.json
    if not data or 'results' not in data:
        return jsonify({'error': 'No results to export'}), 400
    
    # Generate and return report
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], 'compliance_report.pdf')
    # TODO: Implement report generation
    return send_file(report_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 