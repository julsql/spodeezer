import re

spotify_step = 50
spotify_max = 300


def spotify_create_playlist(playlist_name, sp, user_id):
    playlist = sp.user_playlist_create(user_id, playlist_name)
    playlist_id = playlist['id']

    # print(f"La playlist '{playlist_name}' a été créée avec succès !")
    return playlist_id


def spotify_find_playlist(playlist_name, sp, user_id):
    spotify_playlist_id = None

    i = 0
    while i < spotify_max:
        spotify_playlists_response = sp.user_playlists(user_id, limit=spotify_step, offset=i)
        spotify_playlists = spotify_playlists_response['items']
        for playlist in spotify_playlists:
            if playlist['name'] == playlist_name:
                spotify_playlist_id = playlist['id']
                i = spotify_max
                break
        i += spotify_step
    return spotify_playlist_id


def spotify_get_music_id(title, artist, sp):
    parentheses = r'\([^)]*\)'
    title = re.sub(parentheses, '', title)
    artist = re.sub(parentheses, '', artist)

    result = sp.search(q=f'track:{title} artist:{artist}', type='track', limit=1)

    if len(result['tracks']['items']) > 0:
        return result['tracks']['items'][0]['id']


def spotify_add_music_to_playlist(playlist_id, track_id, sp):
    if track_id:
        sp.playlist_add_items(playlist_id, [track_id])


def spotify_add_musics_to_playlist(playlist_id, track_ids, sp):
    if track_ids:
        max_add_playlist = 100
        loop = int(len(track_ids) / max_add_playlist) + 1
        for i in range(loop):
            spotify_track_ids_shorten = track_ids[i * max_add_playlist:(i + 1) * max_add_playlist]
            sp.playlist_add_items(playlist_id, spotify_track_ids_shorten)


def spotify_get_tracks_id_playlist(playlist_id, sp):
    spotify_playlist_tracks = []
    tracks_response = sp.playlist_items(playlist_id, additional_types=('track',))
    tracks = tracks_response['items']
    for track in tracks:
        spotify_playlist_tracks.append(track['track']['id'])
    return spotify_playlist_tracks


def spotify_get_tracks_playlist(playlist_id, sp):
    spotify_playlist_tracks = []

    i = 0
    while i < spotify_max:
        tracks_response = sp.playlist_items(playlist_id, additional_types=('track',), limit=spotify_step, offset=i)
        tracks = tracks_response['items']
        for track in tracks:
            spotify_playlist_tracks.append(
                {'id': track['track']['id'], 'title': track['track']['name'],
                 'album': track['track']['album']['name'],
                 'artist': track['track']['album']['artists'][0]['name']})
        i += spotify_step
    return spotify_playlist_tracks
