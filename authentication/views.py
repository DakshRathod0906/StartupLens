from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, ChangePasswordForm
from .services.registration import RegistrationService
from .services.login import LoginService
from .services.profile import ProfileService
from .services.password import PasswordService
from .exceptions import AuthenticationError

def register_view(request):
    if request.user.is_authenticated:
        return redirect('startup_ideas:dashboard')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = RegistrationService.register_user(form.cleaned_data)
                LoginService.login_user(request, username=user.email, password=form.cleaned_data['password'])
                messages.success(request, "Registration successful. Welcome to StartupLens!")
                return redirect('startup_ideas:dashboard')
            except AuthenticationError as e:
                messages.error(request, str(e))
    else:
        form = RegistrationForm()
        
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('startup_ideas:dashboard')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                LoginService.login_user(
                    request, 
                    username=form.cleaned_data['username'], 
                    password=form.cleaned_data['password'],
                    remember_me=form.cleaned_data.get('remember_me', False)
                )
                return redirect('startup_ideas:dashboard')
            except AuthenticationError as e:
                messages.error(request, str(e))
    else:
        form = LoginForm()
        
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('common:home')

@login_required
def profile_view(request):
    return render(request, 'authentication/profile.html', {'user': request.user})

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                ProfileService.update_profile(request.user, form.cleaned_data)
                messages.success(request, "Profile updated successfully.")
                return redirect('authentication:profile')
            except AuthenticationError as e:
                messages.error(request, str(e))
    else:
        form = ProfileUpdateForm(instance=request.user)
        
    return render(request, 'authentication/profile_edit.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            try:
                PasswordService.change_password(request.user, request, form.cleaned_data['new_password1'])
                messages.success(request, "Password changed successfully.")
                return redirect('authentication:profile')
            except AuthenticationError as e:
                messages.error(request, str(e))
    else:
        form = ChangePasswordForm(user=request.user)
        
    return render(request, 'authentication/change_password.html', {'form': form})
