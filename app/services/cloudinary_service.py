import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

def init_cloudinary():
   cloudinary.config(
       cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
       api_key=os.environ.get("CLOUDINARY_API_KEY"),
       api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
       secure=True,
   )

def upload_image(file_storage, folder: str, public_id: str | None = None) -> str:
   """
   Upload un fichier (Werkzeug FileStorage) sur Cloudinary et retourne l'URL secure.
   """
   if not file_storage:
       return ""

   res = cloudinary.uploader.upload(
       file_storage,
       folder=folder,
       public_id=public_id,
       overwrite=True,
       resource_type="image",
   )
   return res.get("secure_url", "")