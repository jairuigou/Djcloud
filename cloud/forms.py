from django import forms
from django.forms import widgets

class LoginForm(forms.Form):
    username = forms.CharField(label='username',max_length=30)
    password = forms.CharField(label='password',
                                max_length=30,
            widget=widgets.PasswordInput(attrs={'oninvalid':"setCustomValidity('Enter a password')"}))
    
    