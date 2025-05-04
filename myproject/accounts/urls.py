from django.urls import path
from . import views
from .views import TrackListCreateView, TrackDetailView, UpdateSong, AddSong, index

urlpatterns = [
    path('home/', index, name='main_page'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', TrackListCreateView.as_view(), name='song-list-create'),
    path('songs/&lt;int:pk&gt;/', TrackDetailView.as_view(), name='song-detail'),
    path('UpdateSong/&lt;int:pk&gt;', UpdateSong, name='UpdateSong'),
    path('AddSong', AddSong, name='AddSong'),
]
