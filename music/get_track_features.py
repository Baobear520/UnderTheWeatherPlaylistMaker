import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
from spotipy.oauth2 import SpotifyOAuth



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080'))
 
#URLs of the tracks to analylze
track_urls = [
        'https://open.spotify.com/track/0IwXp8V7wgFCIthRh2z8Ot',
        'https://open.spotify.com/track/0yac0FPhLRH9i9lOng3f81',
        'https://open.spotify.com/track/1CXRwGBuGBnP8PK8oRt0UG',
        'https://open.spotify.com/track/75ZvA4QfFiZvzhj2xkaWAh',
        'https://open.spotify.com/track/6wf7Yu7cxBSPrRlWeSeK0Q'
    ]

def get_tracks():  

    #Getting an array of the tracks info 
    get_track = sp.tracks(tracks=track_urls)
    tracks = get_track['tracks']
    return tracks

def get_features():

    #Getting an array of track's features
    features = (sp.audio_features(tracks=track_urls))
    return features


def main():
    tracks = get_tracks()
    features = get_features()

    #Unpacking values for each track
    for name, feature_set in zip(range(len(tracks)),features):
        track = {
            'track': tracks[name]['name'],
            'danceability': feature_set['danceability'],
            'loudness': feature_set['loudness'],
            'energy': feature_set['energy'],
            'valence': feature_set['valence']
        }
        print(track)

if __name__== '__main__':
    main()


        
        





