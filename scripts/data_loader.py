
# download data from yfinance script

import os
from pathlib import Path

import requests
import yfinance as yf
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

TWELVE_DATA_KEY = os.getenv("TWELVE_DATA_API")
TWELVE_DATA_URL = os.getenv("TWELVE_URL")


# downloading the data: yahoo finance block
def yfinance_data(ticker, start, end, interval):
    data = yf.download(
        ticker,
        start = start,
        end = end,
        interval = interval,
        auto_adjust = False,
        actions = True,
        progress = False
    )

    if data.empty:
        raise ValueError(
            f"[-] no yahoo finace data returned"
        )

    return data

# downloading data: twelve data downloader
def twelve_data(ticker, start, end, interval):

    if not TWELVE_DATA_KEY:
        raise ValueError(
            "[-] missing twelve data api key in the .env file"
        )

    # interval map
    interval_map = {
        "1m": "1min",
        "5m": "5min",
        "15m": "15min",
        "30m": "30min",
        "45m": "45min",
        "1h": "1h",
        "2h": "2h",
        "4h": "4h",
        "8h": "8h",
        "1d": "1day",
        "1D": "1day",
        "1day": "1day",
        "1wk": "1week",
        "1mo": "1month",
    }
    td_interval= interval_map.get(interval, interval)

    symbol = ticker.replace("-", "/").upper()
    params = {
        "symbol": symbol,
        "interval": td_interval,
        "start_date": start,
        "end_date": end,
        "timezone": "UTC",
        "order": "asc",
        "apikey": TWELVE_DATA_KEY,
    }

    response = requests.get(
        TWELVE_DATA_URL,
        params = params,
        timeout = 30
    )
    response.raise_for_status()

    result = response.json()

    if "values" not in result:
        raise RuntimeError(
            f"[ERROR] twelve data API error: {result}"
        )

    data = pd.DataFrame(result["values"])
    if data.empty:
        raise ValueError(
            f"[ERROR] no twelve data records returned for {symbol}"
        )

    # parsee timestamps as utc
    data["datetime"] = pd.to_datetime(
        data["datetime"],
        utc = True,
        errors = "raise"
    )
    data = data.set_index("datetime")
    data.index_name = "Date"

    # prices and volumes to numerics
    for column in ["open", "high", "low", "close", "volume"]:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors = "raise"
            )

    
    # matching columns names expected by data cleaener
    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )

    return data.sort_index()

def download_data(ticker, start, end, interval, provider):

    provider = provider.strip().lower()

    if provider == "yfinance":
        return yfinance_data(
            ticker, start, end, interval
        )
    
    elif provider == "twelvedata":
        return twelve_data(
            ticker, start, end, interval
        )

    else:
        raise ValueError(
            "[ERROR] provider must be [yfinance] or [twelvedata]"
        )



# data cleanup
def clean_data(data):

    data = data.copy()

    #  removing column-axis name
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data.columns.name = None

    data.index = pd.to_datetime(data.index)
    data.index.name = "Date"

    required_columns = ["Open", "High", "Low", "Close"]

    missing = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"[ERROR] missing required columns: {missing}"
        )

    # volume unavailbale in some vendors
    if "Volume" not in data.columns:
        data["Volume"] = float("nan")

    # ohlcv configuration
    data = data[
        [   
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]
    ]

    # removing ibalids
    data = data.dropna(
        subset = [
            "Open",
            "High",
            "Low",
            "Close"
        ]
    )

    # duplicate time stamps
    data = data[
        ~data.index.duplicated(keep="last")
    ]

    return data.sort_index()

# saving the data
def save_data_locally(data, path, ticker):

    output_dir = Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = ticker.replace("/", "-").replace("\\", "_")
    output_file = output_dir / f"{filename}.csv"

    data.to_csv(output_file)

    print(
        f"[+] data saved to: {output_file}"
    )

def main():

    print("<===== DATA LOADER INITIALIZED ...... =====>")

    provider = input(
        "[+] choose provider (tfinance/twelvedata): "
    ).strip().lower()

    ticker = input("enter ticker/symbol: ").strip()
    start = input("enter start date (YYYY-MM-DD): ").strip()
    end = input("enter your end date (YYYY-MM-DD): ").strip()
    interval = input("enter interval (example. 1h, 1d, 15m): ").strip()

    # downloading data
    try:
        data = download_data(
            ticker = ticker,
            start = start,
            end = end,
            interval = interval,
            provider = provider
        )

        print(f"{ticker} raw data shape: {data.shape}\n")
        print(f"raw data head(5): \n {data.head()}\n\n")

        # cleaned data
        cleaned_data = clean_data(data)
        print(f"{ticker} cleaned data shape: {cleaned_data.shape}\n")
        print(f"cleaned data head(5): \n {cleaned_data.head()}")

        # saving the cleaned data
        save_choice = input("\n\nwould you like to save the data locally: (yes[y]/no[n]): ").strip().lower()
        if save_choice in ["yes", "y"]:

            path = input("enter the path to save: ").strip()
            save_data_locally(
                cleaned_data,
                path,
                ticker
            )

        else:
            print("[-] data not saved!")

    except (
        ValueError,
        RuntimeError,
        requests.RequestException
    ) as e:
        print(
            f"\n[ERROR] data loader error: {e}"
        )


if __name__ == "__main__":
    main()