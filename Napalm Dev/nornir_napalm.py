# import napalm
import os
import subprocess as sp
import sys
from datetime import datetime
from nornir import InitNornir
from nornir.core.exceptions import NornirSubTaskError
import pandas as pd
from nornir.plugins.functions.text import print_result  # noqa
# from jinja2 import Environment, FileSystemLoader
from nornir.plugins.tasks.data import load_yaml
from nornir.plugins.tasks.text import template_file
from nornir.plugins.tasks.networking import napalm_configure


nr = InitNornir(
    core={"num_workers":
          50},  # running with 50 parallel threads - this can be changed
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
# username = os.getenv("USER")
# password = os.getenv("PASSWORD")

# Print results
# print("Username:", username)
# if password:
#     print("Password: SET")
# else:
#     print("Password: NO PASSWORD DEFINED")


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
# nr.inventory.defaults.username = username
# nr.inventory.defaults.password = password
# nr.inventory.groups["cisco-ios"].connection_options["netmiko"].extras["secret"] = password

# # Update nornir default credentials to environment variables.
# nr_telnet.inventory.defaults.username = username
# nr_telnet.inventory.defaults.password = password
# nr_telnet.inventory.groups["cisco-ios-telnet"].connection_options["netmiko"].extras["secret"] = password

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


# def render_template(task):
#     file_loader = FileSystemLoader(',')

#     env = Environment(loader=file_loader)
#     template = env.get_template('eos_config.j2')
#     output = template.render()


def napalm__diff(task):
    try:
        data = task.run(
            task=load_yaml,
            file=f'{task.host}.yaml'
        )
    except FileNotFoundError:
        print({task.host} + "No changes to make(no config file found).")
 
    else:
        task.host["bgp_neighbour_test"] = data.result["bgp_neighbour_test"]
        task.host["bgp_neighbour_test_remote"] = data.result["bgp_neighbour_test_remote"]
        task.host["bgp_neighbour_test_1"] = data.result["bgp_neighbour_test_1"]
        task.host["bgp_neighbour_test_1_remote"] = data.result["bgp_neighbour_test_1_remote"]
        task.host["host"] = data.result["host"]
        task.host["network"] = data.result["network"]
        task.host["config"] = task.run(task=template_file,
                                       template="eos_config.j2",
                                       path="")
        task.run(task=napalm_configure,
                 configuration=task.host["config"]
                 (replace=False, merge=False))


def napalm_replace(task):
    try:
        data = task.run(
            task=load_yaml,
            file=f'{task.host}.yaml'
        )
    except FileNotFoundError:
        print({task.host} + "No changes to make(no config file found).")

    else:
        task.host["bgp_neighbour_test"] = data.result["bgp_neighbour_test"]
        task.host["bgp_neighbour_test_remote"] = data.result["bgp_neighbour_test_remote"]
        task.host["bgp_neighbour_test_1"] = data.result["bgp_neighbour_test_1"]
        task.host["bgp_neighbour_test_1_remote"] = data.result["bgp_neighbour_test_1_remote"]
        task.host["host"] = data.result["host"]
        task.host["network"] = data.result["network"]
        r = task.run(task=template_file, template="eos_config.j2", path="")
        task.host["template_config"] = r.result
        task.run(task=napalm_configure,
                 configuration=task.host["template_config"]
                 )


# The start of the actual nornir part
# the nr.run will run the task called "main" which we defined above
def main(task):
    if napalm__diff(task):
        choice = input("""\nType COMMIT to commit the confguration changes or hit
        ENTER to abort: """)
        if choice == 'COMMIT':
            print('Committing ...')
            try:
                napalm_replace(task)
            except Exception as inst:
                print('\nAn error occured with the commit')
                print(type(inst))
                sys.exit(inst)
                print()
            else:
                print("Configuration committed")
        else:
            print('Discarding ...')
    else:
        print("Goodbye.")


print("Running...")
r = nr.run(task=main)
print_result(r)
