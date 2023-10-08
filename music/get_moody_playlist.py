import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080'))
data = sp.recommendations(
    limit=12,
    seed_genres=['alternative'],
    min_popularity=50,
    max_dancebility=0.3,
    max_loudness=0.5,
    max_energy=0.5, 
    max_valence=0.3
    )
tracks = data['tracks']
print('Your current mood playlist:')
for num,track in enumerate(tracks,1):
    album = track['album']
    for artist in track ['artists']:
        artist = artist['name']
        track = {
            'name': track['name'],
            'album': album['name'],
            'artist': artist,
            'URL': track['preview_url']
        }
        print(f"\n {num}) Track name - {track['name']}\
            \n  Album - {track['album']}\
            \n  Artist - {track['artist']}\
            \n  Listen to preview - {track['URL']}")





