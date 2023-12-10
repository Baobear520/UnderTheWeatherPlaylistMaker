import os, geocoder
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pyowm.owm import OWM
 

def my_func():
    auth_manager = SpotifyOAuth(
            scope='user-library-read user-top-read playlist-modify-public')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    top_artists = sp.current_user_top_artists(limit=20,time_range='long_term')
    print(f"Obtained a list of user's top-20 artists")
    print(top_artists)

def delete_all_playlists():
    auth_manager = SpotifyOAuth(
            scope='user-library-read user-top-read playlist-modify-public')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    try:
        all_playlists = sp.current_user_playlists()['items']
        for playlist in all_playlists:
            sp.current_user_unfollow_playlist(playlist_id=playlist['id'])
            print(f"Playlist {playlist['name']} has been deleted")
    except Exception as e:
            print('No playlists found')

if __name__ == '__main__':
     delete_all_playlists()
