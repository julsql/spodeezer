import requests
import sys
import re

# Ajouter une musique sur une playlist deezer
# Si playlist n'existe pas : la créer
# Puis ajouter la musique à la playlist


def create_deezer_playlist(playlist_name, access_token, user_id):
    url = 'https://api.deezer.com/user/{}/playlists'.format(user_id)
    params = {'access_token': access_token, 'title': playlist_name}
    response = requests.post(url, params=params)
    # print("Playlist Deezer {} créée !".format(playlist_name))

    playlist_id = response.json()['id']
    # print(playlist_id)
    return playlist_id


def find_playlist_deezer(playlist_name, access_token, user_id):
    deezer_playlist_id = ''  # 11359987904

    max = 200

    i = 0
    while i < max:
        deezer_playlists_response = requests.get(f'https://api.deezer.com/user/{user_id}/playlists',
                                                 params={'access_token': access_token, 'index': i})
        if 'data' in deezer_playlists_response.json():
            deezer_playlists = deezer_playlists_response.json()['data']

            for playlist in deezer_playlists:
                if playlist['title'] == playlist_name:
                    # print(f"Playlist {playlist_name} trouvée sur Deezer !")
                    deezer_playlist_id = playlist['id']
                    i = max
                    break
            i += 25
        else:
            return 0
    return deezer_playlist_id


def get_music_id(title, artist):
    parentheses = r'\([^)]*\)'
    title = re.sub(parentheses, '', title)

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
        # print('Titre:', track['title'])
        # print('Album:', track['album']['title'])
        # print('Id:', track['id'])

        return track['id']


def add_music_to_playlist(playlist_id, track_id, access_token):
    url = f'https://api.deezer.com/playlist/{playlist_id}/tracks'
    params = {'access_token': access_token, 'songs': {track_id, }}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        if response.json() is True:
            return True
        else:
            return response.json()['error']['message']

    return response.status_code == 200


def main(title, artist, playlist, access_token, user_id):
    playlist_id = find_playlist_deezer(playlist, access_token, user_id)
    if playlist_id == '':
        playlist_id = create_deezer_playlist(playlist, access_token, user_id)

    track_id = get_music_id(title, artist)
    if track_id is None:
        return 'Musique non trouvée'

    result = add_music_to_playlist(playlist_id, track_id, access_token)
    if result is True:
        return f'{title} de {artist} ajouté avec succès à la playlist {playlist} !'
    else:
        return result


if __name__ == "__main__":
    import keys
    main(sys.argv[1], sys.argv[2], "Shazam", keys.deezer_access_token, keys.deezer_user_id)
