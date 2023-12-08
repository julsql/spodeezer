import spotipy
import sys


def main(title, artist, playlist, sp_access_token, user_id):
    sp = spotipy.Spotify(auth=sp_access_token)
    playlist_id = spotify_find_playlist(playlist, sp, user_id)
    if playlist_id is None:
        playlist_id = spotify_create_playlist(playlist, sp, user_id)

    track_id = spotify_get_music_id(title, artist, sp)
    if track_id is None:
        return 'Musique non trouvée'

    try:
        spotify_add_music_to_playlist(playlist_id, track_id, sp)
    except Exception as e:
        return str(e)
    else:
        return f'{title} de {artist} ajouté avec succès à la playlist Spotify {playlist} !'


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('title, artist, playlist needed')
    from spodeezer.spodeezer import keys
    from spodeezer.spodeezer import spotify_get_access_token

    spotify_access_token = spotify_get_access_token()
    if spotify_access_token is not None:
        main(sys.argv[1], sys.argv[2], sys.argv[3], spotify_access_token, keys.spotify_user_id)
    else:
        print("token is missing")
