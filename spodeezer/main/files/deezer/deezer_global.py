import re
import requests

deezer_step = 25
deezer_max = 300


def deezer_create_playlist(playlist_name, access_token, user_id):
    url = 'https://api.deezer.com/user/{}/playlists'.format(user_id)
    params = {'access_token': access_token, 'title': playlist_name}
    response = requests.post(url, params=params)
    # print("Playlist Deezer {} créée !".format(playlist_name))
    playlist_id = response.json()['id']
    return playlist_id


def deezer_find_playlist(playlist_name, access_token, user_id):
    deezer_playlist_id = None  # 11359987904

    i = 0
    while i < deezer_max:
        deezer_playlists_response = requests.get(f'https://api.deezer.com/user/{user_id}/playlists',
                                                 params={'access_token': access_token, 'index': i})
        deezer_playlists_response_json = deezer_playlists_response.json()
        if 'data' in deezer_playlists_response_json:
            deezer_playlists = deezer_playlists_response_json['data']

            for playlist in deezer_playlists:
                if playlist['title'] == playlist_name:
                    # print(f"Playlist {playlist_name} trouvée sur Deezer !")
                    deezer_playlist_id = playlist['id']
                    i = deezer_max
                    break
            i += deezer_step
        else:
            return None
    return deezer_playlist_id


def deezer_get_music_id(title, artist):
    parentheses = r'\([^)]*\)'
    title = re.sub(parentheses, '', title)
    artist = re.sub(parentheses, '', artist)

    query = f'track:"{title}" artist:"{artist}"'
    url = 'https://api.deezer.com/search'
    params = {
        'q': query,
        'order': 'RANKING',
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'data' in data and len(data['data']) > 0:
        track = data['data'][0]

        return track['id']


def deezer_add_music_to_playlist(playlist_id, track_id, access_token):
    if track_id:
        url = f'https://api.deezer.com/playlist/{playlist_id}/tracks'
        params = {'access_token': access_token, 'songs': {track_id, }}
        response = requests.post(url, params=params)
        if response.status_code == 200:
            if response.json() is True:
                return True
            else:
                return response.json()['error']['message']

        return response.status_code == 200


def deezer_add_musics_to_playlist(playlist_id, track_ids, access_token):
    if track_ids:
        url = f'https://api.deezer.com/playlist/{playlist_id}/tracks'
        params = {'access_token': access_token, 'songs': str(track_ids)}
        response = requests.post(url, params=params)
        if response.status_code == 200 and response.json() is True:
            return True
        else:
            return response.json().get('error', {}).get('message', 'Unknown error')


def deezer_get_tracks_playlist(playlist_id, access_token):
    deezer_playlist_tracks = []

    i = 0
    while i < deezer_max:
        tracks_response = requests.get(f'https://api.deezer.com/playlist/{playlist_id}/tracks',
                                       params={'access_token': access_token, 'index': i})
        tracks_response_json = tracks_response.json()
        if 'data' in tracks_response_json:
            tracks = tracks_response_json['data']
            for track in tracks:
                deezer_playlist_tracks.append(({'id': track['id'], 'title': track['title'],
                                                'album': track['album']['title'],
                                                'artist': track['artist']['name']}))
            i += deezer_step
        else:
            print(tracks_response.json())
    return deezer_playlist_tracks
