import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt

def load_history_data(fname: str) -> np.ndarray:
    from_strdate = lambda x: datetime.strptime(x.strip('"'), '%m/%d/%Y')
    from_strnum = lambda x: float(x.strip('"'))
    from_strnumm = lambda x: float(x.strip('"').strip('M'))*1_000_000
    from_strpcnt = lambda x: float((x.strip('"').strip('%')))/100
    names=("date", "price", "open", "high", "low", "volume", "change")
    data = np.genfromtxt(fname, delimiter=",", encoding="utf-8", skip_header=1, names=names,
                         dtype=[("date", datetime),
                                ("price", np.float64),
                                ("open", np.float64),
                                ("high", np.float64),
                                ("low", np.float64),
                                ("volume", np.float64),
                                ("change", np.float64)],
                         converters={
                             "date": from_strdate,
                             "price": from_strnum,
                             "open": from_strnum,
                             "high": from_strnum,
                             "low": from_strnum,
                             "volume": from_strnumm,
                             "change": from_strpcnt})
    return data

def plot_price_subplot(data: np.ndarray, title: str, ax) -> None:
    date = data['date']
    price = data['price']
    ax.plot(date, price)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')

def main() -> None:
    # Load data for each asset
    assets = ['MSFT','R', 'TSLA']
    data_files = [ 'C:\\Users\\userPC\\Desktop\\data\\MSFT Historical Data.csv',
                  'C:\\Users\\userPC\\Desktop\\data\\R Historical Data.csv',
                  'C:\\Users\\userPC\\Desktop\\data\\TSLA Historical Data.csv']
    data = [load_history_data(fname) for fname in data_files]

    # Plot price for each asset on separate subplot
    fig, axes = plt.subplots(len(assets), 1, figsize=(10, 6 * len(assets)))
    for idx, asset_data in enumerate(data):
        plot_price_subplot(asset_data, assets[idx], axes[idx])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
