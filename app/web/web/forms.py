from django.contrib.auth.models import User
from django import forms

class GroupForm(forms.ModelForm):
    name =forms.CharField
    loc = forms.CharField
    size = forms.IntegerField()

    #class Meta:
        #model = Group
        #fields = ('name', 'size','loc')
        