from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.102",
    "username": "cisco",
    "password": "cisco",
    "allow_agent": False,
    "use_keys": False,
}

net_connect = ConnectHandler(**device)
print(net_connect.send_command("show running-config"))
