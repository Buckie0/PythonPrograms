# Created by Buckie.

import telnetlib
import time
import getpass
import socket
import os

if __name__ == "__main__":

    print('''\n This Program will log onto a Cisco device and display
                dignostic information. \n''')

# Request Device IP
# Check input is a valid IP, Error if it isnt and return to prompt.
    while True:
        Host = input('Enter CE IP: ')
        while True:
            try:
                socket.inet_aton(Host)
            except socket.error:
                print(' Please Enter a Valid IP! %s')
                Host = input('Enter CE IP: ')
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
            print('Unable to Connect to device, please check device IP')
            continue
        else:
            break
# Try to connect with Username and Password.
# If incorrect return prompt.
    while True:
        while True:
            username = input('Username: ')
            password = getpass.getpass('Password: ')
            try:
                if not username + password:
                    raise ValueError
            except ValueError:
                print(' Please Enter Login Credentials')
                continue
            else:
                break

        output = remote_conn.read_until('sername:', READ_TIMEOUT)
        remote_conn.write(username + "\n")

        output = remote_conn.read_until('ssword:', READ_TIMEOUT)
        remote_conn.write(password + "\n")

        time.sleep(1)
        user = remote_conn.read_very_eager()
        if "failed" in user:
            print(' Invalid Username or Password!')
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
                               "?$$$c,`!!!BUCKIE0!!!;`'`
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
            enable = getpass.getpass('Enable: ')
            try:
                if not enable:
                    raise ValueError
            except ValueError:
                print(' Please Enter Enable Password.')
                continue
            else:
                break

        time.sleep(1)
        remote_conn.write("\n")

        remote_conn.write('enable \n')
        remote_conn.write(enable + '\n')

        time.sleep(1)
        user = remote_conn.read_very_eager()
        if "Error" in user:
            print(' Invalid Enable password!')
            continue
        else:
            break

# The below can all be adjusted depending on your needs

# Clear screen, then print reading logs
    os.system('clear')  # this will need to be removed if using Windows
    print('\n Reading Logs, Please Wait...')

# Disable paging.
    time.sleep(1)
    remote_conn.write('terminal length 0\n')

# Run Command function


def command(com):
    remote_conn.write('com \n')
    time.sleep(1)
    print('''\n Checking...''')
    print('\n Results will be displayed below.')
    time.sleep(2)
    output = remote_conn.read_very_eager()
    return'\n' + output

# Call function wiith your variable

print(command('sh log'))

# Close Telnet Session.

remote_conn.close()
print('\n  Goodbye.')
