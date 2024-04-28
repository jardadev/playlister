from django.shortcuts import redirect, render, HttpResponse
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from django.conf import settings
from pprint import pprint


# Create your views here.

# * Auth


def spotify_auth(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope='user-library-read user-library-modify playlist-read-private'
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def spotify_callback(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI
    )
    code = request.GET.get('code')
    if not code:
        return HttpResponse('No token info')

    token_info = sp_oauth.get_access_token(code)
    # use token_info['access_token'] to make authenticated calls
    if not token_info:
        return HttpResponse('No token info')

    # If token exchange is successful, store the token and redirect
    request.session['spotify_token'] = token_info['access_token']
    # Redirect to a view that uses the token
    return redirect('playlist_view')


# views


def playlist_view(request):
    # Retrieve the Spotify token from the session
    token = request.session.get('spotify_token')
    if not token:
        # Redirect to login if the token is not found
        return redirect('spotify_auth')

    # Create a Spotify client with the retrieved token
    spotify = Spotify(auth=token)

    try:
        playlists = spotify.current_user_playlists()
        # print(playlists[0])
        pprint(playlists['items'])
        return render(request, 'spotify/playlist.html', {'playlists': playlists['items']})
    except Exception as e:  # Consider more specific exception handling
        return HttpResponse(e)
