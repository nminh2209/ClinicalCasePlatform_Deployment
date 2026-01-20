# templates/pdf_renderer.py
"""
PDF rendering service for case templates
Generates PDF previews from case data and template schemas
"""

from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime


class CaseTemplatePDFRenderer:
    """
    Renders case templates and case data to PDF format
    """
    
    def __init__(self, template, case=None):
        self.template = template
        self.case = case
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for Vietnamese text"""
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Field label
        self.styles.add(ParagraphStyle(
            name='FieldLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495e'),
            fontName='Helvetica-Bold'
        ))
        
        # Field value
        self.styles.add(ParagraphStyle(
            name='FieldValue',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
        ))
    
    def _add_header(self, canvas, doc):
        """Add header to each page"""
        canvas.saveState()
        
        # Hospital/Institution name
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(2*cm, A4[1] - 2*cm, "TRƯỜNG ĐẠI HỌC Y DƯỢC")
        
        # Template name
        canvas.setFont('Helvetica', 10)
        canvas.drawString(2*cm, A4[1] - 2.5*cm, f"Mẫu: {self.template.name}")
        
        # Page number
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(
            A4[0] - 2*cm, 
            A4[1] - 2*cm,
            f"Trang {doc.page}"
        )
        
        # Line separator
        canvas.setStrokeColor(colors.grey)
        canvas.line(2*cm, A4[1] - 2.7*cm, A4[0] - 2*cm, A4[1] - 2.7*cm)
        
        canvas.restoreState()
    
    def _add_footer(self, canvas, doc):
        """Add footer to each page"""
        canvas.saveState()
        
        # Line separator
        canvas.setStrokeColor(colors.grey)
        canvas.line(2*cm, 2*cm, A4[0] - 2*cm, 2*cm)
        
        # Footer text
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(
            A4[0] / 2, 
            1.5*cm,
            f"Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )
        
        canvas.restoreState()
    
    def render_template_structure(self):
        """
        Render the template structure (empty form) to PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=3.5*cm,
            bottomMargin=2.5*cm
        )
        
        story = []
        
        # Title
        title = Paragraph(
            f"<b>{self.template.name}</b>",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        # Description
        if self.template.description:
            desc = Paragraph(self.template.description, self.styles['Normal'])
            story.append(desc)
            story.append(Spacer(1, 0.5*cm))
        
        # Specialty information
        specialty_info = []
        if self.template.specialty:
            specialty_info.append(['Chuyên khoa:', self.template.specialty.name])
        if self.template.department:
            specialty_info.append(['Khoa:', self.template.department.name])
        
        if specialty_info:
            info_table = Table(specialty_info, colWidths=[4*cm, 12*cm])
            info_table.setStyle(TableStyle([
                ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
                ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(info_table)
            story.append(Spacer(1, 0.5*cm))
        
        # Render template fields
        if self.template.template_fields:
            sections = self.template.template_fields.get('sections', [])
            for section in sections:
                story.extend(self._render_section(section))
        
        # Render attachment requirements
        if self.template.attachment_requirements:
            story.append(Spacer(1, 1*cm))
            story.append(Paragraph(
                "<b>YÊU CẦU TÀI LIỆU ĐÍNH KÈM</b>",
                self.styles['SectionHeader']
            ))
            
            for key, req in self.template.attachment_requirements.items():
                required = "(*)" if req.get('required') else ""
                story.append(Paragraph(
                    f"• {req.get('label', key)} {required}",
                    self.styles['Normal']
                ))
        
        # Build PDF
        doc.build(
            story,
            onFirstPage=self._add_header,
            onLaterPages=self._add_header
        )
        
        buffer.seek(0)
        return buffer
    
    def _render_section(self, section):
        """Render a template section"""
        elements = []
        
        # Section header
        elements.append(Paragraph(
            f"<b>{section.get('name', 'Untitled Section')}</b>",
            self.styles['SectionHeader']
        ))
        elements.append(Spacer(1, 0.3*cm))
        
        # Fields table
        fields = section.get('fields', [])
        if fields:
            field_data = []
            
            for field in fields:
                label = field.get('label', field.get('name', ''))
                required = " (*)" if field.get('required') else ""
                unit = f" ({field.get('unit')})" if field.get('unit') else ""
                
                # Add field row
                field_data.append([
                    f"{label}{required}{unit}",
                    "____________________________________"
                ])
            
            if field_data:
                field_table = Table(field_data, colWidths=[8*cm, 8*cm])
                field_table.setStyle(TableStyle([
                    ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
                    ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(field_table)
        
        elements.append(Spacer(1, 0.5*cm))
        return elements
    
    def render_filled_case(self):
        """
        Render a completed case with data filled in
        """
        if not self.case:
            raise ValueError("Case data is required for filled rendering")
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=3.5*cm,
            bottomMargin=2.5*cm
        )
        
        story = []
        
        # Title
        title = Paragraph(
            f"<b>BỆNH ÁN: {self.case.title}</b>",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        # Case metadata
        case_info = [
            ['Mã bệnh án:', f"BA-{self.case.id}"],
            ['Chuyên khoa:', self.case.specialty if self.case.specialty else 'N/A'],
            ['Người tạo:', self.case.student.get_full_name() if self.case.student else 'N/A'],
            ['Ngày tạo:', self.case.created_at.strftime('%d/%m/%Y')],
        ]
        
        info_table = Table(case_info, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Render case data
        if self.template.template_fields and self.case.case_data:
            sections = self.template.template_fields.get('sections', [])
            for section in sections:
                story.extend(self._render_filled_section(section, self.case.case_data))
        
        # Build PDF
        doc.build(
            story,
            onFirstPage=self._add_header,
            onLaterPages=self._add_header
        )
        
        buffer.seek(0)
        return buffer
    
    def _render_filled_section(self, section, case_data):
        """Render a filled section with actual case data"""
        elements = []
        
        # Section header
        elements.append(Paragraph(
            f"<b>{section.get('name', 'Untitled Section')}</b>",
            self.styles['SectionHeader']
        ))
        elements.append(Spacer(1, 0.3*cm))
        
        # Get section data
        section_id = section.get('id')
        section_data = case_data.get(section_id, {})
        
        # Fields table
        fields = section.get('fields', [])
        if fields:
            field_data = []
            
            for field in fields:
                field_name = field.get('name')
                label = field.get('label', field_name)
                value = section_data.get(field_name, '—')
                unit = f" {field.get('unit')}" if field.get('unit') else ""
                
                # Format value
                if value:
                    display_value = f"{value}{unit}"
                else:
                    display_value = "—"
                
                field_data.append([
                    f"{label}:",
                    display_value
                ])
            
            if field_data:
                field_table = Table(field_data, colWidths=[7*cm, 9*cm])
                field_table.setStyle(TableStyle([
                    ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
                    ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                elements.append(field_table)
        
        elements.append(Spacer(1, 0.5*cm))
        return elements


def generate_template_pdf(template):
    """
    Generate PDF for empty template structure
    """
    renderer = CaseTemplatePDFRenderer(template)
    return renderer.render_template_structure()


def generate_case_pdf(case):
    """
    Generate PDF for completed case
    Simple version that works with the actual Case model structure
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from io import BytesIO
    import os
    
    # Register Unicode font for Vietnamese support
    try:
        # Try to use DejaVu Sans (common on Windows/Linux)
        font_path = "C:/Windows/Fonts/DejaVuSans.ttf"
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', "C:/Windows/Fonts/DejaVuSans-Bold.ttf"))
            base_font = 'DejaVuSans'
            bold_font = 'DejaVuSans-Bold'
        else:
            # Fallback to Arial Unicode MS if available
            font_path = "C:/Windows/Fonts/arial.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('Arial', font_path))
                pdfmetrics.registerFont(TTFont('Arial-Bold', "C:/Windows/Fonts/arialbd.ttf"))
                base_font = 'Arial'
                bold_font = 'Arial-Bold'
            else:
                # Last resort: use Helvetica (won't show Vietnamese correctly)
                base_font = 'Helvetica'
                bold_font = 'Helvetica-Bold'
    except:
        base_font = 'Helvetica'
        bold_font = 'Helvetica-Bold'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName=bold_font
    )
    story.append(Paragraph(f"<b>BỆNH ÁN: {case.title}</b>", title_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Case metadata
    case_info = [
        ['Mã bệnh án:', f"BA-{case.id}"],
        ['Chuyên khoa:', case.specialty if case.specialty else 'N/A'],
        ['Người tạo:', case.student.get_full_name() if case.student else 'N/A'],
        ['Ngày tạo:', case.created_at.strftime('%d/%m/%Y')],
        ['Trạng thái:', case.get_case_status_display()],
    ]
    
    info_table = Table(case_info, colWidths=[4*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), bold_font, 10),
        ('FONT', (1, 0), (1, -1), base_font, 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Patient info
    section_style = ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        spaceBefore=12,
        fontName=bold_font
    )
    
    # Custom normal style with Vietnamese font
    normal_style = ParagraphStyle(
        name='VietnameseNormal',
        parent=styles['Normal'],
        fontName=base_font,
        fontSize=10
    )
    
    story.append(Paragraph("<b>THÔNG TIN BỆNH NHÂN</b>", section_style))
    patient_info = [
        ['Tên bệnh nhân:', case.patient_name or 'N/A'],
        ['Tuổi:', str(case.patient_age) if case.patient_age else 'N/A'],
        ['Giới tính:', case.get_patient_gender_display() if case.patient_gender else 'N/A'],
        ['Số hồ sơ:', case.medical_record_number or 'N/A'],
    ]
    
    if case.admission_date:
        patient_info.append(['Ngày nhập viện:', case.admission_date.strftime('%d/%m/%Y')])
    if case.discharge_date:
        patient_info.append(['Ngày xuất viện:', case.discharge_date.strftime('%d/%m/%Y')])
    
    patient_table = Table(patient_info, colWidths=[4*cm, 12*cm])
    patient_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), bold_font, 10),
        ('FONT', (1, 0), (1, -1), base_font, 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Case summary in table format (always show)
    story.append(Paragraph("<b>TÓM TẮT CA BỆNH</b>", section_style))
    case_summary_text = case.case_summary or 'Chưa có dữ liệu'
    summary_table = Table([[case_summary_text]], colWidths=[16*cm])
    summary_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), base_font, 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Chief complaint in table format (always show)
    story.append(Paragraph("<b>LÝ DO KHÁM</b>", section_style))
    chief_complaint_text = case.chief_complaint_brief or 'Chưa có dữ liệu'
    chief_table = Table([[chief_complaint_text]], colWidths=[16*cm])
    chief_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), base_font, 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(chief_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Medical sections - ALWAYS show all fields
    if hasattr(case, 'clinical_history'):
        story.append(Paragraph("<b>TIỀN SỬ BỆNH</b>", section_style))
        clinical_data = [
            ['Lý do khám:', case.clinical_history.chief_complaint or 'Chưa có dữ liệu'],
            ['Bệnh sử:', case.clinical_history.history_present_illness or 'Chưa có dữ liệu'],
            ['Tiền sử bệnh:', case.clinical_history.past_medical_history or 'Chưa có dữ liệu'],
            ['Tiền sử gia đình:', case.clinical_history.family_history or 'Chưa có dữ liệu'],
            ['Tiền sử xã hội:', case.clinical_history.social_history or 'Chưa có dữ liệu'],
            ['Dị ứng:', case.clinical_history.allergies or 'Chưa có dữ liệu'],
            ['Thuốc đang dùng:', case.clinical_history.medications or 'Chưa có dữ liệu'],
        ]
    else:
        story.append(Paragraph("<b>TIỀN SỬ BỆNH</b>", section_style))
        clinical_data = [
            ['Lý do khám:', 'Chưa có dữ liệu'],
            ['Bệnh sử:', 'Chưa có dữ liệu'],
            ['Tiền sử bệnh:', 'Chưa có dữ liệu'],
            ['Tiền sử gia đình:', 'Chưa có dữ liệu'],
            ['Tiền sử xã hội:', 'Chưa có dữ liệu'],
            ['Dị ứng:', 'Chưa có dữ liệu'],
            ['Thuốc đang dùng:', 'Chưa có dữ liệu'],
        ]
    
    clinical_table = Table(clinical_data, colWidths=[4.5*cm, 11.5*cm])
    clinical_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), bold_font, 10),
        ('FONT', (1, 0), (1, -1), base_font, 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e9ecef')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(clinical_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Physical examination - ALWAYS show all fields
    if hasattr(case, 'physical_examination'):
        story.append(Paragraph("<b>KHÁM LÂM SÀNG</b>", section_style))
        exam_data = [
            ['Tình trạng chung:', case.physical_examination.general_appearance or 'Chưa có dữ liệu'],
            ['Dấu hiệu sinh tồn:', case.physical_examination.vital_signs or 'Chưa có dữ liệu'],
            ['Đầu - Cổ:', case.physical_examination.head_neck or 'Chưa có dữ liệu'],
            ['Tim mạch:', case.physical_examination.cardiovascular or 'Chưa có dữ liệu'],
            ['Hô hấp:', case.physical_examination.respiratory or 'Chưa có dữ liệu'],
            ['Bụng:', case.physical_examination.abdominal or 'Chưa có dữ liệu'],
            ['Thần kinh:', case.physical_examination.neurological or 'Chưa có dữ liệu'],
            ['Cơ xương khớp:', case.physical_examination.musculoskeletal or 'Chưa có dữ liệu'],
            ['Da:', case.physical_examination.skin or 'Chưa có dữ liệu'],
        ]
    else:
        story.append(Paragraph("<b>KHÁM LÂM SÀNG</b>", section_style))
        exam_data = [
            ['Tình trạng chung:', 'Chưa có dữ liệu'],
            ['Dấu hiệu sinh tồn:', 'Chưa có dữ liệu'],
            ['Đầu - Cổ:', 'Chưa có dữ liệu'],
            ['Tim mạch:', 'Chưa có dữ liệu'],
            ['Hô hấp:', 'Chưa có dữ liệu'],
            ['Bụng:', 'Chưa có dữ liệu'],
            ['Thần kinh:', 'Chưa có dữ liệu'],
            ['Cơ xương khớp:', 'Chưa có dữ liệu'],
            ['Da:', 'Chưa có dữ liệu'],
        ]
    
    exam_table = Table(exam_data, colWidths=[4.5*cm, 11.5*cm])
    exam_table.setStyle(TableStyle([
                ('FONT', (0, 0), (0, -1), bold_font, 10),
                ('FONT', (1, 0), (1, -1), base_font, 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e9ecef')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
    story.append(exam_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Diagnosis and management - ALWAYS show all fields
    if hasattr(case, 'diagnosis_management'):
        story.append(Paragraph("<b>CHẨN ĐOÁN VÀ ĐIỀU TRỊ</b>", section_style))
        diagnosis_data = [
            ['Chẩn đoán chính:', case.diagnosis_management.primary_diagnosis or 'Chưa có dữ liệu'],
            ['Chẩn đoán phân biệt:', case.diagnosis_management.differential_diagnosis or 'Chưa có dữ liệu'],
            ['Kế hoạch điều trị:', case.diagnosis_management.treatment_plan or 'Chưa có dữ liệu'],
            ['Thuốc điều trị:', case.diagnosis_management.medications_prescribed or 'Chưa có dữ liệu'],
            ['Thủ thuật:', case.diagnosis_management.procedures_performed or 'Chưa có dữ liệu'],
            ['Tiên lượng:', case.diagnosis_management.prognosis or 'Chưa có dữ liệu'],
            ['Theo dõi:', case.diagnosis_management.follow_up_plan or 'Chưa có dữ liệu'],
        ]
    else:
        story.append(Paragraph("<b>CHẨN ĐOÁN VÀ ĐIỀU TRỊ</b>", section_style))
        diagnosis_data = [
            ['Chẩn đoán chính:', 'Chưa có dữ liệu'],
            ['Chẩn đoán phân biệt:', 'Chưa có dữ liệu'],
            ['Kế hoạch điều trị:', 'Chưa có dữ liệu'],
            ['Thuốc điều trị:', 'Chưa có dữ liệu'],
            ['Thủ thuật:', 'Chưa có dữ liệu'],
            ['Tiên lượng:', 'Chưa có dữ liệu'],
            ['Theo dõi:', 'Chưa có dữ liệu'],
        ]
    
    diagnosis_table = Table(diagnosis_data, colWidths=[4.5*cm, 11.5*cm])
    diagnosis_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), bold_font, 10),
        ('FONT', (1, 0), (1, -1), base_font, 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e9ecef')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(diagnosis_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Attachments section with embedded images
    story.append(Paragraph("<b>FILE ĐÍNH KÈM</b>", section_style))
    attachments = case.medical_attachments.all()
    
    if attachments.exists():
        for idx, att in enumerate(attachments, 1):
            # Format file size
            size_mb = att.file_size / (1024 * 1024) if att.file_size else 0
            if size_mb < 1:
                size_str = f"{att.file_size / 1024:.1f} KB" if att.file_size else "N/A"
            else:
                size_str = f"{size_mb:.2f} MB"
            
            # Get attachment type display
            type_map = {
                'xray': 'X-quang',
                'ct_scan': 'CT',
                'mri': 'MRI',
                'ultrasound': 'Siêu âm',
                'ecg': 'ECG',
                'lab_report': 'XN phòng thí nghiệm',
                'blood_test': 'XN máu',
                'urine_test': 'XN nước tiểu',
                'pathology': 'Giải phẫu bệnh',
                'injury_photo': 'Ảnh chấn thương',
                'surgical_photo': 'Ảnh phẫu thuật',
                'endoscopy': 'Nội soi',
                'prescription': 'Đơn thuốc',
                'discharge_summary': 'Giấy ra viện',
                'consent_form': 'Phiếu đồng ý',
                'other': 'Khác'
            }
            type_display = type_map.get(att.attachment_type, att.attachment_type)
            uploader_name = att.uploaded_by.get_full_name() if att.uploaded_by else 'N/A'
            
            # Attachment info table
            att_info = [
                ['STT:', str(idx)],
                ['Tên file:', att.title or 'Không có tên'],
                ['Loại:', type_display],
                ['Kích thước:', size_str],
                ['Người tải lên:', uploader_name],
            ]
            
            att_info_table = Table(att_info, colWidths=[3*cm, 13*cm])
            att_info_table.setStyle(TableStyle([
                ('FONT', (0, 0), (0, -1), bold_font, 9),
                ('FONT', (1, 0), (1, -1), base_font, 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e9ecef')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(att_info_table)
            story.append(Spacer(1, 0.2*cm))
            
            # Try to embed image if it's an image file
            try:
                file_path = att.file.path
                file_ext = file_path.lower().split('.')[-1]
                
                if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
                    # Embed the actual image
                    img = RLImage(file_path)
                    # Scale image to fit page width (max 15cm)
                    max_width = 15*cm
                    max_height = 10*cm
                    
                    aspect = img.imageHeight / img.imageWidth
                    if img.imageWidth > max_width:
                        img.drawWidth = max_width
                        img.drawHeight = max_width * aspect
                    else:
                        img.drawWidth = img.imageWidth * 0.5
                        img.drawHeight = img.imageHeight * 0.5
                    
                    if img.drawHeight > max_height:
                        img.drawHeight = max_height
                        img.drawWidth = max_height / aspect
                    
                    story.append(img)
                    story.append(Spacer(1, 0.3*cm))
                elif file_ext == 'pdf':
                    # For PDF files, try to convert to images
                    try:
                        from pdf2image import convert_from_path
                        from PIL import Image as PILImage
                        import tempfile
                        
                        # Convert PDF pages to images
                        images = convert_from_path(file_path, dpi=150, first_page=1, last_page=5)  # Limit to 5 pages
                        
                        for page_num, pil_img in enumerate(images, 1):
                            # Save to temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                                pil_img.save(tmp.name, 'PNG')
                                tmp_path = tmp.name
                            
                            # Add page label
                            page_label = Paragraph(
                                f"<i>Trang {page_num}:</i>",
                                normal_style
                            )
                            story.append(page_label)
                            story.append(Spacer(1, 0.1*cm))
                            
                            # Embed the page image
                            img = RLImage(tmp_path)
                            max_width = 15*cm
                            max_height = 18*cm
                            
                            aspect = img.imageHeight / img.imageWidth
                            img.drawWidth = max_width
                            img.drawHeight = max_width * aspect
                            
                            if img.drawHeight > max_height:
                                img.drawHeight = max_height
                                img.drawWidth = max_height / aspect
                            
                            story.append(img)
                            story.append(Spacer(1, 0.3*cm))
                            
                            # Clean up temp file
                            try:
                                os.unlink(tmp_path)
                            except:
                                pass
                                
                    except ImportError:
                        # pdf2image not available, show info box
                        pdf_info = Paragraph(
                            f"<b>File PDF đính kèm</b><br/>"
                            f"Tên: {att.title}<br/>"
                            f"Kích thước: {size_str}<br/>"
                            f"<i>Để xem nội dung PDF, vui lòng tải file từ hệ thống</i>",
                            normal_style
                        )
                        pdf_box = Table([[pdf_info]], colWidths=[15*cm])
                        pdf_box.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
                            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#ffc107')),
                            ('TOPPADDING', (0, 0), (-1, -1), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                            ('LEFTPADDING', (0, 0), (-1, -1), 10),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                        ]))
                        story.append(pdf_box)
                        story.append(Spacer(1, 0.3*cm))
                    except Exception as pdf_err:
                        # Error converting PDF
                        error_note = Paragraph(
                            f"<i>Không thể hiển thị file PDF: {str(pdf_err)}</i>",
                            normal_style
                        )
                        story.append(error_note)
                        story.append(Spacer(1, 0.3*cm))
            except Exception as e:
                # If can't embed, just continue
                note = Paragraph(
                    f"<i>Không thể hiển thị file đính kèm</i>",
                    normal_style
                )
                story.append(note)
                story.append(Spacer(1, 0.3*cm))
    else:
        no_attachment_table = Table([['Không có file đính kèm']], colWidths=[16*cm])
        no_attachment_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), base_font, 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(no_attachment_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

