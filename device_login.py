import requests

CML_IP = "192.168.0.34"
USER = "admin"
PASSWORD = "CMLpassword"

# Authenticate
auth = requests.post(f"https://{CML_IP}/api/v0/authenticate", verify=False, auth=(USER, PASSWORD))
token = auth.json()["token"]

headers = {"Authorization": f"Bearer {token}"}

# Get labs
labs = requests.get(f"https://{CML_IP}/api/v0/labs", headers=headers, verify=False).json()

for lab_id in labs:
    nodes = requests.get(f"https://{CML_IP}/api/v0/labs/{lab_id}/nodes", headers=headers, verify=False).json()
    for node_id in nodes:
        config = requests.get(f"https://{CML_IP}/api/v0/labs/{lab_id}/nodes/{node_id}/config", headers=headers, verify=False).text
        print(f"Node {node_id} config:\n{config}\n{'-'*50}")
