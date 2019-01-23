#!/usr/bin/env python

# Created by Buckie.

import telnetlib
import time
import socket
import cgi
import cgitb; cgitb.enable()

if __name__ == "__main__":

    form = cgi.FieldStorage()

# Request Device IP
# Check input is a valid IP, Error if it isnt and return to prompt.
    Host = form.getvalue('IP')
    Invalidip = 'http://192.168.0.100/InvalidIP'
    try:
        socket.inet_aton(Host)
    except socket.error:
        print("location: %s\r\n\r") % Invalidip
        quit()
    else:
        True
    # If Valid IP is entered try to connect to device.
    # Error if unable to connect and return prompt.
    unabletoconnect = ('http://192.168.0.100/Unabletoconnect')
    try:
        TELNET_PORT = 23
        TELNET_TIMEOUT = 6
        READ_TIMEOUT = 6
        remote_conn = telnetlib.Telnet(Host, TELNET_PORT,
                                       TELNET_TIMEOUT)
    except socket.error:
        print("location: %s\r\n\r") % unabletoconnect
        quit()
    else:
        True
    # Try to connect with Username and Password.
    # If incorrect return prompt.
    username = form.getvalue('username')
    password = form.getvalue('password')
    enterusername = 'http://192.168.0.100/Enterusername'
    try:
        if not username + password:
            raise ValueError
    except ValueError:
        print("location: %s\r\n\r") % enterusername
        quit()
    else:
        True

    output = remote_conn.read_until("sername:", READ_TIMEOUT)
    remote_conn.write(username + "\n")

    output = remote_conn.read_until("ssword:", READ_TIMEOUT)
    remote_conn.write(password + "\n")

    invaliduser = 'http://192.168.0.100/Invaliduser'

    time.sleep(1)
    user = remote_conn.read_very_eager()
    if "failed" in user:
        print("location: %s\r\n\r") % invaliduser
        quit()
    else:
        True

    # Enter Enable
    enable = form.getvalue('enable')
    enterenable = 'http://192.168.0.100/Enterenable'
    try:
        if not enable:
            raise ValueError
    except ValueError:
        print("location: %s\r\n\r") % enterenable
        quit()
    else:
        True

    time.sleep(1)
    remote_conn.write("\n")
    remote_conn.write("enable \n")
    remote_conn.write(enable + "\n")

    time.sleep(1)
    invalidenable = 'http://192.168.0.100/Invalidenable'
    user = remote_conn.read_very_eager()
    if "Error" in user:
        print("location: %s\r\n\r") % invalidenable
        quit()
    else:
        True

    def Webpage(adddrops, duplexdrop):
        print('Content-type: text/html')
        print
        print '<html>'
        print '<head>'
        print '<link rel="stylesheet"'
        print 'type="text/css"'
        print 'href="http://support2.localnet/buckie/styles.css">'
        print '<title>CallQuality</title>'
        print '</head>'
        print '<body>'
        print '<style>'
        print
        print '#background{'
        print 'background-image:'
        print 'url(http://support2.localnet/buckie/Pictures/Mountain.jpg);'
        print 'background-size:cover;'
        print 'width:100%;'
        print 'height:100%;'
        print 'background-position:center;'
        print 'position:fixed;'
        print 'left:0px;'
        print 'top:0px;'
        print '}'
        print
        print '#layer{'
        print 'background-color: black;'
        print 'top: 0;'
        print 'left: 0;'
        print 'width: 100%;'
        print 'height: 100%;'
        print 'opacity: 0.75;'
        print '}'
        print
        print 'form {'
        print 'text-align: center;'
        print 'vertical-align: middle;'
        print '}'
        print
        print '#header h1 {'
        print 'top: -70px;'
        print 'left: 0px;'
        print '}'
        print
        print '#myVideo {'
        print 'position: fixed;'
        print 'right: 0;'
        print 'bottom: 0;'
        print 'min-width: 100%;'
        print 'min-height: 100%;'
        print '}'
        print
        print '</style>'
        print
        print '<div id="background">'
        print '<div id="layer">'
        print '<div id="header">'
        print
        print '<h3 id="Call Quality Script" style="clear:'
        print 'both;font-size: 1.8em;'
        print 'font-weight: bold; margin: 0px 0.85em;color:'
        print 'white;border-bottom-width: 1px;'
        print 'border-bottom-style: solid; border-bottom-color: white;'
        print "line-height: 1.7em;font-family: LeagueGothic, 'Helvetica Neue',"
        print "Helvetica, Arial, sans-serif; font-weight: normal;color: white;"
        print "font-size: 2.7143em; line-height: 1.2em; margin: 0px;"
        print "text-align: center; padding: 0.3em 0px;border-top-style: solid;"
        print "border-top-width: 1px; border-top-color: white;"
        print "border-bottom-style: solid;"
        print "border-bottom-width: 1px;"
        print 'border-bottom-color: rgb(221, 221, 221);">'
        print '<a name="Call Quality Script" href="#Call Quality Script"'
        print 'style="text-decoration: none;'
        print 'vertical-align: baseline;color:'
        print 'white;color: white;transition:'
        print 'color 0.2s ease-in-out; -webkit-transition:'
        print 'color 0.2s ease-in-out; color: white;'
        print 'text-decoration: none;">'
        print '</a>Call Quality Script</h3>'
        print
        print adddrops
        print
        print duplexdrop
        print
        print '</div>'
        print '</div>'
        print '</div>'
        print
        print '</body>'
        print '</html>'

    # Disable paging.
    time.sleep(1)
    remote_conn.write("terminal length 0\n")

