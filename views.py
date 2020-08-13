from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from ast import literal_eval
import os, time, pyodbc
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@login_required(redirect_field_name='/accounts/login/')
def info(request):
    context = {}
    return render(request, 'accounts/info.html', context)

def killremovemac(request):
    if request.user.is_authenticated:
        try:
            username = request.user.username
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\removemac.txt')
        except:
            pass
        return redirect('/')
    else:
        return redirect('/accounts/login/')

def killremovessid(request):
    if request.user.is_authenticated:
        try:
            username = request.user.username
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\removessid.txt')
        except:
            pass
        return redirect('/')
    else:
        return redirect('/accounts/login/')

def killaddssid(request):
    if request.user.is_authenticated:
        try:
            username = request.user.username
            os.remove('C:\\webs\\mysite\\tempinfo\\'+username+'dir\\addssid.txt')
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addssidDATA.txt')
        except:
            pass
        return redirect('/')
    else:
        return redirect('/accounts/login/')

def killaddmac(request):
    if request.user.is_authenticated:
        try:
            username = request.user.username
            os.remove('C:\\webs\\mysite\\tempinfo\\'+username+'dir\\addmac.txt')
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addmacDATA.txt')
        except:
            pass
        return redirect('/')
    else:
        return redirect('/accounts/login/')


