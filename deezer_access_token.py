import requests
import webbrowser
import keys


def revoke(access_token):
    revoke_url = "https://connect.deezer.com/oauth/revoke.php?access_token={}".format(access_token)

    response = requests.delete(revoke_url)

    if response.status_code == 204:
        print("Token revoked successfully.")
    else:
        print("Error revoking token: {}".format(response.status_code))


# URL d'autorisation Deezer
auth_uri = 'https://connect.deezer.com/oauth/auth.php?app_id={}&redirect_uri={}&perms={}'.format(keys.deezer_client_id,
                                                                                                 keys.deezer_redirect_uri,
                                                                                                 keys.deezer_permissions)
print(auth_uri)
# Get code in url link returned
webbrowser.open_new(auth_uri)

# Rediriger l'utilisateur vers l'URL d'autorisation Deezer et attendre son consentement
# Récupérer le code d'autorisation dans les paramètres GET de l'URL de redirection
deezer_code = input("Enter the code: ")

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
print(response.content)
access_token = response.content.decode().split("access_token=")[1].split("&")[0]

print(access_token)

url = "https://api.deezer.com/user/me?access_token={}".format(access_token)

response = requests.get(url)

if response.status_code == 200:
    user_data = response.json()
    permissions = user_data.get('permissions', {})
    print("Permissions: {}".format(permissions))
else:
    print("Error retrieving user data: {}".format(response.status_code))
