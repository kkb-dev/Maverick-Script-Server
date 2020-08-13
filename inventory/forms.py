from django.core.exceptions import ValidationError
from django import forms
import os, datetime, pyodbc

def valid_show(value):
    if '0' == value:
        raise ValidationError('Choose a show')

class inventoryForm(forms.Form):
    show = forms.ChoiceField(
        required=False,
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        try:

            #sqlconn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=nyccoc-sql-02;DATABASE=ShowDB;UID=ShowDBuser;PWD=zQ+GZ*[z!EtCXv5)')
            #cur = sqlconn.cursor()
            sql = """SELECT name FROM shows ORDER BY move_in"""
            cur.execute(sql)
            item = cur.fetchone()
            SHOW_LIST = []
            SHOW_LIST.append(('', 'SELECT SHOW'))
            while item is not None:
                item = str(item)[2:-4]
                SHOW_LIST.append((item, item))
                item = cur.fetchone()
        except:
            SHOW_LIST = [('', 'Cannot Connect to SQL Server'), ('Testing', 'Test'),('T', 'T')]

        try:
            equiplist = []
            z = os.listdir(r'C:\webs\mysite\ExcelSheets')
            for zdir in z:
                try:
                    y = os.listdir(r'C:\webs\mysite\ExcelSheets' + '\\' + zdir)
                    for ydir in y:
                        try:
                            path = r'C:\webs\mysite\ExcelSheets' + '\\' + zdir + '\\' + ydir
                            x = os.listdir(r'C:\webs\mysite\ExcelSheets' + '\\' + zdir + '\\' + ydir)
                            for xdir in x:
                                eql = (path + '\\' + xdir)
                                eqitem = (str(ydir.upper()) + ' - ' + str(xdir.upper()))
                                equiplist.append((eql, eqitem))
                        except Exception as e:
                            pass
                except Exception as e:
                    pass
        except:
            pass

        super(inventoryForm, self).__init__(*args, **kwargs)
        self.fields['show'] = forms.ChoiceField(choices=SHOW_LIST,
                                                validators=[valid_show])
        self.fields['equip'] = forms.CharField(
            required=True,
            widget=forms.CheckboxSelectMultiple(
                choices=equiplist))
