import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import string
import numpy as np

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

class CommentAnalyzer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def preprocess_text(self, text):
        """Preprocess the text for analysis"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenization
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens 
                 if word not in self.stop_words and word.isalnum()]
        
        return ' '.join(tokens)
    
    def get_sentiment_textblob(self, text):
        """Get sentiment using TextBlob"""
        analysis = TextBlob(text)
        # Classify the polarity of the text
        if analysis.sentiment.polarity > 0.1:
            return 'positive'
        elif analysis.sentiment.polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_comments(self, comments_df):
        """
        Analyze comments and classify them as positive or negative
        
        Args:
            comments_df (pandas.DataFrame): DataFrame containing comments
            
        Returns:
            dict: Dictionary containing DataFrames for all, positive, and negative comments
        """
        if comments_df is None or comments_df.empty:
            return {
                'all_comments': pd.DataFrame(),
                'positive_comments': pd.DataFrame(),
                'negative_comments': pd.DataFrame()
            }
        
        # Make a copy to avoid modifying the original DataFrame
        df = comments_df.copy()
        
        # Preprocess comments
        df['processed_text'] = df['text'].apply(self.preprocess_text)
        
        # Get sentiment using TextBlob
        df['sentiment'] = df['text'].apply(self.get_sentiment_textblob)
        
        # If we have enough data, we could train a more sophisticated model here
        # For now, we'll just use the TextBlob results
        
        # Separate positive and negative comments
        positive_comments = df[df['sentiment'] == 'positive']
        negative_comments = df[df['sentiment'] == 'negative']
        
        return {
            'all_comments': df,
            'positive_comments': positive_comments,
            'negative_comments': negative_comments
        }

# Create a global instance of the analyzer
analyzer = CommentAnalyzer()

def analyze_comments(comments_df):
    """
    Wrapper function to analyze comments using the global analyzer
    """
    return analyzer.analyze_comments(comments_df)
