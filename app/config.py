import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class DevConfig:
   SECRET_KEY = os.environ.get("SECRET_KEY", "dev")

   db_url = os.environ.get("DATABASE_URL")

   if db_url:
       if db_url.startswith("postgres://"):
           db_url = db_url.replace("postgres://", "postgresql://", 1)
       SQLALCHEMY_DATABASE_URI = db_url
   else:
       SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance/local.db")

   SQLALCHEMY_TRACK_MODIFICATIONS = False