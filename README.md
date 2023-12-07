# Spodeezer

This is the repo of my spodeezer api!

It's a Flask project to manage Deezer and Spotify accounts.

> Website available at address: [spodeezer.h.minet.net](http://spodeezer.h.minet.net)

## Table of Contents

- [Commands](#commands)
- [Installation](#installation)
- [Deploy](#deploy)
- [Authors](#authors)

## Commands

- http://127.0.0.1:8000/shazam?title=pomme&title=on%20brûlera&playlist=Shazam:
    Add to the Deezer playlist the song On Brûlera of Pomme. 
    Can be used with Shazam.
    Be careful you need to add in the header of the GET request the access-token (Access-Token) 
    and the user id (User-Id) of the playlist owner.
- http://127.0.0.1:8000/synchronisation: Still building,
    synchronize all your Deezer and Spotify playlists
    and their music.
- http://127.0.0.1:8000/deezer/code: get the deezer token access

## Installation

> You need to have python3 and pip installed on your machine

1. Clone git repository

    ```bash
    git clone git@github.com:juliette39/spodeezer.git
    ```

2. Get some data:
   - User id: Connect to Deezer, go to your profil page and get the user id in the url `https://www.deezer.com/en/profile/<user_id>`
   - App token:
   Go to [Deezer Developers](https://developers.deezer.com/myapps) and create a new applicaiton 
   (Application domain http://localhost:8000, Redirect URL after authentication http://localhost:8000/deezer/auth)
   Get your Application ID and Secret Key.
   
   Create a `keys.py` file in the root of this project and write:

    ```py
    deezer_client_id = 'application_id'
    deezer_client_secret = 'secret_key'
    deezer_user_id = 'your_user_id'
    deezer_redirect_port = '8000'
    deezer_redirect_uri = f'http://localhost:{deezer_redirect_port}/deezer/auth'
    deezer_permissions = "manage_library"
    ```

3. Configure the python virtual environment

    ```bash
    pip install virtualenv
    cd spodeezer
    python3 -m venv env
    source env/bin/activate
    ```
   
4. Install the libraries

    ```bash
    pip install -r requirements.txt
   ```

5. Launch the website

    ```bash
    python3 server.py
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

After installing the project as explained in [Installation](#installation)
you can configure the VM as follows:

```bash
sudo nano /etc/apache2/sites-available/myconfig.conf
```

```
<VirtualHost *:80>
    ServerName votresite.com
    ServerAdmin juliette.debono@telecom-sudparis.eu

    AddDefaultCharset UTF-8

    WSGIDaemonProcess spodeezer user=www-data group=www-data threads=5
    WSGIScriptAlias / /home/juliettedebono/spodeezer/wsgi.wsgi

    <Directory /spodeezer>
        WSGIProcessGroup server
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
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

- Juliette Debono
