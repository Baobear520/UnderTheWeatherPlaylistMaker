from pandas import DataFrame
import spotipy
from spotipy.oauth2 import SpotifyOAuth 




sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080'))
 

results = sp.search(q='rain', type='track', limit=10)  # Replace 'rainy day' with your desired search query

    
#IDs of the tracks to analylze
track_id = [track['id'] for track in results['tracks']['items']]

def get_tracks():  

    #Getting an array of the tracks info 
    get_track = sp.tracks(tracks=track_id)
    tracks = get_track['tracks']
    return tracks
    

def get_features():

    #Getting an array of track's features
    features = (sp.audio_features(tracks=track_id))
    return features


def get_tracks_with_features():
    tracks = get_tracks()
    features = get_features()

    #Unpacking values for each track
    tracks_with_features = []
    for name, feature_set in zip(range(len(tracks)),features):
        track = {
            'track_name': tracks[name]['name'],
            'danceability': feature_set['danceability'],
            'loudness': feature_set['loudness'],
            'energy': feature_set['energy'],
            'valence': feature_set['valence']
        }
        tracks_with_features.append(track)
    return tracks_with_features


def main():
    array = get_tracks_with_features()
    df = DataFrame(array)
    print(df)
    
if __name__== '__main__':
    main()


        
        





