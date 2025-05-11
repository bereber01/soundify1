from django.urls import path
from . import views
from .views import TrackListCreateView, TrackDetailView, UpdateSong, AddSong, index
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='home'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('db/', TrackListCreateView.as_view(), name='song-list-create'),
    path('songs/&lt;int:pk&gt;/', TrackDetailView.as_view(), name='song-detail'),
    path('UpdateSong/&lt;int:pk&gt;', UpdateSong, name='UpdateSong'),
    path('AddSong', AddSong, name='AddSong'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)