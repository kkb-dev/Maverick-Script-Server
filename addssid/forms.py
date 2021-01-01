from django.core.exceptions import ValidationError
from django import forms

def valid_show(value):
    if '0' == value:
        raise ValidationError('Choose a show')

def valid_passw(value):
    if '?' in value:
        raise ValidationError('?')

def valid_vlan(value):
    if value == 207 or value > 704 and value < 715:
        pass
    else:
        raise ValidationError('Wrong VLAN')

def valid_wid(value):
    if value == None or value > 99 and value < 121:
        pass
    else:
        raise ValidationError('Wrong WID')


class addssidForm(forms.Form):

    RADIO_LIST = (
    ('1', '2.4 GHz'),
    ('2', '5.0 GHz'),
    )

    AP_LIST1 = []
    AP_LIST2 = []
    AP_LIST3 = []
    AP_LIST4 = []
    f = open('C:\\webs\\mysite\\tempinfo\\level1.txt', 'r')
    addssid = f.readlines()
    f.close()
    for ap in addssid:
        if '#lev' in ap:
            LEVEL = ap
        else:
            if '1' in LEVEL:
                ap1 = ap.replace('-',' ')
                ap1 = ap1.replace('_',' ')
                AP_LIST1.append((ap,ap1))
            if '2' in LEVEL:
                ap1 = ap.replace('-',' ')
                ap1 = ap1.replace('_',' ')
                AP_LIST2.append((ap,ap1))
            if '3' in LEVEL:
                ap1 = ap.replace('-',' ')
                ap1 = ap1.replace('_',' ')
                AP_LIST3.append((ap,ap1))
            if '4' in LEVEL:
                ap1 = ap.replace('-',' ')
                if '_4' in ap:
                    ap1 = 'Beehive'
                ap1 = ap1.replace('_',' ')
                AP_LIST4.append((ap,ap1))

    show = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        try:
            import pyodbc
            def sqlcred():
                import os, pathlib
                credpath = os.path.dirname(os.path.realpath(__file__))
                cred = pathlib.Path(credpath).parents[0]
                sqlcred = str(cred) + "\\sqlcred.txt"

                f = open("sqlcred.txt","r")
                sql = f.readlines()
                sqlS = sql[0]
                sqld = sql[1]
                sqlP = sql[2]
                
                return (sqlS, sqlD, sqlP)
            cur = sqlconn.cursor()
            sql = """SELECT name FROM shows WHERE GETDATE() between dateadd(day, -7, move_in) and dateadd(day, 3, move_out) ORDER BY move_in"""
            cur.execute(sql)
            item = cur.fetchone()
            SHOW_LIST = []
            SHOW_LIST.append(('', 'SELECT SHOW'))

            while item is not None:
                item = str(item)[2:-4]
                SHOW_LIST.append((item, item))
                item = cur.fetchone()
        except:
            SHOW_LIST = [('0','Cannot Connect to SQL Server')]

        super(addssidForm, self).__init__(*args, **kwargs)
        self.fields['show'] = forms.ChoiceField(choices=SHOW_LIST,
                                                validators=[valid_show])


    name = forms.CharField(
        required=True,
        max_length=30,)

    passw = forms.CharField(
        required=False,
        min_length=8,
        max_length=30,
        validators=[valid_passw])

    vlan = forms.IntegerField(
        initial=207,
        validators=[valid_vlan])

    frequency = forms.CharField(
        required=True,
        widget=forms.CheckboxSelectMultiple(
            choices=RADIO_LIST,
            attrs={'checked' : 'checked'}))

    wid = forms.IntegerField(
        required=False,
        validators=[valid_wid])

    apgroups1 = forms.CharField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            choices=AP_LIST1,
            attrs={'unchecked': 'unchecked'}
            ))
    apgroups2 = forms.CharField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            choices=AP_LIST2,
            attrs={'unchecked': 'unchecked'}
            ))
    apgroups3 = forms.CharField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            choices=AP_LIST3,
            attrs={'unchecked': 'unchecked'}
            ))
    apgroups4 = forms.CharField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            choices=AP_LIST4,
            attrs={'unchecked': 'unchecked'}
            ))

    def clean(self):
        cleaned_data = super(addssidForm, self).clean()
        ap1 = cleaned_data.get("apgroups1")
        ap2 = cleaned_data.get("apgroups2")
        ap3 = cleaned_data.get("apgroups3")
        ap4 = cleaned_data.get("apgroups4")
        aps = ap1+ap2+ap3+ap4
        if aps == "":
            raise ValidationError('No APs')
