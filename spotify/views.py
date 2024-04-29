from django.shortcuts import redirect, render, HttpResponse
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from django.conf import settings
from pprint import pprint


# Create your views here.

# * Auth


def get_spotify_oauth(scope=''):
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=scope
    )


def spotify_auth(request):
    sp_oauth = get_spotify_oauth(
        'user-library-read user-library-modify playlist-read-private')
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def spotify_callback(request):
    sp_oauth = get_spotify_oauth()
    code = request.GET.get('code')
    if not code:
        return HttpResponse('No code provided')

    token_info = sp_oauth.get_access_token(code)
    if not token_info:
        return HttpResponse('Failed to get token info')

    # Store the entire token_info dictionary in the session
    request.session['spotify_token_info'] = token_info
    return redirect('playlist_view')


def refresh_spotify_token(session):
    sp_oauth = get_spotify_oauth()
    token_info = session.get('spotify_token_info')

    # Check if the token is expired
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        # Save the new token info in the session
        session['spotify_token_info'] = token_info

    return token_info['access_token']
# views


def playlist_view(request):
    if 'spotify_token_info' not in request.session:
        # Redirect to authentication if no token info
        return redirect('spotify_auth')

    # Refresh the token if it's expired and get the current access token
    access_token = refresh_spotify_token(request.session)

    # Create a Spotify client with the refreshed token
    spotify = Spotify(auth=access_token)
    playlists = spotify.current_user_playlists()
    return render(request, 'spotify/playlist.html', {'playlists': playlists['items']})
