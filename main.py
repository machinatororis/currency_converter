import os
import requests
import customtkinter as ctk
from tkinter import messagebox
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    messagebox.showerror("Ошибка", "API-ключ не найден. Проверьте файл .env")
    exit()

# Функция для получения списка валют
def get_currency_list():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return list(data["conversion_rates"].keys())
    else:
        messagebox.showerror("Ошибка", "Не удалось получить список валют.")
        return []


# Функция для выбора валюты с прокруткой
def open_currency_selector(var):
    selector = ctk.CTkToplevel(root)  # Создаём новое окно
    selector.title("Выберите валюту")
    selector.geometry("200x300")

    scroll_frame = ctk.CTkScrollableFrame(selector)
    scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

    for currency in currencies:
        btn = ctk.CTkButton(scroll_frame, text=currency, command=lambda c=currency: set_currency(var, c))
        btn.pack(fill="x", pady=2)


# Функция выбора валюты
def set_currency(var, currency):
    var.set(currency)


# Функция для конвертации валют
def convert_currency():
    base_currency = base_currency_var.get()
    target_currency = target_currency_var.get()
    amount = amount_entry.get()

    if not amount.replace(".", "", 1).isdigit():
        messagebox.showerror("Ошибка", "Введите корректное число для суммы!")
        return

    amount = float(amount)
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if target_currency in data["conversion_rates"]:
            rate = data["conversion_rates"][target_currency]
            converted_amount = amount * rate
            result_label.configure(text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
        else:
            messagebox.showerror("Ошибка", "Целевая валюта не найдена.")
    else:
        messagebox.showerror("Ошибка", "Не удалось получить данные с API.")


# Создаем главное окно
ctk.set_appearance_mode("dark")  # Тёмная тема
ctk.set_default_color_theme("blue")  # Цветовая схема

root = ctk.CTk()  # Создаем главное окно
root.title("Конвертер валют")
root.geometry("320x320")
root.resizable(False, False)

# Получаем список валют
currencies = get_currency_list()

# Основной фрейм
frame = ctk.CTkFrame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Поля ввода и выпадающие списки
ctk.CTkLabel(frame, text="Сумма:").pack(anchor="w")
amount_entry = ctk.CTkEntry(frame)
amount_entry.pack(fill="x", padx=5, pady=2)

ctk.CTkLabel(frame, text="Исходная валюта:").pack(anchor="w")
base_currency_var = ctk.StringVar(value="USD")
base_currency_button = ctk.CTkButton(frame, textvariable=base_currency_var, command=lambda: open_currency_selector(base_currency_var))
base_currency_button.pack(fill="x", padx=5, pady=2)

ctk.CTkLabel(frame, text="Целевая валюта:").pack(anchor="w")
target_currency_var = ctk.StringVar(value="EUR")
target_currency_button = ctk.CTkButton(frame, textvariable=target_currency_var, command=lambda: open_currency_selector(target_currency_var))
target_currency_button.pack(fill="x", padx=5, pady=10)

# Кнопка для конвертации
convert_button = ctk.CTkButton(frame, text="Конвертировать", command=convert_currency)
convert_button.pack(fill="x", padx=5, pady=5)

# Поле для вывода результата
result_label = ctk.CTkLabel(frame, text="", font=("Arial", 14))
result_label.pack(anchor="w", padx=5, pady=5)

# Запуск главного цикла Tkinter
root.mainloop()
