# $language = "python"
# $interface = "1.0"

import os, sys, ast
import getpass
import datetime

dic = {}
path = os.path.abspath(os.path.dirname(__file__))

writefile = path + '\\' + 'addmacSTAT.txt'
f = open(path + '\\' + 'info.txt','r')
info = f.readlines()
username = info[0].rstrip()
pwd = info[1].rstrip()
f.close()

f = open(path+'\\addmac.txt', 'r+')
addmac = f.read()
addmac = addmac.replace('\n', '')
addmac = addmac.replace('][', '],[')
addmac = ast.literal_eval(addmac)
addmacdata = addmac[0]
macs = addmac[1]
show_name = str(addmacdata[0])
booth_num = str(addmacdata[1])
WID = str(addmacdata[2])
desc = show_name + ' ' +  booth_num
prompt = ">"
f = open(path + '\\addmacDATA.txt','w+')
f.write('')
f.close()

# Open four controllers simultaneously
crt.Session.ConnectInTab("/S 172.16.255.11 /S 172.16.255.12 /S 172.16.255.13 /S 172.16.255.14")
for x in range(1,4+1):
    host = '172.16.255.1' + str(x)

    objTab = crt.GetTab(x)
    objTab.Screen.Synchronous = True
    objTab.Activate()
    
    if objTab.Session.Connected == True:
        objTab.Screen.Synchronous = True
        f = open(path + '\\addmacDATA.txt','a+')
        f.write('\n'+host+'\n')
        f.close()
        objTab.Screen.Send(username + '\n')
        objTab.Screen.WaitForString("Password:")
        objTab.Screen.Send(pwd + '\n')
        objTab.Screen.WaitForString(">")
        for mac in macs:
            mac = mac.replace('-',':')
            if mac != "":      
                cmd = ("config macfilter add %s %s vlan207 '%s'" + chr(13)) % (mac, WID, desc)
                objTab.Screen.Send(cmd)
                errcode = objTab.Screen.ReadString(prompt)
                if "already exists" in errcode or "Incorrect input" in errcode:
                    try:
                        x = dic[mac]
                    except:
                        x = ""
                    dic[mac] = x + ""
                    f = open(path + '\\addmacDATA.txt','a+')
                    mac = mac + errcode + '\n'
                    f.write(mac)
                    f.close()
                else:
                    try:
                        x = dic[mac]
                    except:
                        x = ""
                    dic[mac] = x + host[-1:]
                    
                    f = open(path + '\\addmacDATA.txt','a+')
                    mac = mac + '\nSuccess!\n'
                    f.write(mac)
                    f.close()
        objTab.Session.Disconnect()

f = open(writefile,"w+")
f.write('')
f = open(writefile,"a+")
for x,y in dic.items():
    item = x + ',' + y
    item = str(item).replace('(','')
    item = item.replace(')','')
    item = item.replace('\'','')
    f.write(item+'\n')
f.close()
crt.Quit()            
