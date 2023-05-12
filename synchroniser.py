import spotipy
import requests
import keys
from spotipy.oauth2 import SpotifyOAuth
import json

# TODO récupérer toutes les playlists sur Deezer et sur Spotify,
# créer celles qui ne sont pas encore créées puis pour chacune
# comparer et ajouter les pistes manquantes.

def synchronize():

    sp_oauth = SpotifyOAuth(client_id=keys.spotify_client_id, client_secret=keys.spotify_client_secret, redirect_uri=keys.spotify_redirect_uri, scope=keys.spotify_scope, cache_path=".cache-" + keys.spotify_username)

    token_info = sp_oauth.refresh_access_token(keys.spotify_refresh_token)
    spotify_access_token = token_info['access_token']

    sp = spotipy.Spotify(auth=spotify_access_token)
    deezer_playlists_tracks = {}
    deezer_playlists_id = {}
    max = 200
    i = 0

    while i < max :
        deezer_playlists_response = requests.get(f'https://api.deezer.com/user/{keys.deezer_user_id}/playlists', params={'access_token': keys.deezer_access_token, 'index': i})
        deezer_playlists = deezer_playlists_response.json()['data']
        # Convertir les playlists Deezer et Spotify en ensembles d'identifiants de chanson
        
        for playlist in deezer_playlists:
            deezer_playlist_id = playlist['id']
            if int(playlist['creator']['id']) == int(keys.deezer_user_id):
                deezer_playlists_tracks[playlist['title']] = []
                deezer_playlists_id[playlist['title']] = deezer_playlist_id
                tracks_response = requests.get(f'https://api.deezer.com/playlist/{playlist["id"]}/tracks', params={'access_token': keys.deezer_access_token})
                tracks = tracks_response.json()['data']
                for track in tracks:
                    deezer_playlists_tracks[playlist['title']].append(({'id' : track['id'], 'title' : track['title'], 'album' : track['album']['title'], 'artists' : track['artist']['name']}))
        i += 25

    # Récupérer les playlists Spotify
    spotify_playlists_tracks = {}
    spotify_playlists_id = {}
    spotify = spotipy.Spotify(auth=spotify_access_token)

    print(len(deezer_playlists_tracks.keys()))
    i = 0

    while i < max :
        spotify_playlists_response = spotify.user_playlists(keys.spotify_username, limit=50, offset=i)
        spotify_playlists = spotify_playlists_response['items']
        for playlist in spotify_playlists:
            spotify_playlists_id[playlist['name']] = playlist['id']
            spotify_playlists_tracks[playlist['name']] = []
            tracks_response = spotify.playlist_tracks(playlist['id'])
            tracks = tracks_response['items']
            for track in tracks:
                spotify_playlists_tracks[playlist['name']].append({'id' : track['track']['id'], 'title' : track['track']['name'], 'album' : track['track']['album']['name'], 'artists' : track['track']['album']['artists'][0]['name']})
        i += 50

    print(len(spotify_playlists_tracks.keys()))
    
    for spotify_playlist_name, spotify_playlist_track in spotify_playlists_tracks.items():
        # Création playlists Deezer à partir des Spotify

        if spotify_playlist_name not in list(deezer_playlists_tracks.keys()):
            print(spotify_playlist_name, 'NOT IN PLAYLIST DEEZER')
            # Playlist n'existe pas

            url = 'https://api.deezer.com/user/{}/playlists'.format(keys.deezer_user_id)
            params = {'access_token': keys.deezer_access_token, 'title': spotify_playlist_name}
            response = requests.post(url, params=params)

            playlist_id = response.text
            print(response.url)
            print(playlist_id)
            print(spotify_playlist_name)
    
    for deezer_playlist_name, deezer_playlist_track in deezer_playlists_tracks.items():
        # Création playlists Spotify à partir des Deezer

        if deezer_playlist_name not in list(spotify_playlists_tracks.keys()):
            print(deezer_playlist_name, 'NOT IN PLAYLIST SPOTIFY')
            # Playlist n'existe pas

            # Obtient l'ID de l'utilisateur Spotify
            user_info = sp.current_user()
            user_id = user_info['id']

            # Crée la playlist
            playlist = sp.user_playlist_create(user_id, deezer_playlist_name)

            # Obtient l'ID de la playlist créée
            playlist_id = playlist['id']

            print(f"La playlist '{deezer_playlist_name}' a été créée avec succès !")
            
    for spotify_playlist_name, spotify_playlist_track in spotify_playlists_tracks.items():
        # Ajouter les musiques de chaque playlist sur Deezer
        deezer_playlist_track = deezer_playlists_tracks[spotify_playlist_name]
        deezer_playlist_id = deezer_playlists_id[spotify_playlist_name]

        for spotify_track in spotify_playlist_track:
            already = False
            for deezer_track in deezer_playlist_track:
                already = already or spotify_track['title'] == deezer_track['title']
            if not already:
                print("On va ajouter la musique {} dans la playlist {}".format(spotify_track['title'], spotify_playlist_name))
                query = 'album:"{}" track:"{}" artist:"{}"'.format(spotify_track['album'], spotify_track['title'], spotify_track['artists'])
                url = 'https://api.deezer.com/search'
                params = {
                    'q': query,
                    'order': 'RANKING',
                    'access_token': keys.deezer_access_token
                }
                response = requests.get(url, params=params)
                data = response.json()

                # Récupération du premier résultat de recherche
                if 'data' in data and len(data['data']) > 0:
                    print("Il faut ajouter dans la playlist deezer cette musique : ")
                    track = data['data'][0]
                    print('Titre:', track['title'])
                    print('Album:', track['album']['title'])
                    print('Id:', track['id'])

                    track_id = track['id']

                    # Envoi de la requête POST
                    url = 'https://api.deezer.com/playlist/{}/tracks'.format(deezer_playlist_id)
                    params = {'access_token': keys.deezer_access_token, 'songs': {track_id,}}
                    response = requests.post(url, params=params)
                    print(response.url)

                    # Vérification de la réponse
                    if response.status_code == 200:
                        print('Musique ajoutée avec succès à la playlist Deezer !')
                    else:
                        print('Erreur lors de l\'ajout de la musique à la playlist.')

                else:
                    print('Aucun résultat trouvé.')
    for deezer_playlist_name, deezer_playlist_track in deezer_playlists_tracks.items():
        # Ajouter les musiques de chaque playlist sur Deezer
        spotify_playlist_track = spotify_playlists_tracks[deezer_playlist_name]
        spotify_playlist_id = spotify_playlists_id[deezer_playlist_name]

        for deezer_track in deezer_playlist_track:
            already = False
            for spotify_track in spotify_playlist_track:
                already = already or spotify_track['title'] == deezer_track['title']
            if not already:
                result = spotify.search(q='track:{} album:{} artist:{}'.format(deezer_track['title'], deezer_track['album'], deezer_track['artists']), type='track', limit=1)

                if len(result['tracks']['items']) > 0:
                    # print("Il faut ajouter dans la playlist spotify cette musique : ")
                    track_id = result['tracks']['items'][0]['id']
                    """track_name = result['tracks']['items'][0]['name']
                    artist_name = result['tracks']['items'][0]['artists'][0]['name']
                    album_name = result['tracks']['items'][0]['album']['name']
                    
                    print("Track name:", track_name)
                    print("Artist name:", artist_name)
                    print("Album name:", album_name)
                    print("Track id:", track_id)"""
                
                    sp.playlist_add_items(spotify_playlist_id, [track_id])
                    print('Musique ajoutée avec succès à la playlist Spotify !')
                else:
                    print("No track found with the given name:")
                    print(deezer_track['title'], deezer_track['album'], deezer_track['artists'])
def permissions():
    # Définition de l'URL de l'API de Deezer pour obtenir les informations de l'utilisateur

    url = "https://api.deezer.com/user/me?access_token={}".format(keys.deezer_access_token)

    response = requests.get(url)

    if response.status_code == 200:
        user_data = response.json()
        permissions = user_data.get('permissions', {})
        print("Permissions: {}".format(permissions))
    else:
        print("Error retrieving user data: {}".format(response.status_code))

# permissions()
synchronize()