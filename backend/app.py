"""
Aurum Ventura Lead Finder - Backend API
Business discovery and lead generation service
"""

import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from database import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///aurum_ventures.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db.init_app(app)
CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))

# Configure logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Internal server error: {error}')
    return jsonify({'error': 'Internal server error'}), 500


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'aurum-ventura-lead-finder'
    }), 200


# Serve the web interface
WEB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web', 'public'))


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(WEB_DIR, 'index.html')


@app.route('/app.js', methods=['GET'])
def web_app_js():
    return send_from_directory(WEB_DIR, 'app.js')


@app.route('/vendor/<path:filename>', methods=['GET'])
def web_vendor(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'vendor'), filename)


# Blueprint imports
from routes.search import search_bp
from routes.export import export_bp

# Register blueprints
app.register_blueprint(search_bp, url_prefix='/api/search')
app.register_blueprint(export_bp, url_prefix='/api/export')


if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        logger.info('Database initialized')
        logger.info('Starting Aurum Ventura Lead Finder')

    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', False)
    )
