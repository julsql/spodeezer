import json

import requests
from spotipy import SpotifyOAuth
import keys as keys
import os

path = os.path.dirname(os.path.abspath(__file__))
deezer_cache_file = os.path.join(path, ".cache/.cache-deezer-token")
spotify_cache_file = os.path.join(path, ".cache/.cache-spotify-token")

sp_oauth = SpotifyOAuth(
        client_id=keys.spotify_client_id,
        client_secret=keys.spotify_client_secret,
        redirect_uri=keys.spotify_redirect_uri,
        scope=keys.spotify_scope,
        cache_path="../../../.cache/.cache-spotify-token")


def spotify_create_access_token(spotify_code):
    token_info = sp_oauth.get_cached_token()

    if not token_info or sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.get_access_token(spotify_code)

    spotify_refresh_token = token_info['access_token']

    return spotify_refresh_token


def deezer_create_access_token(deezer_code):
    # Obtenir l'access token avec la permission manage_library
    deezer_auth_params = {
        'grant_type': 'authorization_code',
        'code': deezer_code,
        'client_id': keys.deezer_client_id,
        'client_secret': keys.deezer_client_secret,
        'redirect_uri': keys.deezer_redirect_uri,
        'scope': keys.deezer_permissions,
    }
    response = requests.post('https://connect.deezer.com/oauth/access_token.php', data=deezer_auth_params)

    if response.content.decode() == "wrong code":
        print("Wrong code")

    access_token = response.content.decode().split("access_token=")[1].split("&")[0]
    with open(deezer_cache_file, 'w') as f:
        f.write(access_token)
    return access_token


def revoke(access_token):
    revoke_url = "https://connect.deezer.com/oauth/revoke.php?access_token={}".format(access_token)

    response = requests.delete(revoke_url)

    if response.status_code == 204:
        print("Token revoked successfully.")
    else:
        print("Error revoking token: {}".format(response.status_code))


def deezer_get_access_token():
    if os.path.isfile(deezer_cache_file):
        with open(deezer_cache_file, 'r') as f:
            deezer_access_token = f.readline()
        return deezer_access_token


def spotify_get_access_token():
    if os.path.isfile(spotify_cache_file):
        with open(spotify_cache_file, 'r') as f:
            data = json.load(f)
        refresh_token = data.get('refresh_token')

        token_info = sp_oauth.refresh_access_token(refresh_token)
        spotify_access_token = token_info['access_token']

        return spotify_access_token
