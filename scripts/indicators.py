
# indicators scripts
import pandas as pd


def simple_moving_averages(data: pd.DataFrame):

    sma_20 = data["Close"].rolling(20).mean()
    sma_50 = data["Close"].rolling(50).mean()
    sma_200 = data["Close"].rolling(200).mean()

    return sma_20, sma_50, sma_200

def exponential_moving_averages(data: pd.DataFrame):
        
    ema_20 = data["Close"].ewm(
        span = 20,
        adjust = False
    ).mean()

    ema_50 = data["Close"].ewm(
            span = 50,
            adjust = False
        ).mean()

    return ema_20, ema_50

# bollinger bands
def bollinger_bands(data: pd.DataFrame) -> int:

    bb_middle = data["Close"].rolling(20).mean()
    bb_std = data["Close"].rolling(20).std()
    bb_upper = (
        bb_middle + 2 * bb_std
    )
    bb_lower = (
        bb_middle - 2 * bb_std
    )

    return bb_middle, bb_upper, bb_lower

# macd
def macd(data: pd.DataFrame) -> int:

    ema_12 = data["Close"].ewm(
        span = 12,
        adjust = False
    ).mean()

    ema_26 = data["close"].ewm(
        span = 26,
        adjust = False
    ).mean()

    macd = ema_12 - ema_26
    macd_signal = macd.ewm(
        span = 9,
        adjust = False
    )
    macd_hist = macd - macd_signal

    return macd, macd_signal, macd_hist

# relative strength index
def rsi(data: pd.DataFrame):

    delta = data["Close"].diff()

    gain = delta.clip(lower = 0)
    loss = delta.clip(upper = 0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # comments from past kami: 
    # when plotting add reference levekls, preffarably 30 and 70
    # pd.Series(30, index=data.index)
    #  you will need them as visual reference levels

    return rsi

# average true range
def atr(data: pd.DataFrame):

    previous_close = data["Close"].shift(1)

    tr1 = data["High"] - data["Low"]
    tr2 = (data["High"] - previous_close).abs()
    tr3 = (data["Low"] - previous_close).abs()

    true_range = pd.concat(
        [tr1, tr2, tr3],
        axis = 1,
    ).max(axis = 1)

    atr_14 = true_range.rolling(14).mean()

    return atr_14