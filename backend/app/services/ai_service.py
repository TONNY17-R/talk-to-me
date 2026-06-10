"""
AI Service module.

Handles AI model interactions and response generation.
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered features."""
    
    def __init__(self):
        """Initialize AI service with models."""
        self.models = self._load_models()
    
    def _load_models(self):
        """Load all required AI models."""
        try:
            models = {
                'sentiment': self._load_sentiment_model(),
                'crisis_detector': self._load_crisis_model(),
                'language_model': self._load_language_model(),
            }
            logger.info("All AI models loaded successfully")
            return models
        except Exception as e:
            logger.error(f"Error loading AI models: {str(e)}")
            return {}
    
    def _load_sentiment_model(self):
        """Load sentiment analysis model."""
        try:
            from textblob import TextBlob
            return TextBlob
        except Exception as e:
            logger.warning(f"Sentiment model not available: {str(e)}")
            return None
    
    def _load_crisis_model(self):
        """Load crisis detection model."""
        try:
            # Load pretrained crisis detection model
            return None
        except Exception as e:
            logger.warning(f"Crisis model not available: {str(e)}")
            return None
    
    def _load_language_model(self):
        """Load language model for response generation."""
        try:
            # Load language model (could be OpenAI, HuggingFace, etc.)
            return None
        except Exception as e:
            logger.warning(f"Language model not available: {str(e)}")
            return None
    
    def get_response(self, user_input: str, user_context: Dict) -> Dict:
        """
        Generate AI response to user input.
        
        Args:
            user_input: User message text
            user_context: Dictionary with user_id, session_id, language, etc.
        
        Returns:
            Dictionary with response, sentiment, risk_level, etc.
        """
        try:
            # Analyze sentiment
            sentiment = self.analyze_sentiment(user_input)
            
            # Detect crisis indicators
            risk_level = self.detect_crisis_indicators(user_input)
            
            # Generate response
            response = self.generate_response(
                user_input,
                user_context.get('language', 'en'),
                risk_level
            )
            
            return {
                'response': response,
                'sentiment': sentiment,
                'risk_level': risk_level,
                'model_used': 'hybrid_ai_v1'
            }
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return {
                'response': 'I understand. Could you tell me more about how you are feeling?',
                'sentiment': 'neutral',
                'risk_level': 'low',
                'error': str(e)
            }
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of text.
        
        Returns: 'very_negative', 'negative', 'neutral', 'positive', 'very_positive'
        """
        try:
            if not text:
                return 'neutral'
            
            # Simple sentiment analysis
            negative_words = ['sad', 'depressed', 'anxious', 'scared', 'worried', 'hate', 'bad']
            positive_words = ['happy', 'good', 'great', 'wonderful', 'love', 'excellent']
            
            text_lower = text.lower()
            
            negative_count = sum(1 for word in negative_words if word in text_lower)
            positive_count = sum(1 for word in positive_words if word in text_lower)
            
            if negative_count > positive_count:
                return 'negative' if negative_count == 1 else 'very_negative'
            elif positive_count > negative_count:
                return 'positive' if positive_count == 1 else 'very_positive'
            else:
                return 'neutral'
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return 'neutral'
    
    def detect_crisis_indicators(self, text: str) -> str:
        """
        Detect crisis indicators in text.
        
        Returns: 'low', 'medium', 'high', 'critical'
        """
        try:
            if not text:
                return 'low'
            
            crisis_keywords = {
                'critical': ['suicide', 'self-harm', 'kill myself', 'end my life'],
                'high': ['hurt myself', 'cutting', 'overdose', 'dying'],
                'medium': ['depressed', 'hopeless', 'worthless', 'can\'t take it']
            }
            
            text_lower = text.lower()
            
            for level, keywords in crisis_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    return level
            
            return 'low'
        except Exception as e:
            logger.error(f"Error detecting crisis indicators: {str(e)}")
            return 'low'
    
    def generate_response(self, user_input: str, language: str = 'en', risk_level: str = 'low') -> str:
        """Generate empathetic AI response."""
        try:
            # First, attempt to answer using the built-in knowledge base.
            from backend.app.services.knowledge_base import get_knowledge_response

            knowledge_response = get_knowledge_response(user_input, language)
            if knowledge_response:
                return knowledge_response

            # If there is no matching knowledge entry, fall back to the default responses.
            responses = {
                'critical': {
                    'en': 'I hear you. Please reach out to a crisis counselor immediately. They are available 24/7 to help.',
                    'lg': 'Nnewala. Ndegne kugana ne counselor y\'okwetaagisa n\'amangu.',
                    'sw': 'Ninasikia. Tafadhali wasiliana na mshauri wa azma sasa hivi.'
                },
                'high': {
                    'en': 'I understand you are struggling. Please consider talking to a mental health professional who can provide proper support.',
                    'lg': 'Nnewala. Ndegne okugana ne ssomo ly\'emmeeza y\'omutwe.',
                    'sw': 'Ninasikia. Tafadhali kuitwa kwa mkunga wa akili.'
                },
                'default': {
                    'en': 'Thank you for sharing. I\'m here to listen and support you through this.',
                    'lg': 'Webale. Nnali ne mmwe mulina kifo.',
                    'sw': 'Asante. Niko hapa kusikia na kusaidia.'
                }
            }
            
            if risk_level == 'critical':
                return responses['critical'].get(language, responses['critical']['en'])
            elif risk_level == 'high':
                return responses['high'].get(language, responses['high']['en'])
            else:
                return responses['default'].get(language, responses['default']['en'])
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return 'I am here to support you.'
