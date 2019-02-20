from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import widgets


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        #if not user or not user.is_active:
        if not user:
            raise forms.ValidationError('Sorry, that login was invalid. Please try again.')
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user