#!/usr/bin/env python

# Created by Buckie.

import telnetlib
import time
import getpass
import socket
import os

if __name__ == "__main__":

    print('''\n This Program will log onto a Cisco Device and display the
        data needed to diagnose Call Quality Issues \n''')

# Request Device IP
# Check input is a valid IP, Error if it isnt and return to prompt.
    while True:
        Host = input("Enter CE IP: ")
        while True:
            try:
                socket.inet_aton(Host)
            except socket.error:
                print(' Please Enter a Valid IP!')
                Host = input("Enter CE IP: ")
                continue
            else:
                break
# If Valid IP is entered try to connect to device.
# Error if unable to connect and return prompt.
        try:
            TELNET_PORT = 23
            TELNET_TIMEOUT = 6
            READ_TIMEOUT = 6
            remote_conn = telnetlib.Telnet(Host, TELNET_PORT,
                                           TELNET_TIMEOUT)
        except socket.error:
            print(''' Unable to Connect to device, please check device IP
                  ''')
            continue
        else:
            break
# Try to connect with Username and Password.
# If incorrect return prompt.
    while True:
        while True:
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            try:
                if not username + password:
                    raise ValueError
            except ValueError:
                print(''' Please Enter Login Credentials
                      ''')
                continue
            else:
                break

        output = remote_conn.read_until("sername:", READ_TIMEOUT)
        remote_conn.write(username + "\n")

        output = remote_conn.read_until("ssword:", READ_TIMEOUT)
        remote_conn.write(password + "\n")

        time.sleep(1)
        user = remote_conn.read_very_eager()
        if "failed" in user:
            print(''' Invalid Username or Password!
                  ''')
            continue
        else:
            break

    print("""
                       .,;;<<!!!>>;;,
                   ,;;!!!!!!!!!!!!!!!!!>,
               ,;<!!!!!!!!!!!!!!!!!!!!!!!>                       .,,,,.
           ,;<!!!!!!!!!!!!!!!!!!!!!!!!!!!!>                 .,cd$$$$$$$
         ,!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!             ,d$$$$$$$$$$$$'
       ,!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'         ,z$$$$$$$$$$$$$$$'
      ;!!!!!!!!!!!!!!''`,;!!!!!!!!!!!!!!!'       ,c$$$$$$$$$$$$$$$$P
      `<!!!!!!!'''  ,<!!!!!!!!!!!!!!!!!!!      c$$$$$$$$$$$$$$$$$$"
                  ;!!!!!!!!!`<!!!!!!!!!     ,z$$$$$$$$$$$$$$$$$$F
                 `!!!!!!`  :!!!!'`!!!!     ,$$$$$$$$$$$$$$$$$$P"
                               ;!!!!'    ,$$$$$$$$$$$$$$$$$$$"
                              ;!!!'    ,c$$$$$$$$$$$$$$$$$P"
                             <!!!     ,$$$$$$$$$$$$$$$$$P"
                           ,<!!'     c$$$$$$$$$$$$$$$$P"   .,zcc$$$$$$$P
                         ,;!!!'     J$$$$$$$$$$$$$$$P" ,zd$$$$$$$$$$$P"
                       ,;!!!!'      $$$$$$$$$$$$$P",d$$$$$$$$$$$$$P""
                  ,;!!!!!!!!(       ?$$$$$$$$$$F,z$$$$$$$$$$$$$P"
              ,c,`!'',cc,``!!!       $$$$$$$$$$$$$$$$$$$$$$P"
            c$$$F c$$$$$$$  !!!>      "$$$$$$$$$$$$$$$PP"      .,,,.
          ,$$$$"d$$$$$$$$$  !!!>       `?$$$$$$$$P"",cccd$$$$$$$$$$$$$$
         d$$$F $$$$$$$$$$P ;!!!!         "$$$$$$$$$$$$$$$$$$$$$$$$$""
        d$$$F,$$$$$$$$$$$";!'``,,          $$$$$$$$$$$$$$$$PP""
 ,zd$$$c,`?? ?$$$$$$$$$$" ,zc$$$$$c,        "$$$$$$$$C,,.
d$$$$$$$$$c    `$$$$$P",c$$$$$$$$$$F         `$$$$$$$$$$$$bc,
d$$$$$$$$$$c    $$PF,cd$$$$$$$$$$$F           `$$$$$$,"$$$$$$c
`$$$$$$$$$$$$,. `,zc$F,,=<cc$$$P"              ?$$$$$$  "" ????
 "$$$$$$$$$$$$$$$$$$$$$"J$$P""                 `$$$$$F
   ?$$$$$$$$$$$$$$$$$P" ".,                     ?$$$$"
     "?$$$$$$$$$$$PF",c$$$$b                    `""3$
       z.. ""        ?$$$$$$b              ,cd$$$$$P"  ,;;!
       $$F$$$F         "$$$$$$c        ,c$$$$$""  :<`;!!!!
       ?$$$$$$           `?$$$$bc     c$$$$F,;!`;!!!!!!!'
        `"?$P"              `?$$$$c,-",;;<<<<<<,`<!!!!'
                               "?$$$c,`!!!Buckie!!!;`'`
                                  "?$$c,`<!!!!!'',/
                                    "??$$c,.,,cP"/
          CONNECTING...                   `"".,cd
           Beep Beep                      "$FJ$$"
                                           $FJ$$
                ..,,,..                    3FJ$
            ,c$$$$$$$$$$,?$c=cc            ? J$
           d$$$$$P"'ccccccccc`"" ?$$$$$$$$$- ,z,
         ,$$$$$",x$$$$$$$$$$$$$$$$$$ccccr,cJ \`?$$bccr,,c=.,cc , ..
         `?$$$',$$$$$$$$$$$$$$$PPP",ccd$$""  "`$bcc,-4",c$P),c$$$$c"$c,
        J$bc,,.`"??????"",,ccccdddPP""         `$$$$$$cc,-4$$$$$$$$bc"$b,
         "?$$$$$$$$$$$$$$$$PPP""                \`$$$$$$$$bc"?$$$$$$$$ $$",
            $$$$$$$$$$$$PPP                     $`?$$$$$$$$$c"$$$$$$P ,zd$
                                                `bc"$$$$$$$$$,$$P"',c$$$$$
                                                 "?$c,""???"".,c$$$$$$$$P"
                                                   "$$$$$$$$$$$$$$$$$P"
                                                     `??$$$$$$PPP"
""")

