from django.contrib import admin
from . import models

@admin.register(models.AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'display_name', 'join_date')
    list_display_links = ('email',)

@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')
    list_display_links = ('user',)
    list_filter = ('user',)