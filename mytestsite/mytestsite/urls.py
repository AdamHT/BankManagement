"""mytestsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

#from mytestsite.apps import views as t_views
#from mytestsite.apps import urls as t_urls
from mytestsite.apps.user_auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
]
IO_url_patterns = [
	#path('input/', t_views.input_view),
	#path('output/', t_views.output_view)
	path('login/', auth_views.login_page),
	path('token_login/', auth_views.tokenlogin)
	
]
#IO_url_patterns = [
#	path('password/', include('mytestsite.apps.urls')),
#]	
urlpatterns += IO_url_patterns