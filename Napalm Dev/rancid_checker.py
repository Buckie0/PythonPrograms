"""
This module contains a series of functions for managing RANCID, or utilising features of RANCID.
"""
import requests


def get_config(management_ip, company_code):
    """
    This function takes a management IP and company code as an argument and retrieves the most recent configuration
    held for this device on RANCID.

    If a valid RANCID configuration was retrieved, it will return this. If non config was retrieved, it will return
    None.
    """
    rancid_url = 'http://rancid.localnet/viewvc/%s/configs/%s?rev=HEAD' % (company_code, management_ip)
    page_data = requests.get(rancid_url)
    config = page_data.content.decode()

    if 'RANCID-CONTENT-TYPE' in config:
        return config

    return None
