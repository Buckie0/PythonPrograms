import os
import sys
from datetime import datetime

from nornir import InitNornir

from nornir.plugins.tasks.networking import netmiko_send_command
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
def check_apply_dhcp(task):
    check_dhcp = task.run(task=netmiko_send_command,
                          command_string="sh run | i dhcp",
                          enable=True)

    if "ip dhcp pool MERAKI_MGMNT" in check_dhcp.result:
        commands = f"""
                ip dhcp pool MERAKI_MGMNT
                no dns-server 10.20.0.53 10.20.2.3
                dns-server 8.8.8.8 8.8.4.4
                """
        command_list = commands.strip().splitlines()
        task.run(
            task=netmiko_send_config,
            config_commands=command_list
        )
        print(f"{task.host.name} - Done")
    else:
        print(f"{task.host.name} - No changes needed")


# Run the above functions and save the config
def main(task):
    check_apply_dhcp(task)

    # Write Memory
    task.run(task=netmiko_save_config)
    print(f"{task.host.name} - Done")


# The start of the actual nornir part
# the nr.run will run the task called "main" which we defined above
print("Running...")
nr.run(task=main)

sys.exit("Goodbye.")
