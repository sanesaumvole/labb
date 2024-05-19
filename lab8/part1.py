import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('crypto_loader')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('crypto_loader.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def get_historical_data(product, start, end, granularity):
    logger = logging.getLogger('crypto_loader.coinbaseloader')
    url = f"https://api.pro.coinbase.com/products/{product}/candles"
    params = {
        "start": start,
        "end": end,
        "granularity": granularity
    }
    logger.debug(f"Запит даних для {product} з {start} до {end} з гранулярністю {granularity}")
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        logger.info(f"Успішно завантажено дані для {product} - {start} до {end}")
        return df
    else:
        logger.error(f"Не вдалося завантажити дані для {product} - {start} до {end}")
        return None

def get_available_products():
    logger = logging.getLogger('crypto_loader.baseloader')
    url = "https://api.pro.coinbase.com/products"
    logger.debug("Запит списку доступних продуктів")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        products = [product['id'] for product in data]
        logger.info("Успішно завантажено список продуктів")
        return products
    else:
        logger.error("Не вдалося завантажити список продуктів")
        return None

products = get_available_products()
if products:
    print("Доступні продукти:", products)
else:
    print("Не вдалося завантажити продукти")

selected_products = ['XTZ-EUR', 'LTC-BTC', 'BTC-USD']
end_date = datetime.now()
start_date_day = end_date - timedelta(days=1)
start_date_month = end_date - timedelta(days=30)
start_date_year = end_date - timedelta(days=365)

dfs = {}
for product in selected_products:
    dfs[product] = {
        'day': get_historical_data(product, start_date_day, end_date, 3600),
        'month': get_historical_data(product, start_date_month, end_date, 86400),
        'year': get_historical_data(product, start_date_year, end_date, 86400 * 30)
    }

fig, axes = plt.subplots(nrows=len(selected_products), ncols=3, figsize=(15, 10))

for i, product in enumerate(selected_products):
    for j, period in enumerate(['day', 'month', 'year']):
        ax = axes[i, j]
        if dfs[product][period] is not None:
            df = dfs[product][period]
            ax.plot(df.index, df['open'], label='Open')
            ax.plot(df.index, df['high'], label='High')
            ax.plot(df.index, df['low'], label='Low')
            ax.plot(df.index, df['close'], label='Close')
            ax.set_title(f'{product} - {period}')
            ax.legend()
        else:
            ax.set_title(f'Немає даних для {product} - {period}')

plt.tight_layout()
plt.show()
