from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from . import models
from rest_framework import generics
from .models import Track, Genre, Album
from .serializer import TrackSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm, LoginForm

# @login_required
# def main_page(request):
#     albums = models.Album.objects.all()
#     genres = models.Genre.objects.all()
#
#     return render(request, 'home.html', {'albums': albums, 'genres': genres})

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

def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        audio_file = request.FILES.get('audio_file')
        track = Track.objects.create(title=title, audio_file=audio_file)
        return JsonResponse({'status': 'success', 'track_id': track.id})
    genres = Genre.objects.all()
    albums = Album.objects.all()
    return render(request, 'index.html', {'genres': genres, 'albums': albums})


def AddSong(request):
    return render(request, 'AddSong.html')

#@login_required
def UpdateSong(request, pk):
    return render(request, 'UpdateSong.html')

def album_detail(request, album_id):
    album = get_object_or_404(Album.objects.prefetch_related('track'), id=album_id)
    return render(request, 'album_detail.html', {'album': album})


def create_album(request):
    if request.method == 'POST':

        album = Album(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            private=request.POST.get('private', False) == 'on',
            cover=request.FILES.get('cover')
        )
        album.save()


        genre_ids = request.POST.getlist('genre')
        for genre_id in genre_ids:
            genre = Genre.objects.get(id=genre_id)
            album.genre.add(genre)


        track_titles = request.POST.getlist('tracks_title[]')
        track_files = request.FILES.getlist('tracks_audio[]')

        for title, audio_file in zip(track_titles, track_files):
            track = Track(title=title, audio_file=audio_file)
            track.save()
            album.track.add(track)

        return redirect('album_detail', album_id=album.id)


    genres = Genre.objects.all()
    return render(request, 'createalbum.html', {'genres': genres})