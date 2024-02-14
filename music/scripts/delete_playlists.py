import spotipy
from spotipy.oauth2 import SpotifyOAuth

 

def delete_all_playlists():
    """Deleting all the users playlists"""

    auth_manager = SpotifyOAuth(
            scope='user-library-read user-top-read playlist-modify-public')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print(auth_manager.get_access_token())
    
    try:
        all_playlists = sp.current_user_playlists()['items']
        for playlist in all_playlists:
            sp.current_user_unfollow_playlist(playlist_id=playlist['id'])
            print(f"Playlist {playlist['name']} has been deleted")
    except Exception as e:
            print('No playlists found')


if __name__ == '__main__':
     delete_all_playlists()
