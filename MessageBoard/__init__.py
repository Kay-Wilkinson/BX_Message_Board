import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.sqlite
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_mail import Mail 
from MessageBoard.config import Config 

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from MessageBoard.users.routes import users
    from MessageBoard.posts.routes import posts
    from MessageBoard.main.routes import main
    from MessageBoard.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    with app.app_context():
    	db.create_all()

    return app




