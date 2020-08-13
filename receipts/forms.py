from django.core.exceptions import ValidationError
from django import forms

serials = []

def valid_show(value):
    if '0' == value:
        raise ValidationError('Choose a show')

# cannot use \/:*?"<>| when making windows folder
def valid_foldername(value):
    errchar = r'\,/,:,*,?,",<,>,|'
    errchar = errchar.split(',')
    for char in errchar:
        if char in value:
            raise ValidationError('Bad Folder Name')


class receiptForm(forms.Form):
    booth_name = forms.CharField(
        required=True,
        max_length=30,
        validators=[valid_foldername]
    )

    booth_num = forms.CharField(
        required=True,
        max_length=15,
        validators=[valid_foldername]
    )

    hall = forms.CharField(
        required=True,
        max_length=10,
    )

    show = forms.ChoiceField(
        choices=[],
    )

    serial1 = forms.CharField(
        required=True,
        max_length=25,
    )

    serial2 = forms.CharField(
        required=False,
        max_length=25,

    )
    serial3 = forms.CharField(
        required=False,
        max_length=25,

    )
    serial4 = forms.CharField(
        required=False,
        max_length=25,

    )
    serial5 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial6 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial7 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial8 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial9 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial10 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial11 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial12 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial13 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial14 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial15 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial16 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial17 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial18 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial19 = forms.CharField(
        required=False,
        max_length=25,
    )
    serial20 = forms.CharField(
        required=False,
        max_length=25,
    )

    def __init__(self, *args, **kwargs):
        try:
            import pyodbc
            #sqlconn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=nyccoc-sql-02;DATABASE=ShowDB;UID=ShowDBuser;PWD=zQ+GZ*[z!EtCXv5)')
            #cur = sqlconn.cursor()
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
            SHOW_LIST = [('', 'Cannot Connect to SQL Server'), ('Test', 'Test'),('2Test','2Test')]

        super(receiptForm, self).__init__(*args, **kwargs)
        self.fields['show'] = forms.ChoiceField(choices=SHOW_LIST,
                                                validators=[valid_show])

    def clean(self):
        cleaned_data = super(receiptForm, self).clean()
        serial1 = cleaned_data.get("serial1")
        serial2 = cleaned_data.get("serial2")
        serial3 = cleaned_data.get("serial3")
        serial4 = cleaned_data.get("serial4")
        serial5 = cleaned_data.get("serial5")
        serial6 = cleaned_data.get("serial6")
        serial7 = cleaned_data.get("serial7")
        serial8 = cleaned_data.get("serial8")
        serial9 = cleaned_data.get("serial9")
        serial10 = cleaned_data.get("serial10")
        serial11 = cleaned_data.get("serial11")
        serial12 = cleaned_data.get("serial12")
        serial13 = cleaned_data.get("serial13")
        serial14 = cleaned_data.get("serial14")
        serial15 = cleaned_data.get("serial15")
        serial16 = cleaned_data.get("serial16")
        serial17 = cleaned_data.get("serial17")
        serial18 = cleaned_data.get("serial18")
        serial19 = cleaned_data.get("serial19")
        serial20 = cleaned_data.get("serial20")

        serials = [serial1, serial2, serial3, serial4, serial5, serial6, serial7, serial8, serial9,
                   serial10, serial11, serial12, serial13, serial14, serial15, serial16, serial17
            , serial18, serial19, serial20]

        for serial in serials:
            if len(serial) > 0:
                count = serials.count(serial)
                if count > 1:
                    raise ValidationError('Duplicate')