from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config

from .routes.user import user
from .routes.post import post
from .models.user import User
from .models.post import Post


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(user)
    app.register_blueprint(post)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'user.login'
    login_manager.login_message = 'You must be autorized'
    login_manager.login_message_category = 'info'

    with app.app_context():
        db.create_all()


    @app.shell_context_processor
    def make_shell_context():
        return {'db' : db, 'User' : User, 'Post' : Post}

    return app




