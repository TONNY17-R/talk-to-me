"""
Gamification & Behavioral Science Service
Habit tracking, achievements, streaks, leaderboards, and engagement incentives
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)


class GamificationService:
    """Gamification engine for mental health engagement and progress tracking"""
    
    def __init__(self):
        self.points_multiplier = 1.0
        self.level_thresholds = [0, 1000, 3000, 6000, 10000, 15000]
        self.readiness_stages = [
            'precontemplation',
            'contemplation',
            'preparation',
            'action',
            'maintenance'
        ]
    
    def track_habit(
        self,
        user_id: int,
        habit_type: str,
        completion_date: str,
        completion_status: str = 'completed',
        notes: str = ''
    ) -> Dict:
        """
        Track user habit completion
        
        Args:
            user_id: User ID
            habit_type: Type of habit (mood_check_in, meditation, exercise, etc.)
            completion_date: Date of completion (YYYY-MM-DD)
            completion_status: completed, skipped, or partial
            notes: Additional notes
        
        Returns:
            Habit tracking record with streak and points
        """
        try:
            # Determine points for this completion
            points_earned = self._calculate_habit_points(habit_type, completion_status)
            
            # Update streak
            streak_result = self._update_streak(user_id, habit_type, completion_date, completion_status)
            
            # Check for achievements
            new_achievements = self._check_habit_achievements(
                user_id,
                habit_type,
                streak_result['current_streak']
            )
            
            return {
                'user_id': user_id,
                'habit_type': habit_type,
                'completion_date': completion_date,
                'completion_status': completion_status,
                'points_earned': points_earned,
                'current_streak': streak_result['current_streak'],
                'longest_streak': streak_result['longest_streak'],
                'streak_maintained': streak_result['status'] == 'maintained',
                'new_achievements_unlocked': new_achievements,
                'total_completions': streak_result['total_completions'],
                'motivation_message': self._generate_motivation_message(
                    streak_result['current_streak'],
                    completion_status
                ),
            }
        except Exception as e:
            logger.error(f"Error tracking habit: {e}")
            return {}
    
    def calculate_user_level_and_points(
        self,
        user_id: int,
        total_points: int
    ) -> Dict:
        """
        Calculate user's level based on accumulated points
        
        Returns:
            Current level, progress to next level, and level details
        """
        try:
            current_level = 1
            for i, threshold in enumerate(self.level_thresholds):
                if total_points >= threshold:
                    current_level = i
                else:
                    break
            
            current_threshold = self.level_thresholds[current_level]
            next_threshold = (
                self.level_thresholds[current_level + 1]
                if current_level + 1 < len(self.level_thresholds)
                else self.level_thresholds[-1] + 10000
            )
            
            progress_percentage = (
                (total_points - current_threshold) /
                (next_threshold - current_threshold) * 100
            )
            
            return {
                'user_id': user_id,
                'current_level': current_level,
                'total_points': total_points,
                'points_to_next_level': next_threshold - total_points,
                'progress_percentage': min(100, progress_percentage),
                'level_progress': f"{total_points - current_threshold}/{next_threshold - current_threshold}",
                'level_title': self._get_level_title(current_level),
                'next_level_benefit': self._get_level_benefit(current_level + 1),
            }
        except Exception as e:
            logger.error(f"Error calculating level: {e}")
            return {}
    
    def unlock_achievement(
        self,
        user_id: int,
        achievement_id: int,
        achievement_data: Dict
    ) -> Dict:
        """
        Unlock a new achievement for user
        
        Args:
            user_id: User ID
            achievement_id: Achievement ID
            achievement_data: Achievement details
        
        Returns:
            Achievement unlock record
        """
        try:
            # Award points for achievement
            points_awarded = achievement_data.get('reward_points', 100)
            
            return {
                'user_id': user_id,
                'achievement_id': achievement_id,
                'achievement_name': achievement_data.get('name'),
                'achievement_category': achievement_data.get('category'),
                'badge_image_url': achievement_data.get('badge_image_url'),
                'description': achievement_data.get('description'),
                'points_awarded': points_awarded,
                'unlocked_at': datetime.now().isoformat(),
                'is_rare': achievement_data.get('category') in ['milestone', 'recovery'],
                'share_eligible': True,
            }
        except Exception as e:
            logger.error(f"Error unlocking achievement: {e}")
            return {}
    
    def get_user_achievements(
        self,
        user_id: int
    ) -> Dict:
        """
        Get all achievements for a user
        
        Returns:
            Grouped achievements by category
        """
        try:
            # Placeholder - in practice would query database
            achievements = {
                'milestone': [
                    {
                        'id': 1,
                        'name': '7-Day Streak',
                        'category': 'milestone',
                        'unlocked': True,
                        'unlocked_date': '2024-01-15'
                    },
                    {
                        'id': 2,
                        'name': '30-Day Streak',
                        'category': 'milestone',
                        'unlocked': False,
                        'progress': 0.3
                    }
                ],
                'consistency': [
                    {
                        'id': 3,
                        'name': 'Habit Master',
                        'category': 'consistency',
                        'unlocked': False,
                        'progress': 0.65
                    }
                ],
                'engagement': [],
                'progress': [],
                'peer_support': [],
                'recovery': []
            }
            
            return {
                'user_id': user_id,
                'total_achievements_unlocked': sum(
                    len([a for a in cat if a.get('unlocked')])
                    for cat in achievements.values()
                ),
                'achievements_by_category': achievements,
                'next_achievement_target': 'Reach 30-day meditation streak for 100 points',
            }
        except Exception as e:
            logger.error(f"Error retrieving achievements: {e}")
            return {}
    
    def assess_readiness_for_change(
        self,
        user_id: int,
        assessment_data: Dict
    ) -> Dict:
        """
        Assess user's readiness for behavioral change
        
        Uses Transtheoretical Model (TTM) stages of change
        
        Returns:
            Current readiness stage and recommendations
        """
        try:
            # Analyze indicators to determine stage
            stage_scores = {
                'precontemplation': 0,
                'contemplation': 0,
                'preparation': 0,
                'action': 0,
                'maintenance': 0,
            }
            
            # Score based on behavior indicators
            if assessment_data.get('engaged_with_resources', False):
                stage_scores['contemplation'] += 1
                stage_scores['preparation'] += 1
            
            if assessment_data.get('has_action_plan', False):
                stage_scores['preparation'] += 2
                stage_scores['action'] += 1
            
            if assessment_data.get('recent_habit_streak', 0) > 7:
                stage_scores['action'] += 2
                stage_scores['maintenance'] += 1
            
            if assessment_data.get('recent_habit_streak', 0) > 30:
                stage_scores['maintenance'] += 2
            
            # Determine primary stage
            primary_stage = max(stage_scores, key=stage_scores.get)
            
            # Generate tailored recommendations
            recommendations = self._get_readiness_recommendations(primary_stage)
            
            return {
                'user_id': user_id,
                'current_readiness_stage': primary_stage,
                'stage_index': self.readiness_stages.index(primary_stage),
                'stage_progression': stage_scores,
                'confidence_score': stage_scores[primary_stage] / max(sum(stage_scores.values()), 1),
                'tailored_recommendations': recommendations,
                'next_stage': self._get_next_stage(primary_stage),
                'stage_description': self._get_stage_description(primary_stage),
            }
        except Exception as e:
            logger.error(f"Error assessing readiness: {e}")
            return {}
    
    def generate_personalized_learning_path(
        self,
        user_id: int,
        readiness_stage: str,
        primary_condition: str,
        available_resources: List[Dict]
    ) -> Dict:
        """
        Generate personalized learning path based on readiness stage and condition
        
        Returns:
            Ordered learning resources and milestones
        """
        try:
            learning_path = {
                'resources': [],
                'milestones': [],
                'estimated_duration_weeks': 0,
            }
            
            # Filter resources by stage
            stage_resources = [
                r for r in available_resources
                if r.get('recommended_stage') == readiness_stage
            ]
            
            # Sort by difficulty progression
            stage_resources.sort(key=lambda x: x.get('difficulty', 1))
            
            learning_path['resources'] = stage_resources[:10]  # Top 10 resources
            
            # Define milestones
            learning_path['milestones'] = self._generate_milestones(readiness_stage)
            learning_path['estimated_duration_weeks'] = len(stage_resources) * 2
            
            return learning_path
        except Exception as e:
            logger.error(f"Error generating learning path: {e}")
            return {}
    
    def calculate_leaderboard_position(
        self,
        user_id: int,
        user_total_points: int,
        all_users_points: List[Tuple[int, int]],
        opt_in_required: bool = True
    ) -> Dict:
        """
        Calculate user's leaderboard position
        
        Args:
            user_id: User ID
            user_total_points: User's total points
            all_users_points: List of (user_id, points) tuples
            opt_in_required: Whether to only rank opted-in users
        
        Returns:
            Leaderboard position and nearby rankings
        """
        try:
            # Sort by points descending
            sorted_users = sorted(all_users_points, key=lambda x: x[1], reverse=True)
            
            # Find user's position
            user_position = next(
                (i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == user_id),
                len(sorted_users)
            )
            
            # Get nearby competitors
            nearby_start = max(0, user_position - 3)
            nearby_end = min(len(sorted_users), user_position + 3)
            nearby = sorted_users[nearby_start:nearby_end]
            
            return {
                'user_id': user_id,
                'leaderboard_position': user_position,
                'total_ranked_users': len(sorted_users),
                'percentile': (1 - user_position / len(sorted_users)) * 100 if sorted_users else 0,
                'user_total_points': user_total_points,
                'nearby_competitors': [
                    {
                        'position': i + nearby_start + 1,
                        'user_id': uid,
                        'points': pts,
                        'is_user': uid == user_id,
                    }
                    for i, (uid, pts) in enumerate(nearby)
                ],
                'points_to_next_rank': (
                    sorted_users[user_position - 2][1] - user_total_points
                    if user_position > 1 else 0
                ),
            }
        except Exception as e:
            logger.error(f"Error calculating leaderboard: {e}")
            return {}
    
    def get_daily_challenge(
        self,
        user_id: int,
        user_readiness_stage: str
    ) -> Dict:
        """
        Generate personalized daily challenge
        
        Returns:
            Daily challenge with reward and difficulty
        """
        try:
            challenges = {
                'precontemplation': [
                    'Read one article about mental health',
                    'Watch a 5-minute wellness video',
                    'Reflect on one personal strength'
                ],
                'contemplation': [
                    'Identify one behavior change you could make',
                    'Journal for 10 minutes about your goals',
                    'Take the 5-question readiness assessment'
                ],
                'preparation': [
                    'Complete one recommended exercise',
                    'Meditate for 5 minutes',
                    'Track one daily habit'
                ],
                'action': [
                    'Complete your therapy exercise',
                    'Meditate for 15 minutes',
                    'Connect with a peer support group',
                    'Track all daily habits'
                ],
                'maintenance': [
                    'Mentor another user',
                    'Maintain your habit streak',
                    'Reflect on your progress',
                    'Help in peer support group'
                ]
            }
            
            import random
            stage_challenges = challenges.get(user_readiness_stage, challenges['action'])
            selected_challenge = random.choice(stage_challenges)
            
            return {
                'user_id': user_id,
                'daily_challenge': selected_challenge,
                'reward_points': self._get_challenge_reward(user_readiness_stage),
                'difficulty': self._get_challenge_difficulty(user_readiness_stage),
                'time_estimate_minutes': self._get_challenge_duration(user_readiness_stage),
                'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating daily challenge: {e}")
            return {}
    
    # Helper methods
    
    def _calculate_habit_points(self, habit_type: str, completion_status: str) -> int:
        """Calculate points for habit completion"""
        base_points = {
            'mood_check_in': 10,
            'meditation': 25,
            'exercise': 30,
            'sleep_tracking': 15,
            'journaling': 20,
            'therapy_session': 50,
            'medication_adherence': 20,
            'social_connection': 25,
            'resource_learning': 15,
        }
        
        base = base_points.get(habit_type, 15)
        
        if completion_status == 'completed':
            return int(base * self.points_multiplier)
        elif completion_status == 'partial':
            return int(base * 0.5 * self.points_multiplier)
        else:  # skipped
            return 0
    
    def _update_streak(self, user_id: int, habit_type: str, completion_date: str, status: str) -> Dict:
        """Update habit streak"""
        # Placeholder - in practice would query database
        return {
            'current_streak': 1,
            'longest_streak': 1,
            'total_completions': 1,
            'status': 'started' if status == 'completed' else 'interrupted',
        }
    
    def _check_habit_achievements(self, user_id: int, habit_type: str, current_streak: int) -> List[Dict]:
        """Check for habit-based achievements"""
        achievements = []
        
        if current_streak == 7:
            achievements.append({'name': 'One Week Warrior', 'points': 100})
        elif current_streak == 30:
            achievements.append({'name': 'Habit Master', 'points': 500})
        elif current_streak == 100:
            achievements.append({'name': 'Century Champion', 'points': 1000})
        
        return achievements
    
    def _generate_motivation_message(self, current_streak: int, status: str) -> str:
        """Generate motivational message"""
        if status != 'completed':
            return 'No worries! Get back on track tomorrow.'
        
        if current_streak == 1:
            return 'Great start! Keep it up tomorrow! 💪'
        elif current_streak == 7:
            return 'You\'ve got a week! Amazing consistency! 🎉'
        elif current_streak == 30:
            return 'One month strong! You\'re unstoppable! 🔥'
        elif current_streak % 7 == 0:
            return f'On a {current_streak}-day streak! You\'re crushing it!'
        else:
            return 'You\'re on fire! Keep going! 🚀'
    
    def _get_level_title(self, level: int) -> str:
        """Get title for level"""
        titles = [
            'Newcomer',
            'Practitioner',
            'Committer',
            'Advocate',
            'Hero',
            'Legend'
        ]
        return titles[min(level, len(titles) - 1)]
    
    def _get_level_benefit(self, level: int) -> str:
        """Get benefit for next level"""
        benefits = [
            'Access to basic resources',
            'Unlock mentor feature',
            'Create peer support group',
            'Priority counselor booking',
            'Lead community initiatives',
            'Exclusive advanced programs'
        ]
        return benefits[min(level, len(benefits) - 1)]
    
    def _get_readiness_recommendations(self, stage: str) -> List[str]:
        """Get tailored recommendations for readiness stage"""
        recommendations = {
            'precontemplation': [
                'Explore resources at your own pace',
                'Consider trying one small self-care activity',
                'No pressure - awareness is the first step'
            ],
            'contemplation': [
                'Create a list of pros and cons about change',
                'Identify potential barriers and solutions',
                'Join a peer support group to hear others\' stories'
            ],
            'preparation': [
                'Set SMART goals for your recovery',
                'Choose specific activities to start',
                'Find an accountability partner or mentor'
            ],
            'action': [
                'Stay committed to your plan',
                'Track progress daily',
                'Celebrate small wins along the way'
            ],
            'maintenance': [
                'Continue your established routines',
                'Help others who are earlier in their journey',
                'Monitor for relapse triggers'
            ]
        }
        return recommendations.get(stage, [])
    
    def _get_next_stage(self, current_stage: str) -> str:
        """Get next readiness stage"""
        idx = self.readiness_stages.index(current_stage)
        return self.readiness_stages[min(idx + 1, len(self.readiness_stages) - 1)]
    
    def _get_stage_description(self, stage: str) -> str:
        """Get description of readiness stage"""
        descriptions = {
            'precontemplation': 'Not considering change yet but open to learning',
            'contemplation': 'Thinking about making changes in the next 6 months',
            'preparation': 'Planning to take action within the next month',
            'action': 'Making active changes right now',
            'maintenance': 'Maintaining changes for 6+ months'
        }
        return descriptions.get(stage, '')
    
    def _generate_milestones(self, stage: str) -> List[Dict]:
        """Generate milestones for learning path"""
        milestones = {
            'precontemplation': [
                {'name': 'Learn basics', 'day': 7},
                {'name': 'Identify interests', 'day': 14},
            ],
            'contemplation': [
                {'name': 'Explore options', 'day': 7},
                {'name': 'Make decision', 'day': 14},
            ],
            'preparation': [
                {'name': 'Create plan', 'day': 3},
                {'name': 'Setup support', 'day': 7},
            ],
            'action': [
                {'name': 'First week', 'day': 7},
                {'name': 'Month check-in', 'day': 30},
            ],
            'maintenance': [
                {'name': 'Quarter review', 'day': 90},
                {'name': 'Mentor others', 'day': 180},
            ]
        }
        return milestones.get(stage, [])
    
    def _get_challenge_reward(self, stage: str) -> int:
        """Get reward points for daily challenge"""
        rewards = {
            'precontemplation': 10,
            'contemplation': 15,
            'preparation': 20,
            'action': 30,
            'maintenance': 25,
        }
        return rewards.get(stage, 15)
    
    def _get_challenge_difficulty(self, stage: str) -> str:
        """Get challenge difficulty level"""
        difficulties = {
            'precontemplation': 'easy',
            'contemplation': 'easy',
            'preparation': 'medium',
            'action': 'hard',
            'maintenance': 'hard',
        }
        return difficulties.get(stage, 'medium')
    
    def _get_challenge_duration(self, stage: str) -> int:
        """Get estimated time for daily challenge"""
        durations = {
            'precontemplation': 5,
            'contemplation': 10,
            'preparation': 15,
            'action': 20,
            'maintenance': 30,
        }
        return durations.get(stage, 15)
