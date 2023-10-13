from pathlib import Path

from dotenv import dotenv_values
from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = dotenv_values(Path(__file__).parent / '.env').get('SECRET_KEY', 'development')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .drive import drive as drive_blueprint
    app.register_blueprint(drive_blueprint)

    return app