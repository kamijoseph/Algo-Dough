
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
    data.index = pd.to_datetime(data.index)
    data.index.name = "Date"
    data = data.reset_index()

    # ohlcv configuration
    data = data[
        [   
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]
    ]

    return data

# saving the data
def save_data_locally(data, location, ticker):
    data.to_csv(f"{location}/{ticker}.csv")

def main():

    print("<===== DATA LOADER INITIALIZED ...... =====>")

    ticker = input("enter ticker: ")
    start = input("enter start date (format: '2025-08-30'): ")
    end = input("enter your end. (format: '2026-09-30'): ")
    interval = input("enter interval. (format: '1D): ")

    # downloading data
    data = download_data(
        ticker = ticker,
        start = start,
        end = end,
        interval = interval
    )

    print(f"{ticker} raw data shape: {data.shape}\n")
    print(f"raw data head(5): \n {data.head()}\n\n")

    # cleaned data
    cleaned_data = clean_data(data)
    print(f"{ticker} cleaned data shape: {cleaned_data.shape}\n")
    print(f"cleaned data head(5): \n {cleaned_data.head()}")

    # saving the cleaned data
    save_data = input("would you like to save the data locally: (yesy/no): ")
    if save_data == "yes":
        save_data_locally(cleaned_data)
    else:
        print("data not saved!")


if __name__ == "__main__":
    main()