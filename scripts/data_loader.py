
# download data from yfinance script

import yfinance as yf
import pandas as pd


# downloading the data
def download_data(ticker, start, end, interval):
    data = yf.download(
        ticker,
        start = start,
        end = end,
        interval = interval,
        auto_adjust = False,
        actions = True
    )

    return data

# data cleanup
def clean_data(data):

    #  removing column-axis name
    data.columns = data.columns.get_level_values(0)
    data.columns.name = None
    data = data.reset_index()

    # ohlcv configuration
    data = data[
        [
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
            "Dividends",
            "Stock Splits"
        ]
    ]

    return data

# saving the data
def save_data_locally(data, location, ticker):
    data.to_csv(f"{location}/{ticker}.csv")