from django import forms
from django.forms import widgets, ModelForm
from .models import send_string

class InputStringForm(ModelForm):
	
	class Meta:
		model = send_string
		fields = ['input_str']
		labels = {'input_str': 'Send a string to the database'}
	
	

