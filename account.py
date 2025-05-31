import requests

def get_account_details(session_token: str):
    url = "https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/customer/accountDetails"

    headers = {
        "Authorization": f"Bearer {session_token.strip()}",
        "Content-Type": "application/json"
    }

    print("🔐 Header Preview:", headers)

    response = requests.get(url, headers=headers)  # ✅ USE GET here
    print("🔁 Status Code:", response.status_code)
    print("🔁 Headers:", response.headers)
    print("🔁 Body:", response.text)

    if response.status_code == 200 and response.text.strip():
        return response.json()
    else:
        raise Exception(f"❌ Failed to fetch account details: {response.status_code} {response.text}")
