import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080'))

categories = sp.categories(country='US')
categories = categories['categories']
for c in categories['items']:
    print(c['name'])