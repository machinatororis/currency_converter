import requests


API_BASE_URL = "https://v6.exchangerate-api.com/v6"
REQUEST_TIMEOUT = 10


def get_currency_list(api_key):
    url = f"{API_BASE_URL}/{api_key}/latest/USD"

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code != 200:
        return None

    data = response.json()
    conversion_rates = data.get("conversion_rates")

    if not conversion_rates:
        return None

    return list(conversion_rates.keys())


def convert_currency(api_key, amount, base_currency, target_currency):
    url = f"{API_BASE_URL}/{api_key}/latest/{base_currency}"

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code != 200:
        return None

    data = response.json()
    conversion_rates = data.get("conversion_rates")

    if not conversion_rates:
        return None

    rate = conversion_rates.get(target_currency)

    if rate is None:
        return None

    return amount * rate