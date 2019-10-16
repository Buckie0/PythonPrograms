import os
import sys
from datetime import datetime

from nornir import InitNornir

from nornir.plugins.tasks.networking import netmiko_send_config, netmiko_save_config


nr = InitNornir(
    core={"num_workers":
          50},  # running with 50 parallel threads - this can be changed
    logging={
        "file": "debug/mylogs",  # everything will be logged to a file called "mylogs" at a debug level
        "level": "debug"
    },
    inventory={
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yaml",  # the inventory creator in the inventory folder will create this
            "group_file": "inventory/groups.yaml",  # this can be kept the same throughout
            "defaults_file": "inventory/defaults.yaml"  # as can this
        }
    }
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

# this sets the output directory to "/path/to/this/script/output"
# please make sure there is an output folder in this script directory
# this is where all of the CSVs will go
if "win" in sys.platform:  # windows version
    directory = (f"{os.getcwd()}\output")
else:
    directory = (f"{os.getcwd()}/output")


# Apply the standby address with the IP from check_ip_stand()
def check_apply_snmp(task):
    if task.inventory.groups == 'cisco_ios':
        commands = f"""
                    snmp-server community Monitor1 RO 26
                    snmp-server host 10.231.241.104 Monitor1
                    access-list 26 permit 10.231.241.104
                """
        command_list = commands.strip().splitlines()
        task.run(
            task=netmiko_send_config,
            config_commands=command_list
        )
        print(f"{task.host.name} - Done")
    if task.inventory.groups == 'huawei':
        commands = f"""
                    snmp-agent community read Monitor1 acl 2025
                    acl number 2025
                      rule 20 permit source 10.231.241.0 0.0.0.255
                    acl number 2002
                      rule 10 permit source 10.231.241.0 0.0.0.255
                """
        command_list = commands.strip().splitlines()
        task.run(
            task=netmiko_send_config,
            config_commands=command_list
        )
        print(f"{task.host.name} - Done")
    else:
        print(f"{task.host.name} - Could not veriy device type.")


# Run the above functions and save the config
def main(task):
    check_apply_snmp(task)

    # Write Memory
    task.run(task=netmiko_save_config)
    print(f"{task.host.name} - Done")


# The start of the actual nornir part
# the nr.run will run the task called "main" which we defined above
print("Running...")
nr.run(task=main)

sys.exit("Goodbye.")
