"""
Heading Matcher - Vietnamese SBERT Semantic Matching for OCR Auto-Fill

This module uses the Vietnamese SBERT model to match OCR-extracted headings
to case template fields using semantic similarity.

Usage:
    matcher = HeadingMatcher()
    field, confidence = matcher.match_heading("Họ và tên")
    # Returns: ("patient_name", 0.95)
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Any
import numpy as np

logger = logging.getLogger(__name__)

# Lazy imports to avoid loading heavy models at module import
_matcher_instance = None


# Field mappings: template_field -> list of Vietnamese heading variations
FIELD_MAPPINGS: Dict[str, List[str]] = {
    # Basic Patient Info
    "patient_name": ["Họ và tên", "Tên bệnh nhân", "Họ tên", "HỌ VÀ TÊN"],
    "patient_age": ["Tuổi", "Năm sinh", "Age"],
    "patient_gender": ["Giới tính", "Giới", "Nam/Nữ"],
    "patient_ethnicity": ["Dân tộc", "Ethnicity"],
    "patient_occupation": ["Nghề nghiệp", "Occupation"],
    "medical_record_number": ["Mã số bệnh án", "Số hồ sơ", "MSV", "Mã bệnh nhân"],
    "admission_date": ["Ngày vào viện", "Ngày nhập viện", "Admission date"],
    "discharge_date": ["Ngày ra viện", "Ngày xuất viện", "Discharge date"],
    
    # Clinical History
    "clinical_history.chief_complaint": [
        "Lý do vào viện", "Triệu chứng chính", "Chief complaint",
        "Lý do đến khám", "Lý do nhập viện"
    ],
    "clinical_history.history_present_illness": [
        "Bệnh sử", "Diễn biến bệnh", "History of present illness",
        "Quá trình bệnh lý", "Bệnh sử hiện tại"
    ],
    "clinical_history.past_medical_history": [
        "Tiền sử", "Tiền sử bản thân", "Tiền sử bệnh",
        "Past medical history", "Bệnh lý nền"
    ],
    "clinical_history.family_history": [
        "Tiền sử gia đình", "Family history", "Gia đình"
    ],
    "clinical_history.social_history": [
        "Tiền sử xã hội", "Social history", "Lối sống"
    ],
    "clinical_history.medications": [
        "Thuốc đang dùng", "Medications", "Thuốc", "Đang dùng thuốc"
    ],
    "clinical_history.allergies": [
        "Dị ứng", "Allergies", "Tiền sử dị ứng"
    ],
    "clinical_history.surgical_history": [
        "Tiền sử phẫu thuật", "Surgical history", "Phẫu thuật"
    ],
    
    # Physical Examination
    "physical_examination.general_appearance": [
        "Khám toàn trạng", "Toàn trạng", "General appearance",
        "Tình trạng chung", "Khám tổng quát"
    ],
    "physical_examination.vital_signs": [
        "Sinh hiệu", "Dấu hiệu sinh tồn", "Vital signs",
        "Mạch, huyết áp, nhiệt độ"
    ],
    "physical_examination.cardiovascular": [
        "Tim mạch", "Khám tim", "Cardiovascular", "Tuần hoàn"
    ],
    "physical_examination.respiratory": [
        "Hô hấp", "Khám phổi", "Respiratory", "Phổi"
    ],
    "physical_examination.abdominal": [
        "Bụng", "Khám bụng", "Abdominal", "Tiêu hóa"
    ],
    "physical_examination.neurological": [
        "Thần kinh", "Khám thần kinh", "Neurological"
    ],
    "physical_examination.head_neck": [
        "Đầu cổ", "Khám đầu cổ", "Head and neck"
    ],
    
    # Investigations
    "detailed_investigations.laboratory_results": [
        "Xét nghiệm", "Kết quả xét nghiệm", "Laboratory", "Cận lâm sàng"
    ],
    "detailed_investigations.imaging_studies": [
        "Chẩn đoán hình ảnh", "X-quang", "CT", "MRI", "Siêu âm"
    ],
    "detailed_investigations.ecg_findings": [
        "Điện tâm đồ", "ECG", "EKG", "Điện tim"
    ],
    
    # Diagnosis & Management
    "diagnosis_management.primary_diagnosis": [
        "Chẩn đoán", "Chẩn đoán xác định", "Chẩn đoán chính",
        "Primary diagnosis", "Diagnosis"
    ],
    "diagnosis_management.differential_diagnosis": [
        "Chẩn đoán phân biệt", "Differential diagnosis"
    ],
    "diagnosis_management.treatment_plan": [
        "Điều trị", "Phương pháp điều trị", "Treatment plan",
        "Hướng điều trị", "Kế hoạch điều trị"
    ],
    "diagnosis_management.medications_prescribed": [
        "Thuốc điều trị", "Đơn thuốc", "Medications prescribed"
    ],
    "diagnosis_management.prognosis": [
        "Tiên lượng", "Prognosis"
    ],
    
    # Case Summary
    "case_summary": [
        "Tóm tắt bệnh án", "Tóm tắt", "Case summary", "Summary"
    ],
}


class HeadingMatcher:
    """
    Matches OCR-extracted headings to case template fields using
    Vietnamese SBERT semantic similarity.
    """
    
    def __init__(self, confidence_threshold: float = 0.6):
        """
        Initialize the matcher with Vietnamese SBERT model.
        
        Args:
            confidence_threshold: Minimum similarity score for a match (0-1)
        """
        self.confidence_threshold = confidence_threshold
        self._model = None
        self._field_embeddings = None
        self._field_names: List[str] = []
        self._heading_texts: List[str] = []
        
    def _ensure_model_loaded(self):
        """Lazy-load the SBERT model."""
        if self._model is not None:
            return
        
        import os
        # Force CPU to avoid CUDA compatibility issues with torch versions
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        
        try:
            from sentence_transformers import SentenceTransformer
            
            logger.info("Loading Vietnamese SBERT model (CPU mode)...")
            self._model = SentenceTransformer(
                'keepitreal/vietnamese-sbert',
                device='cpu'  # Force CPU to avoid CUDA issues
            )
            logger.info("Vietnamese SBERT loaded on CPU")
                
            # Pre-compute embeddings for all field headings
            self._precompute_embeddings()
            
        except Exception as e:
            logger.error(f"Failed to load Vietnamese SBERT: {e}")
            raise
    
    def _precompute_embeddings(self):
        """Pre-compute embeddings for all field heading variations."""
        self._field_names = []
        self._heading_texts = []
        
        # Flatten the field mappings
        for field_name, headings in FIELD_MAPPINGS.items():
            for heading in headings:
                self._field_names.append(field_name)
                self._heading_texts.append(heading)
        
        # Encode all headings
        logger.info(f"Pre-computing embeddings for {len(self._heading_texts)} heading variations...")
        self._field_embeddings = self._model.encode(
            self._heading_texts,
            convert_to_tensor=True,
            show_progress_bar=False
        )
        logger.info("Heading embeddings pre-computed")
    
    def match_heading(self, heading: str) -> Tuple[Optional[str], float]:
        """
        Match a heading to the best template field.
        
        Args:
            heading: The heading text from OCR (e.g., "Họ và tên")
            
        Returns:
            Tuple of (field_name, confidence_score) or (None, 0.0) if no match
        """
        self._ensure_model_loaded()
        
        from sentence_transformers import util
        
        # Encode the input heading
        heading_embedding = self._model.encode(
            heading,
            convert_to_tensor=True,
            show_progress_bar=False
        )
        
        # Compute cosine similarity with all field headings
        similarities = util.cos_sim(heading_embedding, self._field_embeddings)[0]
        
        # Find best match
        best_idx = similarities.argmax().item()
        best_score = float(similarities[best_idx])
        
        if best_score >= self.confidence_threshold:
            return self._field_names[best_idx], best_score
        else:
            return None, best_score
    
    def match_all_headings(
        self, 
        headings: List[str]
    ) -> Dict[str, Tuple[str, float]]:
        """
        Match multiple headings at once (more efficient).
        
        Args:
            headings: List of heading texts
            
        Returns:
            Dict mapping heading -> (field_name, confidence)
        """
        self._ensure_model_loaded()
        
        from sentence_transformers import util
        
        if not headings:
            return {}
        
        # Batch encode all headings
        heading_embeddings = self._model.encode(
            headings,
            convert_to_tensor=True,
            show_progress_bar=False
        )
        
        # Compute similarities for all at once
        similarities = util.cos_sim(heading_embeddings, self._field_embeddings)
        
        results = {}
        for i, heading in enumerate(headings):
            best_idx = similarities[i].argmax().item()
            best_score = float(similarities[i][best_idx])
            
            if best_score >= self.confidence_threshold:
                results[heading] = (self._field_names[best_idx], best_score)
            else:
                results[heading] = (None, best_score)
        
        return results


def extract_headings_from_text(ocr_text: str) -> List[Tuple[str, str]]:
    """
    Extract (heading, content) pairs from OCR text.
    
    Patterns matched:
    - "1. Họ và tên: Nguyễn Văn A"
    - "Họ và tên: Nguyễn Văn A"
    - "II. Bệnh sử"
    - "a. Tiền sử bản thân"
    
    Args:
        ocr_text: The full OCR text output
        
    Returns:
        List of (heading, content) tuples
    """
    results = []
    lines = ocr_text.split('\n')
    
    # Patterns for heading detection
    patterns = [
        # "1. Heading: content" or "1. Heading"
        r'^(\d+)\.\s*([^:]+)(?::\s*(.*))?$',
        # "a. Heading: content" or "a. Heading"
        r'^([a-z])\.\s*([^:]+)(?::\s*(.*))?$',
        # "II. Heading" (Roman numerals)
        r'^([IVX]+)\.\s*([^:]+)(?::\s*(.*))?$',
        # "Heading: content"
        r'^([A-ZÀ-Ỹa-zà-ỹ\s]+):\s*(.+)$',
        # "EPA 1: Heading"
        r'^(EPA\s*\d+):\s*(.+)$',
    ]
    
    current_heading = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        matched = False
        for pattern in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                # Save previous heading/content
                if current_heading:
                    content = '\n'.join(current_content).strip()
                    if content:
                        results.append((current_heading, content))
                
                groups = match.groups()
                if len(groups) == 3:
                    # Pattern with prefix, heading, content
                    current_heading = groups[1].strip()
                    current_content = [groups[2]] if groups[2] else []
                elif len(groups) == 2:
                    # Pattern with heading, content
                    current_heading = groups[0].strip()
                    current_content = [groups[1]] if groups[1] else []
                else:
                    current_heading = groups[0].strip()
                    current_content = []
                
                matched = True
                break
        
        if not matched and current_heading:
            # Continue accumulating content for current heading
            current_content.append(line)
    
    # Don't forget the last heading
    if current_heading:
        content = '\n'.join(current_content).strip()
        if content:
            results.append((current_heading, content))
    
    return results


def autofill_from_ocr(
    ocr_text: str,
    confidence_threshold: float = 0.6
) -> Dict[str, Any]:
    """
    Main entry point: Extract structured data from OCR text.
    
    Args:
        ocr_text: The OCR-extracted text
        confidence_threshold: Minimum match confidence (0-1)
        
    Returns:
        Dict with structure matching the case template, e.g.:
        {
            "patient_name": {"value": "...", "confidence": 0.95},
            "clinical_history": {
                "chief_complaint": {"value": "...", "confidence": 0.88}
            }
        }
    """
    global _matcher_instance
    
    # Get or create singleton matcher
    if _matcher_instance is None:
        _matcher_instance = HeadingMatcher(confidence_threshold)
    
    # Extract headings from text
    heading_pairs = extract_headings_from_text(ocr_text)
    
    if not heading_pairs:
        logger.warning("No headings extracted from OCR text")
        return {}
    
    # Match all headings at once (efficient batch processing)
    headings = [h[0] for h in heading_pairs]
    matches = _matcher_instance.match_all_headings(headings)
    
    # Build structured result
    result: Dict[str, Any] = {}
    
    for heading, content in heading_pairs:
        field_name, confidence = matches.get(heading, (None, 0.0))
        
        if field_name is None:
            continue
        
        # Handle nested fields (e.g., "clinical_history.chief_complaint")
        if '.' in field_name:
            parts = field_name.split('.')
            parent = parts[0]
            child = parts[1]
            
            if parent not in result:
                result[parent] = {}
            
            result[parent][child] = {
                "value": content,
                "confidence": round(confidence, 3),
                "matched_heading": heading
            }
        else:
            result[field_name] = {
                "value": content,
                "confidence": round(confidence, 3),
                "matched_heading": heading
            }
    
    return result


def prewarm_matcher():
    """Pre-load the matcher model at startup."""
    global _matcher_instance
    logger.info("Pre-warming HeadingMatcher...")
    _matcher_instance = HeadingMatcher()
    _matcher_instance._ensure_model_loaded()
    logger.info("HeadingMatcher pre-warmed")
