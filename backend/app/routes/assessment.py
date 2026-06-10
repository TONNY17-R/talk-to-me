"""
Assessment routes module.

Handles mental health assessments (PHQ-9, GAD-7, DASS-21, etc.).
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

logger = logging.getLogger(__name__)

assessment_bp = Blueprint('assessment', __name__)


@assessment_bp.route('/available', methods=['GET'])
@jwt_required()
def get_available_assessments():
    """Get list of available assessments."""
    try:
        assessments = [
            {'id': 'phq9', 'name': 'PHQ-9', 'description': 'Patient Health Questionnaire - Depression', 'duration_minutes': 5},
            {'id': 'gad7', 'name': 'GAD-7', 'description': 'Generalized Anxiety Disorder', 'duration_minutes': 3},
            {'id': 'dass21', 'name': 'DASS-21', 'description': 'Depression Anxiety Stress Scale', 'duration_minutes': 8},
            {'id': 'pc_ptsd', 'name': 'PC-PTSD', 'description': 'PTSD Screening', 'duration_minutes': 5},
            {'id': 'psqi', 'name': 'PSQI', 'description': 'Sleep Quality Index', 'duration_minutes': 10}
        ]
        return jsonify({'assessments': assessments}), 200
    except Exception as e:
        logger.error(f"Error fetching assessments: {str(e)}")
        return jsonify({'error': 'Failed to fetch assessments'}), 500


@assessment_bp.route('/start', methods=['POST'])
@jwt_required()
def start_assessment():
    """Start a new assessment."""
    try:
        from backend.app import db
        from backend.app.models.assessment import Assessment, AssessmentType
        
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('assessment_type'):
            return jsonify({'error': 'Assessment type is required'}), 400
        
        # Create assessment
        assessment = Assessment(
            user_id=user_id,
            assessment_type=AssessmentType(data['assessment_type'])
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        # Get questions for this assessment type
        questions = get_assessment_questions(data['assessment_type'])
        
        logger.info(f"Assessment started: {assessment.id} for user {user_id}")
        
        return jsonify({
            'assessment_id': assessment.id,
            'assessment_type': data['assessment_type'],
            'questions': questions
        }), 201
        
    except Exception as e:
        logger.error(f"Error starting assessment: {str(e)}")
        return jsonify({'error': 'Failed to start assessment'}), 500


@assessment_bp.route('/<int:assessment_id>/answer', methods=['POST'])
@jwt_required()
def answer_question(assessment_id):
    """Record an answer to an assessment question."""
    try:
        from backend.app import db
        from backend.app.models.assessment import Assessment, AssessmentResponse
        
        user_id = get_jwt_identity()
        data = request.get_json()
        
        assessment = Assessment.query.filter_by(id=assessment_id, user_id=user_id).first()
        
        if not assessment:
            return jsonify({'error': 'Assessment not found'}), 404
        
        if not all(k in data for k in ['question_id', 'answer', 'score']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        response = AssessmentResponse(
            assessment_id=assessment_id,
            question_id=data['question_id'],
            answer=data['answer'],
            score=data['score'],
            time_spent_seconds=data.get('time_spent_seconds')
        )
        
        db.session.add(response)
        db.session.commit()
        
        return jsonify({'message': 'Answer recorded'}), 200
        
    except Exception as e:
        logger.error(f"Error recording answer: {str(e)}")
        return jsonify({'error': 'Failed to record answer'}), 500


@assessment_bp.route('/<int:assessment_id>/complete', methods=['POST'])
@jwt_required()
def complete_assessment(assessment_id):
    """Complete an assessment and get results."""
    try:
        from backend.app import db
        from backend.app.models.assessment import Assessment, RiskLevel
        from datetime import datetime
        
        user_id = get_jwt_identity()
        assessment = Assessment.query.filter_by(id=assessment_id, user_id=user_id).first()
        
        if not assessment:
            return jsonify({'error': 'Assessment not found'}), 404
        
        # Calculate scores and risk level
        total_score = sum(r.score for r in assessment.responses)
        risk_level = calculate_risk_level(assessment.assessment_type.value, total_score)
        
        assessment.overall_score = total_score
        assessment.risk_level = risk_level
        assessment.is_completed = True
        assessment.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Assessment completed: {assessment_id} - Risk level: {risk_level}")
        
        return jsonify({
            'assessment': assessment.to_dict(),
            'results': {
                'total_score': total_score,
                'risk_level': risk_level.value if risk_level else None,
                'recommendations': get_recommendations(assessment.assessment_type.value, total_score)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error completing assessment: {str(e)}")
        return jsonify({'error': 'Failed to complete assessment'}), 500


@assessment_bp.route('/history', methods=['GET'])
@jwt_required()
def get_assessment_history():
    """Get user's assessment history."""
    try:
        from backend.app.models.assessment import Assessment
        
        user_id = get_jwt_identity()
        assessments = Assessment.query.filter_by(user_id=user_id, is_completed=True).order_by(Assessment.completed_at.desc()).all()
        
        return jsonify({
            'assessments': [a.to_dict() for a in assessments],
            'total': len(assessments)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching assessment history: {str(e)}")
        return jsonify({'error': 'Failed to fetch history'}), 500


def get_assessment_questions(assessment_type):
    """Get questions for a specific assessment type."""
    questions_db = {
        'phq9': [
            {'id': 1, 'text': 'Little interest or pleasure in doing things', 'options': ['Not at all', 'Several days', 'More than half', 'Nearly every day']},
            {'id': 2, 'text': 'Feeling down, depressed, or hopeless', 'options': ['Not at all', 'Several days', 'More than half', 'Nearly every day']},
            # Add remaining 7 questions...
        ],
        'gad7': [
            {'id': 1, 'text': 'Feeling nervous, anxious or on edge', 'options': ['Not at all', 'Several days', 'More than half', 'Nearly every day']},
            # Add remaining questions...
        ]
    }
    return questions_db.get(assessment_type, [])


def calculate_risk_level(assessment_type, score):
    """Calculate risk level based on assessment type and score."""
    from backend.app.models.assessment import RiskLevel
    
    risk_mapping = {
        'phq9': {
            'low': (0, 9),
            'moderate': (10, 14),
            'high': (15, 19),
            'critical': (20, 27)
        },
        'gad7': {
            'low': (0, 4),
            'moderate': (5, 9),
            'high': (10, 14),
            'critical': (15, 21)
        }
    }
    
    ranges = risk_mapping.get(assessment_type, {})
    for level, (min_score, max_score) in ranges.items():
        if min_score <= score <= max_score:
            return RiskLevel(level)
    
    return RiskLevel.CRITICAL


def get_recommendations(assessment_type, score):
    """Get recommendations based on assessment results."""
    recommendations = {
        'phq9': {
            'low': 'Continue with self-care practices and healthy lifestyle.',
            'moderate': 'Consider speaking with a counselor for support.',
            'high': 'Professional counseling is recommended.',
            'critical': 'Urgent: Please contact a mental health professional or crisis hotline.'
        }
    }
    
    type_recommendations = recommendations.get(assessment_type, {})
    risk_level = calculate_risk_level(assessment_type, score)
    return type_recommendations.get(risk_level.value if risk_level else None, '')
