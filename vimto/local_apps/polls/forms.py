"""
Definition of forms.
"""

from django import forms


class PersonForm(forms.Form):
    display_name = forms.CharField(label='Name', max_length=100)
    age = forms.IntegerField(required=False, label='Age')
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=(('M', 'Male',), ('F', 'Female',)))
    name = forms.CharField(label='Internal_name', max_length=20,
                           widget=forms.HiddenInput(attrs={'id': 'id_name'}))
