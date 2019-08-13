import os
import sys
from datetime import datetime

from nornir import InitNornir

import pandas as pd

from nornir.plugins.tasks.networking import netmiko_send_command  # noqa
from nornir.plugins.tasks.networking import netmiko_send_config  # noqa
from nornir.plugins.functions.text import print_result  # noqa

nr = InitNornir(
    core={"num_workers":
          50},  # running with 50 parallel threads - this can be changed
    logging={
        "file": "mylogs",  # everything will be logged to a file called "mglogs" at a debug level
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

# this sets the output directory to "/path/to/this/script/output"
# please make sure there is an output folder in this script direcotyr
# this is where all of the CSVs will go
if "win" in sys.platform:  # windows version
    directory = (f"{os.getcwd()}\output")
    print(directory)
else:
    directory = (f"{os.getcwd()}/output")
    print(directory)


# this example task logs into each device and checks if it has the option 66 config on it
# doing this we can tell if it's a Howdens voice router or not
# if it does have the config on there it will then check that the
# "no ip dhcp conflict logging" command is present. It will output this command
# to a pandas dataframe. This is for ease of use when pushing it to a csv
def main(task):

    option_66 = task.run(task=netmiko_send_command,
                         command_string="show run | i option 66",
                         enable=True)
    dhcp_pool = task.run(task=netmiko_send_command,
                         command_string="show run | i ip dhcp pool",
                         enable=True)
    if "option 66" in option_66.result:
        output_df = pd.DataFrame(columns=['Host', 'MGMT IP', 'Dhcp pool Name', 'Option66'])
        output_df = output_df.append(
            {
                'Host': task.host.name,
                'MGMT IP': task.host.hostname,
                'Dhcp pool Name': dhcp_pool.result,
                'Option66': option_66.result
            },
            ignore_index=True)
        # you need to open the file and close it after you've written to it
        # this is needed due to "too many files open" error once you get ~450 devices deep
        output_file = open(directory + "/" + task.host.name + ".csv", 'a')
        output_df.to_csv(output_file)
        output_file.close()
        print(f"{task.host.name} - done")
    else:
        print(f"{task.host.name} - skipped")


# The start of the actual nornir part
# the nr.run will run the task called "main" which we defined above
print("Running...")
nr_telnet.run(task=main)

# this part is getting a list of all the files in the output directory
# adding them to a list and then combining all the csvs in the list
# into one csv called "combined.csv" using pandas again
dir_list_base = (os.listdir(directory))
dir_list = []
for x in dir_list_base:
    if ".csv" in x:
        dir_list.append(x)
os.chdir(directory)
combined_csv = pd.concat([pd.read_csv(f) for f in dir_list], sort=True)
combined_csv.to_csv("combined.csv", index=False)
sys.exit("Goodbye.")
