from flask import Flask, request, jsonify, render_template_string
import os
from dotenv import load_dotenv
from auth import get_user_session
from session_manager import save_session, load_saved_session, get_valid_session
from order import place_order, fetch_order_book
from account import get_account_details
from datetime import datetime, time


load_dotenv()

app = Flask(__name__)

def is_market_open():
    now = datetime.now().time()
    # NSE equity market timing: 9:15 AM to 3:30 PM
    return time(9, 15) <= now <= time(15, 30)

@app.route("/")
def home():
    session_data = load_saved_session()
    session_valid = bool(session_data)

    return render_template_string("""
        <html>
        <head><title>AliceBlue Trading Bot</title></head>
        <body style="font-family:sans-serif; padding:30px;">
            <h2>💹 <b>AliceBlue Trading Bot</b></h2>
            {% if session_valid %}
                <p style="color:green;">✅ Session is active for <b>User ID: {{ session_data.user_id }}</b></p>
                <form method="post" action="/trade-now">
                    <button type="submit" style="padding:10px 20px; font-size:16px;">🚀 Place Order</button>
                </form>
                <form method="post" action="/account-info">
                    <button type="submit" style="margin-top: 15px; padding:10px 20px;">👤 Get Account Details</button>
                </form>
            {% else %}
                <p style="color:red;">❌ No active session.</p>
                <form method="get" action="https://ant.aliceblueonline.com/">
                    <input type="hidden" name="appcode" value="{{ appcode }}">
                    <button type="submit" style="padding:10px 20px; font-size:16px;">🔐 Authorize via AliceBlue</button>
                </form>
                
            {% endif %}
        </body>
        </html>
    """, session_valid=session_valid, session_data=session_data or {}, appcode=os.getenv("APP_CODE"))

@app.route("/aliceblue/session", methods=["POST"])
def handle_session():
    try:
        data = request.json
        print("🔵 Received POST /aliceblue/session:", data)

        auth_code = data.get("authCode")
        user_id = data.get("userId")

        session_id = get_user_session(user_id, auth_code)
        save_session(user_id, session_id)

        return jsonify({"status": "success", "session_id": session_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/trade-now", methods=["POST"])
def trade_now():
    if not is_market_open():
        return f"<h3>❌ Market is currently closed. Trades allowed only between 9:15 AM – 3:30 PM.</h3><br><a href='/'>⬅ Back to Home</a>"
    try:
        user_id, session_id = get_valid_session()

        # Step 1: Place the order
        place_order(user_id, session_id)

        # Step 2: Immediately fetch the latest order book
        result = fetch_order_book(session_id, user_id)

        return f"""
        <html><body style='font-family:sans-serif;padding:30px;'>
            <h3>📊 Trade Status</h3>
            <p>{result}</p>
            <br><a href='/'>⬅ Back to Home</a>
        </body></html>
        """
    except Exception as e:
        return f"""
        <html><body style='font-family:sans-serif;padding:30px;'>
            <h3>❌ Trade Failed</h3>
            <p>{str(e)}</p>
            <br><a href='/'>⬅ Back to Home</a>
        </body></html>
        """, 500



@app.route("/account-info", methods=["POST"])
def account_info():
    try:
        _, session_id = get_valid_session()
        details = get_account_details(session_id)

        # 🔤 Mapping of raw keys to pretty labels
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

        html = """
        <html>
        <head>
            <style>
                body { font-family: sans-serif; padding: 20px; }
                table { border-collapse: collapse; width: 60%; margin-top: 20px; }
                th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
                th { background-color: #f2f2f2; }
                caption { text-align: left; font-size: 1.2rem; font-weight: bold; margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <h2>👤 Account Details</h2>
            <table>
                <caption>Profile Information</caption>
                <thead>
                    <tr><th>Field</th><th>Value</th></tr>
                </thead>
                <tbody>
        """

        for key, value in details.items():
            label = label_map.get(key, key.replace("_", " ").title())
            # Special handling for exchEnabled
            if key == "exchEnabled":
                exchanges = [seg.split("_")[0].upper() for seg in value.split("|") if seg]
                value_display = ", ".join(sorted(set(exchanges)))
            elif isinstance(value, list):
                value_display = ", ".join(value)
            else:
                value_display = value
            html += f"<tr><td><b>{label}</b></td><td>{value_display}</td></tr>"

        html += """
                </tbody>
            </table>
            <br><a href='/'>⬅ Back to Home</a>
        </body>
        </html>
        """

        return html
    except Exception as e:
        return f"❌ Failed to fetch account details: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
