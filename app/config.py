import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class DevConfig:
   SECRET_KEY = "plouay"

   SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "..", "instance", "app.db")
   SQLALCHEMY_TRACK_MODIFICATIONS = False