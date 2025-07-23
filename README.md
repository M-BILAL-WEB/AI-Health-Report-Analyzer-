# AI-Health-Report-Analyzer-
# 🏥 AI/ML Health Report Analyzer

> **Intelligent Medical Report Analysis with AI-Powered Health Insights**

A comprehensive full-stack application that uses artificial intelligence to analyze medical reports, extract key health metrics, and provide personalized health recommendations with a modern, intuitive user interface.

## 🌟 Features

### 📋 **Smart Document Processing**
- **Multi-format Support**: PDF, PNG, JPG, JPEG, TXT files
- **OCR Technology**: Extract text from scanned medical reports
- **Advanced Parsing**: Intelligent medical terminology recognition
- **Table Extraction**: Automatically detect and parse lab result tables

### 🧠 **AI-Powered Analysis**
- **15+ Lab Tests**: Comprehensive analysis of common health markers
- **Risk Assessment**: Cardiovascular and diabetes risk scoring
- **Normal Range Comparison**: Automatic detection of abnormal values
- **Trend Analysis**: Historical comparison capabilities

### 💡 **Intelligent Recommendations**
- **Personalized Advice**: Tailored health recommendations
- **Categorized Actions**: Immediate, dietary, exercise, lifestyle, and medical
- **Evidence-Based**: Recommendations based on medical guidelines
- **Priority Alerts**: Critical value notifications

### 🎨 **Modern UI/UX**
- **Responsive Design**: Works seamlessly on all devices
- **Drag & Drop**: Intuitive file upload interface
- **Real-time Processing**: Live progress indicators
- **Beautiful Visualizations**: Color-coded health status display
- **Glass Morphism**: Premium design with smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (optional, for advanced frontend development)
- Tesseract OCR

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/M-BILAL-WEB/health-report-analyzer.git
cd health-report-analyzer
```

#### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt
```

#### 3. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
1. Download Tesseract from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install and add to PATH

#### 4. Run the Application

**Start Backend Server:**
```bash
cd backend
python app.py
```
Server runs on `http://localhost:5000`

**Start Frontend:**
```bash
cd frontend
# Option 1: Direct browser
open index.html

# Option 2: Local server
python -m http.server 8080
```
Frontend available at `http://localhost:8080`

## 📁 Project Structure

```
health-report-analyzer/
├── 📁 backend/
│   ├── 📄 app.py                 # Main Flask server
│   ├── 📄 requirements.txt       # Python dependencies
│   ├── 📄 config.py              # Configuration settings
│   ├── 📁 models/
│   │   ├── 📄 analyzer.py        # Advanced health analysis
│   │   └── 📄 parser.py          # Document parsing utilities
│   ├── 📁 utils/
│   │   └── 📄 preprocessing.py   # Text processing tools
│   └── 📁 uploads/               # Temporary file storage
├── 📁 frontend/
│   └── 📄 index.html             # Complete React application
├── 📁 data/
│   └── 📁 sample_reports/        # Sample medical reports
├── 📄 README.md                  # Project documentation
├── 📄 .env                       # Environment variables
└── 📄 .gitignore                 # Git ignore rules
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# File Upload Settings
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=pdf,png,jpg,jpeg,txt

# Analysis Settings
CONFIDENCE_THRESHOLD=0.8
MAX_PROCESSING_TIME=30

# Server Configuration
API_PORT=5000
FRONTEND_URL=http://localhost:8080
```

## 📊 Supported Health Metrics

| Category | Tests | Normal Ranges |
|----------|-------|---------------|
| **Cardiovascular** | Total Cholesterol, LDL, HDL, Triglycerides, Blood Pressure | Varies by test |
| **Diabetes** | Fasting Glucose, Random Glucose, HbA1c | 70-100 mg/dL (fasting) |
| **Blood Work** | Hemoglobin, Hematocrit, WBC, RBC, Platelets | Gender-specific ranges |
| **Kidney Function** | Creatinine, BUN | 0.6-1.3 mg/dL (creatinine) |
| **Liver Function** | ALT, AST, Bilirubin | Enzyme-specific ranges |
| **Thyroid** | TSH, T3, T4 | 0.4-4.0 mIU/L (TSH) |
| **Physical** | BMI, Heart Rate, Weight, Height | 18.5-24.9 kg/m² (BMI) |

## 🔄 API Documentation

### Endpoints

#### `POST /analyze`



#### `GET /health`


## 🐳 Docker Deployment
### Build and Run
```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d
```





## 🤝 Contributing

We welcome contributions! 
### Development Setup
```bash
# Fork the repository
git clone https://github.com/M-BILAL-WEB/health-report-analyzer.git

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git commit -m "Add your feature"

# Push and create pull request
git push origin feature/your-feature-name
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



### Frequently Asked Questions

**Q: What file formats are supported?**
A: PDF, PNG, JPG, JPEG, and TXT files up to 10MB.

**Q: Is my health data secure?**
A: Yes, files are processed locally and deleted immediately after analysis.

**Q: Can I use this for medical diagnosis?**
A: No, this tool is for informational purposes only. Always consult healthcare professionals.

**Q: How accurate is the analysis?**
A: The tool uses established medical ranges but should not replace professional medical advice.

---

<div align="center">

**Built with ❤️ for better health insights**

[⭐ Star this repo](https://github.com/M-BILAL-WEB/health-report-analyzer) | [🐛 Report Bug](https://github.com/M-BILAL-WEB/health-report-analyzer/issues) | [✨ Request Feature](https://github.com/M-BILAL-WEB/health-report-analyzer/issues)

</div>
