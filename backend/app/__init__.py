import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from .models import db
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS for frontend integration
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize SQLAlchemy database
    db.init_app(app)
    
    # Register API Blueprints
    from .routes.auth import auth_bp
    from .routes.artisan import artisan_bp
    from .routes.buyer import buyer_bp
    from .routes.agent_story import agent_story_bp
    from .routes.agent_pricing import agent_pricing_bp
    from .routes.agent_discovery import agent_discovery_bp, agent_quotation_bp
    from .routes.agent_negotiation import agent_negotiation_bp
    from .routes.orders import order_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(artisan_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(agent_story_bp)
    app.register_blueprint(agent_pricing_bp)
    app.register_blueprint(agent_discovery_bp)
    app.register_blueprint(agent_quotation_bp)
    app.register_blueprint(agent_negotiation_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'project': 'KARIGAR AI',
            'version': '1.0.0',
            'problem_statement': '7.1',
            'database': 'Connected',
            'gate_enforcement': 'ACTIVE'
        })

    return app