def launchscripts(request):

    if request.user.is_authenticated:
        username = request.user.username

        # Deletes Results info of previous scripts
        try:
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addmacDATA.txt')
        except:
            pass
        try:
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addssidDATA.txt')
        except:
            pass
        try:
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\removemacDATA.txt')
        except:
            pass
        try:
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\removessidDATA.txt')
        except:
            pass
        
        sqlconn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=nyccoc-sql-02;DATABASE=ShowDB;UID=ShowDBuser;PWD=zQ+GZ*[z!EtCXv5)')
        cur = sqlconn.cursor()

        # Remove MAC
        try:
            f = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\removemac.txt')
            data = f.readline()
            f.close()
            os.system("SecureCRT.exe /Script C:\\webs\\mysite\\tempinfo\\" + username + "dir\\removeMac.py")

            millis = int(round(time.time() * 1000))
            id = username + str(millis)

            sql = "INSERT INTO [dbo].[global] ([show],[username],[script],[action]) VALUES(NULL,'" + username + "','Remove MAC','" + id + "')"
            cur.execute(sql)
            print(sql)

            data = literal_eval(data)
            macs = ''
            for x in data:
                macs += x[8:25] + ','

            sql = "INSERT INTO [dbo].[remove_mac] ([action],[mac]) VALUES('" + id + "','" + macs[:-1] + "')"
            cur.execute(sql)
            print(sql)
            try:
                sqlconn.commit()
                
                os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\removemac.txt')
            except Exception as e:
                print(e)

        except Exception as e:
            print(username,e)
            

        # Remove SSID



        try:
            f = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\removessid.txt')
            f.close()
            os.system("SecureCRT.exe /Script C:\\webs\\mysite\\tempinfo\\"+username+"dir\\removeSsid.py")
            millis = int(round(time.time() * 1000))
            id = username + str(millis)

            f = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\removessidLIST.txt', 'r')
            data = f.readlines()

            sql = "INSERT INTO [dbo].[global] ([show],[username],[script],[action]) VALUES(NULL,'" + username + "','Remove SSID','" + id + "')"
            cur.execute(sql)
            print(sql)
 
            for line in data:
                name = line.replace('\n', '')
                sql = "INSERT INTO [dbo].[remove_ssid] ([action],[ssid]) VALUES('" + id + "','" + name + "')"
                cur.execute(sql)
                print(sql)
            try:
                sqlconn.commit()
                
                os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\removessid.txt')
            except Exception as e:
                print(e)               

            f.close()


        except Exception as e:
            print(username,e)

        # Add SSID
        try:
            f = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addssid.txt')
            addssid = f.read()
            f.close()

            os.system("SecureCRT.exe /Script C:\\webs\\mysite\\tempinfo\\"+username+"dir\\addSsid.py")
            millis = int(round(time.time() * 1000))
            id = username + str(millis)

            addssid = addssid.replace('\n', '')
            addssid = addssid.replace(']["', ',')
            addssid = addssid.replace('"][', ',')
            addssid = addssid.replace('"', '')
            addssid = literal_eval(addssid)
            showname = addssid[0]
            SSID = addssid[1]
            wpaPASS = addssid[2]
            vlan = str(addssid[3])
            frequency = str(addssid[5])
            APgroup = (str(addssid[6:99]).replace(r'\r\n', '').replace('\'',''))[1:-1]
            s = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addssidSTAT.txt')
            line = s.read()
            line = line.replace('\n', '').split(',')
            cont = line[1]
            s.close()

            sql = "INSERT INTO [dbo].[global] ([show],[username],[script],[action]) VALUES('" + showname + "','" + username + "','Add SSID','" + id + "')"
            cur.execute(sql)
            print(sql)
            sql = "INSERT INTO [dbo].[add_ssid]([action],[controllers],[ap_groups],[ssid],[password],[vlan]) VALUES('" + id + "','" + cont + "','" + APgroup + "','" + SSID + "','" + wpaPASS + "','" + vlan + "')"
            cur.execute(sql)
            print(sql)
            
            f.close()
            try:
                sqlconn.commit()
                
            except Exception as e:
                print(e)

            # ADD SSID EMAIL

            if '1' in frequency and '2' in frequency:
                frequency1 = '2.4GHZ + 5GHz'
            else:
                if '1' in frequency:
                    frequency1 = '2.4Ghz'
                else:
                    frequency1 = '5GHz'

            f = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\info.txt')
            info = f.readlines()
            user = info[0]
            pwd = info[1]
            f.close()

            data = [SSID, wpaPASS, vlan, APgroup, frequency1]
            controller = cont
            full_name = request.user.get_full_name()
            user = info[0].rstrip()
            password = info[1].rstrip()

            sender_email = user + "@javitscenter.com"

            ssid_message_body = """\
            <html>
              <body>
                <p style="color: #201F1E;font-size: 11pt;font-family: Calibri,sans-serif;">An ssid has been added to the system.<br/>
                Please use the following Wi-Fi name and password to connect.<br/>
                <pre style="color: #201F1E;font-size: 11pt;font-family: Calibri,sans-serif;">SSID:                        <strong>""" + \
                                data[0] + """</strong><br/>Password:               <strong>""" + data[
                                    1] + """</strong><br/>Controllers:            <strong>""" + controller + """</strong><br/>Vlan:                        <strong>""" + \
                                data[2] + """</strong><br/>Frequency:             <strong>""" + data[
                                    4] + """</strong><br/><br/>AP Groups:             <strong><br>""" + data[3] + """</strong><br/></pre><br/></p>

                <p style="color: #201F1E;font-size: 11pt;font-family: Calibri,sans-serif;">If you have any issue onsite, please open a ticket at the Javits Center Service Desk or call Technology Solutions at 212-216-5432.</p>

                <p style="color: #201F1E;font-size: 11pt;font-family: Calibri,sans-serif;">Have a great day,<br/>""" + full_name + """</p>

                <span style="color:#727174;font-size:9pt;font-family:Trebuchet MS,sans-serif;line-height:120%;">……………………………………………………………………………………………………………………………………</span>
                <br/>
                <span style="color:#858487;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:115%;"><strong>""" + full_name + """</strong></span>

                <span style="color:#858487;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:115%;"><br>IT Specialist & Technology Solutions Technician</span>
                <br/>
                <a href="mailto:""" + sender_email + """@javitscenter.com" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable">""" + sender_email + """</a>
                <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;line-height:115%;">
                <b><span style="color:#858487;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:115%;">O</span></b><span style="color:#323130;font-size:11pt;font-family:Calibri,sans-serif;line-height:115%;">&nbsp;212.216.2500</span><span style="font-size:11pt;font-family:Calibri,sans-serif;line-height:115%;"></span></p>
                <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;line-height:115%;" data-event-added="1">
                <span style="color:#858487;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:115%;"><span data-markjs="true" class="_2HwZTce1zKwQJyzgqXpmAy" tabindex="0" role="link">655 West 34th Street, New York, NY 10001-1188</span></span><span style="font-size:11pt;font-family:Calibri,sans-serif;line-height:115%;"></span></p>
                <br/>
                <b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://javitscenter.com/"><span style="color:#F5D427;">javitscenter.com</span></a></span></u></b>
                <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;text-autospace:none;line-height:120%;">
                <b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="http://market.javitscenter.com/"><span style="color:#F5D427;">Market</span></a></span></u></b><b><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">
                <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://twitter.com/javitscenter/"><span style="color:#F5D427;">Twitter</span></a></span></u></b>
                <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://www.linkedin.com/company/jacob-k-javits-convention-center-of-new-york/"><span style="color:#F5D427;">LinkedIn</span></a></span></u></b>
                <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://www.instagram.com/javitscenter/"><span style="color:#F5D427;">Instagram</span></a></span></u></b>
                <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://www.youtube.com/user/thejavitscenter/"><span style="color:#F5D427;">Youtube</span></a></span></u></b>
                <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://www.facebook.com/javitscenter/"><span style="color:#F5D427;">Facebook</span></a></span></u></b></p>

                <span style="color:#727174;font-size:9pt;font-family:Trebuchet MS,sans-serif;line-height:120%;">……………………………………………………………………………………………………………………………………</span>
                <a href="https://javitscenter.com/about/expansion/" target="_blank"><img src="https://javitscenter.com/media/120210/expand.png"></a>
              </body>
            </html>
            """

            smtp_server = "smtp.office365.com"
            port = 587  # For starttls
            context = ssl.create_default_context()

            try:
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()  # Can be omitted
                server.starttls(context=context)  # Secure the connection
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                msg = MIMEMultipart()

                recipients = ['technology@javitscenter.com', 'techs@javitscenter.com']  # 'technology@javitscenter.com', 'techs@javitscenter.com'
                msg['From'] = sender_email
                msg['To'] = ", ".join(recipients)
                msg['Subject'] = 'SSID Created'
                part1 = MIMEText(ssid_message_body, "html")
                msg.attach(part1)
                server.sendmail(sender_email, recipients, msg.as_string())

            except Exception as e:
                print(username,'accounts views error 3',e)
            finally:
                server.quit()
                os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addssid.txt')
                os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addssidSTAT.txt')

        except Exception as e:
            print(username,'accounts views error 4', e)


        # Add Mac
        try:
            f = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addmac.txt')
            line = f.readlines()
            f.close()
            data = line[0].split(',')
            data[0] = data[0].split("'")[1]

            os.system("SecureCRT.exe /Script C:\\webs\\mysite\\tempinfo\\"+username+"dir\\addMac.py")
            millis = int(round(time.time() * 1000))
            id = username + str(millis)
            sql = "INSERT INTO [dbo].[global] ([show],[username],[script],[action]) VALUES('" + data[0] + "','" + username + "','Add MAC','" + id + "')"
            cur.execute(sql)
            print(sql)

            try:
                f = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addmacSTAT.txt')
                lines = f.readlines()
                f.close()

                for mac in lines:
                    split_mac = mac.split(',')
                    address = split_mac[0]
                    cont = split_mac[1].replace('\n', '')
                    if len(cont) > 0:
                        cont = split_mac[1]
                    else:
                        cont = "-1"

                    sql = "INSERT INTO [dbo].[add_mac] ([action],[controllers],[mac],[speed],[booth]) VALUES ('" + id + "','" + cont.replace('\n', '') + "','" + mac[:17] + "','" + data[2].split("'")[1] + "','" + data[1].split("'")[1] + "')"
                    cur.execute(sql)
                    print(sql)
                    
                # ADD MAC EMAIL
                if cont != '-1':
                    f = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addmac.txt', 'r')
                    addmac = f.read()
                    f.close()
                    addmac = addmac.replace('\n', '')
                    addmac = addmac.replace('][', '],[')
                    addmac = literal_eval(addmac)
                    addmacdata = addmac[0]
                    addmacshow = addmacdata[0]
                    addmacbooth = addmacdata[1]
                    addmacwid = addmacdata[2]
                    addmacemail = addmacdata[3]
                    if addmacemail != "":
                        f = open('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\info.txt')
                        info = f.readlines()
                        f.close()

                        full_name = request.user.get_full_name()
                        user = info[0].rstrip()
                        password = info[1].rstrip()
                        sender_email = user + "@javitscenter.com"

                        show = addmacshow
                        booth = addmacbooth
                        speed = addmacwid
                        if speed == '3':
                            speed = '@Wi-Fi in Booth 1.5Mbps'
                            wifipass = '3X1biT0r'
                        elif speed == '11':
                            speed = '@Wi-Fi in Booth 5Mbps'
                            wifipass = '3X5biT0R'

                        ssid_message_body = """\
                        <html>
                          <body>
                            <p style="color: #201F1E;font-size: 11pt;font-family: Calibri,sans-serif;">Hello Exhibitor,</p>
    
                            <p style="color: #201F1E;font-size: 11pt;font-family: Calibri,sans-serif;">Your devices have been registered in the system.<br/>
                            Please use the following Wi-Fi name and password to connect.<br/>
                            <pre style="color: #201F1E;font-size: 11pt;font-family: Calibri,sans-serif;">Wi-Fi:                   <strong>""" + speed + """</strong><br/>Password:           <strong>""" + wifipass + """</strong></pre><br/></p>
    
                            <p style="color: #201F1E;font-size: 11pt;font-family: Calibri,sans-serif;">If you have any issue onsite, please open a ticket at the Javits Center Service Desk or call Technology Solutions at 212-216-5432.</p>
    
                            <p style="color: #201F1E;font-size: 11pt;font-family: Calibri,sans-serif;">Have a great day,<br/>""" + full_name + """</p>
    
                            <span style="color:#727174;font-size:9pt;font-family:Trebuchet MS,sans-serif;line-height:120%;">……………………………………………………………………………………………………………………………………</span>
                            <br/>
                            <span style="color:#858487;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:115%;"><strong>""" + full_name + """</strong></span>
    
                            <span style="color:#858487;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:115%;"><br>IT Specialist & Technology Solutions Technician</span>
                            <br/>
                            <a href="mailto:""" + user + """@javitscenter.com" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable">""" + user + """@javitscenter.com</a>
                            <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;line-height:115%;">
                            <b><span style="color:#858487;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:115%;">O</span></b><span style="color:#323130;font-size:11pt;font-family:Calibri,sans-serif;line-height:115%;">&nbsp;212.216.2500</span><span style="font-size:11pt;font-family:Calibri,sans-serif;line-height:115%;"></span></p>
                            <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;line-height:115%;" data-event-added="1">
                            <span style="color:#858487;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:115%;"><span data-markjs="true" class="_2HwZTce1zKwQJyzgqXpmAy" tabindex="0" role="link">655 West 34th Street, New York, NY 10001-1188</span></span><span style="font-size:11pt;font-family:Calibri,sans-serif;line-height:115%;"></span></p>
                            <br/>
                            <b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://javitscenter.com/"><span style="color:#F5D427;">javitscenter.com</span></a></span></u></b>
                            <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;text-autospace:none;line-height:120%;">
                            <b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="http://market.javitscenter.com/"><span style="color:#F5D427;">Market</span></a></span></u></b><b><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">
                            <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://twitter.com/javitscenter/"><span style="color:#F5D427;">Twitter</span></a></span></u></b>
                            <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://www.linkedin.com/company/jacob-k-javits-convention-center-of-new-york/"><span style="color:#F5D427;">LinkedIn</span></a></span></u></b>
                            <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://www.instagram.com/javitscenter/"><span style="color:#F5D427;">Instagram</span></a></span></u></b>
                            <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://www.youtube.com/user/thejavitscenter/"><span style="color:#F5D427;">Youtube</span></a></span></u></b>
                            <b><span style="color:#727174;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;">| </span></b><b><u><span style="color:#F1C53F;font-size:10pt;font-family:Century Gothic,sans-serif;line-height:120%;"><a target="_blank" rel="noopener noreferrer" data-auth="Verified" href="https://www.facebook.com/javitscenter/"><span style="color:#F5D427;">Facebook</span></a></span></u></b></p>
    
                            <span style="color:#727174;font-size:9pt;font-family:Trebuchet MS,sans-serif;line-height:120%;">……………………………………………………………………………………………………………………………………</span><br/>
                            <a href="https://javitscenter.com/about/expansion/" target="_blank"><img src="https://javitscenter.com/media/120210/expand.png"></a>
                          </body>
                        </html>
                        """

                        smtp_server = "smtp.office365.com"
                        port = 587  # For starttls
                        context = ssl.create_default_context()

                        try:
                            server = smtplib.SMTP(smtp_server, port)
                            server.ehlo()  # Can be omitted
                            server.starttls(context=context)  # Secure the connection
                            server.ehlo()  # Can be omitted
                            server.login(sender_email, password)
                            msg = MIMEMultipart()

                            recipients = [
                                addmacemail,'technology@javitscenter.com', 'techs@javitscenter.com']   
                            msg['From'] = sender_email
                            msg['To'] = ", ".join(recipients)
                            msg['Subject'] = show.upper() + ' - Booth#' + booth + ' [Devices added to Booth Wi-Fi]'
                            part1 = MIMEText(ssid_message_body, "html")
                            msg.attach(part1)
                            server.sendmail(sender_email, recipients, msg.as_string())
                        except Exception as e:
                            print(e)
                        finally:
                            server.quit()                        

            except Exception as e:
                print(e)

        except Exception as e:
            print(username, e)
        try:
            sqlconn.commit()
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addmac.txt')
            os.remove('C:\\webs\\mysite\\tempinfo\\' + username + 'dir\\addmacSTAT.txt')  
        except Exception as e:
            print(e)
        
        # Change the redirect to results when results is finished!
        sqlconn.close()
        return redirect('/results')
    else:
        sqlconn.close()
        return redirect('/accounts/login/')


