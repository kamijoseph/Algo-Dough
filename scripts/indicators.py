
# indicators scripts
def moving_averages(data):

    # sma 20
    data["SMA_20"] = data["Close"].rolling(20).mean()

    # sma 50
    data["SMA_50"] = data["Close"].rolling(50).mean()

    # sma 200
    data["SMA_200"] = data["Close"].rolling(200).mean()

    # ema 20
    data["EMA_20"] = data["Close"].ewm(
        span = 20,
        adjust = False
    ).mean()

    data["EMA_50"] = data["Close"].ewm(
            span = 50,
            adjust = False
        ).mean()

    return data