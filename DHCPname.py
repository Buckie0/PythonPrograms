#!/usr/bin/env python

# Created by Buckie.

import telnetlib
import time
import getpass
import socket
import csv

if __name__ == "__main__":

    print("""\n This Program will log onto a Cisco Device and collect its
                DHCP pool details. \n""""")

# Request Device IP
    Host = raw_input("Enter CE IP: ")
    # Check input is a valid IP, Error if it isnt and return to prompt
    while True:
        try:
            socket.inet_aton(Host)
        except socket.error:
            print("Please Enter a Valid IP!")
            Host = raw_input("Enter CE IP: ")
            continue
        else:
            break
            # If Valid IP is entered break loop and try to connect to device
            # if unable to connect return error.
    while True:
        try:
            TELNET_PORT = 23
            TELNET_TIMEOUT = 6
            READ_TIMEOUT = 6
            remote_conn = telnetlib.Telnet(Host, TELNET_PORT,
                                           TELNET_TIMEOUT)
        except socket.error:
            print("Unable to Connect to device, please check device IP")
            Host = raw_input("Enter CE IP: ")
            continue
    # If the device is up, request login details
    # Then send username and password.
        else:
            username = raw_input("Username: ")
            password = getpass.getpass("Password: ")
            enable = getpass.getpass("Enable: ")
        print("""
       ,-----.
     ,'       `.
    :           :
    :CONNECTING!:
    '.         ,'
      `._____,'
          ||
        _,''--.    _____
       (/ __   `._|
      ((_/_)\     |
       (____)`.___|
        (___)____.|_____
          ||
        _\||/_
""")
        break

    output = remote_conn.read_until("sername:", READ_TIMEOUT)
    remote_conn.write(username + "\n")

    output = remote_conn.read_until("ssword:", READ_TIMEOUT)
    remote_conn.write(password + "\n")

# Enter Enable and Disable paging.

    time.sleep(1)
    remote_conn.write("\n")
    remote_conn.write("enable \n")
    remote_conn.write(enable + "\n")

    time.sleep(1)
    remote_conn.write("terminal length 0\n")

    print("\n Gathering DHCP Pool name and saving to file")
    time.sleep(1)

# Run Commands and print to console.
    # Check DHCP Pool information and write to csv file
    remote_conn.write("sh run | i ip dhcp pool \n")
    time.sleep(1)
    output = remote_conn.read_very_eager()
    file = open('DHCPpool.csv', 'wb')
    writer = csv.writer(file)
    file.close()

# Close Telnet Session.

    remote_conn.close()