@login_required(redirect_field_name='/accounts/login/')
def home(request):
    if request.user.is_authenticated:
        username = request.user.username

        addssidshow = None
        addssidssid = None
        addssidpass = None
        addssidvlan = None
        addssidfrequency = None
        addssidapgroups = None
        addssidwid = None
        addmacdata = None
        addmacmacs = None
        addmacshow = None
        addmacbooth = None
        addmacwid = None
        addmacemail = None
        removemac = None
        removessid = None

        # DEBUG
        if settings.DEBUG:
            try:
                User.objects.create_superuser('admin', '', 'admin')
            except:
                pass
        else:
            pass

        # ADD SSID SCRIPT SPLASH PAGE
        try:
            f = open('C:\\webs\\mysite\\tempinfo\\'+username+'dir\\addssid.txt', 'r')
            addssid = f.read()
            f.close()

            if len(addssid) > 0:
                addssid = addssid.replace('\n', '')
                addssid = addssid.replace(']["', ',')
                addssid = addssid.replace('"][', ',')
                addssid = addssid.replace('"', '')
                addssid = literal_eval(addssid)
                addssidshow = addssid[0]
                addssidssid = addssid[1]
                addssidpass = addssid[2]
                addssidvlan = addssid[3]
                addssidwid = addssid[4]
                if addssidwid == None:
                    addssidwid = 'Random WID.'
                addssidfrequency = addssid[5]
                if '1' in addssidfrequency and '2' in addssidfrequency:
                    addssidfrequency = 'Any'
                else:
                    if '1' in addssidfrequency:
                        addssidfrequency = '2.4 GHz Only'
                    else:
                        addssidfrequency = '5.0 GHz Only'
                addssidapgroups = addssid[6:99]
        except:
            pass

        # ADD MAC SCRIPT SPLASH PAGE
        try:
            f = open('C:\\webs\\mysite\\tempinfo\\'+username+'dir\\addmac.txt', 'r')
            addmac = f.read()
            f.close()

            if len(addmac) > 0:
                addmac = addmac.replace('\n', '')
                addmac = addmac.replace('][', '],[')
                addmac = literal_eval(addmac)
                addmacdata = addmac[0]
                addmacmacs = addmac[1]
                addmacshow = addmacdata[0]
                addmacbooth = addmacdata[1]
                addmacwid = addmacdata[2]
                addmacemail = addmacdata[3]
                if addmacemail == "":
                    addmacemail = "none"
        except:
            pass

        # REMOVE MAC SCRIPT SPLASH PAGE
        try:
            f = open('C:\\webs\\mysite\\tempinfo\\'+username+'dir\\removemac.txt', 'r')
            removemac = f.read()
            f.close()
            if len(removemac) > 0:
                removemac = (removemac.replace('\\r\\n',''))
                removemac = (removemac.replace('[', ''))
                removemac = (removemac.replace(']', ''))
                removemac = (removemac.replace('\'', ''))
                removemac = removemac.split(',')
        except:
            pass

        # REMOVE SSID SCRIPT SPLASH PAGE
        try:
            f = open('C:\\webs\\mysite\\tempinfo\\'+username+'dir\\removessid.txt', 'r')
            removessid = f.read()
            f.close()
            if len(removessid) > 0:
                removessid = literal_eval(removessid)

            f = open('C:\\webs\\mysite\\tempinfo\\'+username+'dir\\ssidlist.txt', 'r')
            ssidlist = f.readlines()
            f.close()
            rlist = []
            for rssid in removessid:
                for cssid in ssidlist:
                    if rssid in cssid[8:11]:
                        rlist.append(cssid[0:81])

            if len(removessid) == len(rlist):
                removessid = rlist
            else:
                rlist = []
                for ssid in removessid:
                    rlist.append(ssid)
                removessid = rlist
        except:
            pass

        try:
            context = {
                'addmacdata': addmacdata, 'addmacmacs': addmacmacs,'addmacshow': addmacshow, 'addmacshow': addmacshow,'addmacbooth': addmacbooth,'addmacwid': addmacwid,'addmacemail': addmacemail,
                'addssidpass':addssidpass,'addssidshow':addssidshow, 'addssidssid':addssidssid, 'addssidvlan':addssidvlan, 'addssidfrequency':addssidfrequency, 'addssidapgroups':addssidapgroups, 'addssidwid':addssidwid,
                'removemac':removemac,
                'removessid':removessid
            }
        except:
            context = {}
        if request.user.is_superuser:
            return render(request, 'accounts/adminhome.html', context)
        else:
            return render(request, 'accounts/home.html', context)

    else:
        return redirect('/accounts/login/')



