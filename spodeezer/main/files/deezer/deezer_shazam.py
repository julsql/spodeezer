import sys
from .deezer_global import *


def main(title, artist, playlist, access_token, user_id):
    playlist_id = deezer_find_playlist(playlist, access_token, user_id)
    if playlist_id is None:
        playlist_id = deezer_create_playlist(playlist, access_token, user_id)

    track_id = deezer_get_music_id(title, artist)
    if track_id is None:
        return 'Musique non trouvée'

    result = deezer_add_music_to_playlist(playlist_id, track_id, access_token)
    if result is True:
        return f'{title} de {artist} ajouté avec succès à la playlist Deezer {playlist} !'
    else:
        return result


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('title, artist, playlist needed')
    from spodeezer.spodeezer import keys
    from spodeezer.spodeezer import deezer_get_access_token

    deezer_access_token = deezer_get_access_token()
    if deezer_access_token is not None:
        main(sys.argv[1], sys.argv[2], sys.argv[3], deezer_access_token, keys.deezer_user_id)
    else:
        print("token is missing")
