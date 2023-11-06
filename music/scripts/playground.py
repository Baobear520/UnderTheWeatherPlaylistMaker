import spotipy
from spotipy.oauth2 import SpotifyOAuth 



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        redirect_uri='http://localhost:8080',
        scope=' user-top-read'
        )
    )
try:
    all_playlists = sp.current_user_playlists()['items']
    for playlist in all_playlists:
        sp.current_user_unfollow_playlist(playlist_id=playlist['id'])
        print(f"Playlist {playlist['name']} has been deleted")
except Exception as e:
        print('No playlists found')

