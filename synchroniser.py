import spotipy
from spotify_global import *
from deezer_global import *


def synchronise_playlist(playlist_name, deezer_access_token, spotify_access_token, deezer_user_id, spotify_user_id):
    deezer_playlist_id = deezer_find_playlist(playlist_name, deezer_access_token, deezer_user_id)
    if deezer_playlist_id is None:
        deezer_playlist_id = deezer_create_playlist(playlist_name, deezer_access_token, deezer_user_id)

    sp = spotipy.Spotify(auth=spotify_access_token)
    spotify_playlist_id = spotify_find_playlist(playlist_name, sp, spotify_user_id)
    if spotify_playlist_id is None:
        spotify_playlist_id = spotify_create_playlist(playlist_name, sp, spotify_user_id)

    deezer_playlist_tracks = deezer_get_tracks_playlist(deezer_playlist_id, deezer_access_token)
    spotify_tracks_id_already = spotify_get_tracks_id_playlist(spotify_playlist_id, sp)
    spotify_track_ids = []
    for deezer_track in deezer_playlist_tracks:
        spotify_track_id = spotify_get_music_id(deezer_track['title'], deezer_track['artist'], sp)
        if spotify_track_id not in spotify_tracks_id_already:
            spotify_track_ids.append(spotify_track_id)
    spotify_add_musics_to_playlist(spotify_playlist_id, spotify_track_ids, sp)

    spotify_playlist_tracks = spotify_get_tracks_playlist(spotify_playlist_id, sp)
    deezer_track_ids = []
    for spotify_track in spotify_playlist_tracks:
        deezer_track_id = deezer_get_music_id(spotify_track['title'], spotify_track['artist'])
        if deezer_track_id:
            deezer_track_ids.append(deezer_track_id)

    deezer_add_musics_to_playlist(deezer_playlist_id, deezer_track_ids, deezer_access_token)
    return f'Playlist {playlist_name} correctement synchronisée entre Deezer et Spotify'


def synchronize(deezer_access_token, spotify_access_token, deezer_user_id, spotify_user_id):
    sp = spotipy.Spotify(auth=spotify_access_token)
    deezer_playlists_tracks = {}
    deezer_playlists_id = {}
    max_playlist = 200
    i = 0

    while i < max_playlist:
        deezer_playlists_response = requests.get(f'https://api.deezer.com/user/{deezer_user_id}/playlists',
                                                 params={'access_token': deezer_access_token, 'index': i})
        deezer_playlists = deezer_playlists_response.json()['data']
        # Convertir les playlists Deezer et Spotify en ensembles d'identifiants de chanson

        for playlist in deezer_playlists:
            deezer_playlist_id = playlist['id']
            if int(playlist['creator']['id']) == int(deezer_user_id):
                deezer_playlists_tracks[playlist['title']] = []
                deezer_playlists_id[playlist['title']] = deezer_playlist_id
                tracks_response = requests.get(f'https://api.deezer.com/playlist/{playlist["id"]}/tracks',
                                               params={'access_token': deezer_access_token})
                tracks = tracks_response.json()['data']
                for track in tracks:
                    deezer_playlists_tracks[playlist['title']].append(({'id': track['id'], 'title': track['title'],
                                                                        'album': track['album']['title'],
                                                                        'artists': track['artist']['name']}))
        i += 25

    # Récupérer les playlists Spotify
    spotify_playlists_tracks = {}
    spotify_playlists_id = {}

    print(len(deezer_playlists_tracks.keys()))
    i = 0

    while i < max_playlist:
        spotify_playlists_response = sp.user_playlists(spotify_user_id, limit=50, offset=i)
        spotify_playlists = spotify_playlists_response['items']
        for playlist in spotify_playlists:
            spotify_playlists_id[playlist['name']] = playlist['id']
            spotify_playlists_tracks[playlist['name']] = []
            tracks_response = sp.playlist_items(playlist['id'], additional_types=('track',))
            tracks = tracks_response['items']
            for track in tracks:
                spotify_playlists_tracks[playlist['name']].append(
                    {'id': track['track']['id'], 'title': track['track']['name'],
                     'album': track['track']['album']['name'],
                     'artists': track['track']['album']['artists'][0]['name']})
        i += 50

    print(len(spotify_playlists_tracks.keys()))

    for spotify_playlist_name, spotify_playlist_track in spotify_playlists_tracks.items():
        # Création playlists Deezer à partir des Spotify

        if spotify_playlist_name not in list(deezer_playlists_tracks.keys()):
            print(spotify_playlist_name, 'NOT IN PLAYLIST DEEZER')
            # Playlist n'existe pas

            url = 'https://api.deezer.com/user/{}/playlists'.format(deezer_user_id)
            params = {'access_token': deezer_access_token, 'title': spotify_playlist_name}
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
            sp.user_playlist_create(user_id, deezer_playlist_name)

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
                print("On va ajouter la musique {} dans la playlist {}".format(spotify_track['title'],
                                                                               spotify_playlist_name))
                query = 'album:"{}" track:"{}" artist:"{}"'.format(spotify_track['album'], spotify_track['title'],
                                                                   spotify_track['artists'])
                url = 'https://api.deezer.com/search'
                params = {
                    'q': query,
                    'order': 'RANKING',
                    'access_token': deezer_access_token
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
                    params = {'access_token': deezer_access_token, 'songs': {track_id, }}
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
                result = sp.search(
                    q='track:{} album:{} artist:{}'.format(deezer_track['title'], deezer_track['album'],
                                                           deezer_track['artists']), type='track', limit=1)

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


def permissions(deezer_access_token):
    # Définition de l'URL de l'API de Deezer pour obtenir les informations de l'utilisateur
    url = "https://api.deezer.com/user/me?access_token={}".format(deezer_access_token)

    response = requests.get(url)

    if response.status_code == 200:
        user_data = response.json()
        perms = user_data.get('permissions', {})
        print("Permissions: {}".format(perms))
    else:
        print("Error retrieving user data: {}".format(response.status_code))


if __name__ == "__main__":
    import keys
    from access_token import spotify_get_access_token, deezer_get_access_token

    synchronise_playlist("Bonjour",
                         deezer_get_access_token(),
                         spotify_get_access_token(),
                         keys.deezer_user_id,
                         keys.spotify_user_id)
