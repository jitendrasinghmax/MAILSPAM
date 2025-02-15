# spam_classifier/ml_utils.py
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import ssl
import os

# SSL Fix
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
class SpamClassifier:
    def __init__(self):
        self.ps = PorterStemmer()
        
        # Get the base directory of your Django project
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construct paths to model files
        vectorizer_path = os.path.join(BASE_DIR, 'models', 'vectorizer.pkl')
        model_path = os.path.join(BASE_DIR, 'models', 'model.pkl')
        
        # Load the models
        self.tfidf = pickle.load(open(vectorizer_path, 'rb'))
        self.model = pickle.load(open(model_path, 'rb'))
    def transform_text(self, text):
        text = text.lower()
        text = nltk.word_tokenize(text)
        
        y = []
        for i in text:
            if i.isalnum():
                y.append(i)
        
        text = y[:]
        y.clear()
        
        for i in text:
            if i not in stopwords.words('english') and i not in string.punctuation:
                y.append(i)
        
        text = y[:]
        y.clear()
        
        for i in text:
            y.append(self.ps.stem(i))
        
        return " ".join(y)

    def predict(self, text):
        # 1. preprocess
        transformed_text = self.transform_text(text)
        # 2. vectorize
        vector_input = self.tfidf.transform([transformed_text])
        # 3. predict
        result = self.model.predict(vector_input)[0]
        return result