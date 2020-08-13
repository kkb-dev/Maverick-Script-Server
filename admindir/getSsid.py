# $language = "python"
# $interface = "1.0"

import re
import datetime
import getpass
import os

try: 
    macdict = {}

    path = os.path.abspath(os.path.dirname(__file__))
    writefile = path + '\\' + 'ssidlist.txt'

    f = open(path + '\\' + 'info.txt','r')
    info = f.readlines()
    username = info[0]
    pwd = info[1]
    f.close()

    hosts = ["172.16.255.11","172.16.255.12","172.16.255.13","172.16.255.14"]

    # Open four controllers simultaneously
    crt.Session.ConnectInTab("/S 172.16.255.11 /S 172.16.255.12 /S 172.16.255.13 /S 172.16.255.14")
    for x in range(1,5):
        host = '172.16.255.1' + str(x)
        if host == "172.16.255.11":
            f = open(writefile,"w+")
            f.write('\n'+host+'\n')
            f.close()
        else:
            f = open(writefile,"a+")
            f.write('\n'+host+'\n')
            f.close()
            
        objTab = crt.GetTab(x)
        objTab.Screen.Synchronous = True
        objTab.Activate()
        
        if objTab.Session.Connected == True:
            objTab.Screen.Synchronous = True
            objTab.Screen.Send(username)
            objTab.Screen.WaitForString("Password:")
            objTab.Screen.Send(pwd)
            
            objTab.Screen.WaitForString(">")
            objTab.Screen.Send("show wlan summary" + chr(13))
            stats = objTab.Screen.ReadString(")")
            #crt.Dialog.MessageBox(stats)
            objTab.Screen.WaitForString("uit")
            try:
                f = open(writefile,"a+")
                f.write(str(stats))
                f.close()
            except IOError as e:
                pass

            n = True
            while n:
                objTab.Screen.Send(" ")
                stats = objTab.Screen.ReadString(")")
                f = open(writefile,"a+")
                f.write(str(stats))
                f.close()
                if "like to display the next" in str(stats):
                  n = True
                else:
                  n = False
                  
            objTab.Session.Disconnect()

              
    # Parse file
    f = open(writefile,"r")
    lines = f.readlines()
    f.close()
    f = open(writefile,"w+")
    for line in lines:
        if "172.16.255.1" in line:
            line = '\n' + line + '\n'
            f = open(writefile,"a")
            f.write(line)
            f.close
        if "enabled" in line.lower() or "disabled" in line.lower():
            f = open(writefile,"a")
            f.write(line)
            f.close

    host = ''
    f = open(writefile,'r')
    macs = f.readlines()
    for mac in macs:
        if mac != '\n':
            mac = mac.replace('\n','')
            if "172.16.255.1" in mac:
                host = mac[-1:]
            else:
                if mac not in macdict:
                    macdict[mac] = "" + host
                else:
                    value = macdict.get(mac)
                    macdict[mac] = value + host

    f = open(writefile,'w')
    time = 'Last Updated: ' + str(datetime.datetime.now())
    f.write(time+'\n')
    f.close()
    f = open(writefile,'a+')
    for x,y in macdict.items():
        for value in range(4-len(y)):
            y = str(y) + '-'
        z = y + ' || ' + x 
        f.write(z)
    f.close()
        
    crt.Session.Disconnect()
except:
    pass
finally:
    crt.Quit()
