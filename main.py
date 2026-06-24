# import os
# import sys
# import requests
# import customtkinter as ctk
# from tkinter import messagebox
# from dotenv import load_dotenv
#
#
# # Определяем путь к папке приложения
# def get_base_path():
#     if getattr(sys, "frozen", False):
#         return os.path.dirname(sys.executable)
#     return os.path.dirname(os.path.abspath(__file__))
#
#
# BASE_PATH = get_base_path()
# env_path = os.path.join(BASE_PATH, ".env")
#
# # Загружаем переменные из .env
# load_dotenv(env_path)
#
# API_KEY = os.getenv("API_KEY")
#
# # Языки интерфейса
# current_language = "en"
#
# TEXTS = {
#     "en": {
#         "app_title": "Currency Converter",
#         "amount": "Amount:",
#         "from_currency": "From Currency:",
#         "to_currency": "To Currency:",
#         "convert": "Convert",
#         "select_currency": "Select Currency",
#         "language_button": "EN | RU",
#         "error": "Error",
#         "api_key_missing": "API key not found. Check the .env file.",
#         "currency_list_error": "Failed to get currency list.",
#         "invalid_amount": "Please enter a valid amount.",
#         "target_currency_not_found": "Target currency not found.",
#         "api_error": "Failed to get data from API.",
#     },
#     "ru": {
#         "app_title": "Конвертер валют",
#         "amount": "Сумма:",
#         "from_currency": "Исходная валюта:",
#         "to_currency": "Целевая валюта:",
#         "convert": "Конвертировать",
#         "select_currency": "Выберите валюту",
#         "language_button": "EN | RU",
#         "error": "Ошибка",
#         "api_key_missing": "API-ключ не найден. Проверьте файл .env",
#         "currency_list_error": "Не удалось получить список валют.",
#         "invalid_amount": "Введите корректное число для суммы!",
#         "target_currency_not_found": "Целевая валюта не найдена.",
#         "api_error": "Не удалось получить данные с API.",
#     },
# }
#
#
# def t(key):
#     return TEXTS[current_language][key]
#
#
# if not API_KEY:
#     messagebox.showerror(TEXTS[current_language]["error"], TEXTS[current_language]["api_key_missing"])
#     exit()
#
#
# # Функция для получения списка валют
# def get_currency_list():
#     url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         data = response.json()
#         return list(data["conversion_rates"].keys())
#     else:
#         messagebox.showerror(t("error"), t("currency_list_error"))
#         return []
#
#
# # Функция для выбора валюты с прокруткой
# def open_currency_selector(var):
#     selector = ctk.CTkToplevel(root)
#     selector.title(t("select_currency"))
#     selector.geometry("200x300")
#
#     scroll_frame = ctk.CTkScrollableFrame(selector)
#     scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
#
#     for currency in currencies:
#         btn = ctk.CTkButton(
#             scroll_frame,
#             text=currency,
#             command=lambda c=currency, window=selector: set_currency(var, c, window)
#         )
#         btn.pack(fill="x", pady=2)
#
#
# # Функция выбора валюты
# def set_currency(var, currency, window=None):
#     var.set(currency)
#
#     if window:
#         window.destroy()
#
#
# # Функция для конвертации валют
# def convert_currency():
#     base_currency = base_currency_var.get()
#     target_currency = target_currency_var.get()
#     amount = amount_entry.get().replace(",", ".")
#
#     if not amount.replace(".", "", 1).isdigit():
#         messagebox.showerror(t("error"), t("invalid_amount"))
#         return
#
#     amount = float(amount)
#     url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         data = response.json()
#
#         if target_currency in data["conversion_rates"]:
#             rate = data["conversion_rates"][target_currency]
#             converted_amount = amount * rate
#             result_label.configure(
#                 text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}"
#             )
#         else:
#             messagebox.showerror(t("error"), t("target_currency_not_found"))
#     else:
#         messagebox.showerror(t("error"), t("api_error"))
#
#
# # Функция переключения языка
# def switch_language():
#     global current_language
#
#     if current_language == "en":
#         current_language = "ru"
#     else:
#         current_language = "en"
#
#     update_language()
#
#
# # Функция обновления текстов интерфейса
# def update_language():
#     root.title(t("app_title"))
#
#     amount_label.configure(text=t("amount"))
#     base_currency_label.configure(text=t("from_currency"))
#     target_currency_label.configure(text=t("to_currency"))
#     convert_button.configure(text=t("convert"))
#     language_button.configure(text=t("language_button"))
#
#
# # Создаем главное окно
# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")
#
# root = ctk.CTk()
# root.title(t("app_title"))
# root.geometry("320x350")
# root.resizable(False, False)
#
# # Получаем список валют
# currencies = get_currency_list()
#
# # Основной фрейм
# frame = ctk.CTkFrame(root)
# frame.pack(fill="both", expand=True, padx=10, pady=10)
#
# # Кнопка переключения языка
# language_button = ctk.CTkButton(
#     frame,
#     text=t("language_button"),
#     width=70,
#     command=switch_language
# )
# language_button.pack(anchor="e", padx=5, pady=(10, 5))
#
# # Поля ввода и выбор валют
# amount_label = ctk.CTkLabel(frame, text=t("amount"))
# amount_label.pack(anchor="w")
#
# amount_entry = ctk.CTkEntry(frame)
# amount_entry.pack(fill="x", padx=5, pady=2)
#
# base_currency_label = ctk.CTkLabel(frame, text=t("from_currency"))
# base_currency_label.pack(anchor="w")
#
# base_currency_var = ctk.StringVar(value="USD")
# base_currency_button = ctk.CTkButton(
#     frame,
#     textvariable=base_currency_var,
#     command=lambda: open_currency_selector(base_currency_var)
# )
# base_currency_button.pack(fill="x", padx=5, pady=2)
#
# target_currency_label = ctk.CTkLabel(frame, text=t("to_currency"))
# target_currency_label.pack(anchor="w")
#
# target_currency_var = ctk.StringVar(value="EUR")
# target_currency_button = ctk.CTkButton(
#     frame,
#     textvariable=target_currency_var,
#     command=lambda: open_currency_selector(target_currency_var)
# )
# target_currency_button.pack(fill="x", padx=5, pady=10)
#
# # Кнопка для конвертации
# convert_button = ctk.CTkButton(
#     frame,
#     text=t("convert"),
#     command=convert_currency
# )
# convert_button.pack(fill="x", padx=5, pady=5)
#
# # Поле для вывода результата
# result_label = ctk.CTkLabel(frame, text="", font=("Arial", 14))
# result_label.pack(anchor="w", padx=5, pady=5)
#
# # Запуск главного цикла Tkinter
# root.mainloop()

from app.gui import CurrencyConverterApp


if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()