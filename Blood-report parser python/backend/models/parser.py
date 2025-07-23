import cv2     # pip install opencv-python
import numpy as np
from PIL import Image, ImageEnhance
import pytesseract
import pandas as pd
import re
from typing import Dict, List, Optional

class DocumentParser:
    def __init__(self):
        self.medical_patterns = {
            'lab_value': r'([a-zA-Z\s]+)[:\-\s]*(\d+\.?\d*)\s*([a-zA-Z/μ%]+)?',
            'blood_pressure': r'(?:blood\s*pressure|bp)[:\s]*(\d+)[/\-](\d+)',
            'date': r'(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})',
            'range': r'(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)',
            'table_row': r'([A-Za-z\s]+)\s+(\d+\.?\d*)\s+([A-Za-z/μ%]*)\s+([A-Za-z\s]*)'
        }

    def preprocess_image(self, image_path: str) -> Image:
        """Enhance image for better OCR results"""
        # Read image
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Enhance contrast
        enhanced = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(denoised)
        
        # Convert back to PIL Image
        return Image.fromarray(enhanced)

    def extract_tables(self, text: str) -> List[Dict]:
        """Extract tabular data from text"""
        tables = []
        lines = text.split('\n')
        
        current_table = []
        in_table = False
        
        for line in lines:
            # Detect table headers or structured data
            if re.search(r'\b(test|parameter|value|normal|range)\b', line.lower()):
                in_table = True
                current_table = []
                continue
            
            if in_table:
                # Check if line contains structured data
                match = re.search(self.medical_patterns['table_row'], line)
                if match:
                    current_table.append({
                        'test': match.group(1).strip(),
                        'value': float(match.group(2)),
                        'unit': match.group(3) or '',
                        'status': match.group(4) or ''
                    })
                elif len(line.strip()) == 0:
                    # End of table
                    if current_table:
                        tables.append(current_table)
                        current_table = []
                    in_table = False
        
        return tables

    def extract_medical_entities(self, text: str) -> Dict:
        """Extract medical entities and their values"""
        entities = {}
        
        # Extract all numeric values with units
        pattern = r'([a-zA-Z\s]+)[:\-\s]*(\d+\.?\d*)\s*([a-zA-Z/μ%]+)?'
        matches = re.finditer(pattern, text.lower())
        
        for match in matches:
            entity_name = match.group(1).strip()
            value = float(match.group(2))
            unit = match.group(3) or ''
            
            # Map common variations to standard names
            entity_name = self.normalize_entity_name(entity_name)
            if entity_name:
                entities[entity_name] = {
                    'value': value,
                    'unit': unit,
                    'original_text': match.group(0)
                }
        
        return entities

    def normalize_entity_name(self, name: str) -> Optional[str]:
        """Normalize entity names to standard medical terminology"""
        name = name.lower().strip()
        
        # Mapping dictionary for common variations
        mappings = {
            'cholesterol': ['cholesterol', 'chol', 'total cholesterol'],
            'glucose': ['glucose', 'sugar', 'blood sugar', 'fasting glucose'],
            'hemoglobin': ['hemoglobin', 'hgb', 'hb'],
            'blood_pressure_systolic': ['systolic', 'systolic bp', 'sys'],
            'blood_pressure_diastolic': ['diastolic', 'diastolic bp', 'dia'],
            'bmi': ['bmi', 'body mass index'],
            'creatinine': ['creatinine', 'creat'],
            'triglycerides': ['triglycerides', 'trig']
        }
        
        for standard_name, variations in mappings.items():
            if any(variation in name for variation in variations):
                return standard_name
        
        return None