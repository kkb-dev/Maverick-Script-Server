# $language = "python"
# $interface = "1.0"

import re
import datetime
import getpass
import os, sys, ast

try:
    path = os.path.abspath(os.path.dirname(__file__))
    writefile = path + '\\' + 'removemacSTAT.txt'
    f = open(path + '\\' + 'info.txt','r')
    info = f.readlines()
    username = info[0]
    pwd = info[1]
    f.close()

    f = open(path+'\\removemac.txt', 'r+')
    rmac = f.read()
    rmac = rmac.replace('\n', '')
    rmac = rmac.replace('][', '],[')
    rmac = ast.literal_eval(rmac)

    hosts = ["172.16.255.11","172.16.255.12","172.16.255.13","172.16.255.14"]
        
    for host in hosts:
        try:
            crt.Session.Disconnect()
        finally:
            cmd = "/SSH2 /L %s /PASSWORD %s %s" % (username, pwd, host)
            crt.Session.Connect(cmd)
            crt.Screen.WaitForString(":")
            crt.Screen.Send(username)
            crt.Screen.WaitForString(":")
            crt.Screen.Send(pwd)
            for mac in rmac:
                mac = mac[8:25]
                crt.Screen.WaitForString(">")
                crt.Screen.Send("config macfilter delete "+ str(mac) + chr(13))
            crt.Session.Disconnect()

    crt.Session.Disconnect()
except:
    pass
finally:
    crt.Quit()



