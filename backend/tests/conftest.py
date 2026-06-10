"""Test configuration for Talk to Me."""

import pytest
from backend.app import create_app
from backend.config import Config


class TestConfig(Config):
    """Test configuration."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-secret-key'


@pytest.fixture
def app():
    """Create and configure a test app."""
    app = create_app(TestConfig)
    
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """Test client for app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test CLI runner."""
    return app.test_cli_runner()
