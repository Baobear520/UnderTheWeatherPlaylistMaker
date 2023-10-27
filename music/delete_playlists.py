import spotipy, random
from spotipy.oauth2 import SpotifyOAuth 



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        redirect_uri='http://localhost:8080',
        scope='user-library-read'
        )
    )

all_playlists = sp.current_user_playlists()['items']
for playlist in all_playlists:
    sp.current_user_unfollow_playlist(playlist_id=playlist['id'])




    


