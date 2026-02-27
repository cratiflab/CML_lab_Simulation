import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CML_IP = "192.168.0.34"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb20uY2lzY28udmlybCIsInN1YiI6IjAwMDAwMDAwLTAwMDAtNDAwMC1hMDAwLTAwMDAwMDAwMDAwMCIsImV4cCI6MTc2MDA4Njg2NywiaWF0IjoxNzYwMDAwNDY3LCJqdGkiOiJjZTc4NzZkNy0yYTE4LTQ5OTgtOTE3Yi01YjUzNjAwNDE1NTIifQ.SzT8jUBGSqWAyUUNrX9kLTfunCPyeyAOHjhrQP1JQG0"

headers = {
    "Authorization": f"Bearer {token}"
}

resp = requests.get(f"https://{CML_IP}/api/v0/node_definitions", headers=headers, verify=False)
print(resp.json())