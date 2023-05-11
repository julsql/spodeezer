import requests
import http.server
import socketserver
import webbrowser
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import keys

# spotify_access_token = util.prompt_for_user_token(spotify_username, spotify_scope, client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri=spotify_redirect_uri)
sp_oauth = SpotifyOAuth(client_id=keys.spotify_client_id, client_secret=keys.spotify_client_secret, redirect_uri=keys.spotify_redirect_uri, scope=keys.spotify_scope)

# Obtenez l'URL d'autorisation
auth_url = sp_oauth.get_authorize_url()

# Demandez l'autorisation de l'utilisateur en ouvrant l'URL dans le navigateur
webbrowser.open(auth_url)

print(auth_url)

# Entrez le code de retour après avoir autorisé l'application
code = input("Enter the code: ")

# Obtenez l'access token
token_info = sp_oauth.get_access_token(code)
spotify_access_token = token_info['access_token']
spotify_refresh_token = token_info['refresh_token']

print(spotify_refresh_token)