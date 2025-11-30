def register_blueprints(app):
    from app.routes.main import main_bp
    from app.routes.language import language_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(language_bp, url_prefix='/lang')
