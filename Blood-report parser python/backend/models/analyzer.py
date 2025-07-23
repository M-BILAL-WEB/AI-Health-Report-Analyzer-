import re
import numpy as np
from typing import Dict, List, Tuple
import spacy
from datetime import datetime, timedelta

class AdvancedHealthAnalyzer:
    def __init__(self):
        self.medical_keywords = {
            'cardiovascular': ['heart', 'cardiac', 'blood pressure', 'cholesterol', 'triglycerides'],
            'diabetes': ['glucose', 'sugar', 'insulin', 'hemoglobin a1c', 'hba1c'],
            'liver': ['alt', 'ast', 'bilirubin', 'liver', 'hepatic'],
            'kidney': ['creatinine', 'bun', 'kidney', 'renal', 'urea'],
            'blood': ['hemoglobin', 'hematocrit', 'wbc', 'rbc', 'platelets'],
            'thyroid': ['tsh', 't3', 't4', 'thyroid'],
            'lipid': ['cholesterol', 'ldl', 'hdl', 'triglycerides']
        }
        
        self.severity_levels = {
            'normal': 0,
            'borderline': 1,
            'elevated': 2,
            'high': 3,
            'critical': 4
        }
        
        self.extended_ranges = {
            'cholesterol_total': {'min': 125, 'max': 200, 'unit': 'mg/dL'},
            'cholesterol_ldl': {'min': 50, 'max': 100, 'unit': 'mg/dL'},
            'cholesterol_hdl': {'min': 40, 'max': 80, 'unit': 'mg/dL'},
            'triglycerides': {'min': 50, 'max': 150, 'unit': 'mg/dL'},
            'glucose_fasting': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
            'glucose_random': {'min': 70, 'max': 140, 'unit': 'mg/dL'},
            'hba1c': {'min': 4.0, 'max': 5.7, 'unit': '%'},
            'blood_pressure_systolic': {'min': 90, 'max': 120, 'unit': 'mmHg'},
            'blood_pressure_diastolic': {'min': 60, 'max': 80, 'unit': 'mmHg'},
            'hemoglobin_male': {'min': 13.5, 'max': 17.5, 'unit': 'g/dL'},
            'hemoglobin_female': {'min': 12.0, 'max': 15.5, 'unit': 'g/dL'},
            'creatinine': {'min': 0.6, 'max': 1.3, 'unit': 'mg/dL'},
            'bmi': {'min': 18.5, 'max': 24.9, 'unit': 'kg/m²'},
            'heart_rate': {'min': 60, 'max': 100, 'unit': 'bpm'}
        }

    def calculate_risk_score(self, analysis: Dict) -> Dict:
        """Calculate overall cardiovascular and diabetes risk scores"""
        cv_risk = 0
        diabetes_risk = 0
        
        risk_factors = {
            'cholesterol': 0.3,
            'blood_pressure_systolic': 0.25,
            'blood_pressure_diastolic': 0.15,
            'glucose': 0.2,
            'bmi': 0.1
        }
        
        for test, weight in risk_factors.items():
            if test in analysis:
                status = analysis[test]['status']
                if status == 'high':
                    cv_risk += weight * 3
                    if test == 'glucose':
                        diabetes_risk += 0.5
                elif status == 'borderline':
                    cv_risk += weight * 1.5
                    if test == 'glucose':
                        diabetes_risk += 0.2
        
        return {
            'cardiovascular_risk': min(cv_risk * 100, 100),
            'diabetes_risk': min(diabetes_risk * 100, 100),
            'overall_risk': min((cv_risk + diabetes_risk) * 50, 100)
        }

    def generate_detailed_recommendations(self, analysis: Dict, risk_scores: Dict) -> Dict:
        """Generate detailed, categorized recommendations"""
        recommendations = {
            'immediate': [],
            'dietary': [],
            'exercise': [],
            'lifestyle': [],
            'medical': []
        }
        
        # High-priority immediate actions
        for test, data in analysis.items():
            if data['status'] == 'critical':
                recommendations['immediate'].append(
                    f"URGENT: {test.replace('_', ' ').title()} level ({data['value']}) requires immediate medical attention"
                )
        
        # Dietary recommendations
        if 'cholesterol' in analysis and analysis['cholesterol']['status'] in ['high', 'borderline']:
            recommendations['dietary'].extend([
                "Reduce saturated fat intake to less than 7% of total calories",
                "Include soluble fiber foods (oats, beans, fruits)",
                "Consume omega-3 rich fish twice per week",
                "Choose lean proteins and plant-based options"
            ])
        
        # Exercise recommendations
        if risk_scores['cardiovascular_risk'] > 30:
            recommendations['exercise'].extend([
                "Aim for 150 minutes of moderate aerobic activity weekly",
                "Include 2 sessions of strength training per week",
                "Start with low-impact activities if new to exercise",
                "Consider working with a fitness professional"
            ])
        
        # Lifestyle modifications
        if 'blood_pressure_systolic' in analysis and analysis['blood_pressure_systolic']['status'] != 'normal':
            recommendations['lifestyle'].extend([
                "Limit sodium intake to less than 2300mg daily",
                "Maintain healthy sleep schedule (7-9 hours nightly)",
                "Practice stress reduction techniques",
                "Limit alcohol consumption"
            ])
        
        # Medical follow-up
        if risk_scores['overall_risk'] > 50:
            recommendations['medical'].extend([
                "Schedule comprehensive metabolic panel in 3 months",
                "Consider consultation with cardiologist",
                "Discuss medication options with primary care physician",
                "Regular monitoring of key biomarkers"
            ])
        
        return recommendations
