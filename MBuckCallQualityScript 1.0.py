#!/usr/bin/env python

import telnetlib
import time
import getpass

if __name__ == "__main__":

    # Request Device and Login details

    print """\n This Program will log onto a Cisco Device and display the data
 needed to diagnose Call Quality Issues \n"""

    Host = raw_input("Enter Host: ")
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    enable = getpass.getpass("Enable: ")

    TELNET_PORT = 23
    TELNET_TIMEOUT = 6
    READ_TIMEOUT = 6

# Establish Telnet Connection

    remote_conn = telnetlib.Telnet(Host, TELNET_PORT, TELNET_TIMEOUT)

# Send credentials to device

    output = remote_conn.read_until("sername:", READ_TIMEOUT)
    remote_conn.write(username + "\n")

    output = remote_conn.read_until("ssword:", READ_TIMEOUT)
    remote_conn.write(password + "\n")

# Enter Enable and disable paging

    time.sleep(1)
    remote_conn.write("\n")
    remote_conn.write("enable \n")
    remote_conn.write(enable + "\n")

    time.sleep(1)
    remote_conn.write("terminal length 0\n")

    print "\n Running Commands...."
    time.sleep(1)

# Run Commands and print to console

    remote_conn.write("sh log \n")
    time.sleep(1)
    output = remote_conn.read_very_eager()
    print output

    remote_conn.write("sh int status \n")
    time.sleep(1)
    output = remote_conn.read_very_eager()
    print output

    remote_conn.write("sh int | i CRC \n")
    time.sleep(1)
    output = remote_conn.read_very_eager()
    print output

    remote_conn.write("sh policy-map int\n")
    time.sleep(1)
    output = remote_conn.read_very_eager()
    print output

    print "\n PINGING CORE, PLEASE WAIT...."

    remote_conn.write("ping vrf VOIP 10.81.253.166 source vlan 250 \n")
    time.sleep(5)
    output = remote_conn.read_very_eager()
    print output

# Close Telnet Session

    remote_conn.close()
