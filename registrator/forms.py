from django import forms
from django.contrib.auth.models import User
import smtplib
import os, shutil


class HomeForm(forms.Form):

    fname = forms.CharField(required=False,
                           error_messages={'required': 'Required Field'},
                           widget=forms.TextInput(),
    )
    lname = forms.CharField(required=False,
                           error_messages={'required': 'Required Field'},
                           widget=forms.TextInput(),
    )

    usern = forms.CharField(required=False,
                           error_messages={'required': 'Required Field'},
                           widget=forms.TextInput(),
    )
    passw = forms.CharField(required=False,
                           error_messages={'required': 'Required Field'},
                           widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super(HomeForm, self).clean()
        usern = cleaned_data.get('usern')
        passw = cleaned_data.get('passw')
        fname = cleaned_data.get('fname')
        lname = cleaned_data.get('lname')

        print('|'+usern+'|')

        if usern == None or passw == None or fname == None or lname == None:
            raise forms.ValidationError('ERROR1')
        if usern == '' or passw == '' or fname == '' or lname == '':
            raise forms.ValidationError('ERROR1')

        user = usern + '@javitscenter.com'
        password = passw
        smtpsrv = "smtp.office365.com"
        try:
            smtpserver = smtplib.SMTP(smtpsrv, 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(user, password)
            path = os.getcwd()
            print(path)
            os.mkdir(path+'\\tempinfo\\'+usern+'dir', 777)
            f = open(path+'\\tempinfo\\'+usern+'dir\\info.txt', 'w+')
            if usern == "kbasnayake":
                User.objects.create_superuser(usern, user, passw, first_name=fname, last_name=lname)
            else:
                User.objects.create_user(usern, user, passw, first_name=fname, last_name=lname)

            info = (usern+'\n'+passw+'\n'+fname+'\n'+lname)
            f.write(info)
            f.close()
            f = open(path+'\\tempinfo\\'+usern+'dir\\maclist.txt', 'w+')
            f.write("Last Updated: 2001-01-01 12:00:00.000000")
            f.close()
            f = open(path + '\\tempinfo\\'+usern+'dir\\ssidlist.txt', 'w+')
            f.write("Last Updated: 2001-01-01 12:00:00.000000")
            f.close()
            os.system("attrib +h " + path + "\\tempinfo\\" + usern + 'dir\\info.txt')

            scripts = ['addMac.py','addSsid.py','getMac.py','getSsid.py','removeMac.py','removeSsid.py']
            for script in scripts:
                source = 'C:\\webs\\mysite\\tempinfo\\admindir\\'+script
                destination = 'C:\\webs\\mysite\\tempinfo\\'+usern+'dir\\'+script
                shutil.copyfile(source, destination)

        except Exception as e:
            print(e)
            raise forms.ValidationError('ERROR2')
        finally:
            smtpserver.close()

