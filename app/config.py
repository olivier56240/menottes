import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
   db_url = db_url.replace("postgres://", "postgresql://", 1)

class DevConfig:
   SECRET_KEY = os.environ.get("SECRET_KEY", "plouay")
   SQLALCHEMY_DATABASE_URI = db_url or "sqlite:///" + os.path.join(BASE_DIR, "instance/local.db")
   SQLALCHEMY_TRACK_MODIFICATIONS = False