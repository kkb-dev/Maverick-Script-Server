from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms




class scriptlogForm(forms.Form):

    date = forms.CharField(
        required=False,
        max_length=30,)

    script = forms.CharField(
        required=False)

    show = forms.CharField(
        required=False,
        max_length=30,)

    user = forms.CharField(
        required=False,
        max_length=30,)



