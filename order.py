import requests

def place_order(user_id: str, session_token: str):
    url = "https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/placeOrder/executePlaceOrder"

    # ✅ Correctly formatted Bearer token
    headers = {
        "Authorization": f"Bearer {user_id} {session_token}",
        "Content-Type": "application/json"
    }

    order_payload = [
        {
            "complexty": "regular",
            "discqty": "0",
            "exch": "NSE",
            "pCode": "mis",
            "prctyp": "L",             # Use "MKT" for market order
            "price": "100",
            "qty": 1,
            "ret": "DAY",
            "symbol_id": "212",
            "trading_symbol": "ASHOKLEY-EQ",
            "transtype": "BUY",
            "trigPrice": ""
        }
    ]

    print("📤 Sending order:", order_payload)
    print("🔑 Header:", headers)

    response = requests.post(url, json=order_payload, headers=headers)
    print("🔁 Order Response:", response.text)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"❌ Order failed: {response.text}")

def fetch_order_book(session_id: str, user_id: str) -> str:
    url = "https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/placeOrder/fetchOrderBook"
    headers = {
        "Authorization": f"Bearer {user_id} {session_id}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            orders = response.json()

            # Sort orders by order time (latest first)
            orders.sort(key=lambda o: o.get("OrderedTime", ""), reverse=True)
            latest = orders[0]

            status = latest.get("Status", "").lower()
            if status == "rejected":
                return f"❌ Order Rejected: {latest.get('RejReason', 'Unknown reason')}"
            elif status == "completed":
                return f"✅ Order Completed @ ₹{latest.get('Avgprc', '0.00')}"
            else:
                return f"📤 Order Status: {status.capitalize()}"
        else:
            return f"❌ Could not fetch order book (HTTP {response.status_code})"
    except Exception as e:
        return f"❌ Order book fetch failed: {str(e)}"

