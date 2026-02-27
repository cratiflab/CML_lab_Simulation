from netmiko import ConnectHandler

# Device info
device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.102",
    "username": "cisco",
    "password": "cisco",
    "allow_agent": False,
    "use_keys": False,
}

# Configuration commands
config_commands = [
    "interface GigabitEthernet0/1",
    "description Inside Interface",
    "ip address 192.168.10.1 255.255.255.0",
    "no shutdown",
    "exit",
    # DHCP configuration
    "ip dhcp pool INSIDE-NET",
    "network 192.168.10.0 255.255.255.0",
    "default-router 192.168.10.1",
    "dns-server 8.8.8.8",
    "exit",
    # Exclude router IP from DHCP pool
    "ip dhcp excluded-address 192.168.10.1",
]

# Connect and push configuration
net_connect = ConnectHandler(**device)
output = net_connect.send_config_set(config_commands)
print(output)

# Save config
save_output = net_connect.save_config()
print(save_output)

net_connect.disconnect()
