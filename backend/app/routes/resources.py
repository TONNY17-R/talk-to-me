"""Resources routes (placeholder)."""
from flask import Blueprint

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/list', methods=['GET'])
def get_resources():
    return {'message': 'Get resources'}, 200
