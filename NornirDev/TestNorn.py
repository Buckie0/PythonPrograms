import time

from colored import attr, fg

import subprocess as sp
import os
from datetime import datetime
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
# from nornir.plugins.tasks.networking import netmiko_send_config

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
nr_telnet = InitNornir(
    core={"num_workers": 50},
    logging={"file": "debug/mylogs", "level": "debug"},
    inventory={
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "host_file": "inventory/hosts_telnet.yaml",
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

# Update nornir default credentials to environment variables.
nr_telnet.inventory.defaults.username = username
nr_telnet.inventory.defaults.password = password
nr_telnet.inventory.groups["cisco-ios-telnet"].connection_options["netmiko"].extras["secret"] = password


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
        command_string='sh int status'
    )
    print_result(duplex_check)
    for half in duplex_check.result:
        if half == 'half':
            print('''%s\n  HALF DUPLEX DISCOVERED.
        PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int status)%s
        ''' % (fg(1), attr(0)))
        elif duplex_check:
            print('%s\n  No issues found%s' % (fg(2), attr(0)))


# Check Logs
def logs(task):
    print('\n Reading Logs, Please Wait...')
    log_check = task.run(
        task=netmiko_send_command,
        command_string='sh log'
    )
    print_result(log_check)
    for down in log_check.result:
        if down == "down":
            print('''%s\n  DROPS SEEN.
        PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh log)%s
        ''' % (fg(1), attr(0)))
        elif log_check:
            print('%s\n  No drops seen%s' % (fg(2), attr(0)))


# Check crc
def crc(task):
    print('\n Checking interfaces for errors, Please Wait...')
    crc_check = task.run(
        task=netmiko_send_command,
        command_string='sh run | i CRC'
    )
    print_result(crc_check)
    for crcs in crc_check.result:
        if ("0") not in crcs:
            print('''%s\n  INTERFACE ERRORS SEEN.
        PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int | i CRC)%s
        ''' % (fg(1), attr(0)))
        elif crc_check:
            print('%s\n  No issues found%s' % (fg(2), attr(0)))


# Check policy
def policy(task):
    print('\n Checking interfaces for errors, Please Wait...')
    policy_map = task.run(
        task=netmiko_send_command,
        command_string='sh policy-map'
    )
    print_result(policy_map)


# Check ping
def ping(task):
    print('''\n Checking vrf information...''')
    vrf_check = task.run(
        task=netmiko_send_command,
        command_string='sh vrf'
    )
    for vrf in vrf_check.result:
        if vrf == "VoIP_2":
            print('\n Pinging GSX, Please Wait...')
            print('''%s\n  This will send 1000 pings to the GSX, however you may
            need to run further pings %s''' % (fg(2), attr(0)))
            output = task.run(
                task=netmiko_send_command,
                command_string='ping vrf VoIP_2 10.81.253.166 source Vlan251 r 1000 \n'
            )
            time.sleep(12)
            print('\n' + output)
        if vrf == "VOIP":
            print('\n Pinging GSX, Please Wait...')
            print('''%s\n  This will send 1000 pings to the GSX, however you may
            need to run further pings %s''' % (fg(2), attr(0)))
            output = task.run(
                task=netmiko_send_command,
                command_string='ping vrf VOIP 10.81.253.166 r 1000 \n'
            )
            time.sleep(12)
            print('\n' + output)
        if vrf == "VoIP":
            print('\n Pinging GSX, Please Wait...')
            print('''%s\n  This will send 1000 pings to the GSX, however you may
            need to run further pings %s''' % (fg(2), attr(0)))
            output = task.run(
                task=netmiko_send_command,
                command_string='ping vrf VoIP 10.81.253.166 r 1000 \n'
            )
            time.sleep(12)
            print('\n' + output)
        elif vrf:
            print('''\n Unable to find a VOIP vrf.
            PLEASE LOG ONTO DEVICE AND CHECK WHAT VRF IS IN USE (sh ip vrf)''')


def main(task):

# Run the Program
print("Running...")
nr.run(task=main)

# Goodbye

time.sleep(3)

print('''%s
\n You can paste the below into the ticket and fill in as necessary:

- Checked Logs -
- Checked Duplex -
- Checked Interfaces for errors:
- Checked Policy-Map:
- Ran Pings to the GSX:
\n%s''' % (fg(3), attr(0)))

print('''%s\n  Goodbye.
  For further information, check the guides on Sharepoint.%s
  ''' % (fg(3), attr(0)))
