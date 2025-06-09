import json
import os
from datetime import datetime, time

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect

from account import get_account_details
from auth import get_user_session
from market_analyzer import scan_once  # ✅ now only TradingView
from order import place_order, fetch_order_book
from risk import calculate_position
from session_manager import save_session, load_saved_session, get_valid_session
from strategy_engine import is_good_entry

load_dotenv()
app = Flask(__name__)

def is_market_open():
    now = datetime.now().time()
    return time(9, 15) <= now <= time(15, 30)

@app.route("/")
def home():
    session_data = load_saved_session()
    return render_template("home.html",
                           session_valid=bool(session_data),
                           session_data=session_data or {},
                           appcode=os.getenv("APP_CODE")
                           )

@app.route("/aliceblue/session", methods=["POST"])
def handle_session():
    try:
        data = request.json
        auth_code = data.get("authCode")
        user_id = data.get("userId")

        session_id = get_user_session(user_id, auth_code)
        save_session(user_id, session_id)

        return {"status": "success", "session_id": session_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


@app.route("/top-picks")
def show_top_picks():
    return render_template("loading.html")  # UI loads, redirects to analyzer


@app.route("/fetch-top-picks")
def fetch_top_picks():
    try:
        print("🔁 Running analyzer on-demand...")
        stocks = scan_once()

        if stocks:
            with open("top_stocks.json", "w") as f:
                json.dump(stocks, f, indent=2)
            print(f"✅ Saved {len(stocks)} trade candidates.")
        else:
            print("⚠️ No suitable trade candidates found.")

        return redirect("/view-top-picks")

    except Exception as e:
        return render_template("result.html", logs=[f"❌ Analyzer Error: {str(e)}"])


@app.route("/view-top-picks")
def view_top_picks():
    try:
        with open("top_stocks.json", "r") as f:
            stocks = json.load(f)
        return render_template("top_picks.html", stocks=stocks)
    except Exception as e:
        print(f"⚠️ Could not load top_stocks.json: {e}")
        return render_template("top_picks.html", stocks=[])


@app.route("/trade-top-picks", methods=["POST"])
def trade_top_picks():
    try:
        user_id, session_id = get_valid_session()

        with open("top_stocks.json", "r") as f:
            stocks = json.load(f)

        logs = []
        for stock in stocks:
            symbol = stock["symbol"]
            price = stock["ltp"]

            if not is_good_entry(symbol):
                logs.append(f"⚠️ {symbol}: Strategy rejected")
                continue

            risk = calculate_position(price)
            if not risk:
                logs.append(f"❌ {symbol}: Capital too low or invalid entry")
                continue

            try:
                place_order(user_id, session_id, symbol, risk["qty"], risk["entry"], "LIMIT")
                status = fetch_order_book(session_id, user_id)
                logs.append(f"✅ {symbol}: Order placed for {risk['qty']} @ ₹{risk['entry']} — {status}")
            except Exception as e:
                logs.append(f"🔴 {symbol}: {str(e)}")

        return render_template("result.html", logs=logs)

    except Exception as e:
        return render_template("result.html", logs=[f"❌ Trade Failed: {str(e)}"])

@app.route("/account-info", methods=["POST"])
def account_info():
    try:
        _, session_id = get_valid_session()
        details = get_account_details(session_id)

        label_map = {
            "accountStatus": "Account Status",
            "dpType": "DP Type",
            "accountId": "Account ID",
            "sBrokerName": "Broker Name",
            "product": "Product Types",
            "accountName": "Account Holder Name",
            "cellAddr": "Mobile Number",
            "emailAddr": "Email",
            "exchEnabled": "Enabled Exchanges",
            "poaStatus": "POA Status"
        }

        items = []
        for key, value in details.items():
            label = label_map.get(key, key.replace("_", " ").title())
            if key == "exchEnabled":
                value = ", ".join(sorted({seg.split("_")[0].upper() for seg in value.split("|") if seg}))
            elif isinstance(value, list):
                value = ", ".join(value)
            items.append((label, value))

        return render_template("account_info.html", items=items)

    except Exception as e:
        return render_template("result.html", logs=[f"❌ Failed to fetch account details: {str(e)}"])

if __name__ == "__main__":
    app.run(debug=True)
