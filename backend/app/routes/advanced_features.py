"""
Advanced Features API Routes
All REST endpoints for new and advanced features (predictive analytics, voice, peer matching, etc.)
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
import logging
from datetime import datetime

# Import services
from app.services.predictive_service import PredictiveAnalyticsService
from app.services.voice_biomarker_service import VoiceBiomarkerService
from app.services.peer_matching_service import PeerMatchingService
from app.services.gamification_service import GamificationService
from app.services.crisis_service import CrisisCommandCenterService

logger = logging.getLogger(__name__)

# Initialize services
predictive_service = PredictiveAnalyticsService()
voice_service = VoiceBiomarkerService()
peer_service = PeerMatchingService()
gamification_service = GamificationService()
crisis_service = CrisisCommandCenterService()

# Create blueprints for different feature categories
advanced_bp = Blueprint('advanced_features', __name__, url_prefix='/api/advanced')

# ============================================================================
# 1. PREDICTIVE ANALYTICS ROUTES
# ============================================================================

@advanced_bp.route('/predictions/trajectory', methods=['POST'])
@jwt_required()
def predict_trajectory():
    """
    Predict user's mental health trajectory 2-4 weeks ahead
    
    Request body:
    {
        "assessment_history": [...],
        "engagement_metrics": {...},
        "days_ahead": 28
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = predictive_service.predict_mental_health_trajectory(
            user_id=user_id,
            assessment_history=data.get('assessment_history', []),
            engagement_metrics=data.get('engagement_metrics', {}),
            days_ahead=data.get('days_ahead', 28)
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error predicting trajectory: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/predictions/risk-stratification', methods=['POST'])
@jwt_required()
def get_risk_stratification():
    """Get user's risk tier: low, medium, high, critical"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = predictive_service.stratify_user_risk(
            user_id=user_id,
            phq9_score=data.get('phq9_score', 0),
            gad7_score=data.get('gad7_score', 0),
            crisis_indicators=data.get('crisis_indicators', {}),
            behavioral_data=data.get('behavioral_data', {})
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error stratifying risk: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/predictions/relapse-risk', methods=['POST'])
@jwt_required()
def predict_relapse_risk():
    """Predict relapse risk for users in recovery"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = predictive_service.predict_relapse_risk(
            user_id=user_id,
            recovery_history=data.get('recovery_history', []),
            current_stressors=data.get('current_stressors', []),
            social_support_score=data.get('social_support_score', 5),
            medication_adherence=data.get('medication_adherence', 1.0)
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error predicting relapse: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/predictions/intervention-timing', methods=['GET'])
@jwt_required()
def get_intervention_timing():
    """Get optimal time to reach out to user based on activity patterns"""
    try:
        user_id = get_jwt_identity()
        timezone = request.args.get('timezone', 'UTC')
        
        # Placeholder - would fetch from database
        user_activity = []
        
        result = predictive_service.get_personalized_intervention_timing(
            user_id=user_id,
            user_activity_pattern=user_activity,
            timezone=timezone
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting intervention timing: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# 2. VOICE BIOMARKER ROUTES
# ============================================================================

@advanced_bp.route('/voice/analyze', methods=['POST'])
@jwt_required()
def analyze_voice_recording():
    """
    Comprehensive voice analysis for mental health biomarkers
    
    Request: multipart/form-data with audio file
    """
    try:
        user_id = get_jwt_identity()
        
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en')
        
        # Save file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            audio_file.save(tmp.name)
            
            result = voice_service.analyze_voice_recording(
                audio_path=tmp.name,
                user_id=user_id,
                language=language
            )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error analyzing voice: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/voice/emotion', methods=['POST'])
@jwt_required()
def detect_vocal_emotion():
    """Detect emotional state from voice"""
    try:
        user_id = get_jwt_identity()
        
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            audio_file.save(tmp.name)
            
            result = voice_service.detect_vocal_emotion(tmp.name)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error detecting emotion: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/voice/speech-patterns', methods=['POST'])
@jwt_required()
def analyze_speech_patterns():
    """Analyze speech rate, pitch, intensity, and vocal patterns"""
    try:
        user_id = get_jwt_identity()
        
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            audio_file.save(tmp.name)
            
            result = voice_service.analyze_speech_rate_and_patterns(tmp.name)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error analyzing speech patterns: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/voice/transcribe', methods=['POST'])
@jwt_required()
def transcribe_voice():
    """Transcribe voice recording to text"""
    try:
        user_id = get_jwt_identity()
        
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en')
        
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            audio_file.save(tmp.name)
            
            result = voice_service.transcribe_voice_to_text(tmp.name, language)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error transcribing voice: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# 3. PEER MATCHING & SUPPORT ROUTES
# ============================================================================

@advanced_bp.route('/peers/find-matches', methods=['POST'])
@jwt_required()
def find_peer_matches():
    """Find compatible peer matches for user"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Placeholder - would fetch pool from database
        pool_profiles = []
        
        result = peer_service.find_peer_match(
            user_id=user_id,
            user_profile=data.get('user_profile', {}),
            pool_profiles=pool_profiles,
            max_results=data.get('max_results', 5)
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error finding peer matches: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/peers/recommend-groups', methods=['GET'])
@jwt_required()
def recommend_peer_groups():
    """Get recommended peer support groups"""
    try:
        user_id = get_jwt_identity()
        language = request.args.get('language', 'en')
        
        # Placeholder - would fetch from database
        user_conditions = []
        
        result = peer_service.recommend_peer_groups(
            user_id=user_id,
            user_conditions=user_conditions,
            language=language
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error recommending groups: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/peers/groups', methods=['POST'])
@jwt_required()
def create_peer_group():
    """Create new peer support group"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = peer_service.create_peer_support_group(
            group_name=data.get('group_name'),
            topic=data.get('topic'),
            moderator_id=user_id,
            language=data.get('language', 'en'),
            config=data.get('config', {})
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error creating peer group: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/peers/interaction-record', methods=['POST'])
@jwt_required()
def record_peer_interaction():
    """Record peer support interaction"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = peer_service.record_peer_interaction(
            mentor_id=data.get('mentor_id'),
            mentee_id=user_id,
            interaction_type=data.get('interaction_type'),
            duration_minutes=data.get('duration_minutes'),
            feedback=data.get('feedback', {})
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error recording interaction: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/peers/network-impact', methods=['GET'])
@jwt_required()
def get_peer_network_impact():
    """Calculate impact of peer support on mental health"""
    try:
        user_id = get_jwt_identity()
        
        # Placeholder - would fetch from database
        peer_interactions = []
        assessment_changes = {}
        
        result = peer_service.calculate_peer_network_impact(
            user_id=user_id,
            peer_interactions=peer_interactions,
            assessment_changes=assessment_changes
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error calculating network impact: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# 4. GAMIFICATION ROUTES
# ============================================================================

@advanced_bp.route('/gamification/habit-track', methods=['POST'])
@jwt_required()
def track_habit():
    """Track user habit completion"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = gamification_service.track_habit(
            user_id=user_id,
            habit_type=data.get('habit_type'),
            completion_date=data.get('completion_date'),
            completion_status=data.get('completion_status', 'completed'),
            notes=data.get('notes', '')
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error tracking habit: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/gamification/level', methods=['GET'])
@jwt_required()
def get_user_level():
    """Get user's level and progress"""
    try:
        user_id = get_jwt_identity()
        total_points = int(request.args.get('total_points', 0))
        
        result = gamification_service.calculate_user_level_and_points(
            user_id=user_id,
            total_points=total_points
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting level: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/gamification/achievements', methods=['GET'])
@jwt_required()
def get_achievements():
    """Get user's achievements"""
    try:
        user_id = get_jwt_identity()
        
        result = gamification_service.get_user_achievements(user_id=user_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting achievements: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/gamification/readiness-assessment', methods=['POST'])
@jwt_required()
def assess_readiness():
    """Assess user's readiness for behavioral change"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = gamification_service.assess_readiness_for_change(
            user_id=user_id,
            assessment_data=data
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error assessing readiness: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/gamification/learning-path', methods=['GET'])
@jwt_required()
def get_learning_path():
    """Get personalized learning path"""
    try:
        user_id = get_jwt_identity()
        readiness_stage = request.args.get('readiness_stage', 'action')
        primary_condition = request.args.get('primary_condition', 'depression')
        
        # Placeholder - would fetch resources from database
        available_resources = []
        
        result = gamification_service.generate_personalized_learning_path(
            user_id=user_id,
            readiness_stage=readiness_stage,
            primary_condition=primary_condition,
            available_resources=available_resources
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting learning path: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/gamification/daily-challenge', methods=['GET'])
@jwt_required()
def get_daily_challenge():
    """Get personalized daily challenge"""
    try:
        user_id = get_jwt_identity()
        readiness_stage = request.args.get('readiness_stage', 'action')
        
        result = gamification_service.get_daily_challenge(
            user_id=user_id,
            user_readiness_stage=readiness_stage
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting daily challenge: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/gamification/leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    """Get leaderboard position"""
    try:
        user_id = get_jwt_identity()
        user_points = int(request.args.get('user_points', 0))
        
        # Placeholder - would fetch all users' points from database
        all_users_points = []
        
        result = gamification_service.calculate_leaderboard_position(
            user_id=user_id,
            user_total_points=user_points,
            all_users_points=all_users_points
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting leaderboard: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# 5. CRISIS COMMAND CENTER ROUTES
# ============================================================================

@advanced_bp.route('/crisis/analyze', methods=['POST'])
@jwt_required()
def analyze_crisis():
    """Analyze multimodal crisis indicators"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = crisis_service.analyze_multimodal_crisis_indicators(
            user_id=user_id,
            text_data=data.get('text_data', {}),
            voice_data=data.get('voice_data', {}),
            behavioral_data=data.get('behavioral_data', {}),
            pattern_data=data.get('pattern_data', {})
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error analyzing crisis: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/crisis/emergency-response', methods=['POST'])
@jwt_required()
def trigger_emergency():
    """Trigger emergency response protocols"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = crisis_service.trigger_emergency_response(
            user_id=user_id,
            alert_data=data.get('alert_data', {}),
            emergency_contacts=data.get('emergency_contacts', []),
            available_counselors=data.get('available_counselors', [])
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error triggering emergency: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/crisis/session', methods=['POST'])
@jwt_required()
def create_crisis_session():
    """Create crisis counseling session"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = crisis_service.create_crisis_session(
            user_id=user_id,
            counselor_id=data.get('counselor_id'),
            alert_id=data.get('alert_id'),
            session_type=data.get('session_type', 'video')
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error creating crisis session: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/crisis/session/recommendations', methods=['POST'])
@jwt_required()
def get_session_recommendations():
    """Get AI recommendations during crisis session"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = crisis_service.generate_crisis_session_recommendations(
            session_transcript=data.get('session_transcript', ''),
            user_assessment=data.get('user_assessment', {})
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/crisis/followup-plan', methods=['POST'])
@jwt_required()
def generate_followup_plan():
    """Generate post-crisis follow-up plan"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = crisis_service.post_crisis_followup_plan(
            user_id=user_id,
            crisis_session_data=data.get('crisis_session_data', {}),
            counselor_notes=data.get('counselor_notes', '')
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error generating followup plan: {e}")
        return jsonify({'error': str(e)}), 500


# Export blueprint for registration
def register_advanced_routes(app):
    """Register advanced features blueprint with Flask app"""
    app.register_blueprint(advanced_bp)
    logger.info("Advanced features routes registered")
