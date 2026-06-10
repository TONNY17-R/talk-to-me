"""
Security utilities for authentication and encryption.
"""

import hashlib
import hmac
import os
from datetime import datetime, timedelta
import jwt


def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + key.hex()


def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verify provided password against stored hash."""
    salt = bytes.fromhex(stored_hash[:64])
    stored_key = stored_hash[64:]
    key = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return key.hex() == stored_key


def generate_jwt_token(payload: dict, expires_in_hours: int = 24) -> str:
    """Generate JWT token."""
    secret_key = os.environ.get('JWT_SECRET_KEY', 'dev-secret')
    payload['exp'] = datetime.utcnow() + timedelta(hours=expires_in_hours)
    return jwt.encode(payload, secret_key, algorithm='HS256')


def verify_jwt_token(token: str) -> dict:
    """Verify and decode JWT token."""
    try:
        secret_key = os.environ.get('JWT_SECRET_KEY', 'dev-secret')
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}


def generate_secure_token(length: int = 32) -> str:
    """Generate cryptographically secure token."""
    return os.urandom(length).hex()


def create_signature(data: str, key: str) -> str:
    """Create HMAC signature."""
    return hmac.new(
        key.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()


def verify_signature(data: str, signature: str, key: str) -> bool:
    """Verify HMAC signature."""
    expected_signature = create_signature(data, key)
    return hmac.compare_digest(signature, expected_signature)


def encrypt_sensitive_data(data: str, key: str = None) -> str:
    """Encrypt sensitive data."""
    # Implementation would use cryptography library
    return data


def decrypt_sensitive_data(encrypted_data: str, key: str = None) -> str:
    """Decrypt sensitive data."""
    # Implementation would use cryptography library
    return encrypted_data
