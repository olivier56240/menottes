# app/services/cloudinary_service.py
import os
import cloudinary
import cloudinary.uploader
from werkzeug.datastructures import FileStorage


def init_cloudinary() -> bool:
   cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
   api_key = os.getenv("CLOUDINARY_API_KEY")
   api_secret = os.getenv("CLOUDINARY_API_SECRET")

   if not (cloud_name and api_key and api_secret):
       return False

   cloudinary.config(
       cloud_name=cloud_name,
       api_key=api_key,
       api_secret=api_secret,
       secure=True,
   )
   return True


def upload_image(file_storage: FileStorage, folder: str, public_id: str | None = None) -> str | None:
   if not file_storage:
       return None

   # IMPORTANT : on initialise à chaque upload (safe sur Render)
   if not init_cloudinary():
       return None

   res = cloudinary.uploader.upload(
       file_storage,
       folder=folder,
       public_id=public_id,
       resource_type="image",
   )
   return res.get("secure_url") or res.get("url")