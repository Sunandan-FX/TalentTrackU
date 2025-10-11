
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, ProfileEditForm
from .models import UserProfile
from django.contrib.auth.models import User

@login_required
def profile(request):
    return render(request, 'userpage/profile.html')

def home(request):
    return render(request, 'frontpage/home.html')  # Looks for templates/home.html

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.user_profile.role = form.cleaned_data['role']
            if form.cleaned_data['profile_picture']:
                user.user_profile.profile_picture = form.cleaned_data['profile_picture']
            user.user_profile.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('job:job_list')  # Resolves to /jobs/
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'userpage/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('job:job_list')  # Resolves to /jobs/
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'userpage/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('user_login')

@login_required
def profile_edit(request):
    user = request.user
    try:
        profile = user.user_profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('home')  # Resolves to /
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileEditForm(instance=profile, user=user)
    return render(request, 'userpage/profile_edit.html', {'form': form})


def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        
        user = User.objects.get(username=username)
        if username != username:
        # except User.DoesNotExist:
            messages.error(request, 'Username does not exist.')
            return render(request, 'userpage/password_reset.html')
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'userpage/password_reset.html')
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'userpage/password_reset.html')
        user.set_password(password1)
        user.save()
        messages.success(request, 'Password reset successfully. Please login with your new password.')
        return redirect('user_login')
    return render(request, 'userpage/password_reset.html')
# User search view
def user_search(request):
    query = request.GET.get('q', '').strip()
    user_result = None
    if query:
        try:
            user_result = User.objects.get(username=query)
        except User.DoesNotExist:
            user_result = None
    return render(request, 'userpage/user_search.html', {'query': query, 'user_result': user_result})