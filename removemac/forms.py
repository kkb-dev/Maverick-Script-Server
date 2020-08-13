from django.core.exceptions import ValidationError
from django import forms


class removemacForm(forms.Form):
    def __init__(self,user, *args, **kwargs):
        self.user = user
        MAC_LIST = []
        try:
            f = open('C:\\webs\\mysite\\tempinfo\\'+str(user)+'dir\\maclist.txt', 'r')
            macs = f.readlines()
            f.close()
            for mac in macs:
                if "delMAC" in mac:
                    pass
                elif "Please do not" in mac:
                    pass
                elif "Last Updated:" in mac:
                    pass
                elif len(mac) > 16:
                    MAC_LIST.append((mac, mac))
        except Exception as e:
            print(e)

        super(removemacForm, self).__init__(*args, **kwargs)
        self.fields['macs'] = forms.CharField(
            required=True,
            widget=forms.CheckboxSelectMultiple(
                choices=MAC_LIST))