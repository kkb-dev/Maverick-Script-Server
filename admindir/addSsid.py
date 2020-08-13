# $language = "python"
# $interface = "1.0"

import os, ast
import random
import getpass
import datetime

dict = {}
path = os.path.abspath(os.path.dirname(__file__))
prompt = ') >'

# Login Info
f = open(path+'\\info.txt','r')
info = f.readlines()
username = info[0].rstrip()
pwd = info[1].rstrip()
f.close()


# SSID Info
f = open(path + '\\'+ 'addssid.txt', 'r')
addssid = f.read()
f.close()
addssid = addssid.replace('\n', '')
addssid = addssid.replace(']["', ',')
addssid = addssid.replace('"][', ',')
addssid = addssid.replace('"', '')
addssid = ast.literal_eval(addssid)
APgroup = addssid[6:99]
SSID = addssid[1]
wpaPASS = addssid[2]
inter = 'vlan' + str(addssid[3])
try:
    wID = int(addssid[4])
except:
    wID = 0
radio2 = '1'
radio5 = '1'
frequency = str(addssid[5])

# Assign Frequency
if '1' in frequency and '2' in frequency:
    radio2 = '1'
    radio5 = '1'
else:
    if '1' in frequency:
        radio2 = '1'
        radio5 = '0'
    else:
        radio5 = '1'
        radio2 = '0'

ENABLED= True
Interface=inter

if (wID) > 99:
    wID = str(wID)
else:
    wID= str(random.randint(121,512))

# Open four controllers simultaneously
crt.Session.ConnectInTab("/S 172.16.255.11 /S 172.16.255.12 /S 172.16.255.13 /S 172.16.255.14")

results = ''

for x in range(1,5):
    host = '172.16.255.1' + str(x)
    results = results + '\n' + host + '\n'

    objTab = crt.GetTab(x)
    objTab.Screen.Synchronous = True
    objTab.Activate()
    
    if objTab.Session.Connected == True:
        objTab.Screen.Synchronous = True
        objTab.Screen.Send(username + '\n')
        objTab.Screen.WaitForString("Password:")
        objTab.Screen.Send(pwd + '\n')
        
        objTab.Screen.WaitForString(">")

        objTab.Screen.Send("config wlan create %s '%s'\n" % (wID, SSID) )
        if (objTab.Screen.ReadString(prompt).find("already in use") > -1):
            objTab.Session.Disconnect()
            results = results + 'WLAN Identifier or Profile Name already in use.\n'
        else:
            if radio2 == "1" and radio5 == "1":
                objTab.Screen.Send("config wlan radio %s all\n" % (wID) )
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data
            elif radio2 == "1" and radio5 == "0":
                objTab.Screen.Send("config wlan radio %s 802.11bg\n" % (wID) )
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data
            else:
                objTab.Screen.Send("config wlan radio %s 802.11a-only\n" % (wID) )
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data
            
            objTab.Screen.Send("config wlan interface %s %s\n" % (wID, Interface) )
            data = objTab.Screen.ReadString(prompt)
            results = results + '\n'+data

            objTab.Screen.Send("config wlan security wpa akm 802.1x disable %s\n" % (wID) )
            data = objTab.Screen.ReadString(prompt)
            results = results + '\n'+data

            if wpaPASS=="":
                objTab.Screen.Send("config wlan security wpa disable %s\n" % (wID))
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data
            else:
                objTab.Screen.Send("config wlan security wpa wpa2 ciphers aes enable %s\n" % (wID) )
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data
                objTab.Screen.Send("config wlan security wpa akm psk enable %s\n" % (wID) )
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data
                objTab.Screen.Send("config wlan security wpa akm psk set-key ascii '%s' %s\n" % (wpaPASS, wID) )
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data
                objTab.Screen.Send("config wlan security wpa wpa2 enable %s\n" % (wID) )
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data

            objTab.Screen.Send("config wlan chd %s disable\n" % (wID) )
            data = objTab.Screen.ReadString(prompt)
            results = results + '\n'+data
            
            if ENABLED:
                objTab.Screen.Send("config wlan enable %s\n" % (wID) )
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data

            for AP in APgroup:
                AP=AP.rstrip()
                command = ("config wlan apgroup interface-mapping add %s %s %s\n" % (AP, wID, inter))
                objTab.Screen.Send(command)
                data = objTab.Screen.ReadString(prompt)
                results = results + '\n'+data
            objTab.Screen.Send("save config\n")
            objTab.Screen.ReadString("(y/n)")
            objTab.Screen.Send("y")
            objTab.Session.Disconnect()

            try:
                x = dict[SSID]
            except Exception as e:
                x = ""
            dict[SSID] = x + host[-1:]


writefile = path + '\\' + 'addssidSTAT.txt'
f = open(writefile,"w+")
f.write('')
f = open(writefile,"a+")
for x,y in dict.items():
    item = x + ',' + y
    f.write(item+'\n')
    
writefile = path + '\\' + 'addssidDATA.txt'
f = open(writefile,"w+")
f.write('')
f.write(results)
f.close()              
        
crt.Quit()


