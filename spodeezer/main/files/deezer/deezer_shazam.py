from main.files.deezer.deezer_global import deezer_find_playlist, deezer_create_playlist, deezer_get_music_id, deezer_add_music_to_playlist


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
