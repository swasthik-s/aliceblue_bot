# strategy_engine.py
def is_good_entry(symbol, data):
    # Sample logic: combo of SMA, RSI and MACD
    if data['RSI'] < 30 and data['MACD_CROSS'] == 'BULL' and data['Price'] > data['SMA20']:
        return True
    return False
