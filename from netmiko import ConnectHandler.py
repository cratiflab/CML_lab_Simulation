from netmiko import ConnectHandler

# List of all your devices
devices = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.113",
        "username": "admin",
        "password": "Adeola12345",
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.114",
        "username": "admin",
        "password": "Adeola12345",
 },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.115",
        "username": "admin",
        "password": "Adeola12345",
    },
]

# Command to run
command = "show running-config"

# Loop through each device
for device in devices:
    print(f"\n🔹 Connecting to {device['ip']}...")
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        output = net_connect.send_command(command)
        
        # Save output to a file named after the device IP
        filename = f"{device['ip'].replace('.', '_')}_Devices.txt"
        with open(filename, "a") as f:
            f.write(output)

        print(f"✅ Config saved to {filename}")

        net_connect.disconnect()
    except Exception as e:
        print(f"❌ Failed to connect to {device['ip']}: {e}")






