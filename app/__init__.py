from flask import Flask
from flask_migrate import upgrade

from .config import DevConfig
from .extensions import db, migrate, login_manager, csrf


def create_app():
   app = Flask(__name__, template_folder="templates", static_folder="static")
   app.config.from_object(DevConfig)

   # Init extensions
   db.init_app(app)
   migrate.init_app(app, db)
   login_manager.init_app(app)
   csrf.init_app(app)

   # Run migrations automatically (Render free: pas de shell)
   with app.app_context():
       upgrade()

   login_manager.login_view = "auth.login"

   # Blueprints
   from .auth import bp as auth_bp
   from .notes import bp as notes_bp
   from .activities import bp as activities_bp
   from .main import bp as main_bp

   app.register_blueprint(auth_bp)
   app.register_blueprint(notes_bp)
   app.register_blueprint(activities_bp)
   app.register_blueprint(main_bp)

   return app