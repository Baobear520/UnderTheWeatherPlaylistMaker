import logging
from .genres_algorithms import *
from .user_data import get_top_genres_from_artists

  
logger = logging.getLogger(__name__)


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
    try:
        criteria = weather_criteria.get(weather,{})
        return criteria 
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {}


def get_recommended_tracks(sp,weather):
    try:
        #Obtain data for track recommendation search
        all_genres = get_all_genres(sp)
        genres = get_top_genres_from_artists(sp)
        pop_genres_names = sort_top_genres(sp,genres)
        top_genres = validate_genres_for_playlist(sp,all_genres,pop_genres_names)
        random_seed_genres = add_random_genres(sp,all_genres,top_genres)
        seed_genres = combined_genres(sp,top_genres,random_seed_genres)
        criterea = define_criterea(sp,weather)

        #Search for track recommendations on Spotify
        data = sp.recommendations(
            **criterea,
            limit=100,
            seed_genres=seed_genres,
            min_popularity=20,
            )

        recommended_tracks = data['tracks']
        logger.info(f'We got {len(recommended_tracks)} tracks for you based on weather criterea')
        return recommended_tracks
    except SpotifyException(reason="Couldn't obtain data from track recommendation search") as e:
        logger.error(f"Couldn't obtain data from track recommendation search. Try reloading the page: {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []


def get_word_search_tracks(sp,status):       
        
    # Search for tracks that have "{status}" in their names
    try:
        if status == 'Clear':
            status = 'Sunny'
        word_search = sp.search(q=status, type='track', limit=10)
        word_search_tracks = word_search['tracks']['items']
        logger.info(f'We got {len(word_search_tracks)} tracks that contain the word {status}')
        return word_search_tracks
    except SpotifyException(reason="Couldn't obtain data from the word {status} track search") as e:
        logger.error(f"Couldn't obtain data from the word {status} track search. Try reloading the page: {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []


def generate_tracks(sp,weather,status):
    try:
        recommended_tracks = get_recommended_tracks(sp,weather)
        word_search_tracks = get_word_search_tracks(sp,status)

        # Combine recommended tracks and tracks from word search
        final_list = recommended_tracks + word_search_tracks
        return final_list
    
    except TypeError as e:
        logger.error(f"{e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []
    
def get_shortlisted_tracks(sp,weather,status):
    try:
        final_list = generate_tracks(sp,weather,status)
        number_of_final_tracks = len(final_list) 
        if number_of_final_tracks < 50:
            k == number_of_final_tracks
        k = 50
        random.shuffle(final_list)
        short_list = final_list[:k]
        logger.info(f'Shortlisted {len(short_list)} randomly selected tracks from the final list')
        
        #Grab a list of track ID's
        items_id = [item['id'] for item in short_list]
        return items_id
    
    except TypeError as e:
        logger.error(f"{e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []





    






    