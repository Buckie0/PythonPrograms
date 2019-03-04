from nornir.core import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from colored import fg, attr

nornir_host = InitNornir(config_file='config.yaml')

print(nornir_host.inventory.hosts)
# print('\n Checking Duplex, Please Wait...')
# duplex = nornir_host.run(
#     task=netmiko_send_command,
#     command_string='sh int status'
# )
# if "half" in duplex:
#     print('''%s\n  HALF DUPLEX DISCOVERED.
#   PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int status)%s
#   ''' % (fg(1), attr(0)))
# elif duplex:
#     print('%s\n  No issues found%s' % (fg(2), attr(0)))

# print_result(duplex)
