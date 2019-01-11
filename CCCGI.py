#!/usr/bin/python

import cgi, cgitb

form = cgi.FieldStorage()

IP = form.getvalue('IP')
username = form.getvalue('username')
password = form.getvalue('password')
enable = form.getvalue('enable')

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Hello</title>'
print '</head>'
print '<body>'
print '<h2>Your Details are %s %s %s %s</h2>' % (IP, username, password, enable)
print '</body>'
print '</html>'

