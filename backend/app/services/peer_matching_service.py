"""
Peer Support Matching Service
Intelligent peer matching, mentor assignment, and peer group facilitation
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)


class PeerMatchingService:
    """Intelligent peer matching and support group management"""
    
    def __init__(self):
        self.min_match_score_threshold = 0.6
        self.scaler = None
    
    def find_peer_match(
        self,
        user_id: int,
        user_profile: Dict,
        pool_profiles: List[Dict],
        max_results: int = 5
    ) -> List[Dict]:
        """
        Find compatible peer matches using multiple criteria
        
        Args:
            user_id: User to find matches for
            user_profile: User's profile with condition, recovery stage, preferences
            pool_profiles: List of potential peer profiles
            max_results: Maximum number of matches to return
        
        Returns:
            Ranked list of peer matches with compatibility scores
        """
        try:
            matches = []
            
            for peer in pool_profiles:
                if peer['user_id'] == user_id:  # Skip self
                    continue
                
                # Calculate match score
                match_score = self._calculate_match_score(user_profile, peer)
                
                if match_score >= self.min_match_score_threshold:
                    matches.append({
                        'peer_user_id': peer['user_id'],
                        'match_score': match_score,
                        'peer_profile': {
                            'primary_condition': peer['primary_condition'],
                            'recovery_stage': peer['recovery_stage'],
                            'can_be_mentor': peer.get('can_be_mentor', False),
                            'mentor_experience_years': peer.get('mentor_experience_years', 0),
                        },
                        'compatibility_details': self._get_compatibility_details(user_profile, peer),
                        'connection_reason': self._generate_connection_reason(user_profile, peer)
                    })
            
            # Sort by match score descending
            matches.sort(key=lambda x: x['match_score'], reverse=True)
            
            return matches[:max_results]
        except Exception as e:
            logger.error(f"Error finding peer matches: {e}")
            return []
    
    def assign_mentor(
        self,
        mentee_id: int,
        mentee_profile: Dict,
        available_mentors: List[Dict]
    ) -> Optional[Dict]:
        """
        Assign best-matched mentor to mentee
        
        Returns:
            Best mentor match or None if no suitable mentor found
        """
        try:
            mentor_matches = []
            
            for mentor in available_mentors:
                if not mentor.get('can_be_mentor', False):
                    continue
                
                # Calculate mentor compatibility
                compatibility_score = self._calculate_mentor_compatibility(
                    mentee_profile,
                    mentor
                )
                
                if compatibility_score > 0.6:
                    mentor_matches.append({
                        'mentor_id': mentor['user_id'],
                        'compatibility_score': compatibility_score,
                        'experience_years': mentor.get('mentor_experience_years', 0),
                        'credentials': mentor.get('mentor_credentials', []),
                        'success_rate': mentor.get('match_success_rating', 0),
                    })
            
            if not mentor_matches:
                return None
            
            # Sort by combined score (compatibility + experience + success rate)
            mentor_matches.sort(
                key=lambda x: (x['compatibility_score'] * 0.5 + 
                              (x['experience_years'] / 10) * 0.3 + 
                              (x['success_rate'] / 5) * 0.2),
                reverse=True
            )
            
            return mentor_matches[0]
        except Exception as e:
            logger.error(f"Error assigning mentor: {e}")
            return None
    
    def create_peer_support_group(
        self,
        group_name: str,
        topic: str,
        moderator_id: int,
        language: str = 'en',
        config: Dict = None
    ) -> Dict:
        """
        Create a new peer support group
        
        Args:
            group_name: Name of the group
            topic: Topic/focus area (depression, anxiety, etc.)
            moderator_id: User ID of group moderator
            language: Language preference
            config: Additional configuration options
        
        Returns:
            New group details
        """
        try:
            group_config = config or {}
            
            return {
                'name': group_name,
                'description': f"{topic.replace('_', ' ').title()} Support Group",
                'topic': topic,
                'moderator_id': moderator_id,
                'language': language,
                'max_members': group_config.get('max_members', 15),
                'moderation_mode': group_config.get('moderation_mode', 'hybrid'),
                'meeting_schedule': group_config.get('meeting_schedule', {}),
                'is_active': True,
                'created_at': datetime.now().isoformat(),
                'members_count': 1,
                'total_messages': 0,
            }
        except Exception as e:
            logger.error(f"Error creating peer support group: {e}")
            return {}
    
    def recommend_peer_groups(
        self,
        user_id: int,
        user_conditions: List[str],
        language: str = 'en'
    ) -> List[Dict]:
        """
        Recommend peer support groups for user
        
        Args:
            user_id: User ID
            user_conditions: List of user's mental health conditions
            language: Language preference
        
        Returns:
            List of recommended groups
        """
        # Placeholder implementation - in practice would query database
        return [
            {
                'group_id': 1,
                'name': 'Depression Recovery Circle',
                'topic': 'depression',
                'members_count': 12,
                'match_score': 0.95,
                'language': language,
                'meeting_schedule': {'day': 'Monday', 'time': '19:00'},
            },
            {
                'group_id': 2,
                'name': 'Anxiety Warriors',
                'topic': 'anxiety',
                'members_count': 10,
                'match_score': 0.85,
                'language': language,
                'meeting_schedule': {'day': 'Wednesday', 'time': '18:00'},
            }
        ]
    
    def record_peer_interaction(
        self,
        mentor_id: int,
        mentee_id: int,
        interaction_type: str,
        duration_minutes: int,
        feedback: Dict
    ) -> Dict:
        """
        Record and analyze peer interaction outcomes
        
        Args:
            mentor_id: Mentor's user ID
            mentee_id: Mentee's user ID
            interaction_type: Type of interaction (chat, video, etc.)
            duration_minutes: Duration in minutes
            feedback: Feedback from mentee
        
        Returns:
            Interaction record with outcome analysis
        """
        try:
            # Calculate interaction quality score
            quality_score = self._calculate_interaction_quality(feedback)
            
            # Determine outcome
            outcome = self._determine_interaction_outcome(feedback, quality_score)
            
            return {
                'mentor_id': mentor_id,
                'mentee_id': mentee_id,
                'interaction_type': interaction_type,
                'duration_minutes': duration_minutes,
                'quality_score': quality_score,
                'mentee_rating': feedback.get('rating', 0),
                'mentor_notes': feedback.get('notes', ''),
                'outcome': outcome,
                'recorded_at': datetime.now().isoformat(),
                'followup_recommended': quality_score < 0.5,
            }
        except Exception as e:
            logger.error(f"Error recording peer interaction: {e}")
            return {}
    
    def moderate_peer_group_messages(
        self,
        group_id: int,
        messages: List[Dict]
    ) -> Dict:
        """
        Moderate peer group messages for safety
        
        Returns:
            List of messages with moderation flags
        """
        moderated_messages = []
        unsafe_count = 0
        
        for msg in messages:
            moderation = self._check_message_safety(msg['content'])
            
            if moderation['unsafe']:
                unsafe_count += 1
            
            moderated_messages.append({
                'message_id': msg.get('id'),
                'user_id': msg.get('user_id'),
                'content': msg['content'] if not moderation['require_review'] else '[Removed for review]',
                'moderation_status': moderation['status'],
                'flagged_for_review': moderation['require_review'],
                'flags': moderation.get('flags', []),
            })
        
        return {
            'group_id': group_id,
            'total_messages': len(messages),
            'moderated_messages': moderated_messages,
            'unsafe_count': unsafe_count,
            'escalation_needed': unsafe_count > 0,
        }
    
    def calculate_peer_network_impact(
        self,
        user_id: int,
        peer_interactions: List[Dict],
        assessment_changes: Dict
    ) -> Dict:
        """
        Calculate impact of peer support on user's mental health
        
        Returns:
            Impact metrics and analysis
        """
        try:
            if not peer_interactions:
                return {
                    'peer_network_size': 0,
                    'impact_score': 0,
                    'engagement_level': 'none'
                }
            
            interaction_count = len(peer_interactions)
            avg_quality = np.mean([i.get('quality_score', 0.5) for i in peer_interactions])
            
            # Calculate symptom improvement correlation
            pre_score = assessment_changes.get('baseline_score', 15)
            post_score = assessment_changes.get('current_score', 15)
            improvement = pre_score - post_score
            
            impact_score = (avg_quality * 0.5) + (min(improvement / 10, 1.0) * 0.5)
            
            return {
                'user_id': user_id,
                'peer_network_size': len(set(i.get('peer_id') for i in peer_interactions)),
                'total_interactions': interaction_count,
                'average_interaction_quality': avg_quality,
                'symptom_improvement': improvement,
                'impact_score': min(1.0, impact_score),
                'engagement_level': 'high' if interaction_count > 10 else (
                    'moderate' if interaction_count > 3 else 'low'
                ),
                'recommendation': self._generate_peer_recommendation(impact_score, interaction_count),
            }
        except Exception as e:
            logger.error(f"Error calculating peer network impact: {e}")
            return {}
    
    # Helper methods
    
    def _calculate_match_score(self, user_profile: Dict, peer_profile: Dict) -> float:
        """Calculate overall peer match score"""
        scores = []
        
        # Condition match (most important)
        if user_profile.get('primary_condition') == peer_profile.get('primary_condition'):
            scores.append(0.4)  # Perfect condition match
        else:
            scores.append(0.1)  # Different conditions
        
        # Recovery stage compatibility
        stage_similarity = self._calculate_recovery_stage_similarity(
            user_profile.get('recovery_stage'),
            peer_profile.get('recovery_stage')
        )
        scores.append(stage_similarity * 0.3)
        
        # Preference match
        if user_profile.get('preferred_peer_type') == 'similar_condition':
            scores.append(0.15 if user_profile.get('primary_condition') == peer_profile.get('primary_condition') else 0.05)
        elif user_profile.get('preferred_peer_type') == 'further_ahead':
            scores.append(0.15 if self._is_further_ahead(user_profile, peer_profile) else 0.05)
        else:
            scores.append(0.15)
        
        # Mentor availability
        if peer_profile.get('can_be_mentor') and user_profile.get('recovery_stage') != 'recovered':
            scores.append(0.1)
        else:
            scores.append(0.05)
        
        return sum(scores) / len(scores)
    
    def _calculate_mentor_compatibility(self, mentee_profile: Dict, mentor_profile: Dict) -> float:
        """Calculate mentor-mentee compatibility"""
        score = 0.5
        
        # Mentor has relevant experience
        if mentor_profile.get('mentor_experience_years', 0) > 0:
            score += 0.2
        
        # Similar condition experience
        if mentee_profile.get('primary_condition') in str(mentor_profile.get('mentor_credentials', [])):
            score += 0.2
        
        # Mentor is further ahead in recovery
        if mentor_profile.get('recovery_stage') in ['maintenance', 'recovered']:
            score += 0.1
        
        return min(1.0, score)
    
    def _get_compatibility_details(self, user_profile: Dict, peer_profile: Dict) -> Dict:
        """Generate compatibility details"""
        return {
            'same_condition': user_profile.get('primary_condition') == peer_profile.get('primary_condition'),
            'similar_stage': abs(
                self._stage_to_number(user_profile.get('recovery_stage')) -
                self._stage_to_number(peer_profile.get('recovery_stage'))
            ) <= 1,
            'mentor_available': peer_profile.get('can_be_mentor', False),
            'language_compatible': True,  # Placeholder
        }
    
    def _generate_connection_reason(self, user_profile: Dict, peer_profile: Dict) -> str:
        """Generate human-readable reason for peer match"""
        if user_profile.get('primary_condition') == peer_profile.get('primary_condition'):
            if peer_profile.get('can_be_mentor'):
                return f"Experienced {user_profile.get('primary_condition')} peer mentor with similar struggles"
            else:
                return f"Shares your {user_profile.get('primary_condition')} journey and understanding"
        else:
            return "Shared mental health recovery experiences"
    
    def _calculate_recovery_stage_similarity(self, stage1: str, stage2: str) -> float:
        """Calculate similarity between recovery stages"""
        stages = ['crisis', 'early_recovery', 'ongoing_recovery', 'maintenance', 'recovered']
        try:
            idx1 = stages.index(stage1)
            idx2 = stages.index(stage2)
            distance = abs(idx1 - idx2)
            return max(0, 1 - (distance / len(stages)))
        except:
            return 0.5
    
    def _is_further_ahead(self, user_profile: Dict, peer_profile: Dict) -> bool:
        """Check if peer is further ahead in recovery"""
        stages = ['crisis', 'early_recovery', 'ongoing_recovery', 'maintenance', 'recovered']
        user_idx = stages.index(user_profile.get('recovery_stage', 'ongoing_recovery'))
        peer_idx = stages.index(peer_profile.get('recovery_stage', 'ongoing_recovery'))
        return peer_idx > user_idx
    
    def _stage_to_number(self, stage: str) -> int:
        """Convert recovery stage to numeric value"""
        stages = {'crisis': 0, 'early_recovery': 1, 'ongoing_recovery': 2, 'maintenance': 3, 'recovered': 4}
        return stages.get(stage, 2)
    
    def _calculate_interaction_quality(self, feedback: Dict) -> float:
        """Calculate quality score from feedback"""
        base_score = 0.5
        
        if feedback.get('rating', 0) >= 4:
            base_score += 0.3
        elif feedback.get('rating', 0) >= 3:
            base_score += 0.15
        
        if feedback.get('helpful', False):
            base_score += 0.1
        
        return min(1.0, base_score)
    
    def _determine_interaction_outcome(self, feedback: Dict, quality_score: float) -> str:
        """Determine interaction outcome"""
        if quality_score >= 0.8:
            return 'positive'
        elif quality_score >= 0.5:
            return 'neutral'
        else:
            return 'negative'
    
    def _check_message_safety(self, content: str) -> Dict:
        """Check message for safety concerns"""
        risk_keywords = ['suicide', 'kill', 'harm', 'abuse', 'drugs']
        
        unsafe = any(keyword in content.lower() for keyword in risk_keywords)
        
        return {
            'unsafe': unsafe,
            'require_review': unsafe,
            'status': 'flagged' if unsafe else 'approved',
            'flags': ['self_harm_mentioned'] if unsafe else [],
        }
    
    def _generate_peer_recommendation(self, impact_score: float, interaction_count: int) -> str:
        """Generate recommendation based on peer network impact"""
        if impact_score > 0.7 and interaction_count > 10:
            return "Strong peer support contributing to recovery. Continue engagement."
        elif impact_score > 0.5:
            return "Peer support helpful. Consider increasing interactions."
        else:
            return "Consider more peer interactions or mentorship opportunities."
