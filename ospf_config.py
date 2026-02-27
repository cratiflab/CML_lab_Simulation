import json
from  netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

with open("devices.json") as file:
    devices = json.load(file)
print(f"Starting OSPF Configuration...\n")


for index, device in enumerate(devices, start=1):

    device_params = {
        "device_type": "cisco_ios",
        "host": device["host"],
        "username": device["username"],
        "password": device["password"],
        "allow_agent": False,
        "use_keys": False
}
router_id = f"1.1.1.{index}"

config_commands = [
    "router ospf 1,"
    f"router-id {router_id}",
    "network 192.168.0.1 0.0.0.255 area 0"
]

try:
    print(f"Connecting to {device['host']}...")
    connection = ConnectHandler(**device_params)
    
    print(f"Configuring OSPF on {device['host']} with router-id{router_id}...")
    
    output = connection.send_config_set(config_commands)
    print(output)

    connection.disconnect()
    print(f"Finished configuring {device['host']}\n")

except NetmikoAuthenticationException:
    print(f"Authentication failed for {devices['host']}\n")

except NetmikoTimeoutException:
    print("Connection timed out for {device['host']}\n")

except Exception as e:
    print(f"unexpected error on {device['host']}: {e}\n")

print("OSPF configuration process completed.")

