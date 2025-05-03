from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from . import models
from rest_framework import generics
from .models import Track
from .serializer import TrackSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm, LoginForm

@login_required
def main_page(request):
    albums = models.Album.objects.all()
    genres = models.Genre.objects.all()

    return render(request, 'home.html', {'albums': albums, 'genres': genres})

@login_required
def profile(request):
    return render(request, 'profile.html')

#def register(request):
    #return render(request, 'register.html')

#def login(request):
    #return render(request, 'login.html')



class TrackListCreateView(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def AddSong(request):
    return render(request, 'AddSong.html')

@login_required
def UpdateSong(request, pk):
    return render(request, 'UpdateSong.html')