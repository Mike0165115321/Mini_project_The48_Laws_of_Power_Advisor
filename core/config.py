# core/config.py
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    GOOGLE_API_KEYS = [key.strip() for key in os.getenv("GOOGLE_API_KEYS", "").split(',') if key.strip()]

settings = Settings()