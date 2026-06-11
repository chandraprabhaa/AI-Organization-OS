import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reports.generator import Report

class PDFReportGenerator:
    """Generate professional PDF reports from workflow results"""
    
    def __init__(self, page_size=letter):
        """
        Initialize PDF generator.
        
        Args:
            page_size: reportlab page size (letter or A4)
        """
        self.page_size = page_size
        self.width, self.height = page_size
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#0f2027'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#203a43'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderColor=colors.HexColor('#00c6ff'),
            borderPadding=10,
            borderWidth=2,
            borderLeftWidth=4
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        ))
    
    def generate_pdf(self, report: Report, output_path: str = None):
        """
        Generate PDF report.
        
        Args:
            report: Report object to convert to PDF
            output_path: Path to save PDF (if None, returns BytesIO)
            
        Returns:
            BytesIO object if output_path is None, else None
        """
        
        # Create PDF buffer or file
        if output_path:
            pdf_file = open(output_path, 'wb')
        else:
            pdf_file = io.BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=self.page_size,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title="AI Organization OS Report"
        )
        
        # Build story (content)
        story = []
        
        # Header
        story.extend(self._build_header(report))
        
        # Goal
        story.append(PageBreak())
        story.extend(self._build_section(
            "Business Goal",
            report.business_goal
        ))
        
        # Executive Summary
        story.extend(self._build_section(
            "Executive Summary",
            report.qa_output
        ))
        
        # Execution Plan
        story.append(PageBreak())
        story.extend(self._build_section(
            "Execution Plan",
            report.plan_output
        ))
        
        # Strategy
        story.extend(self._build_section(
            "Strategic Direction",
            report.ceo_output
        ))
        
        # Research
        story.append(PageBreak())
        story.extend(self._build_section(
            "Market Research",
            report.research_output
        ))
        
        # Analysis
        story.extend(self._build_section(
            "Business Analysis",
            report.analyst_output
        ))
        
        # Critique
        story.append(PageBreak())
        story.extend(self._build_section(
            "Critical Review",
            report.critic_output
        ))
        
        # QA Review
        story.extend(self._build_section(
            "Quality Assurance Review",
            report.qa_output
        ))
        
        # Metadata
        story.append(PageBreak())
        story.extend(self._build_metadata(report))
        
        # Build PDF
        doc.build(story)
        
        if output_path:
            pdf_file.close()
            return None
        else:
            pdf_file.seek(0)
            return pdf_file
    
    def _build_header(self, report: Report):
        """Build report header"""
        
        elements = []
        
        # Title
        elements.append(Paragraph(
            "🧠 AI Organization OS",
            self.styles['CustomTitle']
        ))
        
        # Subtitle
        elements.append(Paragraph(
            "Executive Business Report",
            self.styles['Heading2']
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Metadata
        metadata_text = f"<b>Generated:</b> {report.timestamp[:10]} | <b>System:</b> AI Organization OS"
        elements.append(Paragraph(
            metadata_text,
            self.styles['Normal']
        ))
        
        elements.append(Spacer(1, 0.5*inch))
        
        return elements
    
    def _build_section(self, title: str, content: str):
        """Build a report section"""
        
        elements = []
        
        # Section title
        elements.append(Paragraph(title, self.styles['SectionHeading']))
        
        # Content (split if too long)
        if len(content) > 5000:
            # Truncate very long content
            content = content[:5000] + "\n\n[Content truncated for PDF length - see full report for complete details]"
        
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                elements.append(Paragraph(
                    para.replace('\n', '<br/>'),
                    self.styles['CustomBody']
                ))
        
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _build_metadata(self, report: Report):
        """Build metadata section"""
        
        elements = []
        
        elements.append(Paragraph("Report Metadata", self.styles['SectionHeading']))
        
        # Metadata table
        data = [
            ["Generated", report.timestamp],
            ["System", "AI Organization OS"],
            ["Workflow", "Planner → CEO → Research → Analyst → Critic → QA"],
            ["LLM Provider", "Groq"],
            ["LLM Model", "Llama 3.3 70B"],
            ["Embeddings", "Sentence Transformers (all-MiniLM-L6-v2)"],
            ["Vector DB", "ChromaDB"],
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = """
        <p style="text-align:center; font-size:10px; color:#666;">
        This report was generated by an AI multi-agent system. All recommendations should be 
        reviewed and validated by domain experts before implementation.
        <br/><br/>
        © 2024 AI Organization OS. All rights reserved.
        </p>
        """
        
        elements.append(Paragraph(footer_text, self.styles['Normal']))
        
        return elements


def generate_pdf_from_workflow(workflow_result: dict, output_path: str = None):
    """
    Generate PDF directly from workflow result.
    
    Args:
        workflow_result: Output from graph.invoke()
        output_path: Path to save PDF
        
    Returns:
        BytesIO object or None
    """
    
    from reports.generator import create_report
    
    # Create report object
    report = create_report(workflow_result)
    
    # Generate PDF
    generator = PDFReportGenerator()
    return generator.generate_pdf(report, output_path)
