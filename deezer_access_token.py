import requests
import keys
import os

path = os.path.dirname(os.path.abspath(__file__))
cache_file = os.path.join(path, ".cache/.cache-deezer-token")


def create_access_token(deezer_code):
    # Obtenir l'access token avec la permission manage_library
    deezer_auth_params = {
        'grant_type': 'authorization_code',
        'code': deezer_code,
        'client_id': keys.deezer_client_id,
        'client_secret': keys.deezer_client_secret,
        'redirect_uri': keys.deezer_redirect_uri,
        'scope': keys.deezer_permissions,
    }
    response = requests.post('https://connect.deezer.com/oauth/access_token.php', data=deezer_auth_params)

    if response.content.decode() == "wrong code":
        print("Wrong code")

    access_token = response.content.decode().split("access_token=")[1].split("&")[0]
    with open(cache_file, 'w') as f:
        f.write(access_token)
    return access_token

def revoke(access_token):
    revoke_url = "https://connect.deezer.com/oauth/revoke.php?access_token={}".format(access_token)

    response = requests.delete(revoke_url)

    if response.status_code == 204:
        print("Token revoked successfully.")
    else:
        print("Error revoking token: {}".format(response.status_code))


def get_access_token():
    if os.path.isfile(cache_file):
        with open(cache_file, 'r') as f:
            deezer_access_token = f.readline()
        return deezer_access_token


get_access_token()
