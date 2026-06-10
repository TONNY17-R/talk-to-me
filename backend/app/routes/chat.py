"""
Chat routes module.

Handles chat sessions, messages, and AI interactions.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_chat_sessions():
    """Get all chat sessions for the current user."""
    try:
        from backend.app.models.chat import ChatSession
        
        user_id = get_jwt_identity()
        sessions = ChatSession.query.filter_by(user_id=user_id).order_by(ChatSession.started_at.desc()).all()
        
        return jsonify({
            'sessions': [s.to_dict() for s in sessions],
            'total': len(sessions)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching chat sessions: {str(e)}")
        return jsonify({'error': 'Failed to fetch sessions'}), 500


@chat_bp.route('/sessions/<int:session_id>', methods=['GET'])
@jwt_required()
def get_chat_session(session_id):
    """Get a specific chat session with all messages."""
    try:
        from backend.app.models.chat import ChatSession
        
        user_id = get_jwt_identity()
        session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        messages = [m.to_dict() for m in session.messages]
        
        return jsonify({
            'session': session.to_dict(),
            'messages': messages
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching chat session: {str(e)}")
        return jsonify({'error': 'Failed to fetch session'}), 500


@chat_bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_chat_session():
    """Create a new chat session."""
    try:
        from backend.app import db
        from backend.app.models.chat import ChatSession
        
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        session = ChatSession(
            user_id=user_id,
            language=data.get('language', 'en'),
            theme=data.get('theme')
        )
        
        db.session.add(session)
        db.session.commit()
        
        logger.info(f"New chat session created: {session.id} for user {user_id}")
        
        return jsonify({
            'message': 'Chat session created',
            'session': session.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating chat session: {str(e)}")
        return jsonify({'error': 'Failed to create session'}), 500


@chat_bp.route('/sessions/<int:session_id>/messages', methods=['POST'])
@jwt_required()
def send_message(session_id):
    """Send a message and get AI response."""
    try:
        from backend.app import db
        from backend.app.models.chat import ChatSession, ChatMessage
        from backend.app.services.ai_service import AIService
        
        user_id = get_jwt_identity()
        session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        data = request.get_json()
        
        if not data or not data.get('content'):
            return jsonify({'error': 'Message content is required'}), 400
        
        # Save user message
        user_message = ChatMessage(
            session_id=session_id,
            sender_type='user',
            content=data['content'],
            message_type=data.get('message_type', 'text')
        )
        
        db.session.add(user_message)
        db.session.flush()
        
        # Get AI response
        ai_service = AIService()
        ai_response = ai_service.get_response(
            user_input=data['content'],
            user_context={
                'user_id': user_id,
                'session_id': session_id,
                'language': session.language
            }
        )
        
        # Save AI message
        ai_message = ChatMessage(
            session_id=session_id,
            sender_type='assistant',
            content=ai_response['response'],
            sentiment=ai_response.get('sentiment'),
            message_type='text'
        )
        
        db.session.add(ai_message)
        db.session.commit()
        
        logger.info(f"Message exchanged in session {session_id}")
        
        return jsonify({
            'user_message': user_message.to_dict(),
            'ai_response': ai_message.to_dict(),
            'metadata': {
                'risk_level': ai_response.get('risk_level'),
                'sentiment': ai_response.get('sentiment')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return jsonify({'error': 'Failed to send message'}), 500


@chat_bp.route('/sessions/<int:session_id>/close', methods=['POST'])
@jwt_required()
def close_session(session_id):
    """Close a chat session."""
    try:
        from backend.app import db
        from backend.app.models.chat import ChatSession
        from datetime import datetime
        
        user_id = get_jwt_identity()
        session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        session.is_active = False
        session.ended_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Chat session closed: {session_id}")
        
        return jsonify({
            'message': 'Session closed',
            'session': session.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error closing session: {str(e)}")
        return jsonify({'error': 'Failed to close session'}), 500
