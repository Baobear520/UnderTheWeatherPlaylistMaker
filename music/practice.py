import spotipy
from spotipy.oauth2 import SpotifyOAuth 



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        redirect_uri='http://localhost:8080',
        scope='playlist-modify-public'
        )
    )
user = sp.me()
user_id = user['id']
user_name = user['display_name']








    

    


