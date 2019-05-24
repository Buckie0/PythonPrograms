from colored import attr, fg

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command

nornir_host = InitNornir(config_file='config.yaml')

# runhost = nornir_host.filter(groups="cisco-ios")

print(nornir_host.inventory.hosts)


def duplex(task):
    print(' Checking Duplex, Please Wait...')
    duplex_check = task.run(
        task=netmiko_send_command,
        command_string='sh int status'
    )
    print_result(duplex_check)
    if "half" in duplex_check.result:
        print('''%s\n  HALF DUPLEX DISCOVERED.
      PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int status)%s
      ''' % (fg(1), attr(0)))
    elif duplex:
        print('%s\n  No issues found%s' % (fg(2), attr(0)))


def logs():
    print('\n Reading Logs, Please Wait...')
    log_check = nornir_host.run(
        task=netmiko_send_command,
        command_string='sh log'
    )
    print_result(log_check)
    if "down" in log_check.result:
        print('''%s\n  DROPS SEEN.
      PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh log)%s''' % (fg(1), attr(0)))
    elif log_check:
        print('%s\n  No drops seen%s' % (fg(2), attr(0)))


def crc():
    print('\n Checking interfaces for errors, Please Wait...')
    crc_check = nornir_host.run(
        task=netmiko_send_command,
        command_string='sh run | i CRC'
    )
    print_result(crc_check)
    if ("0") not in crc_check.result:
        print('''%s\n  INTERFACE ERRORS SEEN.
      PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int | i CRC)%s
      ''' % (fg(1), attr(0)))
    elif duplex:
        print('%s\n  No issues found%s' % (fg(2), attr(0)))


if __name__ == "__main__":
    duplex(nornir_host)
    logs()
    crc()
