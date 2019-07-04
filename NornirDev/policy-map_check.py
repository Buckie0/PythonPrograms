import csv

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command

nornir_host = InitNornir(config_file='config.yaml')

# print(nornir_host.inventory.hosts)

policy_check = 'Policy-Maps' + '.csv'


# Run Commands, check ouput, then advise.
# Check Duplex
def policy(task):
    print(' Checking Policy, Please Wait...')
    policy = task.run(
        task=netmiko_send_command,
        command_string='sh policy-map'
    )
    with open(policy_check, 'a', newline="\n") as f:
        writer = csv.writer(f)
        writer.writerow(nornir_host.inventory.hosts)
        writer.writerow(print_result(policy))


if __name__ == "__main__":
    policy(nornir_host)
