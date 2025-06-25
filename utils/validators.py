import os
import mimetypes
from marshmallow import Schema, fields, ValidationError
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from typing import Tuple, Optional

class FileUploadSchema(Schema):
    """Schema for file upload validation."""
    method = fields.Str(required=True, validate=lambda x: x in ['enhanced', 'semantic'])
    file = fields.Raw(required=True)

def validate_file_upload(file: FileStorage, allowed_extensions: set) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded file for security and format compliance.
    
    Args:
        file: The uploaded file object
        allowed_extensions: Set of allowed file extensions
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file or not file.filename:
        return False, "No file selected"
    
    # Check file extension
    if '.' not in file.filename:
        return False, "File must have an extension"
    
    extension = file.filename.rsplit('.', 1)[1].lower()
    if extension not in allowed_extensions:
        return False, f"File type '{extension}' not allowed. Allowed types: {', '.join(allowed_extensions)}"
    
    # Check file size (Flask handles this automatically, but we can add custom logic)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    if file_size == 0:
        return False, "File is empty"
    
    if file_size > 16 * 1024 * 1024:  # 16MB
        return False, "File size exceeds 16MB limit"
    
    # Validate MIME type using mimetypes (lightweight alternative)
    try:
        # Guess MIME type from filename
        guessed_mime, _ = mimetypes.guess_type(file.filename)
        
        # Map extensions to expected MIME types
        expected_mimes = {
            'pdf': ['application/pdf'],
            'docx': [
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/zip'  # DOCX files are ZIP archives
            ],
            'txt': ['text/plain']
        }
        
        if extension in expected_mimes and guessed_mime:
            if guessed_mime not in expected_mimes[extension]:
                # For DOCX, also allow application/zip as it's a valid MIME type
                if not (extension == 'docx' and guessed_mime == 'application/zip'):
                    return False, f"File extension doesn't match expected MIME type. Expected {expected_mimes[extension]}, filename suggests {guessed_mime}"
    
    except Exception:
        # If MIME detection fails, continue with other validations
        pass
    
    # Check for potentially dangerous filenames
    secure_name = secure_filename(file.filename)
    if not secure_name:
        return False, "Invalid filename"
    
    # Additional security checks
    dangerous_extensions = {
        'exe', 'bat', 'cmd', 'com', 'pif', 'scr', 'vbs', 'js', 'jar',
        'php', 'asp', 'jsp', 'sh', 'ps1', 'py'
    }
    
    if extension in dangerous_extensions:
        return False, f"File type '{extension}' is not allowed for security reasons"
    
    return True, None

def validate_analysis_method(method: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the analysis method parameter.
    
    Args:
        method: The analysis method string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_methods = {'enhanced', 'semantic'}
    
    if not method:
        return False, "Analysis method is required"
    
    if method not in valid_methods:
        return False, f"Invalid analysis method. Must be one of: {', '.join(valid_methods)}"
    
    return True, None

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Use werkzeug's secure_filename and add timestamp for uniqueness
    import time
    import uuid
    
    secure_name = secure_filename(filename)
    if not secure_name:
        secure_name = f"uploaded_file_{int(time.time())}"
    
    # Add UUID to prevent filename collisions
    name, ext = os.path.splitext(secure_name)
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}_{unique_id}{ext}"

def validate_json_payload(data: dict, required_fields: list) -> Tuple[bool, Optional[str]]:
    """
    Validate JSON payload contains required fields.
    
    Args:
        data: JSON data dictionary
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Invalid JSON payload"
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, None

class SecurityValidator:
    """Security-focused validation utilities."""
    
    @staticmethod
    def check_file_content_safety(content: str) -> Tuple[bool, Optional[str]]:
        """
        Check if extracted content appears safe and legitimate.
        
        Args:
            content: Extracted text content
            
        Returns:
            Tuple of (is_safe, warning_message)
        """
        if not content or not content.strip():
            return False, "No text content could be extracted from the file"
        
        # Check for extremely long content (potential DoS)
        if len(content) > 10 * 1024 * 1024:  # 10MB of text
            return False, "Content is too large to process safely"
        
        # Check for suspicious patterns (basic)
        suspicious_patterns = [
            r'<script.*?>',
            r'javascript:',
            r'vbscript:',
            r'data:.*base64',
        ]
        
        import re
        for pattern in suspicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return False, f"Content contains potentially unsafe elements: {pattern}"
        
        # Check character encoding issues
        try:
            content.encode('utf-8')
        except UnicodeEncodeError:
            return False, "Content contains invalid characters"
        
        return True, None
    
    @staticmethod
    def validate_compliance_results(results: dict) -> Tuple[bool, Optional[str]]:
        """
        Validate compliance analysis results structure.
        
        Args:
            results: Results dictionary from compliance checker
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_keys = ['compliance_score', 'summary', 'details']
        
        for key in required_keys:
            if key not in results:
                return False, f"Missing required key in results: {key}"
        
        # Validate summary structure
        summary = results.get('summary', {})
        required_summary_keys = ['total_controls', 'matched_controls']
        for key in required_summary_keys:
            if key not in summary:
                return False, f"Missing required key in summary: {key}"

        # Validate score ranges
        score = results.get('compliance_score', 0)
        if not (0 <= score <= 100):
            return False, f"Invalid compliance score: {score}. Must be between 0-100"
        
        # Validate control counts
        total = summary.get('total_controls', 0)
        matched = summary.get('matched_controls', 0)
        
        if total <= 0:
            return False, "Total controls must be greater than 0"
        
        if matched < 0 or matched > total:
            return False, f"Matched controls ({matched}) must be between 0 and total controls ({total})"
        
        return True, None 