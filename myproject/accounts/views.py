from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from . import models
from rest_framework import generics
from .models import Track, Genre, Album, PlayList, CustomUser
from .serializer import TrackSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm, LoginForm, AddTrackForm
from django.views.generic import ListView



@login_required
def profile(request):
    return render(request, 'profile.html')




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
    playlists = PlayList.objects.all()
    genres = Genre.objects.all()
    albums = Album.objects.all()
    return render(request, 'index.html', {'genres': genres, 'albums': albums, 'playlists': playlists})


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

class Search(ListView):
    template_name = "index.html"
    paginate_by = 3


    def get_queryset(self):
        return Album.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context["genres"] = Genre.objects.all()
        context["is_search"] = True
        return context


def create_playlist(request):
    if request.method == "POST":
        name_playlist = request.POST.get("name-playlist")
        playlistcover = request.FILES.get("playlistcover")

        create_playlist = PlayList.objects.create(title=name_playlist, cover=playlistcover)
        return redirect("playlist_detail", playlist_id=create_playlist.id)
    return render(request, 'create_playlist.html')


def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(PlayList, id=playlist_id)

    if request.method == "POST":
        form = AddTrackForm(request.POST)
        if form.is_valid():
            track = form.cleaned_data['track']
            playlist.tracks.add(track)
            return redirect("playlist_detail", playlist_id=playlist_id)
    else:
        form = AddTrackForm()

    return render(request, 'playlist_detail.html', {
        'playlist': playlist,
        'form': form,
        'all_tracks': Track.objects.all()
    })

def add_track_to_playlist(request, playlist_id, track_id):
    playlist = get_object_or_404(PlayList, id=playlist_id)
    track = get_object_or_404(Track, id=track_id)
    playlist.tracks.add(track)
    return redirect("playlist_detail", playlist_id=playlist_id)

def listen_playlist(request, playlist_id):
    playlist = get_object_or_404(PlayList.objects.prefetch_related('tracks'), id=playlist_id)
    return render(request, "listentoplaylist.html", {'playlist': playlist})