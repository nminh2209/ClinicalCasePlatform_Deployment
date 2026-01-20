"""
OCR Service - Hybrid Pipeline Implementation

Two detection engines available (set via OCR_ENGINE env var):
- PPSTRUCTURE: Layout analysis with tables (slower, CPU-bound)
- DOCTR: Fast text detection only (GPU-accelerated, ~3-5x faster)

Recognition: VietOCR (GPU) for both engines.

Default is DOCTR for speed. Use PPSTRUCTURE if table extraction is needed.
"""

import os
import time
import logging
import threading
import tempfile
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from django.conf import settings

# Pillow 10.0+ compatibility fix
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

logger = logging.getLogger(__name__)

# Global lock to prevent concurrent access if needed
_ocr_lock = threading.Lock()

# Engine selection: DOCTR (fast, GPU) or PPSTRUCTURE (with tables, CPU)
OCR_ENGINE = os.environ.get('OCR_ENGINE', 'DOCTR').upper()
logger.info(f"OCR Engine: {OCR_ENGINE}")



class OCRService:
    """
    Singleton OCR Service with two detection engines:
    - DOCTR: Fast GPU-based detection (default)
    - PPSTRUCTURE: Layout analysis with table extraction
    """
    _instance = None
    _layout_engine = None
    _det_model = None
    _vietocr_recognizer = None
    _doctr_detector = None  # DocTR detection model

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRService, cls).__new__(cls)
        return cls._instance

    def _get_layout_engine(self):
        """Lazy init table recognition pipeline for layout analysis.
        
        Uses PaddleX `table_recognition` pipeline instead of PPStructureV3.
        This is MUCH lighter (~200MB vs ~3GB) and doesn't crash the system.
        
        Models loaded:
        - SLANet_plus (table structure)
        - PP-OCRv4_server_det (detection)
        - PP-OCRv4_server_rec_doc (recognition)
        """
        if self._layout_engine is None:
            logger.info("Initializing PaddleX Table Recognition Pipeline...")
            try:
                # Clear GPU cache before loading
                import gc
                gc.collect()
                try:
                    import paddle
                    paddle.device.cuda.empty_cache()
                except:
                    pass
                
                from paddlex import create_pipeline
                
                # Use lighter table_recognition pipeline instead of PPStructureV3
                # This avoids loading PP-Chart2Table (1.4GB) and other heavy models
                self._layout_engine = create_pipeline(
                    pipeline="table_recognition",
                    device="gpu:0",  # Use GPU, fallback to CPU if OOM
                )
                logger.info("✅ PaddleX Table Recognition Pipeline Ready")
            except Exception as e:
                logger.error(f"Failed to load table recognition pipeline: {e}")
                # Try CPU fallback
                try:
                    logger.info("Trying CPU fallback...")
                    from paddlex import create_pipeline
                    self._layout_engine = create_pipeline(
                        pipeline="table_recognition",
                        device="cpu",
                    )
                    logger.info("✅ PaddleX Table Recognition Pipeline Ready (CPU)")
                except Exception as e2:
                    logger.error(f"CPU fallback also failed: {e2}")
                    raise
        return self._layout_engine

    def _get_detector(self):
        """Lazy init PaddleOCR for line splitting in tall blocks."""
        if self._det_model is None:
            logger.info("Initializing PaddleOCR (Detection)...")
            try:
                from paddleocr import PaddleOCR
                self._det_model = PaddleOCR(use_textline_orientation=False, lang='en')
                logger.info("✅ PaddleOCR (Detection) Ready")
            except Exception as e:
                logger.error(f"Failed to load PaddleOCR: {e}")
                raise
        return self._det_model

    def _get_recognizer(self):
        """Lazy init VietOCR for text recognition (GPU-accelerated)."""
        if self._vietocr_recognizer is None:
            logger.info("Initializing VietOCR (Recognition)...")
            try:
                from vietocr.tool.predictor import Predictor
                from vietocr.tool.config import Cfg
                import torch
                
                config = Cfg.load_config_from_name('vgg_transformer')
                config['cnn']['pretrained'] = False
                config['predictor']['beamsearch'] = False
                
                # Use GPU if available (ASR is now lazy-loaded, so GPU is free)
                use_cuda = torch.cuda.is_available()
                config['device'] = 'cuda' if use_cuda else 'cpu'
                logger.info(f"VietOCR device: {'CUDA' if use_cuda else 'CPU'}")
                
                self._vietocr_recognizer = Predictor(config)
                # Note: FP16 removed - VietOCR predictor doesn't handle half precision inputs
                
                logger.info("✅ VietOCR (Recognition) Ready")
            except Exception as e:
                logger.error(f"Failed to load VietOCR: {e}")
                raise
        return self._vietocr_recognizer

    def _get_doctr_detector(self):
        """Lazy init DocTR for fast GPU text detection."""
        if self._doctr_detector is None:
            logger.info("Initializing DocTR (Detection - GPU)...")
            try:
                import torch
                from doctr.models import detection_predictor
                
                # Use db_resnet50 - good balance of speed and accuracy
                self._doctr_detector = detection_predictor(arch='db_resnet50', pretrained=True)
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self._doctr_detector = self._doctr_detector.cuda()
                    logger.info("✅ DocTR (Detection) on GPU")
                else:
                    logger.info("✅ DocTR (Detection) on CPU")
            except Exception as e:
                logger.error(f"Failed to load DocTR: {e}")
                raise
        return self._doctr_detector

    def has_layout_elements(self, file_path, mime_type=None):
        """
        Quick preprocessing check: Does this document contain tables or images?
        
        Returns:
            dict: {
                "has_tables": bool,
                "has_images": bool,
                "table_count": int,
                "image_count": int,
                "should_extract": bool  # True if tables OR images found
            }
        """
        import time
        start = time.time()
        
        try:
            # Convert to images for analysis
            images = self._convert_to_images(file_path, max_pages=3)  # Check first 3 pages max (fast)
            
            if not images:
                return {
                    "has_tables": False,
                    "has_images": False,
                    "table_count": 0,
                    "image_count": 0,
                    "should_extract": False
                }
            
            # Use PaddleX layout detection for fast check
            pipeline = self._get_layout_engine()
            
            table_count = 0
            image_count = 0
            
            for img in images:
                try:
                    # Run table recognition pipeline
                    for result in pipeline.predict(img):
                        # Check for table HTML output (indicates tables found)
                        if hasattr(result, 'html') and result.html:
                            # html is a dict mapping table IDs to HTML strings
                            table_count += len(result.html)
                        
                        # Check for figure/image regions in layout detection
                        if hasattr(result, 'json') and result.json:
                            res = result.json.get('res', {})
                            layout_det = res.get('layout_det_res', {})
                            boxes = layout_det.get('boxes', [])
                            
                            for box in boxes:
                                label = box.get('label', '').lower()
                                if 'figure' in label or 'image' in label or 'chart' in label:
                                    image_count += 1
                except Exception as e:
                    logger.warning(f"Layout check failed for page: {e}")
                    continue
            
            elapsed = time.time() - start
            logger.info(f"Layout preprocessing: {table_count} tables, {image_count} images in {elapsed:.2f}s")
            
            return {
                "has_tables": table_count > 0,
                "has_images": image_count > 0,
                "table_count": table_count,
                "image_count": image_count,
                "should_extract": table_count > 0 or image_count > 0
            }
            
        except Exception as e:
            logger.error(f"Layout preprocessing failed: {e}")
            # On error, default to running extraction (fail-safe)
            return {
                "has_tables": True,
                "has_images": True,
                "table_count": 0,
                "image_count": 0,
                "should_extract": True  # Default to extraction on error
            }

    def process(self, file_path, mime_type=None, max_pages=None):
        """Main entry point for OCR processing."""
        start_time = time.time()
        
        try:
            images = self._convert_to_images(file_path, max_pages)
        except Exception as e:
            logger.error(f"File conversion failed: {e}")
            raise ValueError(f"Could not convert file: {str(e)}")

        full_text = []
        page_results = []
        
        # Load models based on engine selection
        recognizer = self._get_recognizer()
        
        if OCR_ENGINE == 'DOCTR':
            # Fast GPU-based detection with DocTR
            detector = self._get_doctr_detector()
            engine_name = "DocTR+VietOCR (GPU)"
            process_fn = lambda img, pn: self._process_page_doctr(detector, recognizer, img, pn)
        else:
            # Full layout analysis with PPStructure (includes tables)
            layout_engine = self._get_layout_engine()
            det_model = self._get_detector()
            engine_name = "PPStructure+VietOCR"
            process_fn = lambda img, pn: self._process_page(layout_engine, det_model, recognizer, img, pn)

        # Parallel page processing for multi-page documents
        # Limited to 2 workers to avoid GPU memory contention
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        num_pages = len(images)
        max_workers = min(2, num_pages)  # Cap at 2 workers for GPU safety
        
        with _ocr_lock:
            if num_pages == 1:
                # Single page: no threading overhead
                logger.info(f"Processing 1 page with {OCR_ENGINE}...")
                try:
                    page_data = process_fn(images[0], 1)
                    page_results.append(page_data)
                    if page_data.get('plain_text'):
                        full_text.append(page_data['plain_text'])
                except Exception as e:
                    logger.error(f"Error processing page 1: {e}", exc_info=True)
            else:
                # Multi-page: parallel processing
                logger.info(f"Processing {num_pages} pages with {OCR_ENGINE} ({max_workers} workers)...")
                page_results = [None] * num_pages
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {
                        executor.submit(process_fn, img, i+1): i 
                        for i, img in enumerate(images)
                    }
                    
                    for future in as_completed(futures):
                        idx = futures[future]
                        try:
                            page_data = future.result()
                            page_results[idx] = page_data
                            logger.info(f"✅ Page {idx+1}/{num_pages} complete")
                        except Exception as e:
                            logger.error(f"Error processing page {idx+1}: {e}", exc_info=True)
                            page_results[idx] = {"page_num": idx+1, "plain_text": "", "error": str(e)}
                
                # Collect text in page order
                for page in page_results:
                    if page and page.get('plain_text'):
                        full_text.append(page['plain_text'])

        elapsed = int((time.time() - start_time) * 1000)
        
        # Compute hints for table/image presence based on page analysis
        hints = self._compute_content_hints(page_results)
        
        return {
            "text": "\n\n".join(full_text),
            "pages": [p for p in page_results if p],  # Filter out None
            "structured": {},
            "hints": hints,  # Hints for table/image presence
            "metadata": {
                "page_count": len(images),
                "elapsed_ms": elapsed,
                "engine": engine_name,
                "parallel_workers": max_workers if num_pages > 1 else 1
            }
        }
    
    def _compute_content_hints(self, page_results):
        """
        Analyze page results to detect if tables or images might be present.
        
        NOTE: Heuristic detection was too aggressive (many false positives).
        For now, always return False - let user explicitly choose full mode
        only when they know the document has tables/images.
        
        Future improvement: Use layout detection model for accurate hints.
        
        Returns:
            dict with has_table_hint and has_image_hint booleans
        """
        # Disabled for now - heuristic had too many false positives
        # Page 1 triggered table=True but had 0 actual tables
        return {
            "has_table_hint": False,  # Always false - let user decide
            "has_image_hint": False,  # Can't detect from DocTR
            "confidence": "disabled"  # Heuristic disabled
        }

    def _process_page_doctr(self, detector, recognizer, img, page_num=1):
        """
        Process a single page using DocTR detection + VietOCR recognition.
        This is the fast GPU-accelerated path (no table extraction).
        
        Pipeline:
        1. Run DocTR detection to get text bounding boxes
        2. Sort boxes by reading order (top-to-bottom, left-to-right)
        3. Crop each box and recognize with VietOCR
        4. Combine into structured output
        """
        import torch
        
        # Convert to numpy if needed
        img_np = np.array(img) if not isinstance(img, np.ndarray) else img
        pil_img = Image.fromarray(img_np) if isinstance(img_np, np.ndarray) else img
        
        h, w = img_np.shape[:2]
        
        # Run DocTR detection
        # detection_predictor returns list of dicts, each with 'words' array
        # Each word is [x1_rel, y1_rel, x2_rel, y2_rel, confidence]
        with torch.no_grad():
            detection_result = detector([img_np])
        
        # Extract boxes from detection result
        text_regions = []
        
        if detection_result and len(detection_result) > 0:
            page_result = detection_result[0]
            words = page_result.get('words', np.array([]))
            
            for box in words:
                if len(box) >= 4:
                    x1_rel, y1_rel, x2_rel, y2_rel = box[:4]
                    
                    # Convert relative coords to absolute pixels
                    x1, y1 = int(x1_rel * w), int(y1_rel * h)
                    x2, y2 = int(x2_rel * w), int(y2_rel * h)
                    
                    # Add padding for better recognition
                    pad = 3
                    x1 = max(0, x1 - pad)
                    y1 = max(0, y1 - pad)
                    x2 = min(w, x2 + pad)
                    y2 = min(h, y2 + pad)
                    
                    # Ensure valid box dimensions
                    if x2 > x1 + 5 and y2 > y1 + 5:
                        text_regions.append({
                            'bbox': (x1, y1, x2, y2),
                            'y_center': (y1 + y2) / 2,
                            'x_center': (x1 + x2) / 2
                        })

        
        # Merge word boxes into lines for faster recognition
        # Group words with similar y_center (within tolerance) into lines
        merged_lines = []
        
        if text_regions:
            # Sort by y_center first, then x_center
            text_regions.sort(key=lambda r: (r['y_center'], r['x_center']))
            
            # Group into lines based on vertical overlap
            line_tolerance = 15  # pixels
            current_line = [text_regions[0]] if text_regions else []
            
            for region in text_regions[1:]:
                # Check if this region is on the same line as current
                last_y = current_line[-1]['y_center']
                if abs(region['y_center'] - last_y) <= line_tolerance:
                    current_line.append(region)
                else:
                    # Start new line, merge and save current
                    if current_line:
                        # Merge boxes in current line
                        x1 = min(r['bbox'][0] for r in current_line)
                        y1 = min(r['bbox'][1] for r in current_line)
                        x2 = max(r['bbox'][2] for r in current_line)
                        y2 = max(r['bbox'][3] for r in current_line)
                        merged_lines.append((x1, y1, x2, y2))
                    current_line = [region]
            
            # Don't forget last line
            if current_line:
                x1 = min(r['bbox'][0] for r in current_line)
                y1 = min(r['bbox'][1] for r in current_line)
                x2 = max(r['bbox'][2] for r in current_line)
                y2 = max(r['bbox'][3] for r in current_line)
                merged_lines.append((x1, y1, x2, y2))
        
        logger.info(f"DocTR: {len(text_regions)} words merged to {len(merged_lines)} lines")
        
        # Recognize each merged line with VietOCR (much fewer calls!)
        recognized_lines = []
        regions_data = []
        
        for (x1, y1, x2, y2) in merged_lines:
            # Skip very thin lines
            if (x2 - x1) < 10 or (y2 - y1) < 8:
                continue
            
            # Crop and recognize the full line
            crop = pil_img.crop((x1, y1, x2, y2))
            
            try:
                text = recognizer.predict(crop)
                if text and text.strip():
                    recognized_lines.append(text.strip())
                    regions_data.append({
                        'type': 'text',
                        'bbox': [x1, y1, x2, y2],
                        'text': text.strip()
                    })
            except Exception as e:
                logger.warning(f"DocTR recognition error: {e}")
                continue
        
        # Combine into full text
        plain_text = '\n'.join(recognized_lines)

        
        return {
            'page_num': page_num,
            'plain_text': plain_text,
            'regions': regions_data,
            'tables': []  # DocTR mode doesn't extract tables
        }

    def _convert_to_images(self, file_path, max_pages=None):

        """Convert PDF/Image to PIL Images."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            # Use 150 DPI instead of default 200 for faster processing
            # (150 DPI = 75% resolution = ~56% pixels = faster inference)
            return convert_from_path(file_path, dpi=150, first_page=0, last_page=max_pages)
        elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            return [Image.open(file_path).convert('RGB')]
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _process_page(self, layout_engine, det_model, recognizer, img, page_num=1):
        """
        Process a single page using the hybrid pipeline:
        1. Run PP-StructureV3 for layout analysis
        2. For each region:
           - Table: Extract HTML
           - Figure: Skip
           - Text: Recognize with VietOCR (with adaptive strategies)
        """
        img_np = np.array(img) if not isinstance(img, np.ndarray) else img
        pil_img = Image.fromarray(img_np) if isinstance(img_np, np.ndarray) else img
        
        # Run PP-StructureV3 (requires file path)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_path = f.name
            pil_img.save(temp_path)
        
        try:
            results = layout_engine.predict(temp_path)
        finally:
            os.unlink(temp_path)
        
        text_lines = []
        tables = []
        regions = []
        warnings = []
        
        # 2. Process each result
        for result in results:
            layout_det = result.get('layout_det_res', None)
            table_res_list = result.get('table_res_list', []) or []
            
            # Process tables
            for table_res in table_res_list:
                html = table_res.get('pred_html', '')
                if html:
                    tables.append({
                        "type": "html",
                        "content": html
                    })
            
            # Process layout regions
            if layout_det:
                boxes = layout_det.get('boxes', []) if hasattr(layout_det, 'get') else getattr(layout_det, 'boxes', [])
                
                for box_info in (boxes or []):
                    if not isinstance(box_info, dict):
                        continue
                    
                    region_type = box_info.get('label', 'unknown').lower()
                    coords = box_info.get('coordinate', [0, 0, 0, 0])
                    bbox = [int(c) for c in coords]
                    
                    if region_type in ['figure', 'image']:
                        # Skip figures to avoid hallucinations
                        regions.append({
                            "type": "figure",
                            "bbox": bbox,
                            "skipped": True
                        })
                        continue
                    
                    if region_type == 'table':
                        regions.append({
                            "type": "table",
                            "bbox": bbox,
                            "skipped": False
                        })
                        continue
                    
                    # Text regions - process with our hybrid strategy
                    try:
                        x1, y1, x2, y2 = bbox
                        if x2 <= x1 or y2 <= y1:
                            continue
                        
                        # Height-based strategy
                        region_h = y2 - y1
                        sub_regions = []
                        
                        if region_h > 50:
                            # Tall block: Split lines with PaddleOCR
                            padding = 20
                            x1_p = max(0, x1 - padding)
                            y1_p = max(0, y1 - padding)
                            x2_p = min(pil_img.width, x2 + padding)
                            y2_p = min(pil_img.height, y2 + padding)
                            
                            macro_crop = pil_img.crop((x1_p, y1_p, x2_p, y2_p))
                            macro_crop_np = np.array(macro_crop)
                            
                            det_results = det_model.predict(macro_crop_np)
                            if det_results:
                                for det_result in det_results:
                                    rec_polys = det_result.get('rec_polys', []) if hasattr(det_result, 'get') else getattr(det_result, 'rec_polys', [])
                                    for poly in rec_polys:
                                        sub_rect = self._box_to_rect(poly)
                                        sx1, sy1, sx2, sy2 = sub_rect
                                        # Convert to global coordinates
                                        gx1 = x1_p + sx1
                                        gy1 = y1_p + sy1
                                        gx2 = x1_p + sx2
                                        gy2 = y1_p + sy2
                                        sub_regions.append([gx1, gy1, gx2, gy2])
                        
                        if not sub_regions:
                            # Single line or fallback
                            sub_regions.append([x1, y1, x2, y2])
                        
                        # Recognize each sub-region
                        for sub_bbox in sub_regions:
                            sx1, sy1, sx2, sy2 = sub_bbox
                            text, conf, final_bbox = self._recognize_with_adaptive(
                                pil_img, recognizer, sx1, sy1, sx2, sy2
                            )
                            
                            if text and conf >= 0.65:
                                text_lines.append(text)
                                regions.append({
                                    "type": "text",
                                    "bbox": final_bbox,
                                    "content": text,
                                    "confidence": conf
                                })
                    
                    except Exception as e:
                        logger.warning(f"Failed to process text region: {e}")
                        warnings.append(str(e))
                        continue
        
        plain_text = "\n".join(text_lines)
        
        return {
            "page": page_num,
            "text": plain_text,
            "plain_text": plain_text,
            "tables": tables,
            "images": [],
            "regions": regions,
            "confidence": 1.0,
            "warnings": warnings
        }

    def _recognize_with_adaptive(self, pil_img, recognizer, x1, y1, x2, y2):
        """
        Recognize text with adaptive strategies:
        1. Padding (6px)
        2. Upscaling for small text
        3. Extension for truncated "Họ và tên" fields
        """
        p = 6  # Padding
        crop = pil_img.crop((
            max(0, x1 - p), max(0, y1 - p),
            min(pil_img.width, x2 + p), min(pil_img.height, y2 + p)
        ))
        
        # Upscale small text
        if crop.height < 32:
            new_size = (int(crop.width * 2), int(crop.height * 2))
            crop = crop.resize(new_size, Image.LANCZOS)
        
        # Recognize
        try:
            rec_result = recognizer.predict(crop, return_prob=True)
            if isinstance(rec_result, tuple):
                text, conf = rec_result
            else:
                text = rec_result
                conf = 1.0
        except TypeError:
            text = recognizer.predict(crop)
            conf = 1.0
        
        final_text = text.strip() if text else ""
        final_bbox = [x1, y1, x2, y2]
        
        # Adaptive Extension for "Họ và tên"
        if final_text and "họ và" in final_text.lower() and (x2 - x1) < 400:
            logger.info(f"⚡ Detected truncated Name field: '{final_text}'. Extending...")
            new_x2 = min(pil_img.width, 1100)
            
            ext_crop = pil_img.crop((
                max(0, x1 - p), max(0, y1 - p),
                min(pil_img.width, new_x2 + p), min(pil_img.height, y2 + p)
            ))
            
            if ext_crop.height < 32:
                new_size = (int(ext_crop.width * 2), int(ext_crop.height * 2))
                ext_crop = ext_crop.resize(new_size, Image.LANCZOS)
            
            try:
                ext_result = recognizer.predict(ext_crop, return_prob=True)
                if isinstance(ext_result, tuple):
                    ext_text, ext_conf = ext_result
                else:
                    ext_text = ext_result
                    ext_conf = 1.0
                
                if len(ext_text) > len(final_text):
                    logger.info(f"⚡ Extended result: '{ext_text}'")
                    final_text = ext_text.strip()
                    final_bbox = [x1, y1, new_x2, y2]
                    conf = ext_conf
            except Exception as e:
                logger.warning(f"Extension failed: {e}")
        
        return final_text, conf, final_bbox

    def _box_to_rect(self, box):
        """Convert 4-point polygon to (x1, y1, x2, y2) rectangle."""
        pts = np.array(box).reshape(-1, 2)
        x1 = int(pts[:, 0].min())
        y1 = int(pts[:, 1].min())
        x2 = int(pts[:, 0].max())
        y2 = int(pts[:, 1].max())
        return (x1, y1, x2, y2)

    def extract_tables(self, file_path, mime_type=None):
        """
        Extract tables from document using PaddleX table_recognition pipeline.
        Returns list of tables with HTML and Markdown content.
        
        Args:
            file_path: Path to PDF or image file
            mime_type: MIME type (optional)
            
        Returns:
            List of dicts: [{"page": 1, "bbox": [...], "html": "...", "markdown": "..."}]
        """
        logger.info(f"Extracting tables from: {file_path}")
        tables = []
        
        try:
            import tempfile
            
            # Convert PDF to images if needed
            if file_path.lower().endswith('.pdf') or (mime_type and 'pdf' in mime_type):
                images = convert_from_path(file_path, dpi=150)
            else:
                images = [Image.open(file_path)]
            
            # Use PaddleX table_recognition pipeline
            pipeline = self._get_layout_engine()
            
            for page_num, img in enumerate(images, start=1):
                # Pipeline requires file path
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                    temp_path = f.name
                    img.save(temp_path)
                
                try:
                    # PaddleX pipeline returns a generator of TableRecognitionResult
                    results = list(pipeline.predict(temp_path))
                    
                    # Iterate through results
                    for result in results:
                        # PaddleX result has .html property which is a dict
                        # Format: {'table_1': '<html>...</html>', 'table_2': '...'}
                        html_dict = getattr(result, 'html', {}) or {}
                        
                        if isinstance(html_dict, dict):
                            for table_key, html_content in html_dict.items():
                                if html_content and isinstance(html_content, str):
                                    # Convert HTML to Markdown
                                    markdown = self._html_table_to_markdown(html_content)
                                    tables.append({
                                        "page": page_num,
                                        "bbox": [],  # PaddleX doesn't provide bbox in html dict
                                        "html": html_content,
                                        "markdown": markdown
                                    })
                                    logger.debug(f"Extracted {table_key} from page {page_num}")
                                
                except Exception as e:
                    logger.warning(f"Table extraction failed for page {page_num}: {e}")
                    continue
                finally:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    
            logger.info(f"Extracted {len(tables)} tables")
            return tables
            
        except Exception as e:
            logger.error(f"Table extraction failed: {e}")
            return []

    def extract_images(self, file_path, mime_type=None):
        """
        Extract figure/image regions from document.
        Crops figure regions and saves as separate files.
        
        Args:
            file_path: Path to PDF or image file
            mime_type: MIME type (optional)
            
        Returns:
            List of dicts: [{"page": 1, "bbox": [...], "url": "/media/...", "caption": "..."}]
        """
        logger.info(f"Extracting images from: {file_path}")
        extracted_images = []
        
        try:
            import uuid
            import tempfile
            
            # Convert PDF to images if needed
            if file_path.lower().endswith('.pdf') or (mime_type and 'pdf' in mime_type):
                images = convert_from_path(file_path, dpi=150)
            else:
                images = [Image.open(file_path)]
            
            # Use PPStructure for layout analysis
            pipeline = self._get_layout_engine()
            
            for page_num, img in enumerate(images, start=1):
                # PPStructureV3 requires file path, not numpy array
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                    temp_path = f.name
                    img.save(temp_path)
                
                try:
                    # PaddleX pipeline returns generator - convert to list
                    results = list(pipeline.predict(temp_path))
                    
                    # Find figure regions from layout_det_res
                    figure_count = 0
                    for result in results:
                        # Access layout detection via result.json['res']['layout_det_res']
                        json_res = getattr(result, 'json', {}).get('res', {})
                        layout_det = json_res.get('layout_det_res', {})
                        boxes = layout_det.get('boxes', [])
                        
                        for box_data in boxes:
                            # box_data format: {'label': 'figure', 'score': Y, 'coordinate': [x1,y1,x2,y2]}
                            label = box_data.get('label', '').lower()
                            if label in ('figure', 'image', 'chart', 'graph', 'picture'):
                                coord = box_data.get('coordinate', [])
                                if len(coord) >= 4:
                                    # Crop the figure region
                                    x1, y1, x2, y2 = int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3])
                                    cropped = img.crop((x1, y1, x2, y2))
                                    
                                    # Save to media folder
                                    figure_count += 1
                                    filename = f"ocr_figure_{uuid.uuid4().hex[:8]}_p{page_num}_f{figure_count}.png"
                                    save_path = os.path.join(settings.MEDIA_ROOT, 'ocr_figures', filename)
                                    
                                    # Ensure directory exists
                                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                                    cropped.save(save_path, 'PNG')
                                    
                                    # Build URL
                                    url = f"/media/ocr_figures/{filename}"
                                    
                                    extracted_images.append({
                                        "page": page_num,
                                        "bbox": list(coord),
                                        "url": url,
                                        "caption": f"Figure {figure_count} (Page {page_num})"
                                    })
                except Exception as e:
                    logger.warning(f"Image extraction failed for page {page_num}: {e}")
                    continue
                finally:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    
            logger.info(f"Extracted {len(extracted_images)} figures")
            return extracted_images
            
        except Exception as e:
            logger.error(f"Image extraction failed: {e}")
            return []

    def _html_table_to_markdown(self, html):
        """Convert HTML table to Markdown format."""
        if not html:
            return ""
        
        try:
            from html.parser import HTMLParser
            
            class TableParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.rows = []
                    self.current_row = []
                    self.current_cell = ""
                    self.in_cell = False
                    
                def handle_starttag(self, tag, attrs):
                    if tag in ('td', 'th'):
                        self.in_cell = True
                        self.current_cell = ""
                        
                def handle_endtag(self, tag):
                    if tag in ('td', 'th'):
                        self.in_cell = False
                        self.current_row.append(self.current_cell.strip())
                    elif tag == 'tr':
                        if self.current_row:
                            self.rows.append(self.current_row)
                            self.current_row = []
                            
                def handle_data(self, data):
                    if self.in_cell:
                        self.current_cell += data
            
            parser = TableParser()
            parser.feed(html)
            
            if not parser.rows:
                return ""
            
            # Build markdown table
            lines = []
            for i, row in enumerate(parser.rows):
                lines.append("| " + " | ".join(row) + " |")
                if i == 0:
                    # Add separator after header
                    lines.append("|" + "|".join(["---"] * len(row)) + "|")
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.warning(f"HTML to Markdown conversion failed: {e}")
            return html  # Return original HTML as fallback


# Singleton instance
ocr_service = OCRService()


def prewarm_models():
    """
    Pre-load OCR models at startup based on OCR_ENGINE setting.
    Call this from Django's AppConfig.ready() to eliminate first-request latency.
    
    Note: PPStructure is NOT preloaded here to prevent memory issues.
    It will be lazy-loaded when the Celery task runs.
    """
    import threading
    
    def _prewarm():
        logger.info(f"🔥 Pre-warming OCR models (engine={OCR_ENGINE})...")
        start = time.time()
        try:
            if OCR_ENGINE == 'DOCTR':
                # Fast path: DocTR detection + VietOCR recognition
                ocr_service._get_doctr_detector()
                ocr_service._get_recognizer()
            else:
                # Full path: PaddleOCR + VietOCR
                ocr_service._get_detector()
                ocr_service._get_recognizer()
            
            # NOTE: PPStructure is NOT preloaded to avoid memory issues
            # It will be loaded on-demand by the Celery worker
            # logger.info("⚠️ PPStructure will be loaded on-demand (not prewarmed)")
            
            elapsed = time.time() - start
            logger.info(f"✅ OCR models pre-warmed in {elapsed:.1f}s")
        except Exception as e:
            logger.error(f"Failed to pre-warm OCR models: {e}")
    
    # Run in background thread to not block server startup
    thread = threading.Thread(target=_prewarm, daemon=True)
    thread.start()
    return thread

