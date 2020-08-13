# $language = "python"
# $interface = "1.0"

import re
import datetime
import getpass
import os, sys, ast


def SSIDDEL():
    path = os.path.abspath(os.path.dirname(__file__))
    writefile = path + '\\' + 'removessidSTAT.txt'
    f = open(path + '\\' + 'info.txt','r')
    info = f.readlines()
    username = info[0]
    pwd = info[1]
    f.close()

    f = open(path+'\\removessid.txt', 'r+')
    rssid = f.read()
    rssid = rssid.replace('\n', '')
    rssid = rssid.replace('][', '],[')
    rssid = ast.literal_eval(rssid)

    username = info[0]
    pwd = info[1]

    hosts = ["172.16.255.11","172.16.255.12","172.16.255.13","172.16.255.14"]     

    for host in hosts:
        cmd = "/SSH2 /L %s /PASSWORD %s %s" % (username, pwd, host)
        crt.Session.Connect(cmd)
        crt.Screen.WaitForString(":")
        crt.Screen.Send(username)
        crt.Screen.WaitForString(":")
        crt.Screen.Send(pwd)
        for wid in rssid:
            crt.Screen.WaitForString(">")
            to_send = "config wlan delete " + str(wid) + chr(13)
            crt.Screen.Send(to_send)
            crt.Screen.Send("y" + chr(13))
            crt.Screen.WaitForString("y")
        crt.Session.Disconnect()
try:
        SSIDDEL()
        crt.Session.Disconnect()
except:
    pass
finally:
    crt.Quit()
