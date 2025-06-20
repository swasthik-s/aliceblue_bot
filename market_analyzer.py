import pandas as pd
import requests
import time
import matplotlib.pyplot as plt
from datetime import datetime

TARGET_SYMBOL = "NIFTY"
OPTION_TYPE = "CE"
EXCHANGE = "NFO"
LOT_SIZE = 50  # For NIFTY

# 🧠 Convert human date to UNIX timestamp in milliseconds
def to_unix_millis(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(time.mktime(dt.timetuple()) * 1000)

# 🛰️ Fetch historical option data from AliceBlue AI Chart API
def fetch_historical_data(token, from_date, to_date, resolution="D"):
    url = "https://ant.aliceblueonline.com/rest/AliceBlueAPIService/chart/history"
    payload = {
        "token": str(token),
        "resolution": resolution,
        "from": str(to_unix_millis(from_date)),
        "to": str(to_unix_millis(to_date)),
        "exchange": EXCHANGE
    }
    res = requests.post(url, json=payload)
    data = res.json()
    if data.get("stat") != "Ok":
        raise Exception(f"Failed to fetch: {data.get('emsg')}")
    return pd.DataFrame(data['result'])

# 💹 Backtest butterfly strategy on downloaded data
def run_butterfly_backtest(df, lower_strike, atm_strike, upper_strike):
    if df.empty:
        print("⚠️ No data to backtest.")
        return

    net_cost = df['close'].iloc[-1]  # Assume today's premium as cost
    payoff = max(0, atm_strike - lower_strike) - 2 * max(0, atm_strike - atm_strike) + max(0, atm_strike - upper_strike)
    capital = 25000
    lots = 1
    total_cost = net_cost * LOT_SIZE * lots
    total_payoff = payoff * LOT_SIZE * lots
    pnl = total_payoff - total_cost

    print("\n📊 Butterfly Strategy Result")
    print(f"Strikes: {lower_strike}-{atm_strike}-{upper_strike}")
    print(f"Net Cost: ₹{net_cost:.2f} | Payoff: ₹{payoff:.2f} | PnL: ₹{pnl:.2f}")

    return {
        "Strikes": f"{lower_strike}-{atm_strike}-{upper_strike}",
        "Cost": net_cost,
        "Payoff": payoff,
        "PnL": pnl
    }

# --- Main Example Usage ---
# 📌 You should replace 'token' with correct option token from contract master
option_token = 123456  # Placeholder
from_date = "2024-06-01"
to_date = "2024-06-30"

try:
    hist_df = fetch_historical_data(option_token, from_date, to_date)
    print("✅ Fetched historical data:")
    print(hist_df.head())

    result = run_butterfly_backtest(hist_df, 24500, 24750, 25000)
except Exception as e:
    print(f"❌ Error: {e}")
