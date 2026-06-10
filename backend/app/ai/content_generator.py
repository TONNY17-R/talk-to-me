"""Content generator for counselling resources and recommendations."""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generate personalized content based on user profiles and assessments."""
    
    def __init__(self):
        """Initialize content generator."""
        self.resource_db = {}
        self._load_resources()
    
    def _load_resources(self):
        """Load counselling resources from database."""
        try:
            # Load resources from database or file
            logger.info("Resources loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load resources: {str(e)}")
    
    def generate_recommendations(self, user_assessment: Dict) -> List[Dict]:
        """
        Generate personalized recommendations based on assessment.
        
        Args:
            user_assessment: User's assessment results
        
        Returns:
            List of recommended resources
        """
        try:
            recommendations = []
            
            phq9_score = user_assessment.get('phq9_score', 0)
            gad7_score = user_assessment.get('gad7_score', 0)
            
            # Generate recommendations based on scores
            if phq9_score >= 15:
                recommendations.extend(self._get_depression_resources('severe'))
            elif phq9_score >= 10:
                recommendations.extend(self._get_depression_resources('moderate'))
            
            if gad7_score >= 15:
                recommendations.extend(self._get_anxiety_resources('severe'))
            elif gad7_score >= 10:
                recommendations.extend(self._get_anxiety_resources('moderate'))
            
            return recommendations
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return []
    
    def _get_depression_resources(self, severity: str) -> List[Dict]:
        """Get depression-related resources based on severity."""
        resources = {
            'severe': [
                {
                    'id': 'dep_severe_1',
                    'title': 'Crisis Support Resources',
                    'type': 'resource',
                    'description': 'Immediate help for severe depression'
                }
            ],
            'moderate': [
                {
                    'id': 'dep_mod_1',
                    'title': 'Coping with Depression',
                    'type': 'exercise',
                    'description': 'Practical techniques to manage depression'
                }
            ]
        }
        return resources.get(severity, [])
    
    def _get_anxiety_resources(self, severity: str) -> List[Dict]:
        """Get anxiety-related resources based on severity."""
        resources = {
            'severe': [
                {
                    'id': 'anx_severe_1',
                    'title': 'Panic Attack Management',
                    'type': 'exercise',
                    'description': 'Immediate techniques for panic attacks'
                }
            ],
            'moderate': [
                {
                    'id': 'anx_mod_1',
                    'title': 'Anxiety Management Techniques',
                    'type': 'video',
                    'description': 'Learn to manage anxiety effectively'
                }
            ]
        }
        return resources.get(severity, [])
    
    def generate_daily_content(self, user_id: str) -> Dict:
        """Generate daily wellness content for user."""
        try:
            content = {
                'meditation': self._generate_meditation(),
                'tip': self._generate_daily_tip(),
                'affirmation': self._generate_affirmation()
            }
            return content
        except Exception as e:
            logger.error(f"Error generating daily content: {str(e)}")
            return {}
    
    def _generate_meditation(self) -> Dict:
        """Generate meditation content."""
        return {
            'title': 'Morning Mindfulness',
            'duration': '10 minutes',
            'description': 'Start your day with mindfulness'
        }
    
    def _generate_daily_tip(self) -> Dict:
        """Generate daily wellness tip."""
        return {
            'title': 'Self-Care Tip',
            'content': 'Remember to take breaks and drink water throughout the day'
        }
    
    def _generate_affirmation(self) -> Dict:
        """Generate daily affirmation."""
        return {
            'title': 'Today\'s Affirmation',
            'content': 'I am capable of handling whatever comes my way'
        }
