import requests
import urllib3

# Disable HTTPS warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===== CML SETTINGS =====
CML_IP = "192.168.1.101"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb20uY2lzY28udmlybCIsInN1YiI6IjAwMDAwMDAwLTAwMDAtNDAwMC1hMDAwLTAwMDAwMDAwMDAwMCIsImV4cCI6MTc2MDI2MzY5MSwiaWF0IjoxNzYwMTc3MjkxLCJqdGkiOiI5NzBmMTcwMi1hNzU5LTRhZjYtYmFkYi05MmM3MGU1NGY3MmMifQ.exsMXRxrgwOWDFC5AY_2ARWsxb_nil-CK6CXMg2nZMQ"

# Build headers for all API calls
headers = {"Authorization": f"Bearer {TOKEN}"}

# ===== GET ALL LABS =====
labs = requests.get(f"https://{CML_IP}/api/v0/labs", headers=headers, verify=False).json()
print("Labs found:", labs)

# ===== LOOP THROUGH LABS AND GET NODE INFO =====
for lab_id in labs:
    print(f"\n=== LAB {lab_id} ===")

    # Get all nodes in each lab
    nodes = requests.get(f"https://{CML_IP}/api/v0/labs/{lab_id}/nodes", headers=headers, verify=False).json()

    for node_id in nodes:
        node_info = requests.get(
            f"https://{CML_IP}/api/v0/labs/{lab_id}/nodes/{node_id}",
            headers=headers,
            verify=False
        ).json()

        print(f"\nDevice: {node_info['label']}")
        print("Type:", node_info['node_definition'])
        print("State:", node_info['state'])
        print("Interfaces:", [i['label'] for i in node_info['interfaces']])

        # ===== GET DEVICE CONFIGURATION =====
        config = requests.get(
            f"https://{CML_IP}/api/v0/labs/{lab_id}/nodes/{node_id}/config",
            headers=headers,
            verify=False
        ).text

        print("\nConfiguration:")
        print(config)
        print("-" * 60)
