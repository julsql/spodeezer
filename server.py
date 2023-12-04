from flask import Flask, request, jsonify
import shazam
import synchroniser

app = Flask(__name__)


@app.route('/')
def home():
    return 'Bienvenue sur mon API Spodeezer!'


@app.route('/shazam', methods=['GET'])
def api_shazam():
    token = request.headers.get('Access-Token')
    if token is None:
        data = {'message': "Il manque un access token Deezer"}
        return jsonify(data)
    user_id = request.headers.get('User-Id')
    if user_id is None:
        data = {'message': "Il manque l'id de l'utilisateur"}
        return jsonify(data)

    title = request.args.get('title')
    artist = request.args.get('artist')
    playlist = request.args.get('playlist')

    response = shazam.main(title, artist, playlist, token, user_id)
    data = {'message': response}
    return jsonify(data)


@app.route('/synchroniser', methods=['GET'])
def api_synchroniser():
    deezer_access_token = request.headers.get('Deezer-Access-Token')
    spotify_access_token = request.headers.get('Spotify-User-Id')
    deezer_client_id = request.headers.get('Deezer-User-Id')
    spotify_client_id = request.headers.get('Spotify-User-Id')

    response = synchroniser.main(deezer_access_token, spotify_access_token, deezer_client_id, spotify_client_id)
    data = {'message': response}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
