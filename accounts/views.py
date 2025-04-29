from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile
from .forms import RoleUpdateForm

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
def user_list(request):
    try:
        if request.user.userprofile.role != 'admin':
            return redirect('session_list')
    except UserProfile.DoesNotExist:
        return redirect('session_list')

    users = UserProfile.objects.select_related('user').all()
    return render(request, 'accounts/user_list.html', {'users': users})

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
def dashboard(request):
    try:
        role = request.user.userprofile.role
        return render(request, f'accounts/{role}_dashboard.html')
    except UserProfile.DoesNotExist:
        return redirect('login')

