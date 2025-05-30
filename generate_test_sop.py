from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
import os

def create_test_sop():
    # Create output directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        "uploads/test_sop.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Create styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )
    
    # Content
    content = []
    
    # Title
    content.append(Paragraph("Information Security Standard Operating Procedures", title_style))
    content.append(Spacer(1, 20))
    
    # Section 5.1: Information Security Policies
    content.append(Paragraph("Section 5.1: Information Security Policies", heading_style))
    content.append(Paragraph("""
    This organization maintains a comprehensive set of information security policies that are regularly reviewed and updated. 
    All employees are required to acknowledge and follow these policies. The information security policy document is reviewed 
    annually by the management team and updated as necessary to reflect changes in business requirements, security threats, 
    and regulatory requirements.
    """, body_style))
    
    # Section 8.1: Asset Management
    content.append(Paragraph("Section 8.1: Asset Management", heading_style))
    content.append(Paragraph("""
    All information assets are identified, classified, and inventoried. Each asset has an assigned owner responsible for 
    its security. The organization maintains an up-to-date inventory of all important assets, including hardware, software, 
    and data. Regular audits are conducted to ensure the accuracy of the asset inventory.
    """, body_style))
    
    # Section 9.1: Access Control
    content.append(Paragraph("Section 9.1: Access Control", heading_style))
    content.append(Paragraph("""
    Access to information and information processing facilities is controlled based on business and security requirements. 
    The organization implements a formal user registration and de-registration process for access to all information systems 
    and services. Access rights are reviewed regularly, and any unnecessary access rights are revoked promptly.
    """, body_style))
    
    # Section 12.1: Operational Security
    content.append(Paragraph("Section 12.1: Operational Security", heading_style))
    content.append(Paragraph("""
    Operational procedures and responsibilities are established and maintained for all information processing facilities. 
    The organization implements change management procedures to control changes to information processing facilities and systems. 
    Capacity management ensures that the performance and capacity of systems are monitored and projections of future capacity 
    requirements are made to ensure adequate performance.
    """, body_style))
    
    # Section 16.1: Incident Management
    content.append(Paragraph("Section 16.1: Incident Management", heading_style))
    content.append(Paragraph("""
    The organization has established procedures for reporting and managing information security events and incidents. 
    All employees are required to report any observed or suspected security events or incidents. The incident management 
    process includes procedures for assessment, decision-making, and response to information security incidents.
    """, body_style))
    
    # Build PDF
    doc.build(content)

if __name__ == "__main__":
    create_test_sop()
    print("Test SOP PDF has been generated in the 'uploads' directory.") 