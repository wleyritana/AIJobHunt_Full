from flask import Flask
from app.config import Config
from app.extensions import db, login_manager
from app.models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.appflow import bp as flow_bp
    from app.blueprints.analytics import bp as analytics_bp
    from app.blueprints.alerts import bp as alerts_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(flow_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(alerts_bp)

    return app
