import os
import subprocess as sp
import sys
from datetime import datetime

from netmiko.ssh_exception import NetMikoAuthenticationException

from nornir import InitNornir
from nornir.core.exceptions import NornirSubTaskError

import pandas as pd

from nornir.plugins.tasks.networking import netmiko_send_command  # noqa
from nornir.plugins.tasks.networking import netmiko_send_config  # noqa
from nornir.plugins.functions.text import print_result  # noqa

nr = InitNornir(
    core={"num_workers":
          20},  # running with 50 parallel threads - this can be changed
    logging={
        "file": "debug/mylogs",  # everything will be logged to a file called "mglogs" at a debug level
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
    core={"num_workers": 20},
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


# Output logs for general actions
def general_logs(task, message):
    file = open(f"debug/general_logs.txt", "a")
    file.write(f"""[{datetime.today().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]}],
                    {task.host.name}, {task.host.hostname}, {message}\n""")
    file.close()


# Output logs for failuress
def failure_logs(task, message):
    file = open(f"debug/failure_logs.txt", "a")
    file.write(f"""[{datetime.today().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]}],
                    {task.host.name}, {task.host.hostname}, {message}\n""")
    file.close()


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
    print("Output Folder = " + directory)
else:
    directory = (f"{os.getcwd()}/output")
    print("Output Folder = " + directory)


# Checks connectivity with ICMP ping
def ping(task):
    output = sp.Popen(
        f"timeout 5 ping -c 2 {task.host.hostname}", stdout=sp.PIPE, stderr=sp.STDOUT, shell=True, close_fds=True
    )
    str_output = str(output.stdout.read())
    if "64 bytes" in str_output:
        return True
    else:
        return False
    output.close()


# this example task logs into each device and checks if it has the option 66 config on it
# doing this we can tell if it's a Howdens voice router or not
# if it does have the config on there it will then check that the
# "no ip dhcp conflict logging" command is present. It will output this command
# to a pandas dataframe. This is for ease of use when pushing it to a csv
def checker(task):
    try:
        option_66 = task.run(task=netmiko_send_command,
                             command_string="show run | i option 66",
                             enable=True)
        dhcp_pool = task.run(task=netmiko_send_command,
                             command_string="show run | i ip dhcp pool",
                             enable=True)
    except (NetMikoAuthenticationException, NornirSubTaskError):
        failure_logs(task, message="Authentication failure")
    else:
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
            print(f"{task.host.name} - Done")
            general_logs(task, message="Done")
        else:
            failure_logs(task, message="Skipped")


# The start of the actual nornir part
# the nr.run will run the task called "main" which we defined above
def main(task):
    if ping(task):
        task_filter = nr_telnet.filter(hostname=task.host.hostname)
        task_filter.run(task=checker)
    else:
        failure_logs(task, message="DOWN")


print("Running...")
nr_telnet.run(task=main)

# this part is getting a list of all the files in the output directory
# adding them to a list and then combining all the csvs in the list
# into one csv called "combined.csv" using pandas again
print("Merging output to combined.csv")
dir_list_base = (os.listdir(directory))
dir_list = []
for x in dir_list_base:
    if ".csv" in x:
        dir_list.append(x)
os.chdir(directory)
combined_csv = pd.concat([pd.read_csv(f) for f in dir_list], sort=True)
combined_csv.to_csv("combined.csv", index=False)
sys.exit("Goodbye.")
