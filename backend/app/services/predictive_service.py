"""
Advanced Predictive Analytics Service
Provides mental health trajectory prediction, risk stratification, and intervention recommendations
"""

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import logging
from config import Config
import tensorflow as tf

logger = logging.getLogger(__name__)


class PredictiveAnalyticsService:
    """Predicts mental health trajectories and recommends interventions"""
    
    def __init__(self):
        self.trajectory_model = None
        self.risk_classifier = None
        self.relapse_predictor = None
        self.scaler = StandardScaler()
        self.load_models()
        
    def load_models(self):
        """Load or initialize ML models"""
        try:
            # Load pre-trained models
            self.trajectory_model = tf.keras.models.load_model(
                'ml_models/trained_models/trajectory_predictor.h5'
            )
            self.risk_classifier = tf.keras.models.load_model(
                'ml_models/trained_models/risk_classifier.h5'
            )
            self.relapse_predictor = tf.keras.models.load_model(
                'ml_models/trained_models/relapse_detector.h5'
            )
            logger.info("Pre-trained models loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load pre-trained models: {e}")
            self._initialize_default_models()
    
    def _initialize_default_models(self):
        """Initialize models with default architecture if training data not available"""
        self.trajectory_model = GradientBoostingRegressor(n_estimators=100)
        self.risk_classifier = RandomForestClassifier(n_estimators=100)
        self.relapse_predictor = RandomForestClassifier(n_estimators=100)
    
    def predict_mental_health_trajectory(
        self, 
        user_id: int,
        assessment_history: List[Dict],
        engagement_metrics: Dict,
        days_ahead: int = 28
    ) -> Dict:
        """
        Predict user's mental health trajectory 2-4 weeks ahead
        
        Args:
            user_id: User ID
            assessment_history: List of historical assessments (PHQ-9, GAD-7 scores)
            engagement_metrics: User engagement data
            days_ahead: Days to predict ahead (default 28 days)
        
        Returns:
            Dictionary with prediction, confidence, and recommendations
        """
        try:
            # Extract features from history
            features = self._extract_trajectory_features(
                assessment_history, 
                engagement_metrics
            )
            
            # Scale features
            features_scaled = self.scaler.fit_transform([features])
            
            # Make prediction
            if self.trajectory_model:
                prediction = self.trajectory_model.predict(features_scaled)[0]
            else:
                prediction = self._estimate_trajectory(assessment_history)
            
            # Determine trajectory direction
            if len(assessment_history) >= 2:
                recent_trend = assessment_history[-1]['score'] - assessment_history[-2]['score']
            else:
                recent_trend = 0
            
            projected_score = assessment_history[-1]['score'] + (recent_trend * (days_ahead / 30))
            
            severity = self._classify_severity(projected_score)
            confidence = min(0.95, 0.5 + (len(assessment_history) / 100))
            
            recommendation = self._generate_intervention_recommendation(
                current_score=assessment_history[-1]['score'],
                projected_score=projected_score,
                trend=recent_trend
            )
            
            return {
                'user_id': user_id,
                'current_score': assessment_history[-1]['score'],
                'projected_score': projected_score,
                'prediction_days_ahead': days_ahead,
                'predicted_severity': severity,
                'confidence_score': confidence,
                'trend': 'improving' if recent_trend < -2 else ('declining' if recent_trend > 2 else 'stable'),
                'factors': {
                    'recent_engagement': engagement_metrics.get('engagement_score', 0),
                    'assessment_frequency': len(assessment_history),
                    'crisis_events': engagement_metrics.get('crisis_count', 0),
                    'therapy_adherence': engagement_metrics.get('therapy_adherence', 0),
                },
                'recommended_intervention': recommendation,
                'intervention_timing': self._determine_timing(severity),
                'predicted_date': (datetime.now() + timedelta(days=days_ahead)).date().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in trajectory prediction: {e}")
            return self._fallback_trajectory(assessment_history)
    
    def stratify_user_risk(
        self,
        user_id: int,
        phq9_score: int,
        gad7_score: int,
        crisis_indicators: Dict,
        behavioral_data: Dict
    ) -> Dict:
        """
        Stratify user into risk tier: low, medium, high, critical
        
        Args:
            user_id: User ID
            phq9_score: PHQ-9 depression assessment score (0-27)
            gad7_score: GAD-7 anxiety assessment score (0-21)
            crisis_indicators: Dictionary of crisis indicators
            behavioral_data: Dictionary of behavioral metrics
        
        Returns:
            Risk tier and detailed breakdown
        """
        try:
            # Compile risk factors
            risk_scores = {
                'depression_score': phq9_score / 27,  # Normalize to 0-1
                'anxiety_score': gad7_score / 21,      # Normalize to 0-1
                'crisis_keywords': min(1.0, crisis_indicators.get('keyword_count', 0) / 5),
                'failed_sessions': min(1.0, crisis_indicators.get('failed_sessions', 0) / 3),
                'days_without_engagement': min(1.0, crisis_indicators.get('days_inactive', 0) / 30),
                'self_harm_indicators': min(1.0, crisis_indicators.get('self_harm_mentions', 0) / 2),
                'substance_use': min(1.0, behavioral_data.get('substance_use_score', 0)),
                'isolation_score': behavioral_data.get('isolation_score', 0),
            }
            
            # Calculate composite risk score
            weights = {
                'depression_score': 0.25,
                'anxiety_score': 0.20,
                'crisis_keywords': 0.15,
                'self_harm_indicators': 0.20,
                'failed_sessions': 0.10,
                'substance_use': 0.05,
                'days_without_engagement': 0.03,
                'isolation_score': 0.02,
            }
            
            composite_score = sum(
                risk_scores[key] * weights[key] 
                for key in risk_scores
            )
            
            # Determine tier
            if composite_score >= 0.75:
                tier = 'critical'
            elif composite_score >= 0.5:
                tier = 'high'
            elif composite_score >= 0.25:
                tier = 'medium'
            else:
                tier = 'low'
            
            return {
                'user_id': user_id,
                'current_tier': tier,
                'composite_risk_score': composite_score,
                'phq9_score': phq9_score,
                'gad7_score': gad7_score,
                'risk_factors': risk_scores,
                'highest_risk_areas': sorted(
                    risk_scores.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:3],
                'reassessment_frequency': self._get_reassessment_frequency(tier),
                'monitoring_level': self._get_monitoring_level(tier),
                'stratification_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in risk stratification: {e}")
            return {'user_id': user_id, 'current_tier': 'medium', 'error': str(e)}
    
    def predict_relapse_risk(
        self,
        user_id: int,
        recovery_history: List[Dict],
        current_stressors: List[str],
        social_support_score: float,
        medication_adherence: float
    ) -> Dict:
        """
        Predict relapse risk for users in recovery
        
        Args:
            user_id: User ID
            recovery_history: Historical recovery data
            current_stressors: Current life stressors
            social_support_score: Score of social support (0-10)
            medication_adherence: Medication adherence rate (0-1)
        
        Returns:
            Relapse risk prediction and protective factors
        """
        try:
            # Calculate risk factors
            risk_factors = {
                'days_in_recovery': len(recovery_history),
                'stressor_count': len(current_stressors),
                'social_support_deficit': 10 - social_support_score,
                'medication_non_adherence': 1 - medication_adherence,
                'previous_relapse_count': sum(1 for r in recovery_history if r.get('relapsed')),
            }
            
            # Calculate risk probability
            relapse_probability = (
                0.2 * min(1.0, risk_factors['days_in_recovery'] / 365) +  # Time factor
                0.2 * min(1.0, risk_factors['stressor_count'] / 5) +  # Stressor factor
                0.2 * risk_factors['social_support_deficit'] / 10 +  # Support factor
                0.2 * risk_factors['medication_non_adherence'] +  # Adherence factor
                0.2 * min(1.0, risk_factors['previous_relapse_count'] / 3)  # History factor
            )
            
            # Identify high-risk periods
            risk_periods = self._identify_relapse_risk_periods(
                current_stressors, 
                recovery_history
            )
            
            # Generate protective strategies
            protective_strategies = self._generate_protective_strategies(
                risk_factors,
                social_support_score,
                medication_adherence
            )
            
            return {
                'user_id': user_id,
                'relapse_probability': relapse_probability,
                'risk_level': 'critical' if relapse_probability > 0.7 else (
                    'high' if relapse_probability > 0.4 else 'moderate' if relapse_probability > 0.2 else 'low'
                ),
                'risk_factors': risk_factors,
                'high_risk_periods': risk_periods,
                'protective_factors': {
                    'medication_adherence': medication_adherence,
                    'social_support_available': social_support_score / 10,
                    'time_in_recovery': risk_factors['days_in_recovery'],
                },
                'protective_strategies': protective_strategies,
                'monitoring_frequency': 'daily' if relapse_probability > 0.7 else (
                    'weekly' if relapse_probability > 0.4 else 'monthly'
                ),
                'prediction_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in relapse prediction: {e}")
            return {'user_id': user_id, 'relapse_probability': 0.5, 'error': str(e)}
    
    def get_personalized_intervention_timing(
        self,
        user_id: int,
        user_activity_pattern: List[Dict],
        timezone: str = 'UTC'
    ) -> Dict:
        """
        Determine optimal time to reach out to user based on activity patterns
        
        Returns:
            Recommended contact times and channels
        """
        try:
            # Analyze activity patterns
            activity_by_hour = {}
            for activity in user_activity_pattern:
                hour = int(activity['timestamp'].split('T')[1].split(':')[0])
                activity_by_hour[hour] = activity_by_hour.get(hour, 0) + 1
            
            # Find peak engagement hours
            peak_hours = sorted(
                activity_by_hour.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]
            
            # Determine best contact times
            optimal_hours = [hour for hour, _ in peak_hours]
            
            return {
                'user_id': user_id,
                'optimal_contact_hours': optimal_hours,
                'optimal_contact_times': [f"{h:02d}:00" for h in optimal_hours],
                'timezone': timezone,
                'recommended_channel': self._recommend_channel(user_activity_pattern),
                'frequency': self._determine_optimal_frequency(user_activity_pattern),
                'avoid_contact_hours': list(set(range(24)) - set(optimal_hours))[-5:],
                'next_recommended_contact': self._calculate_next_contact_time(optimal_hours),
            }
        except Exception as e:
            logger.error(f"Error calculating intervention timing: {e}")
            return {'user_id': user_id, 'error': str(e)}
    
    # Helper methods
    
    def _extract_trajectory_features(self, assessment_history, engagement_metrics):
        """Extract features for trajectory prediction model"""
        if len(assessment_history) == 0:
            return [0] * 10
        
        scores = [a['score'] for a in assessment_history[-12:]]  # Last 12 assessments
        
        features = [
            np.mean(scores),
            np.std(scores),
            scores[-1] if scores else 0,
            scores[-1] - scores[0] if len(scores) > 1 else 0,
            engagement_metrics.get('engagement_score', 0),
            engagement_metrics.get('crisis_count', 0),
            engagement_metrics.get('therapy_adherence', 0),
            engagement_metrics.get('chat_frequency', 0),
            engagement_metrics.get('resource_views', 0),
            len(assessment_history),
        ]
        return features
    
    def _estimate_trajectory(self, assessment_history):
        """Fallback trajectory estimation using linear regression"""
        if len(assessment_history) < 2:
            return assessment_history[-1]['score'] if assessment_history else 15
        
        x = np.arange(len(assessment_history))
        y = np.array([a['score'] for a in assessment_history])
        
        # Simple linear regression
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        return float(p(len(assessment_history) + 28/30))
    
    def _classify_severity(self, score):
        """Classify score to severity level"""
        if score < 5:
            return 'minimal'
        elif score < 10:
            return 'mild'
        elif score < 15:
            return 'moderate'
        elif score < 20:
            return 'moderately_severe'
        else:
            return 'severe'
    
    def _generate_intervention_recommendation(self, current_score, projected_score, trend):
        """Generate intervention recommendation based on trajectory"""
        if projected_score > 20:
            return "Increase therapy frequency. Consider psychiatric evaluation."
        elif projected_score > 15 and trend > 1:
            return "Proactive outreach recommended. Increase engagement with coping resources."
        elif projected_score > 15:
            return "Maintain current intervention level. Monitor closely."
        elif projected_score < 5 and current_score > 10:
            return "Celebrate progress! Transition to maintenance phase."
        else:
            return "Continue current treatment plan. Regular follow-ups recommended."
    
    def _determine_timing(self, severity):
        """Determine intervention timing based on severity"""
        timing_map = {
            'critical': 'immediate',
            'high': 'within_24h',
            'severe': 'within_24h',
            'moderately_severe': 'within_week',
            'moderate': 'within_week',
            'mild': 'scheduled',
            'minimal': 'scheduled',
        }
        return timing_map.get(severity, 'scheduled')
    
    def _get_reassessment_frequency(self, tier):
        """Determine reassessment frequency by risk tier"""
        frequencies = {
            'critical': 'weekly',
            'high': 'bi-weekly',
            'medium': 'monthly',
            'low': 'quarterly',
        }
        return frequencies.get(tier, 'monthly')
    
    def _get_monitoring_level(self, tier):
        """Determine monitoring level by risk tier"""
        levels = {
            'critical': 'intensive',
            'high': 'regular',
            'medium': 'standard',
            'low': 'minimal',
        }
        return levels.get(tier, 'standard')
    
    def _identify_relapse_risk_periods(self, stressors, recovery_history):
        """Identify periods of high relapse risk"""
        seasonal_risks = ['winter', 'anniversary_of_trauma']
        life_event_risks = stressors[:3]
        
        return seasonal_risks + life_event_risks
    
    def _generate_protective_strategies(self, risk_factors, social_support, adherence):
        """Generate protective strategies"""
        strategies = []
        
        if risk_factors['social_support_deficit'] > 5:
            strategies.append("Strengthen social support network. Join peer support groups.")
        
        if risk_factors['medication_non_adherence'] > 0.2:
            strategies.append("Improve medication adherence. Set reminders, use pill organizers.")
        
        if risk_factors['stressor_count'] > 3:
            strategies.append("Stress management intensification. Weekly therapy recommended.")
        
        return strategies
    
    def _recommend_channel(self, activity_pattern):
        """Recommend contact channel based on activity"""
        if any('chat' in str(a).lower() for a in activity_pattern[-5:]):
            return 'in_app_message'
        elif any('voice' in str(a).lower() for a in activity_pattern[-5:]):
            return 'phone_call'
        else:
            return 'sms'
    
    def _determine_optimal_frequency(self, activity_pattern):
        """Determine optimal contact frequency"""
        if len(activity_pattern) > 5:
            return 'weekly'
        elif len(activity_pattern) > 2:
            return 'bi-weekly'
        else:
            return 'as_needed'
    
    def _calculate_next_contact_time(self, optimal_hours):
        """Calculate next recommended contact time"""
        if not optimal_hours:
            return datetime.now() + timedelta(hours=1)
        
        next_hour = optimal_hours[0]
        now = datetime.now()
        next_contact = now.replace(hour=next_hour, minute=0, second=0)
        
        if next_contact < now:
            next_contact += timedelta(days=1)
        
        return next_contact.isoformat()
    
    def _fallback_trajectory(self, assessment_history):
        """Fallback response if prediction fails"""
        recent_score = assessment_history[-1]['score'] if assessment_history else 15
        return {
            'current_score': recent_score,
            'predicted_score': recent_score,
            'confidence_score': 0.3,
            'predicted_severity': self._classify_severity(recent_score),
            'recommended_intervention': 'Standard monitoring recommended',
            'error': 'Prediction computed with limited data'
        }
