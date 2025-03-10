import os
from flask import Flask, send_from_directory
from config.config import config
from app.extensions import db, migrate, ma, cors
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)

    # Register blueprints
    from app.api.vendors import vendors_bp
    from app.api.drones import drones_bp
    
    app.register_blueprint(vendors_bp, url_prefix='/api/v1/vendors')
    app.register_blueprint(drones_bp, url_prefix='/api/v1/drones')

    # Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Drone Database API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/api/swagger.json")
    def specs():
        return send_from_directory(os.path.join(app.root_path, 'swagger'), 'swagger.json')

    return app 