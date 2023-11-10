import os, geocoder
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pyowm.owm import OWM
 


def delete_all_playlists():
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
        
def mock_observ():
    #owm = OWM(api_key=os.environ.get('OPENWEATHER_API_KEY'))
    #Obtain the manager object
    try:
        mng = None
        observation = mng.weather_at_coords(lat=40.00, lon=50.00)
        print(observation)
    except AssertionError as e:
         print(e)

def my_IP_location():
    #Obtaining geolocation coordinates
 
    my_loc = None
    lat,lon = my_loc.latlng
    print(lat, lon)
        
        
    #except Exception as e:
        #print(f"Couldn't obtain user's geolocation coordinates: {e}")
        

if __name__ == '__main__':
      my_IP_location()