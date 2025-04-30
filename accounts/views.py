from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile
from .forms import RoleUpdateForm

# ----------------------------
# Registration & Login
# ----------------------------

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

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'errorMessage': 'Invalid username or password'})
    else:
        if request.user.is_authenticated:
            return landingPage(request)
        return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('session_list')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def userlogout(request):
    logout(request)
    return redirect('login')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------------
# User Management
# ----------------------------

@login_required
def user_list(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'admin':
        return redirect('session_list')

    users = UserProfile.objects.select_related('user').all()
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def edit_role(request, user_id):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'admin':
        return redirect('session_list')

    profile = get_object_or_404(UserProfile, user__id=user_id)
    form = RoleUpdateForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, 'accounts/edit_role.html', {'form': form, 'profile': profile})


# ----------------------------
# Profile & Landing
# ----------------------------

@login_required
def profile(request):
    if request.method == "GET":
        return render(request, 'updateProfile.html')

    user = request.user
    user.username = request.POST['username']
    user.first_name = request.POST['firstname']
    user.last_name = request.POST['lastname']
    user.email = request.POST['email']
    user.save()

    # Team group assignment
    teamnumber = request.POST['teamnumber']
    old_group = next((g for g in user.groups.all() if g.name.startswith("Team")), None)
    new_group_name = f"Team{teamnumber}"
    new_group, _ = Group.objects.get_or_create(name=new_group_name)

    if old_group and old_group.name != new_group_name:
        user.groups.remove(old_group)
    user.groups.add(new_group)

    return redirect('landingPage')


@login_required
def landingPage(request):
    roles = [
        ('Administrator', 'Administrator'),
        ('Engineer', 'Engineer'),
        ('Team Leader', 'Team Leader'),
        ('Department Leader', 'Department Leader'),
        ('Senior Manager', 'Senior Manager'),
    ]
    for group, label in roles:
        if request.user.groups.filter(name=group).exists():
            return render(request, 'landingPage.html', {'accessLevel': label})
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


# ----------------------------
# Custom Signup with Roles
# ----------------------------

def usersignup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {"responseMessage": "Username already taken."})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=request.POST['firstname'],
            last_name=request.POST['lastname']
        )

        selectedRole = request.POST['options']
        role_group = Group.objects.get(name=selectedRole)
        user.groups.add(role_group)

        team_group_name = f"Team{request.POST['teamnumber']}"
        team_group, _ = Group.objects.get_or_create(name=team_group_name)
        user.groups.add(team_group)

        login(request, user)
        return landingPage(request)
    return render(request, 'signup.html')
