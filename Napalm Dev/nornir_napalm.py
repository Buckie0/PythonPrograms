import napalm
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

# Use the appropriate network driver to connect to the device
driver = napalm.get_network_driver('eos')

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


def napalm_command(task, config_file):
    """Load a config for the device."""

    if not (os.path.exists(config_file) and os.path.isfile(config_file)):
        msg = 'Missing or invalid config file {0}'.format(config_file)
        raise ValueError(msg)

    print('Loading config file {0}.'.format(config_file))

    print('Opening ...')
    task.open()

    print('Loading config ...')
    task.load_merge_candidate(filename=config_file)

    # Note that the changes have not been applied yet. Before applying
    # the configuration you can check the changes:
    print('\nDiff:')
    diffs = task.compare_config()

    # You can commit or discard the candidate changes.

    if len(diffs) > 0:
        print(diffs)

        choice = input("""\nType COMMIT to commit the confguration changes or hit
    ENTR to abort: """)
        if choice == 'COMMIT':
            print('Committing ...')
            try:
                task.commit_config()

            except Exception as inst:
                print('\nAn error occured with the commit')
                print(type(inst))
                sys.exit(inst)
                print()

            else:
                print("Configuration committed")

        else:
            print('Discarding ...')
            task.discard_config()
    else:
        print("No changes ceeded")


def rollback(device):
    choice_rollback = input("""\n type ROLLBACK to rollback or hit
NTER to save them: """)
    if choice_rollback == 'ROLLBACK':
        print('Rolling Back Changes...')
        try:
            device.discard_config()
        except Exception as inst:
            print("An error occured with the rollback")
            print(type(inst))
            sys.exit(inst)
            print()
    else:
        device.close()
        print('Done.')


# The start of the actual nornir part
# the nr.run will run the task called "main" which we defined above
def main(task):
    if ping(task):
        task_filter = nr.filter(hostname=task.host.hostname)
        task_filter.run(task=napalm_command)
    else:
        failure_logs(task, message="DOWN")


print("Running...")
if len(sys.argv) < 2:
    print('Please supply the full path to "new_good.conf"')
    sys.exit(1)
    config_file = sys.argv[1]
nr.run(task=main)
