import requests
import keys
import sys
import re


# Ajouter une musique sur une playlist deezer
# Si playlist n'existe pas : la créer
# Puis ajouter la musique à la playlist

def create_deezer_playlist(playlist_name):
    url = 'https://api.deezer.com/user/{}/playlists'.format(keys.deezer_user_id)
    params = {'access_token': keys.deezer_access_token, 'title': playlist_name}
    response = requests.post(url, params=params)
    # print("Playlist Deezer {} créée !".format(playlist_name))

    playlist_id = response.json()['id']
    # print(playlist_id)
    return playlist_id


playlist_name = "Shazam"


def main(title, artist):
    deezer_playlist_id = ''  # 3026993382

    max = 200

    i = 0
    found = False
    while i < max:  # 25
        deezer_playlists_response = requests.get(f'https://api.deezer.com/user/{keys.deezer_user_id}/playlists',
                                                 params={'access_token': keys.deezer_access_token, 'index': i})
        deezer_playlists = deezer_playlists_response.json()['data']
        # Convertir les playlists Deezer et Spotify en ensembles d'identifiants de chanson

        for playlist in deezer_playlists:
            if playlist['title'] == playlist_name:
                # print(f"Playlist {playlist_name} trouvée sur Deezer !")
                found = True
                deezer_playlist_id = playlist['id']
                i = max
                break
        i += 25

    if not found:
        # La playlist n'existe pas
        deezer_playlist_id = create_deezer_playlist(playlist_name)
    parentheses = r'\([^)]*\)'
    title = re.sub(parentheses, '', title)

    query = f'track:"{title}" artist:"{artist}"'
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
        # print("Il faut ajouter dans la playlist deezer cette musique : ")
        track = data['data'][0]
        # print('Titre:', track['title'])
        # print('Album:', track['album']['title'])
        # print('Id:', track['id'])

        track_id = track['id']

        # Envoi de la requête POST

        url = 'https://api.deezer.com/playlist/{}/tracks'.format(deezer_playlist_id)
        params = {'access_token': keys.deezer_access_token, 'songs': {track_id, }}
        response = requests.post(url, params=params)

        # Vérification de la réponse
        if response.status_code == 200:
            print(f'{title} de {artist} ajoutée avec succès à la playlist {playlist_name} !')
            return 1
        else:
            print('Erreur lors de l\'ajout de la musique à la playlist.')
            return 0
    print('Musique non trouvée')
    return 0


if __name__ == "__main__":
    # title, artist
    main(sys.argv[1], sys.argv[2])
