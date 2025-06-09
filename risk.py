def calculate_position(entry_price: float, capital: float = 500.0):
    """
    Calculate quantity, TP, SL based on ₹10 target, ₹5 stoploss.
    Ensures capital is not exceeded.
    """
    target = entry_price + 10
    stoploss = entry_price - 5

    # Round to 1 rupee precision (safety buffer)
    qty = int(capital // entry_price)

    # Ensure at least 1 quantity and proper bounds
    if qty < 1 or stoploss < 1:
        return None

    return {
        "entry": round(entry_price, 2),
        "qty": qty,
        "target": round(target, 2),
        "stoploss": round(stoploss, 2),
        "total_cost": round(qty * entry_price, 2),
        "risk_per_trade": round(qty * 5, 2),
        "reward_per_trade": round(qty * 10, 2)
    }
