from flask import Flask
from flask_login import LoginManager

from .config import CONFIG
from .models import db, User

def create_app():
    app = Flask(__name__)
    app.config.update(CONFIG)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .drive import drive as drive_blueprint
    app.register_blueprint(drive_blueprint)

    return app