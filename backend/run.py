"""
Application entry point.

Run with: python run.py
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Set Flask environment
os.environ.setdefault('FLASK_ENV', os.environ.get('FLASK_ENV', 'development'))
os.environ.setdefault('FLASK_APP', 'run.py')

from backend.app import create_app, db

# Create app
app = create_app(config_name=os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Register shell context for flask shell."""
    return {'db': db}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return {'status': 'healthy', 'service': 'Talk to Me API'}, 200


if __name__ == '__main__':
    debug = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║          Talk to Me - Mental Health Platform          ║
    ║                   Backend Server                       ║
    ╚═══════════════════════════════════════════════════════╝
    
    Environment: {os.environ.get('FLASK_ENV', 'development')}
    Debug Mode: {debug}
    Port: {port}
    """)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
