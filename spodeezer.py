import spotipy
from flask import Flask, request, jsonify, redirect

import keys
import deezer_shazam
import spotify_shazam
import synchroniser
from access_token import deezer_create_access_token, spotify_create_access_token, sp_oauth
from deezer_global import deezer_find_playlist
from spotify_global import spotify_find_playlist

app = Flask(__name__)


@app.route('/')
def home():
    return 'Bienvenue sur mon API Spodeezer!'


@app.route('/deezer/shazam', methods=['GET'])
def api_deezer_shazam():
    token = request.headers.get('Access-Token')
    if token is None:
        data = {'message': "Il manque un access token Deezer"}
        return jsonify(data)
    user_id = request.headers.get('User-Id')
    if user_id is None:
        data = {'message': "Il manque l'id de l'utilisateur"}
        return jsonify(data)

    title = request.args.get('title')
    if title is None:
        data = {'message': "Il manque le titre"}
        return jsonify(data)
    artist = request.args.get('artist')
    if artist is None:
        data = {'message': "Il manque le nom de l'artiste"}
        return jsonify(data)
    playlist = request.args.get('playlist')
    if playlist is None:
        data = {'message': "Il manque le nom de la playlist"}
        return jsonify(data)

    response = deezer_shazam.main(title, artist, playlist, token, user_id)
    data = {'message': response}
    return jsonify(data)


@app.route('/spotify/shazam', methods=['GET'])
def api_spotify_shazam():
    token = request.headers.get('Access-Token')
    if token is None:
        data = {'message': "Il manque un access token Deezer"}
        return jsonify(data)
    user_id = request.headers.get('User-Id')
    if user_id is None:
        data = {'message': "Il manque l'id de l'utilisateur"}
        return jsonify(data)

    title = request.args.get('title')
    if title is None:
        data = {'message': "Il manque le titre"}
        return jsonify(data)
    artist = request.args.get('artist')
    if artist is None:
        data = {'message': "Il manque le nom de l'artiste"}
        return jsonify(data)
    playlist = request.args.get('playlist')
    if playlist is None:
        data = {'message': "Il manque le nom de la playlist"}
        return jsonify(data)

    response = spotify_shazam.main(title, artist, playlist, token, user_id)
    data = {'message': response}
    return jsonify(data)


@app.route('/synchronisation', methods=['GET'])
def api_synchronisation():
    deezer_access_token = request.headers.get('Deezer-Access-Token')
    if deezer_access_token is None:
        data = {'message': "Il manque un access token Deezer"}
        return jsonify(data)
    spotify_access_token = request.headers.get('Spotify-Access-Token')
    if spotify_access_token is None:
        data = {'message': "Il manque un access token Spotify"}
        return jsonify(data)
    deezer_user_id = request.headers.get('Deezer-User-Id')
    if deezer_user_id is None:
        data = {'message': "Il manque l'id de l'utilisateur Deezer"}
        return jsonify(data)
    spotify_user_id = request.headers.get('Spotify-User-Id')
    if spotify_user_id is None:
        data = {'message': "Il manque l'id de l'utilisateur Spotify"}
        return jsonify(data)

    response = synchroniser.synchronize(deezer_access_token, spotify_access_token, deezer_user_id, spotify_user_id)
    data = {'message': response}
    return jsonify(data)


@app.route('/synchronisation/playlist', methods=['GET'])
def api_synchronisation_playlist():
    deezer_access_token = request.headers.get('Deezer-Access-Token')
    if deezer_access_token is None:
        data = {'message': "Il manque un access token Deezer"}
        return jsonify(data)
    spotify_access_token = request.headers.get('Spotify-Access-Token')
    if spotify_access_token is None:
        data = {'message': "Il manque un access token Spotify"}
        return jsonify(data)
    deezer_user_id = request.headers.get('Deezer-User-Id')
    if deezer_user_id is None:
        data = {'message': "Il manque l'id de l'utilisateur Deezer"}
        return jsonify(data)
    spotify_user_id = request.headers.get('Spotify-User-Id')
    if spotify_user_id is None:
        data = {'message': "Il manque l'id de l'utilisateur Spotify"}
        return jsonify(data)

    playlist = request.args.get('playlist')

    response = synchroniser.synchronise_playlist(playlist, deezer_access_token,
                                                 spotify_access_token, deezer_user_id, spotify_user_id)
    data = {'message': response}
    return jsonify(data)


@app.route('/deezer/playlist_id', methods=['GET'])
def api_deezer_playlist_id():
    deezer_access_token = request.headers.get('Deezer-Access-Token')
    if deezer_access_token is None:
        data = {'message': "Il manque un access token Deezer"}
        return jsonify(data)
    deezer_user_id = request.headers.get('Deezer-User-Id')
    if deezer_user_id is None:
        data = {'message': "Il manque l'id de l'utilisateur Deezer"}
        return jsonify(data)

    playlist = request.args.get('playlist')

    response = deezer_find_playlist(playlist, deezer_access_token, deezer_user_id)
    data = {'message': response}
    return jsonify(data)


@app.route('/spotify/playlist_id', methods=['GET'])
def api_spotify_playlist_id():
    spotify_access_token = request.headers.get('Spotify-Access-Token')
    if spotify_access_token is None:
        data = {'message': "Il manque un access token Spotify"}
        return jsonify(data)
    spotify_user_id = request.headers.get('Spotify-User-Id')
    if spotify_user_id is None:
        data = {'message': "Il manque l'id de l'utilisateur Spotify"}
        return jsonify(data)

    playlist = request.args.get('playlist')
    sp = spotipy.Spotify(auth=spotify_access_token)
    response = spotify_find_playlist(playlist, sp, spotify_user_id)
    data = {'message': response}
    return jsonify(data)


@app.route('/deezer/auth')
def deezer_code_receive():
    deezer_code = request.args.get('code')
    deezer_access_token = deezer_create_access_token(deezer_code)
    return deezer_access_token


@app.route('/spotify/auth')
def spotify_code_receive():
    spotify_code = request.args.get('code')
    spotify_access_token = spotify_create_access_token(spotify_code)
    return spotify_access_token


@app.route('/deezer/code')
def deezer_code_ask():
    auth_uri = 'https://connect.deezer.com/oauth/auth.php?app_id={}&redirect_uri={}&perms={}'.format(
        keys.deezer_client_id,
        keys.deezer_redirect_uri,
        keys.deezer_permissions)
    return redirect(auth_uri)


@app.route('/spotify/code')
def spotify_code_ask():
    auth_uri = sp_oauth.get_authorize_url()
    return redirect(auth_uri)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
