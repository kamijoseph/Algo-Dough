
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
        base_risk_management: float,
        loss_streak: int,
        rr_ratio: float = 2.0,
        max_consq_loss: int = 3
) -> dict:
    pass
