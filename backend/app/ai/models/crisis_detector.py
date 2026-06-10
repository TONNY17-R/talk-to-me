"""Crisis detection model for identifying high-risk situations."""

import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class CrisisDetector:
    """Detect crisis indicators in user communications."""
    
    def __init__(self):
        """Initialize crisis detector."""
        self.model = None
        self._load_model()
        self.crisis_keywords = self._load_crisis_keywords()
    
    def _load_model(self):
        """Load pre-trained crisis detection model."""
        try:
            logger.info("Crisis detector model loaded")
        except Exception as e:
            logger.warning(f"Could not load crisis detector: {str(e)}")
    
    def _load_crisis_keywords(self) -> dict:
        """Load crisis-related keywords by severity level."""
        return {
            'critical': [
                'suicide', 'self-harm', 'kill myself', 'end my life',
                'jump', 'overdose', 'poison', 'hanging'
            ],
            'high': [
                'hurt myself', 'cutting', 'self-injury', 'dying',
                'not worth living', 'better off dead', 'harm'
            ],
            'medium': [
                'depressed', 'hopeless', 'worthless', 'can\'t take it',
                'can\'t go on', 'give up', 'no point'
            ]
        }
    
    def detect(self, text: str) -> Tuple[str, float]:
        """
        Detect crisis indicators in text.
        
        Args:
            text: User input text
        
        Returns:
            Tuple of (risk_level, confidence_score)
        """
        try:
            if not text:
                return 'low', 0.0
            
            # Use keyword-based detection
            risk_level = self._keyword_detection(text)
            confidence = self._calculate_confidence(text, risk_level)
            
            return risk_level, confidence
        except Exception as e:
            logger.error(f"Error detecting crisis: {str(e)}")
            return 'low', 0.5
    
    def _keyword_detection(self, text: str) -> str:
        """Detect crisis using keyword matching."""
        text_lower = text.lower()
        
        for level, keywords in self.crisis_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return level
        
        return 'low'
    
    def _calculate_confidence(self, text: str, risk_level: str) -> float:
        """Calculate confidence score for detection."""
        text_lower = text.lower()
        
        # Count matching keywords
        matches = 0
        for keyword in self.crisis_keywords.get(risk_level, []):
            matches += text_lower.count(keyword)
        
        # Normalize confidence
        confidence = min(matches * 0.3, 1.0)
        return confidence
    
    def get_recommended_action(self, risk_level: str) -> dict:
        """Get recommended action based on risk level."""
        actions = {
            'critical': {
                'action': 'immediate_intervention',
                'notification': True,
                'alert_admin': True,
                'message': 'Please contact emergency services or a crisis counselor immediately'
            },
            'high': {
                'action': 'urgent_counselling',
                'notification': True,
                'alert_admin': True,
                'message': 'Please reach out to a mental health professional'
            },
            'medium': {
                'action': 'recommend_resources',
                'notification': False,
                'alert_admin': False,
                'message': 'Consider accessing our support resources'
            },
            'low': {
                'action': 'continue_chat',
                'notification': False,
                'alert_admin': False,
                'message': 'Continue with support'
            }
        }
        return actions.get(risk_level, actions['low'])
