import urllib.request
import json
import urllib.error

BASE_URL = "http://127.0.0.1:8000/api"

def register(username, password):
    url = f"{BASE_URL}/register/"
    data = json.dumps({"username": username, "password": password}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

# 1. Create user
print("--- Attempt 1: Create 'debuguser' ---")
status1, body1 = register("debuguser", "password123")
print(f"Status: {status1}")
print(f"Body: {body1}")

# 2. Create duplicate
print("\n--- Attempt 2: Create 'debuguser' (Duplicate) ---")
status2, body2 = register("debuguser", "password123")
print(f"Status: {status2}")
print(f"Body: {body2}")
print("---------------------------------------")
