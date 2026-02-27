import paramiko
#Define Vareiables
ip_address = '192.168.1.114'
username = 'admin'
password = 'Adeola12345'
#Establish SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_address, username=username, password=password)
#send command
stdin, stdout, stderr = ssh.exec_command('show version')
#print output
print(stdout.read().decode())
#close connection
ssh.close()