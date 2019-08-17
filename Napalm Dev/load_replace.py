# Sample script to demonstrate loading a config for a device.
#
# Note: this script is as simple as possible: it assumes that you have
# followed the lab setup in the quickstart tutorial, and so hardcodes
# the device IP and password.  You should also have the
# 'new_good.conf' configuration saved to disk.
from __future__ import print_function

import napalm
import sys
import os


def render_template():
    file_loader = FileSystemLoader(',')

    env = Environment(loader=file_loader)
    template = env.get_template('eos_config.j2')
    output = template.render()


def main(config_file):
    """Load a config for the device."""

    if not (os.path.exists(config_file) and os.path.isfile(config_file)):
        msg = 'Missing or invalid config file {0}'.format(config_file)
        raise ValueError(msg)

    print('Loading config file {0}.'.format(config_file))

    # Use the appropriate network driver to connect to the device:
    driver = napalm.get_network_driver('eos')

    # Connect:
    device = driver(hostname='127.0.0.1', username='vagrant',
                    password='vagrant', optional_args={'port': 12443})

    print('Opening ...')
    device.open()

    print('Loading config ...')
    device.load_merge_candidate(filename=config_file)

    # Note that the changes have not been applied yet. Before applying
    # the configuration you can check the changes:
    print('\nDiff:')
    diffs = device.compare_config()

    # You can commit or discard the candidate changes.

    if len(diffs) > 0:
        print(diffs)

        choice = input("""\nType COMMIT to commit the confguration changes or hit
ENTER to abort: """)
        if choice == 'COMMIT':
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
        print("No changes ceeded")


def rollback(device):
    choice_rollback = input("""\n type ROLLBACK to rollback or hit
ENTER to save them: """)

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

    # close the session with the device.


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please supply the full path to "new_good.conf"')
        sys.exit(1)
    config_file = sys.argv[1]
    main(config_file)
exit
