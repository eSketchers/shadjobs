'''
Created on May 9, 2014

@author: Muneeb
'''
from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, required=True)