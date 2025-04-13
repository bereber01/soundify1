from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import AbstractUser
from . import services
from django.core.validators import FileExtensionValidator

class AuthUser(models.Model):
    """ Модель пользователя на платформе
    """
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=services.get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), services.validate_size_image]
    )

    @property
    def is_authenticated(self):
        """ Всегда возвращает True. Это способ узнать, был ли пользователь аутентифицированы
        """
        return True

    def __str__(self):
        return self.email

class Genre(models.Model):
    """ Модель жанров треков
    """
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    """ Модель альбомов для треков
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
         upload_to=services.get_path_upload_cover_album,
         blank=True,
         null=True,
         validators=[FileExtensionValidator(allowed_extensions=['jpg']), services.validate_size_image])


class Track(models.Model):
    """ Модель треков
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre, related_name='track_genres')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    link_of_author = models.CharField(max_length=500, blank=True, null=True)
    file = models.FileField(
         upload_to=services.get_path_upload_track,
         validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])]
     )
    create_at = models.DateTimeField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
         upload_to=services.get_path_upload_cover_track,
         blank=True,
         null=True,
         validators=[FileExtensionValidator(allowed_extensions=['jpg']), services.validate_size_image]
     )



class PlayList(models.Model):
    """ Модель плейлистов пользователя
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='play_lists')
    title = models.CharField(max_length=50)
    tracks = models.ManyToManyField(Track, related_name='track_play_lists')
    cover = models.ImageField(
        upload_to=services.get_path_upload_cover_playlist,
         blank=True,
         null=True,
         validators=[FileExtensionValidator(allowed_extensions=['jpg']), services.validate_size_image]
     )