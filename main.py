import os
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Читаем API-ключ
API_KEY = os.getenv("API_KEY")

# Проверяем, есть ли ключ
if not API_KEY:
    print("Ошибка: API-ключ не найден. Проверьте файл .env")
else:
    print("API-ключ загружен успешно!")

# Тестовый запрос
url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
response = requests.get(url)

if response.status_code == 200:
    print("API-ключ работает!")
    data = response.json()
    print(f"Пример курса: 1 USD = {data['conversion_rates'] ['EUR']} EUR")

else:
    print(f"Ошибка: API не отвечает. Код состояния {response.status_code}")
    print(f"Сообщение от сервера: {response.text}")
