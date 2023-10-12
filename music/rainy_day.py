import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
from spotipy.oauth2 import SpotifyOAuth


#Autentication
sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            redirect_uri='http://localhost:8080',
            scope='playlist-modify-public'
            )
    )
def generate_rainy_day_playlist():

    #Getting an array of all available genres
    genres = sp.recommendation_genre_seeds()
    genres = genres['genres']

    #Randomly choose 5 genres
    seed_genres = random.choices(population=genres,k=5)

    #Define criterea for songs that would suit the playlist
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

    #Search for tracks that have "rain" in their names
    data_search = sp.search(q='rain', type='track', limit=10)
    rain_results = data_search['tracks']['items']

    #Combine recommended tracks and tracks from search
    final_list = recommendation_tracks + rain_results
    random.shuffle(final_list)

    """
    print(f"Your current mood playlist \nchosen from favorite genres ({','.join(genre for genre in seed_genres)})\
    and songs that have 'rain' in their names):\n")

    #Traverse through the list of track objects and print the info
    for num,track in enumerate(final_list,1):
    
        print(f"{num}.Track name - {track['name']}")
        print(f"Album - {track['album']['name']}")
        print(f"Image - {track['album']['images'][1]['url']}")
        print(f"Artist - {', '.join([artist['name'] for artist in track['artists']])}")
        print(f"Link - {track['external_urls']['spotify']}")
        print("\n")
    """
    return final_list

def create_playlist(): 
    user = sp.me()
    user_id = user['id']
    user_name = user['display_name']

    playlist = sp.user_playlist_create(
        user=user_id,
        name = 'Rainy Day Mood',
        description=f"Tracks for {user_name} on a rainy day"
    )
    playlist_id = playlist['id']
    return playlist_id

def add_tracks():
    items = generate_rainy_day_playlist()
    playlist_id = create_playlist()
    items_id = [item['id'] for item in items]
    sp.playlist_add_items(
        playlist_id=playlist_id,
        items = items_id 
        )
    return items
    
 

