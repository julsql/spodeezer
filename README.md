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

- http://spodeezer.h.minet.net/shazam?title=pomme&title=on%20brûlera&playlist=Shazam:
    Add to the Deezer playlist the song On Brûlera of Pomme. 
    Can be used with Shazam.
    Be careful you need to add in the header of the GET request the access-token (Access-Token) 
    and the user id (User-Id) of the playlist owner.
- http://spodeezer.h.minet.net/synchronisation: Still building,
    synchronize all your Deezer and Spotify playlists
    and their music.
- http://spodeezer.h.minet.net/deezer/code: get the deezer token access

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
   (Application domain http://spodeezer.h.minet.net, Redirect URL after authentication http://spodeezer.h.minet.net/deezer/auth)
   Get your Application ID and Secret Key.
   
   Create a `keys.py` file in the root of this project and write:

    ```py
    deezer_client_id = 'application_id'
    deezer_client_secret = 'secret_key'
    deezer_user_id = 'your_user_id'
    deezer_redirect_uri = 'http://spodeezer.h.minet.net/deezer/auth'
    deezer_permissions = "manage_library"
    ```

3. Create a .cache file
    
   ```bash
    mkdir .cache
    ```

4. Configure the python virtual environment

    ```bash
    pip install virtualenv
    cd spodeezer
    python3 -m venv env
    source env/bin/activate
    ```
   
5. Install the libraries

    ```bash
    pip install -r requirements.txt
   ```

6. Launch the website

    ```bash
    python3 spodeezer.py
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
sudo chmod -R 775 .cache/
sudo chown -R www-data:www-data .cache/
```

Update the link to the python virtual env in the `spodeezer.wsgi` file.

Configure the VM as follows:

```bash
sudo nano /etc/apache2/sites-available/myconfig.conf
```

```
<VirtualHost *:80>
     ServerName spodeezer.h.minet.net
     WSGIScriptAlias / /home/juliettedebono/spodeezer/spodeezer.wsgi application-group=%{GLOBAL}
     WSGIDaemonProcess app user=www-data group=www-data threads=2 python-home=/home/juliettedebono/spodeezer/env python-path=/home/juliettedebono/spodeezer

     <Directory /home/juliettedebono/spodeezer/>
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

- Juliette Debono
