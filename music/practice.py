import spotipy, os
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
from spotipy.oauth2 import SpotifyOAuth



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080'))
 
#URLs of the tracks to analylze
track_urls = [
        'https://open.spotify.com/track/6WBqq0c5ui2SRMOtmMfODr',
        'https://open.spotify.com/track/4U4wBmE5KUP39VIpWMWGA3',
        'https://open.spotify.com/track/6YwLgicpvVuMt1eE2OldwQ'
    ]

def get_tracks():  

    #Getting an array of the tracks info 
    get_track = sp.tracks(tracks=track_urls)
    tracks = get_track['tracks']
    return tracks

def get_features():

    #Getting an array of tracks features
    features = (sp.audio_features(tracks=track_urls))
    return features


def main():
    tracks = get_tracks()
    features = get_features()

    #Unpacking values for each track
    for name, feature_set in zip(range(len(tracks)),features):
        track = {
            'track': tracks[name]['name'],
            'energy': feature_set['energy'],
            'valence': feature_set['valence']
        }
        print(track)

if __name__== '__main__':
    main()


        
        





