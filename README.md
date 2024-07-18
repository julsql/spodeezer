# Spodeezer

This is the repo of my spodeezer api!

It's a Flask project to manage Deezer and Spotify accounts.

> API available at address: [spodeezer.h.minet.net](http://spodeezer.h.minet.net)

## Table of Contents

- [Commands](#commands)
- [Installation](#installation)
- [Deploy](#deploy)
- [Authors](#authors)

## Commands

- http://spodeezer.h.minet.net/deezer/shazam?title=pomme&title=on%20brûlera&playlist=Shazam:
    Add to the Deezer playlist the song On Brûlera of Pomme. 
    Can be used with Shazam.
    Be careful you need to add in the header of the GET request the access-token (Access-Token) 
    and the user id (User-Id) of the playlist owner.
- http://spodeezer.h.minet.net/spotify/shazam?title=pomme&title=on%20brûlera&playlist=Shazam:
    Same but for Spotify (No need for the Access-Token, you just have to generate it one time)
- http://spodeezer.h.minet.net/synchronisation/playlist?playlist=Coucou:
    Synchronize a playlist between Deezer and Spotify and their tracks.
    Generate an Spotify access token first.
    Be careful you need to add in the header of the GET request:
  - the Deezer access-token (Deezer-Access-Token)
  - the Deezer user id (Deezer-User-Id)
  - the Spotify user id (Spotify-User-Id)

- http://spodeezer.h.minet.net/synchronisation: Still building,
    Same as command before, but for all the playlists of the accounts
- http://spodeezer.h.minet.net/deezer/code: get the deezer token access
- http://spodeezer.h.minet.net/spotify/code: get the spotify token access

## Installation

> You need to have python3 and pip installed on your machine

1. Clone git repository

    ```bash
    git clone git@github.com:julsql/spodeezer.git
    ```

2. Get Deezer data:
   - User id: Connect to Deezer, go to your profil page and get the user id in the url `https://www.deezer.com/en/profile/<user_id>`
   - App token:
   Go to [Deezer Developers](https://developers.deezer.com/myapps) and create a new applicaiton 
   (Application domain http://spodeezer.h.minet.net, Redirect URL after authentication http://spodeezer.h.minet.net/deezer/auth)
   Get your Application ID and Secret Key.
   
   Create a `keys.py` file in [spodeezer/main](spodeezer/main) of this project and write:

    ```py
    deezer_client_id = 'application_id'
    deezer_client_secret = 'secret_key'
    deezer_user_id = 'your_user_id'
    deezer_redirect_uri = 'http://spodeezer.h.minet.net/deezer/auth'
    deezer_permissions = "manage_library"
    ```

3. Get Spotify data:
   - User id: Connect to Spotify, go to update profil page https://www.spotify.com/fr/account/profile/ and get the user id in the first input
   - App token:
   Go to [Spotify for developers](https://developer.spotify.com/dashboard) and create a new applicaiton 
   (Application domain http://spodeezer.h.minet.net, Redirect URL after authentication http://spodeezer.h.minet.net/spotify/auth)
   Get your Client ID and Client secret.
   
   Add to the `keys.py` file:

    ```py
    spotify_client_id = 'client_id'
    spotify_client_secret = 'client_secret'
    spotify_user_id = 'your_user_id'
    spotify_redirect_uri = 'http://spodeezer.h.minet.net/spotify/auth'
    spotify_scope = "playlist-modify-public"
    ```

4. Create a .cache folder
    
   ```bash
    mkdir spodeezer/main/files/.cache
    ```

5. Configure the python virtual environment in the root of the project

    ```bash
    pip install virtualenv
    python3 -m venv env
    source env/bin/activate
    ```
   
6. Install the libraries

    ```bash
    pip install -r requirements.txt
   ```

7. Run the server

    ```bash
    python3 spodeezer/main/spodeezer.py
    ```

## Deploy

You need to configure your VM.

Download git, python, apache2, pip on your VM:
    
```bash
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install postgresql
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install git
sudo apt-get install python3-venv
```

Install the project as explained in [Installation](#installation)

Give the access permissions of the apache server to the .cache file

```bash
sudo chmod -R 775 spodeezer/main/files/.cache
sudo chown -R www-data:www-data spodeezer/main/files/.cache
```

Update the link to the python virtual env in the ` spodeezer/spodeezer/spodeezer.wsgi` file.

Configure the VM as follows:

```bash
sudo nano /etc/apache2/sites-available/myconfig.conf
```

```
<VirtualHost *:80>
     ServerName spodeezer.h.minet.net
     ServerAdmin admin@email.fr

     WSGIScriptAlias / /home/username/spodeezer/spodeezer/spodeezer/spode>
     WSGIDaemonProcess app user=www-data group=www-data threads=2 python-home=/>

     <Directory /home/username/spodeezer>
            Options FollowSymLinks
            AllowOverride None
            Require all granted
     </Directory>
     ErrorLog ${APACHE_LOG_DIR}/error.log
     LogLevel warn
     CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

You load the configuration and restart the apache server
```bash
sudo a2ensite myconfig.conf
sudo service apache2 restart
```

> To unload a configuration: `sudo a2dissite myconfig.conf`

## Authors

- Jul SQL
