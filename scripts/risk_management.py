
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
def kamis_risk():
    pass
