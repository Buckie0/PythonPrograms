"""This module contains functions to handle the upgrade of.
"""
from netmiko import ConnectHandler, FileTransfer
import logging
import time
import re

logger = logging.getLogger(__name__)


def net_file_transfer(file_to_transfer, shelf_selection):
    """Utilises the Netmiko file transfer module to SCP a file to the device.

    file_to_transfer: file to transfer to the device, netmiko will check if the file exists, check that there is enough
    space and then transfer the file to the device.

    shelf_selection (Optional): used to pass shelf selection information from router build script.
    """
    ios_source_file = '/home/networksupport/website/website/media/' + file_to_transfer
    destination_file = file_to_transfer.split('ssip_operating_system/', 1)
    device = {
        'device_type': 'cisco_ios',
        'host': shelf_selection['router_ip'],
        'username': 'bustradius',
        'password': 'unreliable',
    }

    # Create the Netmiko SSH connection
    ssh_conn = ConnectHandler(**device)
    logger.info(f"transfering {destination_file[1]} to {shelf_selection['router_ip']}")
    with FileTransfer(ssh_conn,
                      source_file=ios_source_file,
                      dest_file=destination_file[1],
                      file_system='flash:'
                      ) as scp_transfer:

        if not scp_transfer.check_file_exists():
            logger.info('IOS meets current SSIP standard')
            if not scp_transfer.verify_space_available():
                logger.critical("Insufficient space available on remote device")

        logger.info("New IOS copied to device - Verifying file")
        if scp_transfer.verify_file():
            logger.info("Source and destination MD5 matches")

        else:
            logger.critical("MD5 failure between source and destination files")

    return ssh_conn, destination_file


def reload_device(ssh_conn, destination_file, current_firmware):
    """Applies the new IOS file to boot and reloads the router.

    ssh_conn: netmiko device parameters.

    destination_file: file to set the system boot to.
    """

    # Delete the old Firmware
    logger.info('Deleting old firmware')
    ssh_conn.send_commmand(f'delete flash:{current_firmware}')

    # Add new IOS file to boot.
    logger.info('Adding new IOS to boot')
    set_boot_image = f"""
    default boot system
    boot system flash {destination_file[1]}
    """
    set_boot_image_list = set_boot_image.strip().splitlines()
    ssh_conn.send_config_set(config_commands=set_boot_image_list)

    time.sleep(1)
    ssh_conn.write_channel('wr mem')
    time.sleep(4)

    logger.info('Reloading device, sleeping until the device returns')
    ssh_conn.write_channel('reload in 1\r')
    ssh_conn.read_until_pattern('[confirm]')
    ssh_conn.write_channel('\r')
    time.sleep(120)


def return_current_firmware_filename(ssh_conn):
    logger.info('Gathering current IOS file')
    output = ssh_conn.send_command("show version")
    current_firmware_filename = re.search(r"System image file is.+?(?<=\.bin)", output).group(0)
    current_firmware = re.split(":", current_firmware_filename)[1]
    return current_firmware
