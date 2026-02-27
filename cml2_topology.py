import requests
import json
from netmiko import ConnectHandler
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===== CML Settings =====
CML_IP = "192.168.0.34"
USERNAME = "cratiflab"
PASSWORD = "adeola01"
PROJECT_ID = 1  # adjust if needed

# ===== Authenticate to CML =====
auth_url = f"https://{CML_IP}/api/v0/authenticate"
resp = requests.post(auth_url, json={"username": USERNAME, "password": PASSWORD}, verify=False)
token = resp.text.strip()

headers = {"Authorization": f"Bearer {token}"}

# ===== Node Definitions =====
routers = ["R1", "R2", "R3", "R4", "R5"]
switches = ["SW1", "SW2"]

def create_node(label, node_def, image):
    payload = {
        "label": label,
        "node_definition": node_def,
        "image": image,
        "icon": "Router" if "R" in label else "Switch"
    }
    resp = requests.post(f"https://{CML_IP}/api/v0/projects/{PROJECT_ID}/nodes", 
                         headers=headers, json=payload, verify=False)
    
    print(f"Creating node {label} returned status {resp.status_code}")
    print(resp.text)  # <--- this will show the exact error
    
    return resp.json()["id"]

def get_first_image(node_def):
    resp = requests.get(f"https://{CML_IP}/api/v0/node_definitions/{node_def}", headers=headers, verify=False)
    data = resp.json()
    images = data.get("images", [])
    print(f"DEBUG: node_def={node_def}, images={images}")  # Debug print
    if not images:
        raise ValueError(f"No images found for node definition '{node_def}'")
    return images[0]

# ===== Fetch images dynamically =====
router_image = get_first_image("iosv")
switch_image = get_first_image("iosvl2")

# ===== Create Routers & Switches =====
router_ids = [create_node(r, "iosv", router_image) for r in routers]
switch_ids = [create_node(s, "iosvl2", switch_image) for s in switches]

# ===== Create Links (Routers <-> Switches) =====
for r_id in router_ids:
    create_link(r_id, switch_ids[0])
    create_link(r_id, switch_ids[1])

# Connect SW1 <-> SW2 for redundancy
create_link(switch_ids[0], switch_ids[1])

print("Links created.")

# ===== Wait for devices to boot =====
print("Waiting 60 seconds for devices to start...")
time.sleep(60)  # adjust if boot takes longer

# ===== Push Initial Configs via Netmiko =====
devices = [
    {"host": "192.168.0.101", "name": "R1"},
    {"host": "192.168.0.102", "name": "R2"},
    {"host": "192.168.0.103", "name": "R3"},
    {"host": "192.168.0.104", "name": "R4"},
    {"host": "192.168.0.105", "name": "R5"},
    {"host": "192.168.0.201", "name": "SW1"},
    {"host": "192.168.0.202", "name": "SW2"}
]

for dev in devices:
    net_connect = ConnectHandler(
        device_type="cisco_ios" if "R" in dev["name"] else "cisco_ios",
        host=dev["host"],
        username="admin",
        password="your_password"
    )
    
    config_commands = [
        f"hostname {dev['name']}",
        "no ip domain-lookup",
    ]
    
    # Example: Router-specific interface config & OSPF
    if "R" in dev["name"]:
        config_commands += [
            "interface GigabitEthernet0/1",
            f"description Connected to inside network",
            f"ip address 10.{router_ids.index(dev['name'])+1}.0.1 255.255.255.0",
            "no shutdown",
            "exit",
            "router ospf 1",
            f"network 10.{router_ids.index(dev['name'])+1}.0.0 0.0.0.255 area 0",
            "exit"
        ]
    
    # Example: Switch VLAN config
    else:
        config_commands += [
            "vlan 10",
            "name USERS",
            "exit",
            "vlan 20",
            "name SERVERS",
            "exit",
            "interface range Gi0/1-2",
            "switchport mode trunk",
            "exit"
        ]
    
    output = net_connect.send_config_set(config_commands)
    print(f"{dev['name']} config pushed:\n", output)
    
    save_output = net_connect.save_config()
    print(save_output)
    net_connect.disconnect()

print("Automation complete: topology created and initial configs applied.")