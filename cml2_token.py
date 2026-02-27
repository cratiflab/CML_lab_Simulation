import requests

headers = {
    "Content-Type": "application/json"
}

url_projects = f"https://192.168.0.34/api/v0/projects"
resp = requests.get(url_projects, headers=headers, verify=False)
print(resp.json())