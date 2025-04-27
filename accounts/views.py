from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect

# Create your views here.

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def signupaccount(request):
    if request.method == 'Post':
        user = User.objects.create_user(request.POST["username"],request.POST["email"],request.POST['password'])
        user.save()
        login(request,user)
        return redirect('home')
