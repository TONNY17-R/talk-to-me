"""
Authentication routes module.

Handles user authentication, registration, login, JWT token management.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request JSON:
        email: User email
        password: User password
        first_name: User first name
        last_name: User last name
        phone: User phone number
        country: User country
        preferred_language: Preferred language (en, lg, sw)
    """
    try:
        from backend.app import db
        from backend.app.models.user import User
        from backend.app.utils.validators import validate_email, validate_password
        
        data = request.get_json()
        
        # Validation
        if not data or not all(k in data for k in ['email', 'password', 'first_name', 'last_name']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not validate_password(data['password']):
            return jsonify({'error': 'Password must be at least 8 characters with uppercase, lowercase, and number'}), 400
        
        # Check if user exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        
        # Create new user
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone'),
            country=data.get('country'),
            preferred_language=data.get('preferred_language', 'en')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"New user registered: {user.email}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user.id,
            'email': user.email
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT tokens.
    
    Request JSON:
        email: User email
        password: User password
    """
    try:
        from backend.app.models.user import User
        
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            logger.warning(f"Failed login attempt for email: {data['email']}")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'User account is inactive'}), 403
        
        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        # Update last login
        user.last_login = datetime.utcnow()
        from backend.app import db
        db.session.commit()
        
        logger.info(f"User logged in: {user.email}")
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token."""
    try:
        user_id = get_jwt_identity()
        access_token = create_access_token(
            identity=user_id,
            expires_delta=timedelta(hours=24)
        )
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Token refresh failed'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (add token to blacklist)."""
    try:
        user_id = get_jwt_identity()
        logger.info(f"User logged out: {user_id}")
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500


@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """Verify user email with verification code."""
    try:
        from backend.app.models.user import User
        from backend.app import db
        
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('verification_code'):
            return jsonify({'error': 'Missing email or verification code'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.verify_email(data['verification_code']):
            db.session.commit()
            logger.info(f"Email verified: {user.email}")
            return jsonify({'message': 'Email verified successfully'}), 200
        else:
            return jsonify({'error': 'Invalid verification code'}), 400
            
    except Exception as e:
        logger.error(f"Email verification error: {str(e)}")
        return jsonify({'error': 'Email verification failed'}), 500


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset."""
    try:
        from backend.app.models.user import User
        from backend.app.services.email_service import send_password_reset_email
        
        data = request.get_json()
        
        if not data or not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user:
            # Generate reset token
            reset_token = user.generate_reset_token()
            from backend.app import db
            db.session.commit()
            
            # Send email
            send_password_reset_email(user.email, reset_token)
            logger.info(f"Password reset requested for: {user.email}")
        
        # Always return success to avoid email enumeration
        return jsonify({'message': 'If email exists, reset link will be sent'}), 200
        
    except Exception as e:
        logger.error(f"Password reset request error: {str(e)}")
        return jsonify({'error': 'Password reset request failed'}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token."""
    try:
        from backend.app.models.user import User
        from backend.app import db
        
        data = request.get_json()
        
        if not all(k in data for k in ['token', 'password']):
            return jsonify({'error': 'Missing token or password'}), 400
        
        user = User.verify_reset_token(data['token'])
        
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 400
        
        user.set_password(data['password'])
        db.session.commit()
        
        logger.info(f"Password reset for: {user.email}")
        
        return jsonify({'message': 'Password reset successful'}), 200
        
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        return jsonify({'error': 'Password reset failed'}), 500
