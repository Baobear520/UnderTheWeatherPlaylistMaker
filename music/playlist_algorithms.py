from .genres_algorithms import *
from .user_data import get_top_genres_from_artists
from .weather import weather_type


try: 
    weather, status = weather_type() 
except TypeError:
    print("Couldn't obtain weather data")


def define_criterea(sp,weather):
    
    # Define criteria for songs that suit the playlist based on weather
    weather_criteria = {
        'Rainy': {
            'max_danceability': 0.3,
            'max_loudness': 0.5,
            'max_energy': 0.5,
            'max_valence': 0.3
        },
        'Cloudy': {
            'max_danceability': 0.6,
            'max_loudness': 0.7,
            'max_energy': 0.7,
            'max_valence': 0.5
        },
        'Sunny': {
            'min_danceability': 0.5,
            'min_energy': 0.5,
        },
        'Snowy/Athmosphere': {
            'max_danceability': 0.5,
            'max_loudness': 0.7,
            'max_energy': 0.7,
            'max_valence': 0.6
        }
    }
    # Get recommended tracks based on the chosen genres and weather criteria
    criteria = weather_criteria.get(weather,{})
    return criteria 


def get_recommended_tracks(sp):

    all_genres = get_all_genres(sp)
    genres = get_top_genres_from_artists(sp)
    pop_genres_names = sort_top_genres(sp,genres)
    top_genres = validate_genres_for_playlist(sp,all_genres,pop_genres_names)
    random_seed_genres = add_random_genres(sp,all_genres,top_genres)
    seed_genres = combined_genres(sp,top_genres,random_seed_genres)
    criterea = define_criterea(sp,weather)

    
    data = sp.recommendations(
        **criterea,
        limit=45,
        seed_genres=seed_genres,
        min_popularity=25,
        )

    recommended_tracks = data['tracks']
    print(f'We got {len(recommended_tracks)} tracks for you')

    if len(recommended_tracks) != 0:
        random.shuffle(recommended_tracks)

    return recommended_tracks
        
def get_word_search_tracks(sp):       
        
    # Search for tracks that have "{status}" in their names

    word_search = sp.search(q=status, type='track', limit=5)
    word_search_tracks = word_search['tracks']['items']
    return word_search_tracks


def generate_playlist(sp):
    recommended_tracks = get_recommended_tracks(sp)
    word_search_tracks = get_word_search_tracks(sp)

    # Combine recommended tracks and tracks from word search
    final_list = recommended_tracks + word_search_tracks
    random.shuffle(final_list)

    #Grab a list of track ID's
    items_id = [item['id'] for item in final_list]
    return items_id
    
   

    






    