# Enter Enable
    while True:
        while True:
            enable = getpass.getpass("Enable: ")
            try:
                if not enable:
                    raise ValueError
            except ValueError:
                print(''' Please Enter Enable Password.
                       ''')
                continue
            else:
                break

        time.sleep(1)
        remote_conn.write("\n")
        remote_conn.write("enable \n")
        remote_conn.write(enable + "\n")

        time.sleep(1)
        user = remote_conn.read_very_eager()
        if "Error" in user:
            print('%s Invalid Enable password! %s')
            continue
        else:
            break

# Clear screen, then print
    os.system("clear")
    print('\n Reading Logs, Please Wait...')

# Disable paging.
    time.sleep(1)
    remote_conn.write("terminal length 0\n")

# Run Commands, check ouput, then advise.
    # Check Logs
    remote_conn.write("sh log \n")
    time.sleep(1)
    logs = remote_conn.read_very_eager()
    if "down" in logs:
        print('''\n  DROPS SEEN.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh log)''')
    elif logs:
        print('\n  No drops seen')

    # Check duplex settings on interfaces.
    # Will display error
    remote_conn.write("sh int status \n")
    time.sleep(1)
    print('\n Checking Duplex, Please Wait...')
    duplex = remote_conn.read_very_eager()
    if "half" in duplex:
        print('''\n  HALF DUPLEX DISCOVERED.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int status)
  ''')
    elif duplex:
        print('\n  No issues found')

    # Check interfaces for CRC's.
    # Will display error if any number other than 0 seen.
    remote_conn.write("sh int | i CRC \n")
    time.sleep(1)
    print('\n Checking interfaces for errors, Please Wait...')
    crc = remote_conn.read_very_eager()
    if "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" in crc:
        print('''\n  INTERFACE ERRORS SEEN.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int | i CRC)
  ''')
    elif duplex:
        print('\n  No issues found%s')

    # Display Policy-Map.
    remote_conn.write("sh policy-map \n")
    time.sleep(1)
    print('''\n Checking policy-map...''')
    print('''\n  This will be displayed below, you will also need to check
  the Core Policy-Map by following the Guide on Sharepoint
  ''')
    time.sleep(2)
    output = remote_conn.read_very_eager()
    print('\n' + output)

    #  Check vrf and ping the GSX.
    remote_conn.write("sh ip vrf \n")
    print('''\n Checking vrf information...''')
    time.sleep(1)
    vrf = remote_conn.read_very_eager()
    if "VoIP_2" in vrf:
        print('\n Pinging GSX, Please Wait...')
        print('''\n  This will send 1000 pings to the GSX, however you may
  need to run further pings''')
        remote_conn.write("""
        ping vrf VoIP_2 10.81.253.166 source Vlan251 r 1000 \n""")
        time.sleep(12)
        output = remote_conn.read_very_eager()
        print('\n' + output)
    if "VOIP" in vrf:
        print('\n Pinging GSX, Please Wait...')
        print('''\n  This will send 1000 pings to the GSX, however you may
  need to run further pings''')
        remote_conn.write("ping vrf VOIP 10.81.253.166 r 1000 \n")
        time.sleep(12)
        output = remote_conn.read_very_eager()
        print('\n' + output)
    elif "VoIP" in vrf:
        print('\n Pinging GSX, Please Wait...')
        print('''\n  This will send 1000 pings to the GSX, however you may
  need to run further pings ''')
        remote_conn.write("ping vrf VoIP 10.81.253.166 r 1000 \n")
        time.sleep(12)
        output = remote_conn.read_very_eager()
        print('\n' + output)
    elif vrf:
        print('''\n Unable to find a VOIP vrf.
  PLEASE LOG ONTO DEVICE AND CHECK WHAT VRF IS IN USE (sh ip vrf)''')

# Close Telnet Session.

    remote_conn.close()
    print('''\n  Goodbye.
  For further information, check the guides on Sharepoint.
  ''')
