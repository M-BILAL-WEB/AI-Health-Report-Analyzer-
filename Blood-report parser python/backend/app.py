from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import PyPDF2
import io
from PIL import Image
import pytesseract
import re
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class HealthReportAnalyzer:
    def __init__(self):
        self.normal_ranges = {
            'cholesterol': {'min': 125, 'max': 200, 'unit': 'mg/dL'},
            'blood_pressure_systolic': {'min': 90, 'max': 120, 'unit': 'mmHg'},
            'blood_pressure_diastolic': {'min': 60, 'max': 80, 'unit': 'mmHg'},
            'glucose': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
            'hemoglobin': {'min': 12.0, 'max': 17.5, 'unit': 'g/dL'},
            'white_blood_cells': {'min': 4000, 'max': 11000, 'unit': '/μL'},
            'bmi': {'min': 18.5, 'max': 24.9, 'unit': 'kg/m²'}
        }
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def extract_text_from_image(self, file_path):
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            return f"Error reading image: {str(e)}"
    
    def parse_lab_values(self, text):
        """Extract lab values from text using regex patterns"""
        lab_values = {}
        
        # Common patterns for lab values
        patterns = {
            'cholesterol': r'cholesterol[:\s]*(\d+\.?\d*)',
            'glucose': r'glucose[:\s]*(\d+\.?\d*)',
            'hemoglobin': r'hemoglobin[:\s]*(\d+\.?\d*)',
            'blood_pressure': r'blood pressure[:\s]*(\d+)/(\d+)',
            'bmi': r'bmi[:\s]*(\d+\.?\d*)',
            'weight': r'weight[:\s]*(\d+\.?\d*)',
            'height': r'height[:\s]*(\d+\.?\d*)'
        }
        
        text_lower = text.lower()
        
        for test, pattern in patterns.items():
            matches = re.findall(pattern, text_lower)
            if matches:
                if test == 'blood_pressure':
                    lab_values['blood_pressure_systolic'] = float(matches[0][0])
                    lab_values['blood_pressure_diastolic'] = float(matches[0][1])
                else:
                    lab_values[test] = float(matches[0])
        
        return lab_values
    
    def analyze_values(self, lab_values):
        """Analyze lab values against normal ranges"""
        analysis = {}
        alerts = []
        
        for test, value in lab_values.items():
            if test in self.normal_ranges:
                normal_range = self.normal_ranges[test]
                status = "normal"
                
                if value < normal_range['min']:
                    status = "low"
                    alerts.append({
                        'test': test,
                        'value': value,
                        'status': 'low',
                        'message': f"{test.replace('_', ' ').title()} is below normal range"
                    })
                elif value > normal_range['max']:
                    status = "high"
                    alerts.append({
                        'test': test,
                        'value': value,
                        'status': 'high',
                        'message': f"{test.replace('_', ' ').title()} is above normal range"
                    })
                
                analysis[test] = {
                    'value': value,
                    'status': status,
                    'normal_range': f"{normal_range['min']}-{normal_range['max']} {normal_range['unit']}"
                }
        
        return analysis, alerts
    
    def generate_recommendations(self, analysis, alerts):
        """Generate health recommendations based on analysis"""
        recommendations = []
        
        for alert in alerts:
            test = alert['test']
            status = alert['status']
            
            if test == 'cholesterol':
                if status == 'high':
                    recommendations.extend([
                        "Reduce intake of saturated fats and trans fats",
                        "Increase fiber-rich foods like oats and beans",
                        "Exercise regularly (30 minutes, 5 days a week)",
                        "Consider consulting a cardiologist"
                    ])
            elif test in ['blood_pressure_systolic', 'blood_pressure_diastolic']:
                if status == 'high':
                    recommendations.extend([
                        "Reduce sodium intake (less than 2300mg daily)",
                        "Maintain healthy weight",
                        "Limit alcohol consumption",
                        "Practice stress management techniques",
                        "Consult with your doctor about blood pressure medication"
                    ])
            elif test == 'glucose':
                if status == 'high':
                    recommendations.extend([
                        "Monitor carbohydrate intake",
                        "Choose whole grains over refined carbs",
                        "Maintain regular meal times",
                        "Increase physical activity",
                        "Consider diabetes screening with your doctor"
                    ])
            elif test == 'bmi':
                if status == 'high':
                    recommendations.extend([
                        "Create a calorie deficit through diet and exercise",
                        "Focus on whole foods and portion control",
                        "Aim for 150 minutes of moderate exercise weekly",
                        "Consider consulting a nutritionist"
                    ])
        
        # General recommendations
        if not recommendations:
            recommendations = [
                "Maintain current healthy lifestyle",
                "Continue regular check-ups",
                "Stay hydrated and eat balanced meals",
                "Keep up with regular physical activity"
            ]
        
        return list(set(recommendations))  # Remove duplicates
    
    def create_summary(self, analysis, alerts):
        """Create a simple summary of the report"""
        total_tests = len(analysis)
        abnormal_tests = len(alerts)
        normal_tests = total_tests - abnormal_tests
        
        if abnormal_tests == 0:
            overall_status = "Good"
            summary_text = "Your health report shows normal values across all tested parameters. Keep maintaining your healthy lifestyle!"
        elif abnormal_tests <= 2:
            overall_status = "Attention Needed"
            summary_text = f"Your report shows {abnormal_tests} parameter(s) outside normal range. Some adjustments to your lifestyle may be beneficial."
        else:
            overall_status = "Medical Consultation Recommended"
            summary_text = f"Your report shows {abnormal_tests} parameters outside normal range. Please consult with your healthcare provider."
        
        return {
            'overall_status': overall_status,
            'summary_text': summary_text,
            'total_tests': total_tests,
            'normal_tests': normal_tests,
            'abnormal_tests': abnormal_tests
        }

# Initialize analyzer
analyzer = HealthReportAnalyzer()

@app.route('/')
def home():
    return jsonify({"message": "Health Report Analyzer API is running!"})

@app.route('/analyze', methods=['POST'])
def analyze_report():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                extracted_text = analyzer.extract_text_from_pdf(file_path)
            elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                extracted_text = analyzer.extract_text_from_image(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()
            
            # Parse lab values
            lab_values = analyzer.parse_lab_values(extracted_text)
            
            # Analyze values
            analysis, alerts = analyzer.analyze_values(lab_values)
            
            # Generate recommendations
            recommendations = analyzer.generate_recommendations(analysis, alerts)
            
            # Create summary
            summary = analyzer.create_summary(analysis, alerts)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return jsonify({
                'success': True,
                'extracted_text': extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
                'lab_values': lab_values,
                'analysis': analysis,
                'alerts': alerts,
                'recommendations': recommendations,
                'summary': summary,
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)