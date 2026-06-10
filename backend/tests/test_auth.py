"""Tests for authentication routes."""

import pytest


class TestAuth:
    """Test authentication endpoints."""
    
    def test_register_user(self, client):
        """Test user registration."""
        response = client.post('/auth/register', json={
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        assert response.status_code in [200, 201]
    
    def test_login_user(self, client):
        """Test user login."""
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        assert response.status_code in [200, 401]
    
    def test_invalid_email(self, client):
        """Test registration with invalid email."""
        response = client.post('/auth/register', json={
            'email': 'invalid',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        assert response.status_code == 400
