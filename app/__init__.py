from flask import Flask
from dotenv import load_dotenv
from config import Config
from app.extensions import db, migrate, login_manager

load_dotenv()  # ✅ Load environment variables from .env

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print("🔗 Using Database URL:", app.config["SQLALCHEMY_DATABASE_URI"])  # ✅ Add this
    print("Using Database URL:", app.config["SQLALCHEMY_DATABASE_URI"])


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app import models

    return app

