import os
from dotenv import load_dotenv
import cloudinary

# Load environment variables from .env
load_dotenv()

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("Cloudinary_cloud"),
    api_key=os.getenv("Cloudinary_API_Key"),
    api_secret=os.getenv("Cloudinary_API_Secret"),
)
