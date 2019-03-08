from colored import attr, fg

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command

nornir_host = InitNornir(config_file='config.yaml')

# runhost = nornir_host.filter(role="CiscoIOS")

print(nornir_host.inventory.hosts)

print('\n Checking Duplex, Please Wait...')
duplex = nornir_host.run(
    task=netmiko_send_command,
    command_string='sh int status'
)
print_result(duplex)
if "half" in duplex:
    print('''%s\n  HALF DUPLEX DISCOVERED.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int status)%s
  ''' % (fg(1), attr(0)))
elif duplex:
    print('%s\n  No issues found%s' % (fg(2), attr(0)))


print('\n Reading Logs, Please Wait...')
log_check = nornir_host.run(
    task=netmiko_send_command,
    command_string='sh log'
)
print_result(log_check)
if "down" in log_check:
    print('''%s\n  DROPS SEEN.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh log)%s''' % (fg(1), attr(0)))
elif log_check:
    print('%s\n  No drops seen%s' % (fg(2), attr(0)))


print('\n Checking interfaces for errors, Please Wait...')
crc = nornir_host.run(
    task=netmiko_send_command,
    command_string='sh run | i CRC'
)
print_result(crc)
if ("0") not in crc:
    print('''%s\n  INTERFACE ERRORS SEEN.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int | i CRC)%s
  ''' % (fg(1), attr(0)))
elif duplex:
    print('%s\n  No issues found%s' % (fg(2), attr(0)))
