"""
Routes package initialization.

Registers all route blueprints for the application.
"""

from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__)
chat_bp = Blueprint('chat', __name__)
assessment_bp = Blueprint('assessment', __name__)
counselling_bp = Blueprint('counselling', __name__)
resources_bp = Blueprint('resources', __name__)
admin_bp = Blueprint('admin', __name__)

# Import route handlers
from backend.app.routes.auth import *
from backend.app.routes.chat import *
from backend.app.routes.assessment import *
from backend.app.routes.counselling import *
from backend.app.routes.resources import *
from backend.app.routes.admin import *

__all__ = [
    'auth_bp',
    'chat_bp',
    'assessment_bp',
    'counselling_bp',
    'resources_bp',
    'admin_bp'
]
