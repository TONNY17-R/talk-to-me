"""
Crisis Command Center Service
Real-time crisis detection, multi-modal analysis, automated responses, and emergency protocols
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)


class CrisisCommandCenterService:
    """Advanced crisis detection and response management"""
    
    def __init__(self):
        self.alert_levels = ['warning', 'severe', 'critical', 'emergency']
        self.response_times = {
            'emergency': 5,  # minutes
            'critical': 15,
            'severe': 60,
            'warning': 240,
        }
    
    def analyze_multimodal_crisis_indicators(
        self,
        user_id: int,
        text_data: Dict,
        voice_data: Dict,
        behavioral_data: Dict,
        pattern_data: Dict
    ) -> Dict:
        """
        Comprehensive crisis detection using multiple data sources
        
        Args:
            user_id: User ID
            text_data: Text analysis results (keywords, sentiment)
            voice_data: Voice analysis (emotion, speech patterns)
            behavioral_data: Usage patterns, engagement changes
            pattern_data: Historical patterns and anomalies
        
        Returns:
            Crisis alert with alert level and recommended response
        """
        try:
            # Score each modality
            text_score = self._score_text_analysis(text_data)
            voice_score = self._score_voice_analysis(voice_data)
            behavioral_score = self._score_behavioral_changes(behavioral_data)
            pattern_score = self._score_pattern_anomalies(pattern_data)
            
            # Calculate composite score
            weights = {
                'text': 0.3,
                'voice': 0.3,
                'behavioral': 0.2,
                'pattern': 0.2,
            }
            
            composite_score = (
                text_score * weights['text'] +
                voice_score * weights['voice'] +
                behavioral_score * weights['behavioral'] +
                pattern_score * weights['pattern']
            )
            
            # Determine alert level
            alert_level = self._determine_alert_level(composite_score)
            
            # Identify contributing factors
            factors = self._identify_crisis_factors(
                text_data, voice_data, behavioral_data
            )
            
            # Detect location if available
            location_data = behavioral_data.get('location', {})
            
            return {
                'user_id': user_id,
                'alert_level': alert_level,
                'composite_crisis_score': composite_score,
                'individual_scores': {
                    'text_analysis': text_score,
                    'voice_analysis': voice_score,
                    'behavioral_changes': behavioral_score,
                    'pattern_anomalies': pattern_score,
                },
                'detection_method': self._get_detection_method(
                    text_score, voice_score
                ),
                'confidence_score': max(text_score, voice_score, behavioral_score),
                'contributing_factors': factors,
                'location_data': location_data,
                'recommended_response': self._get_recommended_response(alert_level),
                'estimated_response_time_minutes': self.response_times[alert_level],
                'timestamp': datetime.now().isoformat(),
                'requires_immediate_action': alert_level in ['critical', 'emergency'],
            }
        except Exception as e:
            logger.error(f"Error in crisis analysis: {e}")
            return {'error': str(e)}
    
    def trigger_emergency_response(
        self,
        user_id: int,
        alert_data: Dict,
        emergency_contacts: List[Dict],
        available_counselors: List[int]
    ) -> Dict:
        """
        Trigger emergency response protocols
        
        Returns:
            Emergency response action plan
        """
        try:
            actions = {
                'notify_emergency_contacts': [],
                'assign_counselor': None,
                'emergency_services_alert': False,
                'location_alert': False,
                'follow_up_schedule': None,
            }
            
            alert_level = alert_data['alert_level']
            
            # Notify emergency contacts for critical/emergency
            if alert_level in ['critical', 'emergency']:
                actions['notify_emergency_contacts'] = self._prepare_emergency_notifications(
                    user_id,
                    emergency_contacts,
                    alert_data
                )
                
                # Consider alerting emergency services
                if alert_level == 'emergency':
                    actions['emergency_services_alert'] = True
                    actions['location_alert'] = bool(alert_data.get('location_data'))
            
            # Assign highest-priority counselor
            if available_counselors:
                actions['assign_counselor'] = available_counselors[0]
            
            # Schedule immediate follow-up
            actions['follow_up_schedule'] = {
                'first_contact': '5_minutes',
                'video_session': '15_minutes',
                'ongoing_monitoring': 'continuous'
            }
            
            return {
                'user_id': user_id,
                'alert_level': alert_level,
                'emergency_response_triggered': True,
                'actions': actions,
                'response_started': datetime.now().isoformat(),
                'escalation_protocol': self._get_escalation_protocol(alert_level),
            }
        except Exception as e:
            logger.error(f"Error triggering emergency response: {e}")
            return {}
    
    def create_crisis_session(
        self,
        user_id: int,
        counselor_id: int,
        alert_id: int,
        session_type: str = 'video'
    ) -> Dict:
        """
        Create crisis counseling session
        
        Returns:
            Crisis session details with AI co-pilot setup
        """
        try:
            return {
                'user_id': user_id,
                'counselor_id': counselor_id,
                'alert_id': alert_id,
                'session_type': session_type,
                'session_started': datetime.now().isoformat(),
                'ai_copilot_enabled': True,
                'ai_suggestions_frequency': 'real_time',
                'transcript_recording': True,
                'emergency_protocols_active': True,
                'live_suicide_risk_monitoring': True,
                'session_timeout': (datetime.now() + timedelta(hours=2)).isoformat(),
                'followup_scheduling': 'automatic',
            }
        except Exception as e:
            logger.error(f"Error creating crisis session: {e}")
            return {}
    
    def generate_crisis_session_recommendations(
        self,
        session_transcript: str,
        user_assessment: Dict
    ) -> Dict:
        """
        Generate AI recommendations during crisis session
        
        Returns:
            Real-time suggestions for counselor
        """
        try:
            # Analyze current dialogue
            risk_indicators = self._analyze_risk_indicators_in_transcript(
                session_transcript
            )
            
            recommendations = []
            
            # Generate interventions based on content
            if 'suicide' in session_transcript.lower():
                recommendations.append({
                    'type': 'safety_planning',
                    'action': 'Initiate safety plan discussion',
                    'priority': 'critical'
                })
            
            if 'hopelessness' in session_transcript.lower():
                recommendations.append({
                    'type': 'hope_building',
                    'action': 'Use motivational interviewing techniques',
                    'priority': 'high'
                })
            
            if 'isolation' in session_transcript.lower():
                recommendations.append({
                    'type': 'social_connection',
                    'action': 'Discuss social support activation',
                    'priority': 'high'
                })
            
            return {
                'risk_level': risk_indicators.get('overall_risk', 'unknown'),
                'immediate_recommendations': recommendations,
                'counselor_guidance': self._generate_counselor_guidance(
                    risk_indicators
                ),
                'hospitalization_recommended': risk_indicators.get('active_suicidality', False),
            }
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {}
    
    def post_crisis_followup_plan(
        self,
        user_id: int,
        crisis_session_data: Dict,
        counselor_notes: str
    ) -> Dict:
        """
        Generate post-crisis follow-up plan
        
        Returns:
            Automated follow-up schedule and interventions
        """
        try:
            return {
                'user_id': user_id,
                'plan_start_date': datetime.now().isoformat(),
                'followup_schedule': {
                    'day_1': 'Phone check-in - morning',
                    'day_2': 'Video session with counselor',
                    'day_3': 'Peer support group introduction',
                    'week_1': 'Twice-weekly therapy sessions',
                    'week_2': 'Assess medication adjustment',
                    'week_4': 'Comprehensive reassessment',
                },
                'safety_monitoring': {
                    'frequency': 'daily',
                    'method': 'in_app_check_ins',
                    'emergency_hotline': 'always_available',
                },
                'therapeutic_interventions': [
                    'Crisis-focused CBT',
                    'Safety planning exercises',
                    'Coping skill development',
                    'Medication management if applicable',
                ],
                'peer_support_referrals': ['Crisis_recovery_group', 'Suicidal_ideation_support_group'],
                'lifestyle_recommendations': [
                    'Sleep hygiene protocol',
                    'Physical activity schedule',
                    'Nutrition guidance',
                    'Substance avoidance enforcement',
                ],
                'barriers_to_address': self._identify_followup_barriers(counselor_notes),
                'success_indicators': [
                    'Engagement in therapy sessions',
                    'Completion of homework assignments',
                    'Stabilization of mood scores',
                    'No further crisis indicators',
                ],
                'next_review_date': (datetime.now() + timedelta(weeks=2)).isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating followup plan: {e}")
            return {}
    
    # Helper methods
    
    def _score_text_analysis(self, text_data: Dict) -> float:
        """Score text-based crisis indicators"""
        score = 0.0
        
        crisis_keywords = text_data.get('crisis_keywords_detected', 0)
        score += min(0.5, crisis_keywords / 5)
        
        sentiment_score = text_data.get('sentiment_score', 0)
        score += max(0, -sentiment_score) * 0.3  # Negative sentiment increases score
        
        hopelessness_indicators = text_data.get('hopelessness_indicators', 0)
        score += min(0.2, hopelessness_indicators / 3)
        
        return min(1.0, score)
    
    def _score_voice_analysis(self, voice_data: Dict) -> float:
        """Score voice-based crisis indicators"""
        score = 0.0
        
        suicidality_score = voice_data.get('suicidality_risk_score', 0)
        score += suicidality_score * 0.6
        
        depression_likelihood = voice_data.get('depression_likelihood', 0)
        score += depression_likelihood * 0.3
        
        emotional_flatness = 1.0 - voice_data.get('emotion_confidence', 0.5)
        score += emotional_flatness * 0.1
        
        return min(1.0, score)
    
    def _score_behavioral_changes(self, behavioral_data: Dict) -> float:
        """Score behavioral change indicators"""
        score = 0.0
        
        engagement_drop = behavioral_data.get('engagement_drop_percentage', 0)
        score += min(0.5, engagement_drop / 100)
        
        sleep_disruption = abs(behavioral_data.get('sleep_change', 0))
        score += min(0.3, sleep_disruption / 8)
        
        social_withdrawal = behavioral_data.get('social_withdrawal_score', 0)
        score += social_withdrawal * 0.2
        
        return min(1.0, score)
    
    def _score_pattern_anomalies(self, pattern_data: Dict) -> float:
        """Score pattern-based anomalies"""
        score = pattern_data.get('anomaly_score', 0)
        return min(1.0, score)
    
    def _determine_alert_level(self, composite_score: float) -> str:
        """Determine alert level from composite score"""
        if composite_score >= 0.85:
            return 'emergency'
        elif composite_score >= 0.65:
            return 'critical'
        elif composite_score >= 0.45:
            return 'severe'
        elif composite_score >= 0.25:
            return 'warning'
        else:
            return 'warning'
    
    def _identify_crisis_factors(self, text_data, voice_data, behavioral_data) -> List[str]:
        """Identify contributing factors"""
        factors = []
        
        if text_data.get('crisis_keywords_detected', 0) > 0:
            factors.append('Expressed suicidal ideation')
        
        if voice_data.get('suicidality_risk_score', 0) > 0.6:
            factors.append('Voice indicators of suicidality')
        
        if behavioral_data.get('engagement_drop_percentage', 0) > 50:
            factors.append('Dramatic disengagement from app')
        
        if behavioral_data.get('social_withdrawal_score', 0) > 0.7:
            factors.append('Social isolation indicators')
        
        return factors
    
    def _get_detection_method(self, text_score, voice_score):
        """Get primary detection method"""
        if voice_score > text_score:
            return 'voice_analysis'
        elif text_score > voice_score:
            return 'text_analysis'
        else:
            return 'multimodal'
    
    def _get_recommended_response(self, alert_level: str) -> str:
        """Get recommended response for alert level"""
        responses = {
            'emergency': 'Immediate emergency services contact + crisis counselor + family notification',
            'critical': 'Immediate crisis counselor assignment + emergency contact notification',
            'severe': 'Urgent counselor assignment + close monitoring + family optional notification',
            'warning': 'Scheduled counselor contact + increased monitoring',
        }
        return responses.get(alert_level, 'Standard monitoring')
    
    def _prepare_emergency_notifications(self, user_id: int, contacts: List[Dict], alert_data: Dict) -> List[Dict]:
        """Prepare emergency contact notifications"""
        notifications = []
        
        for contact in contacts:
            notifications.append({
                'contact_id': contact['contact_id'],
                'phone': contact.get('phone'),
                'email': contact.get('email'),
                'message': f"Your loved one has been flagged for a mental health emergency. Contact them immediately or call local emergency services.",
                'send_immediately': True,
                'followup_after_minutes': 10,
            })
        
        return notifications
    
    def _get_escalation_protocol(self, alert_level: str) -> Dict:
        """Get escalation protocol details"""
        protocols = {
            'emergency': {
                'step_1': 'Call emergency services if immediate danger',
                'step_2': 'Attempt direct contact with user',
                'step_3': 'Notify emergency contacts',
                'step_4': 'Crisis counselor begins immediate session',
            },
            'critical': {
                'step_1': 'Crisis counselor begins immediate call',
                'step_2': 'Notify emergency contacts',
                'step_3': 'Arrange video session if phone not successful',
                'step_4': 'Assess hospitalization need',
            },
            'severe': {
                'step_1': 'Attempt counselor contact within 30 minutes',
                'step_2': 'Provide crisis resources',
                'step_3': 'Optional family notification',
                'step_4': 'Close monitoring for escalation',
            },
            'warning': {
                'step_1': 'Schedule counselor contact',
                'step_2': 'Increase app engagement checks',
                'step_3': 'Provide educational resources',
                'step_4': 'Reassess in 24 hours',
            },
        }
        return protocols.get(alert_level, {})
    
    def _analyze_risk_indicators_in_transcript(self, transcript: str) -> Dict:
        """Analyze risk indicators in session transcript"""
        indicators = {
            'overall_risk': 'low',
            'active_suicidality': False,
            'self_harm_risk': False,
            'hopelessness': False,
        }
        
        transcript_lower = transcript.lower()
        
        if any(w in transcript_lower for w in ['kill', 'suicide', 'dead', 'die']):
            indicators['active_suicidality'] = True
            indicators['overall_risk'] = 'high'
        
        if 'harm' in transcript_lower or 'cut' in transcript_lower:
            indicators['self_harm_risk'] = True
            indicators['overall_risk'] = 'moderate' if indicators['overall_risk'] == 'low' else indicators['overall_risk']
        
        if 'hopeless' in transcript_lower or 'no point' in transcript_lower:
            indicators['hopelessness'] = True
        
        return indicators
    
    def _generate_counselor_guidance(self, risk_indicators: Dict) -> List[str]:
        """Generate guidance for counselor"""
        guidance = []
        
        if risk_indicators['active_suicidality']:
            guidance.append('Implement safety planning immediately')
            guidance.append('Assess access to lethal means')
            guidance.append('Consider hospitalization')
        
        if risk_indicators['self_harm_risk']:
            guidance.append('Discuss alternative coping mechanisms')
            guidance.append('Remove access to self-harm tools if possible')
        
        if risk_indicators['hopelessness']:
            guidance.append('Use behavioral activation techniques')
            guidance.append('Build collaborative hope')
        
        return guidance
    
    def _identify_followup_barriers(self, notes: str) -> List[str]:
        """Identify barriers mentioned in counselor notes"""
        barriers = []
        
        if 'transportation' in notes.lower():
            barriers.append('Transportation challenges')
        
        if 'financial' in notes.lower():
            barriers.append('Financial constraints')
        
        if 'family' in notes.lower():
            barriers.append('Family relationship issues')
        
        if 'substance' in notes.lower():
            barriers.append('Substance use involvement')
        
        return barriers if barriers else ['None identified']
