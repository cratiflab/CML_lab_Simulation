from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.113",
    "username": "admin",
    "password": "Adeola12345"
}

# Connect to the device
net_connect = ConnectHandler(**device)

# Enter enable mode (important if 'show run' is restricted)
net_connect.enable()

# Send the command
output = net_connect.send_command("show running-config")

# Save output to a file named after the device IP
filename = f"{device['ip'].replace('.', '_')}_running_config.txt"
with open(filename, "w") as f:
    f.write(output)
# Print output
print(output)

# Close the connection
net_connect.disconnect()
