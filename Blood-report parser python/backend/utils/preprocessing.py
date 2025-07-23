import re
import string
from typing import List, Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

class TextPreprocessor:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
            
        self.stop_words = set(stopwords.words('english'))
        
        # Medical abbreviations that should not be removed
        self.medical_terms = {
            'bp', 'hr', 'bmi', 'ldl', 'hdl', 'tsh', 'wbc', 'rbc',
            'hgb', 'hct', 'mcv', 'mch', 'mchc', 'rdw', 'plt'
        }

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove special characters but preserve medical symbols
        text = re.sub(r'[^\w\s\-/:.%μ]', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove extra spaces
        text = text.strip()
        
        return text

    def extract_sentences_with_numbers(self, text: str) -> List[str]:
        """Extract sentences that contain numeric values"""
        sentences = sent_tokenize(text)
        numeric_sentences = []
        
        for sentence in sentences:
            if re.search(r'\d+', sentence):
                numeric_sentences.append(sentence)
        
        return numeric_sentences

    def tokenize_medical_text(self, text: str) -> List[str]:
        """Tokenize text while preserving medical terminology"""
        # Convert to lowercase but preserve medical abbreviations
        tokens = word_tokenize(text.lower())
        
        # Filter out stopwords but keep medical terms
        filtered_tokens = [
            token for token in tokens 
            if token not in self.stop_words or token in self.medical_terms
        ]
        
        return filtered_tokens
