"""
Analytics & Outcomes Service
Population health metrics, treatment efficacy tracking, QALY/DALY calculations, and impact reporting
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np
import logging

logger = logging.getLogger(__name__)


class PopulationHealthAnalytics:
    """Analyzes aggregate mental health metrics for population"""
    
    @staticmethod
    def calculate_population_metrics(
        user_assessments: List[Dict],
        region: Optional[str] = None,
        age_group: Optional[str] = None,
        gender: Optional[str] = None
    ) -> Dict:
        """Calculate population-level mental health metrics"""
        
        try:
            if not user_assessments:
                return {}
            
            phq9_scores = [a.get('phq9_score', 0) for a in user_assessments if a.get('phq9_score')]
            gad7_scores = [a.get('gad7_score', 0) for a in user_assessments if a.get('gad7_score')]
            
            # Calculate depression prevalence (PHQ-9 >= 10 = moderate or higher)
            depression_cases = sum(1 for score in phq9_scores if score >= 10)
            depression_prevalence = (depression_cases / len(phq9_scores) * 100) if phq9_scores else 0
            
            # Calculate anxiety prevalence (GAD-7 >= 10 = moderate or higher)
            anxiety_cases = sum(1 for score in gad7_scores if score >= 10)
            anxiety_prevalence = (anxiety_cases / len(gad7_scores) * 100) if gad7_scores else 0
            
            return {
                'reporting_date': datetime.now().date().isoformat(),
                'region': region or 'Overall',
                'age_group': age_group or 'All',
                'gender': gender or 'All',
                'total_users': len(user_assessments),
                'avg_phq9_score': np.mean(phq9_scores) if phq9_scores else 0,
                'avg_gad7_score': np.mean(gad7_scores) if gad7_scores else 0,
                'depression_prevalence_percentage': depression_prevalence,
                'anxiety_prevalence_percentage': anxiety_prevalence,
                'comorbidity_rate': PopulationHealthAnalytics._calculate_comorbidity(
                    phq9_scores, gad7_scores
                ),
            }
        except Exception as e:
            logger.error(f"Error calculating population metrics: {e}")
            return {}
    
    @staticmethod
    def _calculate_comorbidity(phq9_scores: List[float], gad7_scores: List[float]) -> float:
        """Calculate rate of comorbid depression and anxiety"""
        if not phq9_scores or not gad7_scores:
            return 0
        
        min_len = min(len(phq9_scores), len(gad7_scores))
        comorbid = sum(
            1 for i in range(min_len)
            if phq9_scores[i] >= 10 and gad7_scores[i] >= 10
        )
        
        return (comorbid / min_len * 100) if min_len > 0 else 0


class TreatmentEfficacyTracker:
    """Tracks and analyzes treatment efficacy"""
    
    @staticmethod
    def calculate_treatment_efficacy(
        therapy_program_id: int,
        baseline_scores: List[float],
        endpoint_scores: List[float],
        user_satisfaction_ratings: List[float]
    ) -> Dict:
        """Calculate treatment efficacy metrics"""
        
        try:
            if not baseline_scores or not endpoint_scores:
                return {}
            
            # Calculate improvement
            improvements = [baseline - endpoint for baseline, endpoint in 
                           zip(baseline_scores, endpoint_scores)]
            
            mean_improvement = np.mean(improvements)
            std_improvement = np.std(improvements)
            
            # Calculate remission (endpoint score < 5)
            remission_count = sum(1 for score in endpoint_scores if score < 5)
            remission_rate = (remission_count / len(endpoint_scores)) if endpoint_scores else 0
            
            # Calculate response rate (>50% improvement)
            response_count = sum(1 for imp in improvements if imp > np.mean(baseline_scores) * 0.5)
            response_rate = (response_count / len(improvements)) if improvements else 0
            
            # Calculate effect size (Cohen's d)
            effect_size = mean_improvement / std_improvement if std_improvement > 0 else 0
            
            # Average user satisfaction
            avg_satisfaction = np.mean(user_satisfaction_ratings) if user_satisfaction_ratings else 0
            
            return {
                'therapy_program_id': therapy_program_id,
                'sample_size': len(baseline_scores),
                'baseline_severity_avg': np.mean(baseline_scores),
                'endpoint_severity_avg': np.mean(endpoint_scores),
                'mean_improvement': mean_improvement,
                'improvement_std_dev': std_improvement,
                'remission_rate': remission_rate,
                'response_rate': response_rate,
                'effect_size_cohens_d': effect_size,
                'user_satisfaction_avg': avg_satisfaction,
                'efficacy_score': (
                    (remission_rate * 0.4) +
                    (response_rate * 0.3) +
                    (min(effect_size, 2.0) / 2.0 * 0.2) +
                    (avg_satisfaction / 5 * 0.1)
                ),
                'calculated_at': datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error calculating efficacy: {e}")
            return {}
    
    @staticmethod
    def track_relapse_rate(
        program_id: int,
        recovered_users: int,
        relapsed_users: int,
        months_followup: int = 6
    ) -> Dict:
        """Track relapse rates over follow-up period"""
        
        total_users = recovered_users + relapsed_users
        
        return {
            'program_id': program_id,
            'followup_period_months': months_followup,
            'recovered_users_maintained': recovered_users,
            'relapsed_users': relapsed_users,
            'total_followup_users': total_users,
            'relapse_rate': (relapsed_users / total_users * 100) if total_users > 0 else 0,
            'recovery_sustainability': (recovered_users / total_users * 100) if total_users > 0 else 0,
        }


class QALYDALYCalculator:
    """Calculates Quality-Adjusted Life Years and Disability-Adjusted Life Years"""
    
    @staticmethod
    def calculate_qaly(
        baseline_health_state: float,
        post_intervention_health_state: float,
        years_of_treatment: float
    ) -> Dict:
        """
        Calculate Quality-Adjusted Life Years (QALY)
        
        Health states: 0 = death, 1 = perfect health
        """
        
        try:
            # Assume linear improvement over treatment period
            qaly_gained = (
                (post_intervention_health_state - baseline_health_state) *
                years_of_treatment
            )
            
            return {
                'baseline_health_state': baseline_health_state,
                'post_intervention_health_state': post_intervention_health_state,
                'treatment_duration_years': years_of_treatment,
                'qaly_gained': max(0, qaly_gained),
                'interpretation': QALYDALYCalculator._interpret_qaly(qaly_gained),
            }
        except Exception as e:
            logger.error(f"Error calculating QALY: {e}")
            return {}
    
    @staticmethod
    def calculate_daly(
        years_lived_with_disability: float,
        years_of_life_lost_premature: float
    ) -> Dict:
        """
        Calculate Disability-Adjusted Life Years (DALY)
        
        DALY = YLD + YLL
        YLD = Years Lived with Disability
        YLL = Years of Life Lost due to premature death
        """
        
        try:
            total_daly = years_lived_with_disability + years_of_life_lost_premature
            
            return {
                'years_lived_with_disability': years_lived_with_disability,
                'years_of_life_lost': years_of_life_lost_premature,
                'total_daly': total_daly,
                'interpretation': QALYDALYCalculator._interpret_daly(total_daly),
            }
        except Exception as e:
            logger.error(f"Error calculating DALY: {e}")
            return {}
    
    @staticmethod
    def _interpret_qaly(qaly_gained: float) -> str:
        """Interpret QALY gained"""
        if qaly_gained < 0:
            return 'Health declined'
        elif qaly_gained < 0.1:
            return 'Minimal improvement'
        elif qaly_gained < 0.5:
            return 'Modest improvement'
        elif qaly_gained < 1.0:
            return 'Substantial improvement'
        else:
            return 'Significant improvement'
    
    @staticmethod
    def _interpret_daly(daly: float) -> str:
        """Interpret DALY burden"""
        if daly < 0.1:
            return 'Minimal burden'
        elif daly < 0.5:
            return 'Low burden'
        elif daly < 1.0:
            return 'Moderate burden'
        else:
            return 'Significant burden'


class ImpactReporting:
    """Generates impact reports for donors and stakeholders"""
    
    @staticmethod
    def generate_impact_report(
        reporting_period_start: str,
        reporting_period_end: str,
        metrics: Dict
    ) -> Dict:
        """Generate comprehensive impact report"""
        
        try:
            return {
                'report_title': 'TALK 2 ME Mental Health Platform - Impact Report',
                'reporting_period': f"{reporting_period_start} to {reporting_period_end}",
                'report_generated_date': datetime.now().isoformat(),
                
                'key_outcomes': {
                    'total_users_served': metrics.get('total_users', 0),
                    'crisis_interventions': metrics.get('crisis_interventions', 0),
                    'lives_positively_impacted': metrics.get('users_improved', 0),
                    'crisis_episodes_resolved': metrics.get('crisis_resolved', 0),
                },
                
                'clinical_outcomes': {
                    'users_achieving_remission': metrics.get('remission_count', 0),
                    'average_symptom_improvement': metrics.get('avg_improvement', 0),
                    'users_with_treatment_response': metrics.get('response_rate', 0),
                    'quality_of_life_improvement': metrics.get('qol_improvement', 0),
                },
                
                'reach_and_access': {
                    'rural_users_served': metrics.get('rural_users', 0),
                    'urban_users_served': metrics.get('urban_users', 0),
                    'low_income_users_served': metrics.get('low_income_users', 0),
                    'youth_served_percent': metrics.get('youth_percent', 0),
                    'women_served_percent': metrics.get('women_percent', 0),
                },
                
                'economic_impact': {
                    'total_qaly_generated': metrics.get('total_qaly', 0),
                    'total_daly_prevented': metrics.get('total_daly', 0),
                    'economic_value_created_usd': metrics.get('economic_value', 0),
                    'cost_per_user_usd': metrics.get('cost_per_user', 0),
                    'cost_per_qaly_usd': metrics.get('cost_per_qaly', 0),
                    'return_on_investment_percent': metrics.get('roi_percent', 0),
                },
                
                'engagement_metrics': {
                    'active_users': metrics.get('active_users', 0),
                    'daily_active_users': metrics.get('dau', 0),
                    'average_session_duration_minutes': metrics.get('avg_session_minutes', 0),
                    'user_retention_rate_percent': metrics.get('retention_rate', 0),
                    'peer_support_interactions': metrics.get('peer_interactions', 0),
                },
                
                'donor_impact': {
                    'lives_saved_estimate': metrics.get('lives_saved', 0),
                    'hospitalizations_prevented': metrics.get('hospitalizations_prevented', 0),
                    'suicide_attempts_prevented': metrics.get('suicide_attempts_prevented', 0),
                    'family_relationships_strengthened': metrics.get('family_outcomes', 0),
                    'employment_outcomes_improved': metrics.get('employment_improved', 0),
                },
                
                'sustainability': {
                    'revenue_generated_usd': metrics.get('revenue', 0),
                    'cost_per_user_monthly_usd': metrics.get('monthly_cost_per_user', 0),
                    'fundraising_status': 'On track',
                    'sustainability_horizon_years': 5,
                },
            }
        except Exception as e:
            logger.error(f"Error generating impact report: {e}")
            return {}
    
    @staticmethod
    def generate_research_dataset_export(
        anonymized: bool = True,
        data_start_date: Optional[str] = None,
        data_end_date: Optional[str] = None,
        include_fields: Optional[List[str]] = None
    ) -> Dict:
        """Generate research dataset for academic collaboration"""
        
        return {
            'dataset_id': f"RESEARCH_{datetime.now().timestamp()}",
            'export_date': datetime.now().isoformat(),
            'anonymization_level': 'full' if anonymized else 'partial',
            'date_range': f"{data_start_date} to {data_end_date}",
            'total_records': 0,
            'data_fields': include_fields or [
                'age_group',
                'gender',
                'region',
                'primary_condition',
                'baseline_severity',
                'endpoint_severity',
                'treatment_type',
                'outcome',
            ],
            'file_format': 'CSV',
            'encryption': 'AES-256',
            'access_agreement_required': True,
            'publication_required': True,
            'status': 'ready_for_download',
        }


class AnalyticsService:
    """Central analytics service"""
    
    def __init__(self):
        self.population_analytics = PopulationHealthAnalytics()
        self.efficacy_tracker = TreatmentEfficacyTracker()
        self.qaly_daly = QALYDALYCalculator()
        self.impact_reporting = ImpactReporting()
    
    def get_comprehensive_analytics(self, user_id: Optional[int] = None) -> Dict:
        """Get comprehensive analytics"""
        
        if user_id:
            return {
                'analytics_type': 'individual',
                'user_id': user_id,
                'period': 'last_90_days',
                'metrics': {}
            }
        else:
            return {
                'analytics_type': 'population',
                'period': 'last_30_days',
                'metrics': {}
            }


# Global analytics service instance
analytics_service = AnalyticsService()
