import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth 
from .weather import weather_type



#Autentication
sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            redirect_uri='http://localhost:8080',
            scope ='playlist-modify-public'
        )
    )

WEATHER = weather_type()

def generate_playlist():

    #Getting an array of all available genres
    genres = sp.recommendation_genre_seeds()
    genres = genres['genres']

    #Extract user's favorite genres from favorite artists
    items = sp.current_user_top_artists()['items']
    list_genres = [genre['genre'] for genre in items]
    



    #Randomly choose 2 genres
    random_seed_genres = random.choices(population=genres,k=2)
    
    #Define lists of similar weather types
    rainy = ['Thunderstorm','Drizzle','Rain']
    cloudy = ['Clouds']
    sunny = ['Clear']
    snowy_or_rest = ['Snow','Atmosphere']

    #Define criterea for songs that would suit the playlist


    if WEATHER in rainy:  
        seed_genres=seed_genres,
        max_dancebility=0.3,
        min_dancebility = 0,
        max_loudness=0.5,
        min_loudness = 0,
        max_energy=0.5, 
        min_energy = 0,
        max_valence=0.3,
        min_valence=0
    elif WEATHER in cloudy:
        seed_genres=seed_genres,
        max_dancebility=0.5,
        min_dancebility = 0.2,
        max_loudness=0.7,
        min_loudness = 0.3,
        max_energy=0.6, 
        min_energy = 0.2,
        max_valence=0.5,
        min_valence=0
    elif WEATHER in sunny:
        seed_genres=seed_genres,
        max_dancebility=0.99,
        min_dancebility = 0.5,
        max_loudness=0.99,
        min_loudness = 0.5,
        max_energy=0.99, 
        min_energy = 0.5,
        max_valence=0.99,
        min_valence=0.5
    elif WEATHER in snowy_or_rest:
        seed_genres=seed_genres,
        max_dancebility=0.5,
        min_dancebility = 0.2,
        max_loudness=0.7,
        min_loudness = 0,
        max_energy=0.7, 
        min_energy = 0,
        max_valence=0.6,
        min_valence=0
    data_recomm = sp.recommendations(
        limit=45,
        seed_genres=seed_genres,
        max_dancebility=max_dancebility,
        min_dancebility=min_dancebility,
        max_loudness=max_loudness,
        min_loudness=min_loudness,
        max_energy=max_energy, 
        min_energy=min_energy,
        max_valence=max_valence,
        min_valence=min_valence,
        min_popularity=30
    )
        
    recommendation_tracks = data_recomm['tracks']

    #Search for tracks that have "____" in their names
    word_search = sp.search(q=WEATHER, type='track', limit=5)
    word_search_results = word_search['tracks']['items']

    #Combine recommended tracks and tracks from word search
    final_list = recommendation_tracks + word_search_results
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

"""
def create_playlist(): 
    #Get current user's id and name
    user = sp.me()
    user_id = user['id']
    user_name = user['display_name']

    #Check if a playlist with the desired name already exists
    name = f'{MOOD} Day Mood'
    my_playlists = sp.current_user_playlists()
    
    playlist_names = [playlist['name'] for playlist in my_playlists['items']]
    if name not in playlist_names:
        #Create a playlist and grab its id
        playlist = sp.user_playlist_create(
            user=user_id,
            name = 'Rainy Day Mood',
            description=f"Tracks for {user_name} on a rainy day"
        )
        playlist_id = playlist['id']
        return playlist_id
    else:
        raise MyException('Playlist with this name already exists')

def add_tracks():

    #Combine the above logic
    playlist_id = create_playlist()
    items = generate_rainy_day_playlist()
    items_id = [item['id'] for item in items]
    #Add generated tracks to the new playlist
    sp.playlist_add_items(
        playlist_id=playlist_id,
        items = items_id 
        )
    return items
"""

   


    
 

