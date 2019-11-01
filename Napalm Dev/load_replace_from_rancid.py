import napalm
import sys
from rancid_checker import get_config
import getpass

# Gather user information
comp_code = input('Please input Company Code:')
while not comp_code:
    comp_code = input('Please input Company Code:')

mgmt_ip = input('Please input Management IP: ')
while not mgmt_ip:
    mgmt_ip = input('Please input Management IP: ')

tacacs_user = input('Please input tacacs username: ')
while not tacacs_user:
    tacacs_user = input('Please input tacacs username: ')

tacacs_pass = getpass.getpass('Please input tacacs password: ')
while not tacacs_pass:
    tacacs_pass = getpass.getpass('Please input tacacs password: ')

# Use the appropriate network driver to connect to the device:
driver = napalm.get_network_driver('ios')

# Connect:
device = driver(hostname=mgmt_ip, username=tacacs_user,
                password=tacacs_pass, optional_args={'secret': tacacs_pass})


# Gather config from rancid and create a jinja template
def render_template():
    config_file = get_config(management_ip=mgmt_ip, company_code=comp_code)
    print('Loading config file...')
    config = config_file.split('config-register 0x2102', 1)
    return config[1]


def diff_commit(config_file):
    """Load a config for the device."""
    try:
        print('Opening connection to device...')
        device.open()
    except napalm.base.exceptions.ConnectionException:
        print('Could not connect to device')

    print('Loading config ...')
    device.load_merge_candidate(filename=config_file)

    # Note that the changes have not been applied yet. Before applying
    # the configuration you can check the changes:
    print('\nDiff:')
    diffs = device.compare_config()

    # You can commit or discard the candidate changes.

    if len(diffs) > 0:
        print(diffs)

        choice_commit = input("""\nType COMMIT to commit the configuration changes or hit
ENTER to abort: """)
        if choice_commit == 'COMMIT':
            print('Committing ...')
            try:
                device.commit_config()

            except Exception as inst:
                print('\nAn error occured with the commit')
                print(type(inst))
                sys.exit(inst)
                print()

            else:
                print("Configuration committed")

        else:
            print('Discarding ...')
            device.discard_config()
    else:
        print("No difference found")


def rollback():

    try:
        device.discard_config()
    except Exception as inst:
        print("An error occured with the rollback")
        print(type(inst))
        sys.exit(inst)
        print()

    # close the session with the device.


def main():
    config_file = render_template()
    choice_commit = diff_commit(config_file)
    if choice_commit == 'COMMIT':
        choice_rollback = input("""\n if you are happy with the changes hit ENTER. To rollback type ROLLBACK
    to rollback: """)
        if choice_rollback == 'ROLLBACK':
            print('Rolling Back Changes...')
            rollback()
        else:
            device.close()
            print('Done.')


if __name__ == '__main__':
    main()
