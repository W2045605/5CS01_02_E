from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login

# Create your views here.

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password = password)

        if user is not None:
            login(request,user)
           
            return redirect('home')  # go to homepage if login is correct
        else:
            return render(request,'login.html',{'errorMessage9' :'Invalid username or password'})
    else:
        return render(request,'login.html')
      

def usersignup(request):
    if request.method == "GET":
        return render(request,'signup.html')
    else:
        user = User.objects.create_user(request.POST["username"],request.POST["email"],request.POST['password'])
        user.save()
        return login(request)

    
