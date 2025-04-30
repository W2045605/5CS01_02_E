from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile
from .forms import RoleUpdateForm

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_first = User.objects.count() == 1
            UserProfile.objects.create(
                user=user,
                full_name=user.username,
                role='admin' if is_first else 'engineer',
                join_date=timezone.now()
            )
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # go to homepage if login is correct
        else:
            return render(request, 'login.html', {'errorMessage': 'Invalid username or password'})
    else:
        if request.user.is_authenticated:
            return landingPage(request)
        return render(request, 'login.html')

@login_required
def userlogout(request):
    logout(request)
    return redirect('login')

@login_required
def user_list(request):
    try:
        if request.user.userprofile.role != 'admin':
            return redirect('session_list')
    except UserProfile.DoesNotExist:
        return redirect('session_list')

    users = UserProfile.objects.select_related('user').all()
    return render(request, 'accounts/user_list.html', {'users': users})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('session_list')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_role(request, user_id):
    try:
        if request.user.userprofile.role != 'admin':
            return redirect('session_list')
    except UserProfile.DoesNotExist:
        return redirect('session_list')

    profile = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == 'POST':
        form = RoleUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = RoleUpdateForm(instance=profile)
    return render(request, 'accounts/edit_role.html', {'form': form, 'profile': profile})

@login_required
def profile(request):
    if request.method == "GET":
        return render(request, 'updateProfile.html')
    else:
        user = request.user
        user.username = request.POST['username']
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email = request.POST['email']

        teamnumber = request.POST['teamnumber']
        old_team_group_name = None
        for group in user.groups.all():
            if group.name.startswith("Team"):
                old_team_group_name = group.name
                break

        new_team_group_name = f"Team{teamnumber}"
        
        # Update team group
        if old_team_group_name != new_team_group_name:
            if old_team_group_name:
                old_team_group = Group.objects.filter(name=old_team_group_name).first()
                if old_team_group:
                    user.groups.remove(old_team_group)
            new_team_group, created = Group.objects.get_or_create(name=new_team_group_name)
            user.groups.add(new_team_group)

        user.save()
        return redirect('landingPage')

def landingPage(request):
    if request.user.groups.filter(name='Administrator').exists():
        return render(request, 'landingPage.html', {'accessLevel': 'Administrator'})
    elif request.user.groups.filter(name='Engineer').exists():
        return render(request, 'landingPage.html', {'accessLevel': 'Engineer'})
    elif request.user.groups.filter(name='Team Leader').exists():
        return render(request, 'landingPage.html', {'accessLevel': 'Team Leader'})
    elif request.user.groups.filter(name='Department Leader').exists():
        return render(request, 'landingPage.html', {'accessLevel': 'Department Leader'})
    elif request.user.groups.filter(name='Senior Manager').exists():
        return render(request, 'landingPage.html', {'accessLevel': 'Senior Manager'})
    return render(request, 'landingPage.html', {'accessLevel': 'Engineer'})

def home(request):
    return landingPage(request)

@login_required
def dashboard(request):
    try:
        role = request.user.userprofile.role
        return render(request, f'accounts/{role}_dashboard.html')
    except UserProfile.DoesNotExist:
        return redirect('login')

def usersignup(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST["username"]).exists():
            return render(request, 'signup.html', {"responseMessage": "Username already taken. Please choose another."})

        user = User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST['password'],
            first_name=request.POST['firstname'],
            last_name=request.POST['lastname']
        )
        user.save()

        selectedRole = request.POST['options']
        user.groups.add(Group.objects.get(name=selectedRole))

        team_group_name = f"Team{request.POST['teamnumber']}"
        team_group, created = Group.objects.get_or_create(name=team_group_name)
        user.groups.add(team_group)

        login(request, user)
        return landingPage(request)
