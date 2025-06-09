import json
import os
import time

SESSION_FILE = os.path.join(os.path.dirname(__file__), "session_store.json")

def save_session(user_id, session_id):
    data = {
        "user_id": user_id,
        "session_id": session_id,
        "timestamp": time.time()
    }
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(data, f)
        print("✅ Session saved to", SESSION_FILE)
    except Exception as e:
        print("❌ Failed to save session:", e)

def load_saved_session():
    if not os.path.exists(SESSION_FILE):
        print("❌ session_store.json not found")
        return None

    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
        if time.time() - data.get("timestamp", 0) < 23 * 3600:
            return data
        else:
            print("⚠️ Session expired")
    except Exception as e:
        print("❌ Error reading session:", e)

    return None

def get_valid_session():
    data = load_saved_session()
    if data:
        return data["user_id"], data["session_id"]
    raise Exception("🛑 Session expired or missing. Login required.")
