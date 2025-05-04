from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    #list_display_links = ('user',)
    #list_filter = ('user',)

@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'categorie', 'artist',)
    search_fields = ('title', 'artist')

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(models.CustomUser, UserAdmin)
