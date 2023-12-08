import spotipy
from .deezer.deezer_global import *


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
    # deezer_track_ids = []
    for spotify_track in spotify_playlist_tracks:
        deezer_track_id = deezer_get_music_id(spotify_track['title'], spotify_track['artist'])
        if deezer_track_id:
            # deezer_track_ids.append(deezer_track_id)
            deezer_add_music_to_playlist(deezer_playlist_id, deezer_track_id, deezer_access_token)

    return f'Playlist {playlist_name} correctement synchronisée entre Deezer et Spotify'


def synchronize(deezer_access_token, spotify_access_token, deezer_user_id, spotify_user_id):
    sp = spotipy.Spotify(auth=spotify_access_token)
    all_playlists = []
    max_playlist = 200
    i = 0

    while i < max_playlist:
        deezer_playlists_response = requests.get(f'https://api.deezer.com/user/{deezer_user_id}/playlists',
                                                 params={'access_token': deezer_access_token, 'index': i})
        deezer_playlists = deezer_playlists_response.json()['data']
        for playlist in deezer_playlists:
            if int(playlist['creator']['id']) == int(deezer_user_id):
                all_playlists.append(playlist['title'])
        i += 25

    i = 0
    while i < max_playlist:
        spotify_playlists_response = sp.user_playlists(spotify_user_id, limit=50, offset=i)
        spotify_playlists = spotify_playlists_response['items']
        for playlist in spotify_playlists:
            all_playlists.append(playlist['name'])
        i += 50

    for playlist_name in all_playlists:
        synchronise_playlist(playlist_name, deezer_access_token, spotify_access_token, deezer_user_id, spotify_user_id)

    return f'Playlists correctement synchronisées entre Deezer et Spotify'

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
    from spodeezer.spodeezer import keys
    from spodeezer.spodeezer import spotify_get_access_token, deezer_get_access_token

    synchronise_playlist("Bonjour",
                         deezer_get_access_token(),
                         spotify_get_access_token(),
                         keys.deezer_user_id,
                         keys.spotify_user_id)
