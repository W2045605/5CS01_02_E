from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password = password)
        
        
        if user is not None:
            login(request,user)
           
            return landingPage(request) 
        else:
            return render(request,'login.html',{'errorMessage' :'Invalid username or password'})
    else:

        if request.user.is_authenticated:
            return landingPage(request)
        
        return render(request,'login.html')
    
   

@login_required
def userlogout(request):
    logout(request)
    print("logging out")
    return redirect('login')


def usersignup(request):
    if request.method == "GET":
        return render(request,'signup.html')
    else:

        if User.objects.filter(username=request.POST["username"]).exists():
            return render(request, 'signup.html', {
                "responseMessage": "Username already taken. Please choose another."
            })
        
        user = User.objects.create_user(username=request.POST["username"],email=request.POST["email"],password=request.POST['password'],first_name=request.POST['firstname'],last_name=request.POST['lastname'])
        user.save()

        selectedRole = request.POST['options']

        user.groups.add(Group.objects.get(name= selectedRole ))
        team_group_name = f"Team{request.POST['teamnumber']}"
        team_group, created = Group.objects.get_or_create(name=team_group_name)
        user.groups.add(team_group)

        
        selected_role = request.POST['options']
        role_group = Group.objects.get(name=selected_role)
        user.groups.add(role_group)

        login(request,user)

        return landingPage(request)
    
@login_required
def profile(request):
    if request.method == "GET":
        return render(request,'updateProfile.html')
    else:
        username = request.POST['username']
        email = request.POST['email']
        teamnumber = request.POST['teamnumber']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        user = request.user

        old_team_group_name = None
        for group in user.groups.all():
            if group.name.startswith("Team"):
                old_team_group_name = group.name
                break

        
        new_team_group_name = f"Team{teamnumber}"

        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        
        if old_team_group_name != new_team_group_name:
           
            if old_team_group_name:
                old_team_group = Group.objects.filter(name=old_team_group_name).first()
                if old_team_group:
                    user.groups.remove(old_team_group)

           
            new_team_group, created = Group.objects.get_or_create(name=new_team_group_name)
            user.groups.add(new_team_group)


        user.save()
        return render(request,'updateProfile.html',{"responseMessage": "Updated Successfully."})

    
def home(request):
    return landingPage(request)
    

def landingPage(request):
    
    if request.user.groups.filter(name='Administrator').exists():
        return render(request, 'landingPage.html', {'accessLevel':'Administrator'})
    
    elif request.user.groups.filter(name='Engineer').exists():
        return render(request, 'landingPage.html', {'accessLevel':'Engineer'})
    
    elif request.user.groups.filter(name='Team Leader').exists():
        return render(request, 'landingPage.html', {'accessLevel':'Team Leader'})
    
    elif request.user.groups.filter(name='Department Leader').exists():
        return render(request, 'landingPage.html', {'accessLevel':'Department Leader'})
    
    elif request.user.groups.filter(name='Senior Manager').exists():
        return render(request, 'landingPage.html', {'accessLevel':'Senior Manager'})

    elif request.user.groups.filter(name='Engineer').exists():
        return render(request, 'landingPage.html', {'accessLevel':'Engineer'})    

    return render(request, 'landingPage.html', {'accessLevel':'Engineer'}) 

    
