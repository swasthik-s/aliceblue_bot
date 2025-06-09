import json
from datetime import datetime

from tradingview_ta import TA_Handler, Interval

# ✅ Predefined top NSE stocks (can be replaced with dynamic in future)
NSE_TOP_25 = [
    "RELIANCE", "TCS", "INFY", "SBIN", "HDFCBANK", "ICICIBANK", "AXISBANK",
    "ITC", "LT", "ADANIENT", "WIPRO", "HCLTECH", "SUNPHARMA", "TECHM",
    "TATAMOTORS", "MARUTI", "POWERGRID", "COALINDIA", "TITAN", "ONGC",
    "NTPC", "BAJFINANCE", "HINDUNILVR", "BHARTIARTL", "ULTRACEMCO"
]


def fetch_indicators_from_tv(symbols):
    picks = []

    for symbol in symbols:
        try:
            handler = TA_Handler(
                symbol=symbol,
                screener="india",  # ✅ Use India screener
                exchange="NSE",  # ✅ Ensure NSE exchange
                interval=Interval.INTERVAL_1_HOUR
            )

            analysis = handler.get_analysis()
            reco = analysis.summary.get("RECOMMENDATION", "NEUTRAL")

            if reco not in ["BUY", "STRONG_BUY"]:
                continue

            indicators = analysis.indicators

            picks.append({
                "symbol": symbol,
                "ltp": round(indicators.get("close", 0), 2),
                "rsi": round(indicators.get("RSI", 0), 2),
                "macd": round(indicators.get("MACD.macd", 0), 2),
                "signal": round(indicators.get("MACD.signal", 0), 2),
                "recommendation": reco,
                "timestamp": datetime.now().strftime("%H:%M")
            })

        except Exception as e:
            print(f"⚠️ Skipped {symbol}: {e}")
            continue

    print(f"✅ Final NSE trade candidates: {len(picks)}")
    return picks


def scan_once():
    print("🔁 Running NSE-based TradingView Analyzer...")

    picks = fetch_indicators_from_tv(NSE_TOP_25)

    if picks:
        with open("top_stocks.json", "w") as f:
            json.dump(picks, f, indent=2)
        print(f"📁 Saved {len(picks)} picks to top_stocks.json")
    else:
        print("⚠️ No BUY/STRONG_BUY candidates found.")

    return picks


if __name__ == "__main__":
    scan_once()