# Run Commands, check ouput, then advise.
    # Check Logs
    remote_conn.write("sh log \n")
    time.sleep(1)
    logs = remote_conn.read_very_eager()
    dropspage = """
<p style= "color: red; font-weight: bold;
font-family: Terminus; font-size: 1.3em;
position: absolute; left: 10px">DROPS SEEN.
PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh log)</p>"""
    if "down" in logs:
        print Webpage(dropspage)
    elif logs:
        print ('\n  No drops seen')

    # Check duplex settings on interfaces.
    # Will display error
    remote_conn.write("sh int status \n")
    time.sleep(1)
    print ('\n Checking Duplex, Please Wait...')
    duplex = remote_conn.read_very_eager()
    dupdrop = """
<p style= "color: LawnGreen; font-weight: bold;
font-family: Terminus; font-size: 1.3em;
position: absolute; left: 10px">No Issues Found</p>
        """
    if "half" in duplex:
        print ('''\n  HALF DUPLEX DISCOVERED.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int status)
  ''')
    elif duplex:
        print Webpage(dropspage, dupdrop)

        # Test
    remote_conn.close()
    quit()

    # Check interfaces for CRC's.
    # Will display error if any number other than 0 seen.
    remote_conn.write("sh int | i CRC \n")
    time.sleep(1)
    print ('\n Checking interfaces for errors, Please Wait...')
    crc = remote_conn.read_very_eager()
    if "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" in crc:
        print ('''\n  INTERFACE ERRORS SEEN.
  PLEASE CONNECT TO DEVICE AND INVESTIGATE (sh int | i CRC)
  ''')
    elif duplex:
        print ('\n  No issues found%s')

    # Display Policy-Map.
    remote_conn.write("sh policy-map \n")
    time.sleep(1)
    print ('''\n Checking policy-map...''')
    print ('''\n  This will be displayed below, you will also need to check
  the Core Policy-Map by following the Guide on Sharepoint
  ''')
    time.sleep(2)
    output = remote_conn.read_very_eager()
    print ('\n' + output)

    #  Check vrf and ping the GSX.
    remote_conn.write("sh ip vrf \n")
    print ('''\n Checking vrf information...''')
    time.sleep(1)
    vrf = remote_conn.read_very_eager()
    if "VoIP_2" in vrf:
        print ('\n Pinging GSX, Please Wait...')
        print ('''\n  This will send 1000 pings to the GSX, however you may
  need to run further pings''')
        remote_conn.write("""
        ping vrf VoIP_2 10.81.253.166 source Vlan251 r 1000 \n""")
        time.sleep(12)
        output = remote_conn.read_very_eager()
        print ('\n' + output)
    if "VOIP" in vrf:
        print ('\n Pinging GSX, Please Wait...')
        print ('''\n  This will send 1000 pings to the GSX, however you may
  need to run further pings''')
        remote_conn.write("ping vrf VOIP 10.81.253.166 r 1000 \n")
        time.sleep(12)
        output = remote_conn.read_very_eager()
        print ('\n' + output)
    elif "VoIP" in vrf:
        print ('\n Pinging GSX, Please Wait...')
        print ('''\n  This will send 1000 pings to the GSX, however you may
  need to run further pings ''')
        remote_conn.write("ping vrf VoIP 10.81.253.166 r 1000 \n")
        time.sleep(12)
        output = remote_conn.read_very_eager()
        print ('\n' + output)
    elif vrf:
        print ('''\n Unable to find a VOIP vrf.
  PLEASE LOG ONTO DEVICE AND CHECK WHAT VRF IS IN USE (sh ip vrf)''')

# Close Telnet Session.

    remote_conn.close()
    print ('''\n  Goodbye.
  For further information, check the guides on Sharepoint.
  ''')
