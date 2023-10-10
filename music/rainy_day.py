import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up your Spotify API credentials

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080'))

# Define your feature criteria
valence_range = (0.1, 0.5)
energy_range = (0.2, 0.6)
instrumentalness_range = (0.5, 1.0)
acousticness_range = (0.6, 1.0)
loudness_max = -10  # Adjust as needed

# Search for tracks that match the criteria
results = sp.search(q='rainy day', type='track', limit=10)  # Replace 'rainy day' with your desired search query

for track in results['tracks']['items']:
    track_id = track['id']
    features = sp.audio_features([track_id])[0]
    
    if (
        valence_range[0] <= features['valence'] <= valence_range[1] and
        energy_range[0] <= features['energy'] <= energy_range[1] and
        instrumentalness_range[0] <= features['instrumentalness'] <= instrumentalness_range[1] and
        acousticness_range[0] <= features['acousticness'] <= acousticness_range[1] and
        features['loudness'] <= loudness_max
    ):
        print(f"Track Name: {track['name']}")
        print(f"Artist: {', '.join([artist['name'] for artist in track['artists']])}")
        print(f"Valence: {features['valence']}")
        print(f"Energy: {features['energy']}")
        print(f"Tempo: {features['tempo']}")
        print(f"Instrumentalness: {features['instrumentalness']}")
        print(f"Acousticness: {features['acousticness']}")
        print(f"Loudness: {features['loudness']}")
        print("\n")
    
print('No tracks found')
