import requests
import urllib3

# Disable HTTPS warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CML_IP = "192.168.1.101"
USER = "cratiflab"
PASSWORD = "adeola01"

# Authenticate
auth_url = f"https://{CML_IP}/api/v0/authenticate"
payload = {"username": USER, "password": PASSWORD}

auth = requests.post(auth_url, json=payload, verify=False)

# Debug check
print("Auth status code:", auth.status_code)
print("Auth response:", auth.text)

# Handle failed login gracefully
if "token" not in auth.json():
    print("Authentication failed! Response:", auth.text)
    exit()

token = auth.json()["token"]
headers = {"Authorization": f"Bearer {token}"}

# Get labs
labs = requests.get(f"https://{CML_IP}/api/v0/labs", headers=headers, verify=False).json()

for lab_id in labs:
    nodes = requests.get(f"https://{CML_IP}/api/v0/labs/{lab_id}/nodes", headers=headers, verify=False).json()
    for node_id in nodes:
        config = requests.get(
            f"https://{CML_IP}/api/v0/labs/{lab_id}/nodes/{node_id}/config",
            headers=headers,
            verify=False
        ).text
        print(f"Node {node_id} config:\n{config}\n{'-'*50}")
