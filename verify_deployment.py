import urllib.request
import json
import urllib.error

BASE_URL = "http://127.0.0.1:8000/api"

def request(method, endpoint, data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Token {token}'
    
    encoded_data = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                return None
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()}")
        return None

def run_verification():
    print("1. Registering User...")
    user_data = {"username": "api_tester", "password": "password123", "email": "tester@example.com"}
    reg_resp = request("POST", "/register/", user_data)
    if not reg_resp and "username" not in str(reg_resp): # Might fail if user exists
        print("User might already exist, trying login...")

    print("\n2. Logging in...")
    login_data = {"username": "api_tester", "password": "password123"}
    auth_resp = request("POST", "/login/", login_data)
    
    if not auth_resp or 'token' not in auth_resp:
        print("Login Failed!")
        return
    
    token = auth_resp['token']
    print(f"Success! Token: {token[:10]}...")

    print("\n3. Creating Task...")
    task_data = {
        "title": "Test Task",
        "due_date": "2026-01-25",
        "reminder_time": "2026-01-25T10:00:00Z"
    }
    task_resp = request("POST", "/tasks/", task_data, token)
    if task_resp:
        print(f"Task Created: {task_resp.get('title')}")
    else:
        print("Task Creation Failed")

    print("\n4. Checking Calendar View...")
    calendar_resp = request("GET", "/tasks/calendar/", token=token)
    if calendar_resp:
        print("Calendar Response:")
        print(json.dumps(calendar_resp, indent=2))
        if "2026-01-25" in calendar_resp:
            print("Verification PASSED: Task found in calendar.")
        else:
            print("Verification FAILED: Task not found in calendar.")
    else:
        print("Calendar View Failed")

if __name__ == "__main__":
    run_verification()
