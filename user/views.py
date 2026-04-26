from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user.forms import LoginUserForm, RegisterUserForm


# Create your views here.

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')


def check_username(request):
    username=request.GET.get('username', '')
    if len(username) > 3:
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse('<div style="color: red;">Username already exists</div>',)
        else:
            return HttpResponse('<div style="color: green;" >Username is available</div>')
    else:
        return HttpResponse('')

def check_email(request):
    email=request.GET.get('email', '')
    if len(email) > 5:
        if get_user_model().objects.filter(email=email).exists():
            return HttpResponse('<div style="color: red;">Email already exists</div>',)
        else:
            return HttpResponse('<div style="color: green;" >Email is available</div>')
    else:
        return HttpResponse('')



