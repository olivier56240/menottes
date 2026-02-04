from flask import Flask
from .config import DevConfig
from .extensions import db, migrate, login_manager, csrf

# ⚠️ IMPORTANT : permet à Flask-Migrate de voir les modèles
from . import models


def create_app():
   app = Flask(__name__, template_folder="templates", static_folder="static")
   app.config.from_object(DevConfig)

   # Init extensions
   db.init_app(app)
   migrate.init_app(app, db)
   login_manager.init_app(app)
   csrf.init_app(app)

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
   app = Flask(__name__, template_folder="templates", static_folder="static")
   app.config.from_object(DevConfig)

   # ✅ FORCE la DB ici (Render / prod)
   db_url = os.environ.get("DATABASE_URL")
   if db_url and db_url.startswith("postgres://"):
       db_url = db_url.replace("postgres://", "postgresql://", 1)

   if db_url:
       app.config["SQLALCHEMY_DATABASE_URI"] = db_url
   else:
       app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "instance/local.db")

   db.init_app(app)
   migrate.init_app(app, db)
   login_manager.init_app(app)
   csrf.init_app(app)

   login_manager.login_view = "auth.login"

   # blueprints...
   from .auth import bp as auth_bp
   from .notes import bp as notes_bp
   from .activities import bp as activities_bp
   from .main import bp as main_bp
   
   app.register_blueprint(auth_bp)
   app.register_blueprint(notes_bp)
   app.register_blueprint(activities_bp)
   app.register_blueprint(main_bp)
   

   return app