@login_required(redirect_field_name='/accounts/login/')
def results(request):
    if request.user.is_authenticated:
        #return redirect('/')
        username = request.user.username
        path = ('C:\\webs\\mysite\\tempinfo\\'+username+'dir')
        context = {}
        # ADD MAC Results
        try:
            f = open(path + '\\addmacDATA.txt', 'r')
            data = f.readlines()
            f.close()
            count = 0

            c1 = {}
            c2 = {}
            c3 = {}
            c4 = {}

            for line in data:
                line = line.replace('\n', '')
                line = line.replace('(Javits-5508-1) ', '')
                line = line.replace('(Javits-5508-2) ', '')
                line = line.replace('(Javits-5508-3) ', '')
                line = line.replace('(Javits-5508-4) ', '')
                if line != '':
                    if '172.16.255.1' in line:
                        controller = line
                    else:
                        line = line.replace('\n', 'Incorrect input! MAC Address is invalid.')
                        count = count + 1
                        if count == 1:
                            pass
                            mac = line[0:17]
                        if count == 2:
                            if 'Use \'' in line:
                                status = 'Incorrect input! Invalid MAC Address or bad format.'
                            else:
                                status = line
                            count = 0
                            if '11' in controller:
                                c1[mac] = status
                            if '12' in controller:
                                c2[mac] = status
                            if '13' in controller:
                                c3[mac] = status
                            if '14' in controller:
                                c4[mac] = status
            addmachtml = {'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4}
            context.update(addmachtml)
        except:
            pass

        try:
            f = open(path + '\\addssidDATA.txt', 'r')
            lines = f.readlines()
            f.close()

            asc1 = []
            asc2 = []
            asc3 = []
            asc4 = []

            for line in lines:
                line = line.rstrip()
                if '172.16.255.1' in line:
                    cont = line
                else:
                    if len(line) > 15:
                        if 'WLAN Identifier or Profile Name already in use' in line:
                            line = 'WLAN Identifier or Profile Name already in use.'
                        if '11' in cont:
                            asc1.append(line.rstrip())
                        elif '12' in cont:
                            asc2.append(line.rstrip())
                        elif '13' in cont:
                            asc3.append(line.rstrip())
                        else:
                            asc4.append(line.rstrip())
            addssidhtml = {'asc1':asc1,'asc2':asc2,'asc3':asc3,'asc4':asc4}
            context.update(addssidhtml)
        except:
            pass

        return render(request, 'accounts/results.html', context)
