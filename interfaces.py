import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ====== CML SETTINGS ======
CML_IP = "192.168.1.101"
USERNAME = "cratiflab"
PASSWORD = "adeola01"
LAB_ID = "8be2580b-79de-40b5-a180-78a32fdb01ec"

# ====== TRY AUTHENTICATION ======
auth_endpoints = [
    f"https://{CML_IP}/api/v0/authenticate",      # CML 2.4+
    f"https://{CML_IP}/api/v0/login"              # CML 2.2 or earlier
]

token = None
for url in auth_endpoints:
    print(f"Trying {url} ...")
    resp = requests.post(url, json={"username": USERNAME, "password": PASSWORD}, verify=False)
    if resp.status_code == 200 and len(resp.text.strip()) > 10:
        token = resp.text.strip()
        print("✅ Authenticated successfully")
        break
    else:
        print(f"❌ {resp.status_code}: {resp.text}")

if not token:
    raise SystemExit("Authentication failed — check CML version or credentials.")

headers = {"Authorization": f"Bearer {token}"}

# ====== GET INTERFACES ======
interfaces_url = f"https://{CML_IP}/api/v0/labs/{LAB_ID}/interfaces"
response = requests.get(interfaces_url, headers=headers, verify=False)

if response.status_code == 200:
    interfaces = response.json()
    print(json.dumps(interfaces, indent=2))
else:
    print(f"Error {response.status_code}: {response.text}")
