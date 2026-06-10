"""Startup and configuration regression tests."""

import backend.config as config_module


class BrokenConfig:
    """Config object that points at an invalid MySQL host."""

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@does-not-resolve.invalid/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = ['http://localhost:3000']
    SECRET_KEY = 'test-secret'
    JWT_SECRET_KEY = 'test-jwt-secret'
    DEBUG = False


def test_create_app_handles_unavailable_database(monkeypatch):
    """Startup should not crash when the configured DB host is unreachable."""
    original_config = config_module.config.copy()
    monkeypatch.setattr(config_module, 'config', {'testing': BrokenConfig})

    try:
        app = __import__('backend.app', fromlist=['create_app']).create_app('testing')
    finally:
        monkeypatch.setattr(config_module, 'config', original_config)

    assert app is not None
