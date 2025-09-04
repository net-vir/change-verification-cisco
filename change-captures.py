## This code is used to capture cisco show commands before and after the change.
import paramiko
import time
import getpass
import csv


def ssh_connect(host, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password)
        return client
    except Exception as e:
        print(f"Failed to connect to {host}: {e}")
        return None

change_type = input("Enter change type (e.g., 'pre' or 'post'): ")
change_type = change_type.upper()

change_id = input("Enter change ID: ")

username = input("Enter your SSH username: ")
password = getpass.getpass("Enter your SSH password: ")

   
with open('input.csv', 'r', newline='', encoding='utf-8-sig') as file:
    reader = list(csv.DictReader(file))


for row in reader:
    hostname = row['HOSTNAME']
    hostip = row['MANAGEMENT_IP']
    commnands = row['COMMANDS'].splitlines()
    connection = ssh_connect(hostip, username, password)
    channel = connection.invoke_shell()
    time.sleep(1)
    for command in commnands:
        channel.send(command + '\n')
        time.sleep(5)
        output = channel.recv(65535).decode('utf-8')
        with open(f'{change_type}_{change_id}.txt', 'a') as f:
            f.write(output)
            f.write("\n\n")
    channel.close()
    connection.close()
