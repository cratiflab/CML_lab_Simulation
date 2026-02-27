import netmiko

device_type = 'cisco_ios'
ip_address = '192.168.1.113'
username = 'admin'
password = 'Adeola12345'
config_commands = ['interface Ethernet0/1', 'ip address 10.0.0.2 255.255.255.0', 'no shutdown']
config_commands = ['interface Ethernet0/2', 'ip address 10.0.1.2 255.25.255.0', 'no shutdown']
config_commands = ['router ospf 1', 'router-id 1.1.1.1']
device = {
    'device_type': device_type,
    'ip': ip_address,
    'username': username,
    'password': password,
}
net_connect = netmiko.ConnectHandler(**device)
output = net_connect.send_config_set(config_commands)
print(output)  
net_connect.disconnect()