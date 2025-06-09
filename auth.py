import hashlib
import requests
import os

def get_user_session(user_id, auth_code):
    api_secret = os.getenv("API_SECRET")

    raw = user_id + auth_code + api_secret
    checksum = hashlib.sha256(raw.encode()).hexdigest()

    response = requests.post(
        "https://ant.aliceblueonline.com/rest/AliceBlueAPIService/sso/getUserDetails",
        json={"checkSum": checksum}
    )

    data = response.json()
    if data.get("stat") == "Ok":
        return data.get("userSession")
    else:
        raise Exception(f"SSO Failed: {data}")
