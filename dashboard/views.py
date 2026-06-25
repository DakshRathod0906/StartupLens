from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'base.html')

def profile_view(request):
    return render(request, 'base.html')

def settings_view(request):
    return render(request, 'base.html')
