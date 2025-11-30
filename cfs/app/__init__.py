import os
from flask import Flask, session
from app.config import config
from app.extensions import db, migrate, login_manager


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        from app import models

        instance_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)

    @app.before_request
    def set_default_language():
        if 'language' not in session:
            session['language'] = 'en'

    from app.routes import register_blueprints
    register_blueprints(app)

    return app
