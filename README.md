# synchronisazion

This is a Flask server to manage Deezer and Spotify playlists.

- http://127.0.0.1:5000/shazam?title=pomme&title=on%20brûlera&playlist=Shazam: Add to the Deezer playlist the song On Brûlera of Pomme. 
    Can be used with Shazam.
    Be careful you need to add in the header of the GET request the access-token (Access-Token) 
    and the user id (User-Id) of the playlist owner.
- http://127.0.0.1:5000/synchronisation: Still building, 
  synchronize all your Deezer and Spotify playlists
  and their musics.
