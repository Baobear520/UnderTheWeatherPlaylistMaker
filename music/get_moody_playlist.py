import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Autentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080'))

#Getting an array of all available genres
genres = sp.recommendation_genre_seeds()
genres = genres['genres']
seed_genres = random.choices(population=genres,k=5)
data_recomm = sp.recommendations(
    limit=40,
    seed_genres=seed_genres,
    min_popularity=30,
    max_dancebility=0.3,
    max_loudness=0.5,
    max_energy=0.5, 
    max_valence=0.3
    )
recommendation_tracks = data_recomm['tracks']
data_search = sp.search(q='rain', type='track', limit=10)
rain_results = data_search['tracks']['items']
final_list = recommendation_tracks + rain_results

print(f"Your current mood playlist \nchosen from favorite genres ({','.join(genre for genre in seed_genres)})\
      and songs that have 'rain' in their names):\n")
for num,track in enumerate(final_list[:5],1):
  
    print(f"{num}.Track name - {track['name']}")
    print(f"Album - {track['album']['name']}")
    print(f"Image - {track['album']['images'][1]['url']}")
    print(f"Artist - {', '.join([artist['name'] for artist in track['artists']])}")
    print(f"Link - {track['external_urls']}")
    print("\n")


