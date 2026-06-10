"""Admin routes (placeholder)."""
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    return {'message': 'Admin dashboard'}, 200
