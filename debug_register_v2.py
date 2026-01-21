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

# Create duplicate
status, body = register("debuguser", "password123")

print(f"Status: {status}")
print(f"Body: {body}")

with open('last_error.json', 'w', encoding='utf-8') as f:
    f.write(body)
