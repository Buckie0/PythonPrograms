# -*- coding: utf-8 -*-

# !/usr/bin/env python

import telnetlib
import sys
import getpass

HOST = input("Enter Hostname: ")
user = input("Username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until("login: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")

tn.write("conf t\n")
tn.write("int fa1/0\n")
tn.write("ip address 1.1.1.1 255.255.255.255")
tn.write("end\n")
tn.write("exit\n")
# print tn.read_all()
