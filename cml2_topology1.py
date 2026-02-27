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
LAB_ID = "your_lab_id."  # Replace with your actual lab ID

# ===== Authenticate to CML =====
auth_url = f"https://{CML_IP}/api/v0/authenticate"
resp = requests.post(auth_url, json={"username": USERNAME, "password": PASSWORD}, verify=False)

if resp.status_code != 200:
    print("Authentication failed. Status code:", resp.status_code)
    print("Response:", resp.text)
    exit(1)

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
    resp = requests.post(f"https://{CML_IP}/api/v0/labs/{LAB_ID}/nodes", 
                         headers=headers, json=payload, verify=False)
    resp_json = resp.json()
    if "id" not in resp_json:
        print(f"Failed to create node '{label}'. Response: {resp_json}")
        exit(1)
    return resp_json["id"]

# ===== Create Routers & Switches =====
router_ids = [create_node(r, "iosv", "iosv-15.9.3") for r in routers]
switch_ids = [create_node(s, "ioll2-xe", "iol2-xe") for s in switches]

print("Nodes created:", router_ids + switch_ids)

# ===== Create Links (Routers <-> Switches) =====
def create_link(node_a, node_b, adapter_a=0, port_a=0, adapter_b=0, port_b=0):
    payload = {
        "nodes": [
            {"node_id": node_a, "adapter_number": adapter_a, "port_number": port_a},
            {"node_id": node_b, "adapter_number": adapter_b, "port_number": port_b}
        ]
    }
    resp = requests.post(f"https://{CML_IP}/api/v0/projects/{PROJECT_ID}/links", 
                         headers=headers, json=payload, verify=False)
    return resp.json()

# Connect each router to SW1 and SW2 for redundancy
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
