from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required
def main_page(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')