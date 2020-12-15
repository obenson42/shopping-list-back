""" __init__.py : create all the flask objects needed by the app
and a create_app function which allows for different configurations (eg production or test) """
import os
from flask import Flask, g
from flask_login import LoginManager, user_loaded_from_header
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask.sessions import SecureCookieSessionInterface
from config import Config

class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)

@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True

login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.session_interface = CustomSessionInterface()

    login.init_app(app)
    login.login_view = 'auth.login'

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app import routes, models
    app.register_blueprint(routes.bp)

    return app
