
# perfomance metrics
import pandas as pd
import numpy as np

def perfomance_metrics(results: pd.DataFrame) -> pd.Series:

    returns = results["Strategy_Return"].dropna()
    total_return = results["Equity"].iloc[-1] - 1

    years = (
        results.index[-1] - results.index[0]
    ).days / 365.25

    cagr = (
        results["Equity"].iloc[-1] ** (1 / years)
    ) - 1

    volatility = returns.std() * np.sqrt(252)
    sharpe = (
        returns.mean() / returns.std()
    ) * np.sqrt(252)

    running_max = results["Equity"].cummax()
    drawdown = (
        results["Equity"] / running_max
    ) - 1
    max_drawdown = drawdown.min()

    return pd.Series(
        {
            "Total Return": total_return,
            "CAGR": cagr,
            "Annualized volatility": volatility,
            "Sharpe": sharpe,
            "Max Drawdown": max_drawdown
        }
    )