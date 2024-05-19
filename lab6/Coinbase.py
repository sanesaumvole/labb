import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_historical_data(product, start, end, granularity):
    url = f"https://api.pro.coinbase.com/products/{product}/candles"
    params = {
        "start": start,
        "end": end,
        "granularity": granularity
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        return df
    else:
        print(f"Failed to retrieve data for {product} - {start} to {end}")
        return None

def get_available_products():
    url = "https://api.pro.coinbase.com/products"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        products = [product['id'] for product in data]
        return products
    else:
        print("Failed to retrieve products")
        return None

products = get_available_products()
print("Available products:", products)
selected_products = ['BTC-USD', 'ETH-USD', 'XRP-USD']
end_date = datetime.now()
start_date_week = end_date - timedelta(days=7)
start_date_month = end_date - timedelta(days=90)
start_date_year = end_date - timedelta(days=365)

dfs = {}
for product in selected_products:
    dfs[product] = {
        'week': get_historical_data(product, start_date_week, end_date, 3600),
        'month': get_historical_data(product, start_date_month, end_date, 86400),
        'year': get_historical_data(product, start_date_year, end_date, 86400 * 30)
    }

fig, axes = plt.subplots(nrows=len(selected_products), ncols=3, figsize=(15, 10))

for i, product in enumerate(selected_products):
    for j, period in enumerate(['week', 'month', 'year']):
        ax = axes[i, j]
        if dfs[product][period] is not None:
            df = dfs[product][period]
            ax.plot(df.index, df['close'], label='Close')
            ax.set_title(f'{product} - {period}')
            ax.legend()
        else:
            ax.set_title(f'No data available for {product} - {period}')

plt.tight_layout()
plt.show()
