#!/usr/bin/env python

import os

URL = input("Enter URL:")

os.system("host -t SRV _sip._tcp." + URL)
