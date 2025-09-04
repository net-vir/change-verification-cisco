## This code is used to capture cisco show commands before and after the change.
import paramiko
import time
import csv
import argparse
import sys


def ssh_connect(host, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password)
        return client
    except Exception as e:
        print(f"Failed to connect to {host}: {e}")
        return None


def main():
    # ----------------------------
    # Parse Jenkins parameters
    # ----------------------------
    parser = argparse.ArgumentParser(description="Capture Cisco show commands before/after change")
    parser.add_argument("--csv", required=True, help="Path to input CSV file with HOSTNAME, MANAGEMENT_IP, COMMANDS")
    parser.add_argument("--username", required=True, help="SSH username")
    parser.add_argument("--password", required=True, help="SSH password")
    parser.add_argument("--change_id", required=True, help="Change ID for tracking")
    parser.add_argument("--change_type", required=True, help="Change type (PRE or POST)")
    parser.add_argument("--output", required=True, help="Output file to store command results")

    args = parser.parse_args()

    change_type = args.change_type.upper()
    change_id = args.change_id
    username = args.username
    password = args.password
    input_csv = args.csv
    output_file = args.output

    # ----------------------------
    # Read CSV
    # ----------------------------
    try:
        with open(input_csv, 'r', newline='', encoding='utf-8-sig') as file:
            reader = list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"CSV file {input_csv} not found!")
        sys.exit(1)

    # ----------------------------
    # Loop through devices
    # ----------------------------
    for row in reader:
        hostname = row['HOSTNAME']
        hostip = row['MANAGEMENT_IP']
        commands = row['COMMANDS'].splitlines()

        print(f"\nConnecting to {hostname} ({hostip})...")

        connection = ssh_connect(hostip, username, password)
        if not connection:
            continue

        channel = connection.invoke_shell()
        time.sleep(1)

        for command in commands:
            channel.send(command + '\n')
            time.sleep(5)
            output = channel.recv(65535).decode('utf-8')

            # Save results in output file
            with open(output_file, 'a') as f:
                f.write(f"### Host: {hostname} ({hostip}) | Command: {command}\n")
                f.write(output)
                f.write("\n\n")

        channel.close()
        connection.close()


if __name__ == "__main__":
    main()
