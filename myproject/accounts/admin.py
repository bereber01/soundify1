from django.contrib import admin
from . import models



@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    #list_display_links = ('user',)
    #list_filter = ('user',)

@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    #list_display_links = ('user',)
    #list_filter = ('user',)