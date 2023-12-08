import spotipy
from main.files.spotify.spotify_global import spotify_find_playlist, spotify_create_playlist, spotify_get_music_id, spotify_add_music_to_playlist
from main.files.access_token import spotify_get_access_token


def main(title, artist, playlist, user_id):
    sp_access_token = spotify_get_access_token()
    if sp_access_token is None:
        return "Please generate an access token"

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
