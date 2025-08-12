from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'urbanapp/index.html')

def about(request):
    return render(request, 'urbanapp/about.html')

def services(request):
    return render(request, 'urbanapp/services-list.html')

def servicedetails(request):
    return render(request, 'urbanapp/service-details.html')

def categories(request):
    return render(request, 'urbanapp/categories.html')



def register(request):
    return render(request, 'urbanapp/register.html')


def user_login(request):
    return render(request, 'urbanapp/login.html')



def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')