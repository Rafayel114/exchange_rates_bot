database_path = './exchange_data.sqlite'
telegram_bot_token = '1086043254:AAHAc0Z7cOdORX74Z71uMbjDtkiuvqL76Og'
REQUEST_KWARGS = {
    # Comment proxy_url if you are not in Russia
    # "USERNAME:PASSWORD@" is optional, if you need authentication:
    'proxy_url': 'https://180.210.201.55:3129',
}

polling_interval = 10 # time to consider our DB data not relevant (in minutes)
currency_base = "USD" # base currency for DB
graph_period = 7 # Days number in history graph (in days)

url_all_currencies = f"https://api.exchangeratesapi.io/latest?base={currency_base}"
url_graph = "https://api.exchangeratesapi.io/history?start_at=%s&end_at=%s&base=%s&symbols=%s"
