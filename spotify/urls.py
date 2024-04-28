from django.urls import path
from . import views

urlpatterns = [
    path("auth/", views.spotify_auth, name="spotify_auth"),
    path("callback/", views.spotify_callback, name='spotify_callback'),
    path("playlist/", views.playlist_view, name='playlist_view')
]
