from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InputStringForm
from .models import send_string

# Create your views here.
def input_view(request):
	string_form = InputStringForm(request.POST or None)
	if string_form.is_valid():
		#return redirect('/')
		the_str = string_form.save()
	return render(request, 'input.html', {'form': string_form})
	
def output_view(request):
	most_recent_str = send_string.objects.latest('id').input_str
	return render(request, 'output.html', {'string': most_recent_str})