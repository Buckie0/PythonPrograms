import os

import time
from datetime import datetime

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command

nr = InitNornir(
    core={"num_workers": 50},
    logging={"file": "debug/mylogs", "level": "debug"},
    inventory={
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        },
    },
)

# Gather current date/time
now = datetime.now()
today = now.strftime("%d-%m-%Y")

# Gather username & password from local environment variables.
username = os.getenv("USER")
password = os.getenv("PASSWORD")

# Print results
print("Username:", username)
if password:
    print("Password: SET")
else:
    print("Password: NO PASSWORD DEFINED")

# Update nornir default credentials to environment variables.
nr.inventory.defaults.username = username
nr.inventory.defaults.password = password
nr.inventory.groups["cisco-ios"].connection_options["netmiko"].extras["secret"] = password


# Output logs for general actions
def general_logs(task, message):
    file = open(f"debug/general_logs.txt", "a")
    file.write(f"[{datetime.today().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]}], {task.host.hostname}, {message}\n")
    file.close()


# Output logs for failuress
def failure_logs(task, message):
    file = open(f"debug/failure_logs.txt", "a")
    file.write(f"[{datetime.today().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]}], {task.host.hostname}, {message}\n")
    file.close()


print(nr.inventory.hosts)


# Run Commands, check ouput, then advise.
# Check Duplex
def duplex(task):
    print(' Checking Duplex, Please Wait...')
    duplex_check = task.run(
        task=netmiko_send_command,
        command_string='sh int status',
        enable=True
    )
    if "half" in duplex_check.result:
        print('''\n  HALF DUPLEX DISCOVERED.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int status)
    ''')
    elif duplex_check:
        print('\n  No issues found')


# Check Logs
def logs(task):
    print('\n Reading Logs, Please Wait...')
    log_check = task.run(
        task=netmiko_send_command,
        command_string='sh log',
        enable=True
    )
    if "down" in log_check.result:
        print('''\n  DROPS SEEN.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh log)
    ''')

    elif log_check:
        print('\n  No drops seen')


# Check crc
def crc(task):
    print('\n Checking interfaces for errors, Please Wait...')
    crc_check = task.run(
        task=netmiko_send_command,
        command_string='sh int | i CRC',
        enable=True
    )
    if ("1", "2", "3", "4", "5", "6", "7", "8", "9") in crc_check.result:
        print('''\n  INTERFACE ERRORS SEEN.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int | i CRC)
    ''')
    elif crc_check:
        print('\n  No issues found')


# Check policy
def policy(task):
    print('\n Display Policy-Map....')
    policy_map = task.run(
        task=netmiko_send_command,
        command_string='sh policy-map',
        enable=True
    )
    print_result(policy_map)


# Check ping
def ping(task):
    print('''\n Checking vrf information...''')
    vrf_check = task.run(
        task=netmiko_send_command,
        command_string='sh vrf',
        enable=True
    )
    if "VoIP_2" in vrf_check.result:
        print('\n Pinging GSX, Please Wait...')
        print('''\n  This will send 1000 pings to the GSX, however you may
  need to run further pings ''')
        output = task.run(
            task=netmiko_send_command,
            command_string='ping vrf VoIP_2 10.81.253.166 source Vlan251 r 1000 \n',
            enable=True
        )
        time.sleep(12)
        print_result('\n' + output.result)
    if "VOIP" in vrf_check.result:
        print('\n Pinging GSX, Please Wait...')
        print('''\n  This will send 1000 pings to the GSX, however you may
  need to run further pings ''')
        output = task.run(
            task=netmiko_send_command,
            command_string='ping vrf VOIP 10.81.253.166 r 1000 \n',
            enable=True
        )
        time.sleep(12)
        print_result('\n' + output.result)
    if "VoIP" in vrf_check.result:
        print('\n Pinging GSX, Please Wait...')
        print('''\n  This will send 1000 pings to the GSX, however you may
  need to run further pings ''')
        output = task.run(
            task=netmiko_send_command,
            command_string='ping vrf VoIP 10.81.253.166 r 1000 \n',
            enable=True
        )
        time.sleep(12)
        print_result('\n' + output.result)
    else:
        print('''\n Unable to find a VOIP vrf.
  PLEASE LOG ONTO DEVICE AND CHECK WHAT VRF IS IN USE (sh ip vrf)''')


def main(task):
    print(task.host.name)
    duplex(task)
    time.sleep(2)
    logs(task)
    time.sleep(2)
    crc(task)
    time.sleep(2)
    policy(task)
    time.sleep(2)
    ping(task)


# Run the Program
print("Running...")
nr.run(task=main)

# Goodbye

time.sleep(2)

print('''
\n You can paste the below into the ticket and fill in as necessary:

- Checked Logs -
- Checked Duplex -
- Checked Interfaces for errors:
- Checked Policy-Map:
- Ran Pings to the GSX:
\n''')

print('''  Goodbye.
  For further information, check the guides on Sharepoint.
  ''')
