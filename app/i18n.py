TEXTS = {
    "en": {
        "app_title": "Currency Converter",
        "amount": "Amount:",
        "from_currency": "From Currency:",
        "to_currency": "To Currency:",
        "convert": "Convert",
        "select_currency": "Select Currency",
        "language_button": "EN | RU",
        "error": "Error",
        "api_key_missing": "API key not found. Check the .env file.",
        "currency_list_error": "Failed to get currency list.",
        "invalid_amount": "Please enter a valid amount.",
        "target_currency_not_found": "Target currency not found.",
        "api_error": "Failed to get data from API.",
    },
    "ru": {
        "app_title": "Конвертер валют",
        "amount": "Сумма:",
        "from_currency": "Исходная валюта:",
        "to_currency": "Целевая валюта:",
        "convert": "Конвертировать",
        "select_currency": "Выберите валюту",
        "language_button": "EN | RU",
        "error": "Ошибка",
        "api_key_missing": "API-ключ не найден. Проверьте файл .env.",
        "currency_list_error": "Не удалось получить список валют.",
        "invalid_amount": "Введите корректное число для суммы!",
        "target_currency_not_found": "Целевая валюта не найдена.",
        "api_error": "Не удалось получить данные с API.",
    },
}


def get_text(language, key):
    return TEXTS[language][key]