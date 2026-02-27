import netmiko

device_type = 'cisco_ios'
ip_address = '192.168.1.113'
username = 'admin'
password = 'Adeola12345'
config_commands = ['hostname Router1']
# Create a connection to the device
device = {
    'device_type': device_type,
    'ip': ip_address,
    'username': username,
    'password': password,
}
net_connect = netmiko.ConnectHandler(**device)
# Send the configuration commands to the device
output = net_connect.send_config_set(config_commands)
print(output)
# Disconnect from the device
net_connect.disconnect()