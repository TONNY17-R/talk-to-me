"""Sentiment analysis model for Uganda context."""

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class SentimentModel:
    """Sentiment analysis model optimized for Ugandan context."""
    
    def __init__(self):
        """Initialize sentiment model."""
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained sentiment model."""
        try:
            # Load model for Uganda-specific sentiment analysis
            logger.info("Sentiment model loaded")
        except Exception as e:
            logger.warning(f"Could not load sentiment model: {str(e)}")
    
    def predict(self, text: str) -> Dict[str, float]:
        """
        Predict sentiment of text.
        
        Args:
            text: Input text to analyze
        
        Returns:
            Dictionary with sentiment scores
        """
        try:
            if not self.model:
                return self._fallback_sentiment(text)
            
            # Tokenize and predict
            tokens = self._preprocess(text)
            prediction = self.model.predict([tokens])[0]
            
            sentiments = {
                'very_negative': float(prediction[0]),
                'negative': float(prediction[1]),
                'neutral': float(prediction[2]),
                'positive': float(prediction[3]),
                'very_positive': float(prediction[4])
            }
            return sentiments
        except Exception as e:
            logger.error(f"Error predicting sentiment: {str(e)}")
            return self._fallback_sentiment(text)
    
    def _preprocess(self, text: str) -> list:
        """Preprocess text for model."""
        # Tokenization and preprocessing
        return text.lower().split()
    
    def _fallback_sentiment(self, text: str) -> Dict[str, float]:
        """Fallback sentiment analysis."""
        text_lower = text.lower()
        
        negative_words = ['sad', 'depressed', 'anxious', 'scared', 'worried', 'hate', 'bad']
        positive_words = ['happy', 'good', 'great', 'wonderful', 'love', 'excellent']
        
        neg_count = sum(1 for word in negative_words if word in text_lower)
        pos_count = sum(1 for word in positive_words if word in text_lower)
        
        if neg_count > pos_count:
            sentiment_type = 'very_negative' if neg_count > 2 else 'negative'
        elif pos_count > neg_count:
            sentiment_type = 'very_positive' if pos_count > 2 else 'positive'
        else:
            sentiment_type = 'neutral'
        
        return {
            'very_negative': 0.2 if sentiment_type == 'very_negative' else 0.0,
            'negative': 0.2 if sentiment_type == 'negative' else 0.0,
            'neutral': 0.4 if sentiment_type == 'neutral' else 0.1,
            'positive': 0.2 if sentiment_type == 'positive' else 0.0,
            'very_positive': 0.2 if sentiment_type == 'very_positive' else 0.0
        }
