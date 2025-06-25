import os
import io
from datetime import datetime
from typing import Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

class ComplianceReportGenerator:
    """
    Professional PDF report generator for compliance analysis results.
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2C3E50'),
            alignment=TA_CENTER
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#3498DB'),
            alignment=TA_LEFT
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=16,
            textColor=colors.HexColor('#2C3E50'),
            alignment=TA_LEFT
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        # Evidence style
        self.styles.add(ParagraphStyle(
            name='Evidence',
            parent=self.styles['Normal'],
            fontSize=9,
            leftIndent=20,
            spaceAfter=4,
            textColor=colors.HexColor('#7F8C8D'),
            fontName='Helvetica-Oblique'
        ))
    
    def generate_report(self, results: Dict, filename: str, output_path: str) -> str:
        """
        Generate a comprehensive compliance report.
        
        Args:
            results: Compliance analysis results
            filename: Original filename of analyzed document
            output_path: Directory to save the report
            
        Returns:
            Path to generated report file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Generate report filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"compliance_report_{timestamp}.pdf"
        report_path = os.path.join(output_path, report_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            report_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build report content
        story = []
        
        # Title page
        story.extend(self._create_title_page(results, filename))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary(results))
        story.append(PageBreak())
        
        # Detailed analysis
        story.extend(self._create_detailed_analysis(results))
        
        # Recommendations
        story.extend(self._create_recommendations(results))
        
        # Appendices
        story.extend(self._create_appendices(results))
        
        # Build PDF
        doc.build(story)
        
        return report_path
    
    def _create_title_page(self, results: Dict, filename: str) -> List:
        """Create title page content."""
        story = []
        
        # Title
        title = Paragraph("ISO 27002 Compliance Analysis Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.5*inch))
        
        # Document info table
        doc_info = [
            ["Document Analyzed:", filename],
            ["Analysis Method:", results.get('method', 'Unknown')],
            ["Analysis Date:", datetime.now().strftime("%B %d, %Y")],
            ["Overall Compliance Score:", f"{results.get('compliance_score', 0):.1f}%"],
            ["Controls Evaluated:", str(results.get('total_controls', 0))],
            ["Controls Matched:", str(results.get('matched_controls', 0))]
        ]
        
        doc_table = Table(doc_info, colWidths=[2.5*inch, 3*inch])
        doc_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(doc_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Compliance score visualization
        story.append(self._create_compliance_chart(results))
        
        return story
    
    def _create_compliance_chart(self, results: Dict) -> Drawing:
        """Create a visual representation of compliance score."""
        drawing = Drawing(400, 200)
        
        score = results.get('compliance_score', 0)
        matched = results.get('matched_controls', 0)
        total = results.get('total_controls', 1)
        
        # Pie chart for compliance overview
        pie = Pie()
        pie.x = 50
        pie.y = 50
        pie.width = 100
        pie.height = 100
        pie.data = [matched, total - matched]
        pie.labels = ['Compliant', 'Non-compliant']
        pie.slices[0].fillColor = colors.HexColor('#27AE60')
        pie.slices[1].fillColor = colors.HexColor('#E74C3C')
        
        drawing.add(pie)
        
        # Add score text
        from reportlab.graphics.shapes import String
        score_text = String(200, 100, f"Overall Score: {score:.1f}%", fontSize=16)
        drawing.add(score_text)
        
        return drawing
    
    def _create_executive_summary(self, results: Dict) -> List:
        """Create executive summary section."""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Summary text
        score = results.get('compliance_score', 0)
        matched = results.get('matched_controls', 0)
        total = results.get('total_controls', 1)
        method = results.get('method', 'Unknown')
        
        summary_text = f"""
        This report presents the results of an ISO 27002 compliance analysis conducted using the 
        {method} method. The analysis evaluated {total} security controls and found evidence 
        of compliance for {matched} controls, resulting in an overall compliance score of {score:.1f}%.
        """
        
        story.append(Paragraph(summary_text, self.styles['BodyText']))
        story.append(Spacer(1, 12))
        
        # Key findings
        story.append(Paragraph("Key Findings", self.styles['SectionHeader']))
        
        if score >= 80:
            finding_text = "The organization demonstrates strong compliance with ISO 27002 standards."
        elif score >= 60:
            finding_text = "The organization shows moderate compliance with areas for improvement."
        elif score >= 40:
            finding_text = "The organization has basic compliance but requires significant improvements."
        else:
            finding_text = "The organization shows limited compliance and requires comprehensive security program development."
        
        story.append(Paragraph(finding_text, self.styles['BodyText']))
        
        # Semantic analysis summary if available
        semantic_analysis = results.get('semantic_analysis', {})
        if semantic_analysis:
            story.append(Spacer(1, 12))
            story.append(Paragraph("Semantic Analysis Summary", self.styles['SectionHeader']))
            
            for feature, count in semantic_analysis.items():
                feature_text = f"• {feature.replace('_', ' ').title()}: {count} references found"
                story.append(Paragraph(feature_text, self.styles['BodyText']))
        
        return story
    
    def _create_detailed_analysis(self, results: Dict) -> List:
        """Create detailed analysis section."""
        story = []
        
        story.append(Paragraph("Detailed Control Analysis", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        details = results.get('details', [])
        
        # Group controls by category
        categories = {}
        for detail in details:
            control_id = detail.get('control_id', '')
            category = control_id.split('.')[0] if '.' in control_id else 'Other'
            
            if category not in categories:
                categories[category] = []
            categories[category].append(detail)
        
        # Create analysis for each category
        for category, controls in sorted(categories.items()):
            category_name = self._get_category_name(category)
            story.append(Paragraph(f"Category {category}: {category_name}", self.styles['Subtitle']))
            
            # Create table for controls in this category
            table_data = [['Control', 'Name', 'Status', 'Score']]
            for control in controls:
                if control.get('status') == 'High Confidence':
                    status_color = colors.HexColor('#27AE60')
                elif control.get('status') == 'Medium Confidence':
                    status_color = colors.HexColor('#F39C12')
                elif control.get('status') == 'Low Confidence':
                    status_color = colors.HexColor('#E67E22')
                else:
                    status_color = colors.HexColor('#E74C3C')
                
                table_data.append([
                    control.get('control_id', ''),
                    control.get('control_name', '')[:40] + ('...' if len(control.get('control_name', '')) > 40 else ''),
                    control.get('status', ''),
                    f"{control.get('score', 0):.2f}"
                ])
            
            table = Table(table_data, colWidths=[0.8*inch, 3*inch, 1*inch, 0.8*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 12))
              # Add evidence for compliant controls
            high_confidence_controls = [c for c in controls if c.get('status') == 'High Confidence']
            medium_confidence_controls = [c for c in controls if c.get('status') == 'Medium Confidence']
            low_confidence_controls = [c for c in controls if c.get('status') == 'Low Confidence']
            
            compliant_controls = high_confidence_controls + medium_confidence_controls + low_confidence_controls
            
            if compliant_controls:
                story.append(Paragraph("Evidence Found:", self.styles['SectionHeader']))
                for control in compliant_controls[:3]:  # Limit to first 3 for space
                    evidence = control.get('evidence', [])
                    if evidence:
                        control_text = f"<b>{control.get('control_id', '')}</b>: {control.get('control_name', '')} ({control.get('status', '')})"
                        story.append(Paragraph(control_text, self.styles['BodyText']))
                        for ev in evidence[:2]:  # Limit evidence per control
                            story.append(Paragraph(f"• {ev[:100]}...", self.styles['Evidence']))
                story.append(Spacer(1, 12))
        
        return story
    
    def _create_recommendations(self, results: Dict) -> List:
        """Create recommendations section."""
        story = []
        
        story.append(Paragraph("Recommendations", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        score = results.get('compliance_score', 0)
        details = results.get('details', [])
        
        # General recommendations based on score
        if score < 50:
            recommendations = [
                "Conduct a comprehensive security assessment to identify all gaps",
                "Develop a formal information security management system (ISMS)",
                "Establish clear security policies and procedures",
                "Implement regular security awareness training for all personnel",
                "Create an incident response plan and test it regularly"
            ]
        elif score < 75:
            recommendations = [
                "Focus on implementing missing controls identified in this analysis",
                "Regular review and update of existing security policies",
                "Enhance monitoring and logging capabilities",
                "Conduct regular security audits and assessments",
                "Improve documentation of security procedures"
            ]
        else:
            recommendations = [
                "Maintain current good practices and continue regular reviews",
                "Consider advanced security measures for enhanced protection",
                "Regular testing of security controls effectiveness",
                "Continuous monitoring and improvement of security posture",
                "Stay updated with latest security threats and best practices"
            ]
        
        story.append(Paragraph("Priority Actions:", self.styles['SectionHeader']))
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", self.styles['BodyText']))
        
        # Specific recommendations for non-compliant controls
        non_compliant = [d for d in details if d.get('status') != 'Compliant']
        if non_compliant:
            story.append(Spacer(1, 12))
            story.append(Paragraph("Control-Specific Recommendations:", self.styles['SectionHeader']))
            
            for control in non_compliant[:10]:  # Limit to top 10
                control_id = control.get('control_id', '')
                control_name = control.get('control_name', '')
                rec_text = f"<b>{control_id}</b>: Implement {control_name.lower()}"
                story.append(Paragraph(rec_text, self.styles['BodyText']))
        
        return story
    
    def _create_appendices(self, results: Dict) -> List:
        """Create appendices section."""
        story = []
        
        story.append(PageBreak())
        story.append(Paragraph("Appendices", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Appendix A: Complete control list
        story.append(Paragraph("Appendix A: Complete Control Assessment", self.styles['Subtitle']))
        
        details = results.get('details', [])
        table_data = [['Control ID', 'Control Name', 'Status', 'Score', 'Evidence Count']]
        
        for detail in details:
            evidence_count = len(detail.get('evidence', []))
            table_data.append([
                detail.get('control_id', ''),
                detail.get('control_name', '')[:50] + ('...' if len(detail.get('control_name', '')) > 50 else ''),
                detail.get('status', ''),
                f"{detail.get('score', 0):.2f}",
                str(evidence_count)
            ])
        
        table = Table(table_data, colWidths=[0.8*inch, 2.5*inch, 1*inch, 0.7*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(table)
        
        # Appendix B: Methodology
        story.append(Spacer(1, 24))
        story.append(Paragraph("Appendix B: Analysis Methodology", self.styles['Subtitle']))
        
        method = results.get('method', 'Unknown')
        methodology_text = f"""
        This analysis was conducted using the {method} method. The assessment evaluates 
        compliance against ISO/IEC 27002:2022 information security controls through 
        automated text analysis and pattern matching.
        
        Scoring Methodology:
        • Each control is scored from 0.0 to 1.0 based on evidence found
        • Overall compliance score is calculated as percentage of controls with score > 0.3
        • Evidence extraction provides context for compliance determination
        
        Limitations:
        • Automated analysis may not capture all nuances of compliance
        • Human review and validation is recommended for critical assessments
        • This analysis is based on document content only and does not include operational verification
        """
        
        story.append(Paragraph(methodology_text, self.styles['BodyText']))
        
        return story
    
    def _get_category_name(self, category: str) -> str:
        """Get descriptive name for control category."""
        category_names = {
            '5': 'Information Security Policies',
            '6': 'Organization of Information Security',
            '7': 'Human Resource Security',
            '8': 'Asset Management',
            '9': 'Access Control',
            '10': 'Cryptography',
            '11': 'Physical and Environmental Security',
            '12': 'Operations Security',
            '13': 'Communications Security',
            '14': 'System Acquisition, Development and Maintenance',
            '15': 'Supplier Relationships',
            '16': 'Information Security Incident Management',
            '17': 'Information Security in Business Continuity',
            '18': 'Compliance'
        }
        return category_names.get(category, 'Other Controls') 