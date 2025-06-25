import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional
import traceback

class ComplianceLogger:
    """
    Centralized logging utility for the compliance checker application.
    Provides structured logging with proper formatting and rotation.
    """
    
    def __init__(self, name: str = 'compliance_checker', log_file: Optional[str] = None, 
                 log_level: str = 'INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers(log_file)
    
    def _setup_handlers(self, log_file: Optional[str] = None):
        """Setup console and file handlers with appropriate formatting."""
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation if log file is specified
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=10*1024*1024, backupCount=5  # 10MB per file, 5 backups
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str, **kwargs):
        """Log info message with optional context."""
        self.logger.info(self._format_message(message, kwargs))
    
    def debug(self, message: str, **kwargs):
        """Log debug message with optional context."""
        self.logger.debug(self._format_message(message, kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message with optional context."""
        self.logger.warning(self._format_message(message, kwargs))
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log error message with optional exception details."""
        formatted_message = self._format_message(message, kwargs)
        
        if exception:
            formatted_message += f" | Exception: {str(exception)}"
            self.logger.error(formatted_message)
            self.logger.debug(f"Exception traceback: {traceback.format_exc()}")
        else:
            self.logger.error(formatted_message)
    
    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log critical message with optional exception details."""
        formatted_message = self._format_message(message, kwargs)
        
        if exception:
            formatted_message += f" | Exception: {str(exception)}"
            self.logger.critical(formatted_message)
            self.logger.debug(f"Exception traceback: {traceback.format_exc()}")
        else:
            self.logger.critical(formatted_message)
    
    def log_file_upload(self, filename: str, file_size: int, method: str, user_ip: str):
        """Log file upload events with security context."""
        self.info(
            "File upload",
            filename=filename,
            file_size=file_size,
            method=method,
            user_ip=user_ip,
            timestamp=datetime.utcnow().isoformat()
        )
    
    def log_analysis_start(self, method: str, content_length: int, **kwargs):
        """Log analysis start with method and content info."""
        self.info(
            f"Analysis started using {method} method",
            method=method,
            content_length=content_length,
            **kwargs
        )
    
    def log_analysis_complete(self, method: str, compliance_score: float, 
                            processing_time: float, **kwargs):
        """Log analysis completion with results summary."""
        self.info(
            f"Analysis completed using {method} method",
            method=method,
            compliance_score=compliance_score,
            processing_time_seconds=processing_time,
            **kwargs
        )
    
    def log_security_event(self, event_type: str, severity: str, details: dict):
        """Log security-related events."""
        message = f"Security event: {event_type}"
        
        if severity.upper() in ['HIGH', 'CRITICAL']:
            self.critical(message, **details)
        elif severity.upper() == 'MEDIUM':
            self.warning(message, **details)
        else:
            self.info(message, **details)
    
    def log_performance_metrics(self, operation: str, duration: float, **metrics):
        """Log performance metrics for monitoring."""
        self.info(
            f"Performance metrics for {operation}",
            operation=operation,
            duration_seconds=duration,
            **metrics
        )
    
    def _format_message(self, message: str, context: dict) -> str:
        """Format message with context information."""
        if not context:
            return message
        
        context_str = " | ".join(f"{k}={v}" for k, v in context.items())
        return f"{message} | {context_str}"

# Global logger instance
_global_logger = None

def get_logger(name: str = 'compliance_checker', log_file: Optional[str] = None, 
               log_level: str = 'INFO') -> ComplianceLogger:
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name
        log_file: Optional log file path
        log_level: Logging level
        
    Returns:
        ComplianceLogger instance
    """
    global _global_logger
    
    if _global_logger is None:
        _global_logger = ComplianceLogger(name, log_file, log_level)
    
    return _global_logger

def setup_app_logging(app):
    """
    Setup application-wide logging configuration.
    
    Args:
        app: Flask application instance
    """
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    log_file = app.config.get('LOG_FILE')
    
    logger = get_logger(log_file=log_file, log_level=log_level)
    
    # Store logger in app context for easy access
    app.logger_instance = logger
    
    # Log application startup
    logger.info("Application starting up", 
                debug_mode=app.debug,
                environment=app.config.get('ENV', 'unknown'))
    
    return logger

# Utility functions for common logging patterns
def log_request_info(request, logger: ComplianceLogger):
    """Log incoming request information."""
    logger.debug(
        "Incoming request",
        method=request.method,
        endpoint=request.endpoint,
        user_agent=request.headers.get('User-Agent', 'Unknown'),
        ip_address=request.remote_addr,
        content_length=request.content_length
    )

def log_response_info(response, logger: ComplianceLogger, processing_time: float = None):
    """Log response information."""
    logger.debug(
        "Outgoing response",
        status_code=response.status_code,
        content_length=response.content_length,
        processing_time=processing_time
    ) 