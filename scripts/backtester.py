
# backtester script; genericion de long
import pandas as pd

def longs_backtester(data:pd.DataFrame, signal: pd.Series)  -> pd.DataFrame:

    results = data.copy()

    # position taken rom previous bar's signal
    results["Position"] = signal.shift(1).fillna(0)

    # market return
    results["Market_Return"] = results["Close"].pct_change()

    # strategy return
    results["Strategy_Return"] = (
        results["Position"] * results["Market_Return"]
    )

    # equity cyrve
    results["Equity"] = (
        1 + results["Strategy_Return"]
    ).cumprod()

    return results