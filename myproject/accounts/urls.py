from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]