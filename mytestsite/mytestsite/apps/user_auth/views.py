from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import LoginForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK
)
from rest_framework.response import Response

# Create your views here.
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def tokenlogin(request):
	username = request.data.get("username")
	password = request.data.get("password")
	if username is None or password is None:
		return Response({'error': 'Please provide both username and password'},
						status=HTTP_400_BAD_REQUEST)
	user = authenticate(username=username, password=password)
	if not user:
		return Response({'error': 'Invalid Credentials'},
						status=HTTP_404_NOT_FOUND)
	user_query_set = User.objects.filter(id=user.id)#this is a query set type thing, it can return a lot of things depending on what you ask it for
	user_object = user_query_set[0]
	if user_object.employee.isadmin:
		user_type = 1
	if user_object.employee.isteller:
		user_type = 2					
						
	token, _ = Token.objects.get_or_create(user=user)
	data = {'token':token.key, 'usertype':user_type}
	return Response(data, status=HTTP_200_OK)

def login_page(request):
	#the lines below, set apart by spaces are new
	
	user_query_set = User.objects.filter(id=request.user.id)#this is a query set type thing, it can return a lot of things depending on what you ask it for
	user_object = user_query_set[0]
	if user_object.employee.isadmin:
		user_type = 1
	if user_object.employee.isteller:
		user_type = 2
	
	if request.user.is_authenticated:
		#return redirect("/")
		return JsonResponse({'usertype':user_type})
	form = LoginForm(request.POST or None)
	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request, user)
			#return redirect("/")
			return JsonResponse({'usertype':user_type})
	#return render(request, 'login.html', {'login_form': form})
	return JsonResponse({'usertype': 0})
	
#@csrf_exempt
#@api_view(["GET"])
#def sample_api(request):
	#data = {'usertype': 1}
	#return Response(data, status=HTTP_200_OK)
	




