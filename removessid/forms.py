from django import forms
from django.core.exceptions import ValidationError
from ast import literal_eval



class removessidForm(forms.Form):
    def __init__(self,user, *args, **kwargs,):
        self.user = user
        def Sort_Tuple(tup):
            tup.sort(key=lambda x: x[0])
            return tup

        tup = []
        try:
            f = open('C:\\webs\\mysite\\tempinfo\\'+str(user)+'dir\\ssidlist.txt', 'r')
            addssid = f.readlines()
            f.close()

            for ap in addssid:
                if "Last Updated:" in ap:
                    pass
                else:
                    cont = ap[0:7]
                    wid = ap[8:11]
                    status = ap[90:91]
                    vlan = (ap[100::])[:-4]
                    name = ap[12:90]


                    tup.append((int(ap[8:11]),ap[0:81]))
            (Sort_Tuple(tup))

        except Exception as e:
            print(e)

        def wid100(value):
            value = (literal_eval(value))
            if not user.is_superuser:
                for wid in value:
                    if int(wid) < 100:
                        raise ValidationError('No WID above 100')

        super(removessidForm, self).__init__(*args, **kwargs)
        self.fields['ssids'] = forms.CharField(
            required=True,
            validators=[wid100],
            widget=forms.CheckboxSelectMultiple(
                choices=tup))


