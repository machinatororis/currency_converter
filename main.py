import os
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Читаем API-ключ
API_KEY = os.getenv("API_KEY")