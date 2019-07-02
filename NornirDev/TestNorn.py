import time

from colored import attr, fg

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command

nornir_host = InitNornir(config_file='config.yaml')

# runhost = nornir_host.filter(groups="cisco-ios")

print(nornir_host.inventory.hosts)


# Disable paging.
def paging(task):
    task.run(
        task=netmiko_send_command,
        command_string='terminal length 0\n'
    )


# Run Commands, check ouput, then advise.
# Check Duplex
def duplex(task):
    print(' Checking Duplex, Please Wait...')
    duplex_check = task.run(
        task=netmiko_send_command,
        command_string='sh int status'
    )
    print_result(duplex_check)
    for half in duplex_check:
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
    for down in log_check:
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
    for crcs in crc_check:
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
    for vrf in vrf_check:
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


# Run the Program
if __name__ == "__main__":
    paging(nornir_host)
    time.sleep(1)
    duplex(nornir_host)
    time.sleep(1)
    logs(nornir_host)
    time.sleep(1)
    crc(nornir_host)
    time.sleep(1)
    policy(nornir_host)
    time.sleep(1)
    ping(nornir_host)
    time.sleep(1)

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
