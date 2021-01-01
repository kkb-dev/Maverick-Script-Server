from django.core.exceptions import ValidationError
from django import forms

def valid_show(value):
    if '0' == value:
        raise ValidationError('Choose a show')

def valid_mac(value):
    if value[2::3] == '-----' or value[2::3] == ':::::':
        pass
    else:
        raise ValidationError('Incorrect Format')




class addmacForm(forms.Form):

    SPEED_CHOICE = [
    ('3','1.5 Mbps'),
    ('11','5.0 Mbps')
    ]

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

            sqlconn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=ShowDB;UID=ShowDBuser;PWD=zQ+GZ*[z!EtCXv5)') % (sqlcred())
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

        super(addmacForm, self).__init__(*args, **kwargs)
        self.fields['show'] = forms.ChoiceField(choices=SHOW_LIST,
                                                validators=[valid_show])



    booth = forms.CharField(
        max_length=10,
    )

    email = forms.EmailField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={'placeholder': 'user@example.com'}))

    speed = forms.ChoiceField(
        choices=SPEED_CHOICE,
        widget=forms.RadioSelect(
            attrs={'class': 'form-check-label'}))

    mac1 = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac2 = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac3 = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac4 = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac5 = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac6 = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac7 = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac8 = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac9 = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac10 = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac11 = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)
    mac12 = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'Enter a MAC...'}),
                            min_length=17,
                            max_length=17,
                            validators=[valid_mac],)

    def clean(self):
        cleaned_data = super(addmacForm, self).clean()
        mac1 = cleaned_data.get("mac1")
        mac2 = cleaned_data.get("mac2")
        mac3 = cleaned_data.get("mac3")
        mac4 = cleaned_data.get("mac4")
        mac5 = cleaned_data.get("mac5")
        mac6 = cleaned_data.get("mac6")
        mac7 = cleaned_data.get("mac7")
        mac8 = cleaned_data.get("mac8")
        mac9 = cleaned_data.get("mac9")
        mac10 = cleaned_data.get("mac10")
        mac11 = cleaned_data.get("mac11")
        mac12 = cleaned_data.get("mac12")

        try:
            macs = mac1+mac2+mac3+mac4+mac5+mac6+mac7+mac8+mac9+mac10+mac11+mac12
        except:
            macs = 'invalid'
        if macs == "":
            raise ValidationError('No macs')
