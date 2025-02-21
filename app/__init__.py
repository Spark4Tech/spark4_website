# app/__init__.py

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.after_request
    def add_security_headers(response):
        csp = {
            'default-src': ["'self'"],
            'script-src': [
                "'self'",
                "'unsafe-inline'",
                "'unsafe-eval'",
                "https://www.googletagmanager.com",
                "https://unpkg.com",
                "https://*.googleapis.com"
            ],
            'style-src': [
                "'self'",
                "'unsafe-inline'",
                "https://fonts.googleapis.com",
                "https://unpkg.com"
            ],
            'font-src': [
                "'self'",
                "https://fonts.gstatic.com"
            ],
            'img-src': ["'self'", "data:", "https:"],
            'connect-src': ["'self'", "https:"],
            'frame-src': ["'self'"],
            'media-src': ["'self'"]
        }
        
        response.headers['Content-Security-Policy'] = '; '.join([
            f"{key} {' '.join(values)}"
            for key, values in csp.items()
        ])
        return response
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    Bootstrap(app)

    # Import models to ensure they are registered with SQLAlchemy
    from app import models

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # If you have a blog blueprint, ensure it's set up correctly
    # Uncomment the following lines if you have a blog blueprint
    from app.blog.routes import blog
    app.register_blueprint(blog, url_prefix='/blog')

    return app
