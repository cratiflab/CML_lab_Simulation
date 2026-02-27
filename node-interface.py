from netmiko import ConnectHandler

# ===== List of Devices =====
devices = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.102",
        "username": "cisco",
        "password": "cisco",
        "allow_agent": False,
        "use_keys": False,
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.100.4",
        "username": "cisco",
        "password": "cisco",
        "allow_agent": False,
        "use_keys": False,
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.100.5",
        "username": "cisco",
        "password": "cisco",
        "allow_agent": False,
        "use_keys": False,
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.100.7",
        "username": "cisco",
        "password": "cisco",
        "allow_agent": False,
        "use_keys": False,
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.100.8",
        "username": "cisco",
        "password": "cisco",
        "allow_agent": False,
        "use_keys": False,
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.100.9",
        "username": "cisco",
        "password": "cisco",
        "allow_agent": False,
        "use_keys": False,
    } 

]

# ===== Loop through all devices =====
for device in devices:
    print(f"\nConnecting to {device['ip']} ...")
    try:
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command("show running-config")

        # Save to file
        filename = f"{device['ip']}_running-config.txt"
        with open(filename, "w") as f:
            f.write(output)

        print(f"✅ Configuration from {device['ip']} saved as {filename}\n")
        net_connect.disconnect()

    except Exception as e:
        print(f"❌ Failed to connect to {device['ip']}: {e}")
