from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import AbstractUser
from . import services
from django.core.validators import FileExtensionValidator



class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='user'
    )

class Genre(models.Model):
    """ Модель жанров треков
    """
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name




class Track(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio/', null=True, default=None)

    def __str__(self):
        return self.title

class Album(models.Model):
    """ Модель альбомов для треков
    """
    #user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre, related_name='album_genres')
    track = models.ManyToManyField(Track, related_name='album_tracks', blank=True)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
         upload_to=services.get_path_upload_cover_album,
         blank=True,
         null=True,
         validators=[FileExtensionValidator(allowed_extensions=['jpg']), services.validate_size_image])


class PlayList(models.Model):
    """ Модель плейлистов пользователя
    """
    #user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='play_lists')
    title = models.CharField(max_length=50)
    tracks = models.ManyToManyField(Track, related_name='track_play_lists')
    cover = models.ImageField(
        upload_to=services.get_path_upload_cover_playlist,
         blank=True,
         null=True,
         validators=[FileExtensionValidator(allowed_extensions=['jpg']), services.validate_size_image]
     )