import spotipy, random
from spotipy.oauth2 import SpotifyOAuth 



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        redirect_uri='http://localhost:8080',
        scope=' user-top-read'
        )
    )

all_playlists = sp.current_user_playlists()['items']
if all_playlists:
    for playlist in all_playlists:
        sp.current_user_unfollow_playlist(playlist_id=playlist['id'])
        print(f'Playlist {playlist} has been deleted')
else:
    print('No playlists found')

