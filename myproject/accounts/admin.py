from django.contrib import admin
from . import models



@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    #list_display_links = ('user',)
    #list_filter = ('user',)