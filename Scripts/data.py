
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