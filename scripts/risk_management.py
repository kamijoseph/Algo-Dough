
# count pips
def pips_calculator(
        entry: float,
        exit: float,
        pip_size: float
) -> float:

    if pip_size <= 0:
        raise ValueError("pip size must be greater than zero")

    return (exit - entry) / pip_size

# kamis risk management
def kamis_risk(
        current_equity: float,
        base_risk_pct: float,
        loss_streak: int,
        rr_ratio: float = 2.0,
        max_consq_losses: int = 3
) -> dict:

    # validation
    if current_equity <= 0:
        raise ValueError("current equity must be greater zero brokie")

    if base_risk_pct <= 0:
        raise ValueError("base risk management must be greater than zero")

    if loss_streak < 0:
        raise ValueError("loss streak cannot be negative")

    if rr_ratio <= 0:
        raise ValueError("risk to reward ratio must be greater than zero")

    if max_consq_losses <= 0:
        raise ValueError("max consecutive losses must be greater than zero")

    # stop trading after maximum consecutive losses
    if loss_streak >= max_consq_losses:

        return {
            "trading_allowed": False,
            "loss_streak": loss_streak,
            "risk_percentage": 0.0,
            "risk_amount": 0.0,
            "reward_amount": 0.0,
            "rr_ratio": rr_ratio,
        }

    # risk reduction by n / 2, n / 4
    risk_pct = base_risk_pct / (2 ** loss_streak)
    risk_amount = current_equity * (risk_pct / 100)
    reward_amount = risk_amount * rr_ratio

    return {
        "trading_allowed": True,
        "loss_streak": loss_streak,
        "risk_percentage": risk_pct,
        "risk_amount": risk_amount,
        "reward_amount": reward_amount,
        "rr_ratio": rr_ratio,
    }