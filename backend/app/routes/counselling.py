"""Counselling routes (placeholder)."""
from flask import Blueprint

counselling_bp = Blueprint('counselling', __name__)

@counselling_bp.route('/appointments', methods=['GET'])
def get_appointments():
    return {'message': 'Get appointments'}, 200
