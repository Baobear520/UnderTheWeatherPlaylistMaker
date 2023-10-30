import random
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth
from .weather import weather_type


#Autentication
sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            redirect_uri='http://localhost:8080',
            scope='user-library-read user-top-read playlist-modify-public'
        )
    )

WEATHER, STATUS = weather_type() 

def get_top_genres():
    # Get the user's liked tracks
    top_artists = sp.current_user_top_artists(limit=20, time_range='long_term')
    genres = []
    for artist in top_artists['items']:
        genres.extend(artist['genres'])
    print(f'You have {len(genres)} favorite genres')
    #Use a dict to store best genres
    popular_genres = {}  
    for g in genres:
            if popular_genres.get(g) is not None:
                popular_genres[g] = popular_genres[g] + 1
            else:
                popular_genres[g] = 1
    sorted_genres_by_occurances = sorted(
        popular_genres.items(),
        key=lambda x:x[1],
        reverse=True)
    popular_genres_names = []
    for data in sorted_genres_by_occurances:
        if data[1] > 1:
            popular_genres_names.append(data[0])

    print(f'Your top genres are {popular_genres_names}')
    return popular_genres_names

def get_genres_for_playlist():
    #Getting an array of all available genres
    genres = sp.recommendation_genre_seeds()['genres']
    print(f'total {len(genres)} genres available')
    
    top_genres = get_top_genres()

    #Verify that genres from saved track exist in the list of all the genres
    for g in top_genres:
        if g not in genres:
            top_genres.remove(g)
            print(f'{g} is not valid genres name. Removed')

    top_pop_genres = top_genres[:3]

    #Remove the pop genres from the whole genres selection to avoid duplicates 
    for i in top_pop_genres:
        if i in genres:
            genres.remove(i)
            print(f'Removing {i} because it is already chosen')
    
    #Randomly choose 2 genres but those that are not in the list of most popular 
    random_seed_genres = random.choices(population=genres,k=2)
    print(f'Randomly selected genres are {random_seed_genres}')

    #Combine selected genres
    seed_genres = top_pop_genres + random_seed_genres
    print(f'{seed_genres} been selected for recommendations')
    return seed_genres

def generate_playlist():
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
    seed_genres = get_genres_for_playlist()
    

    # Get recommended tracks based on the chosen genres and weather criteria
    criteria = weather_criteria.get(WEATHER,{}) 
    
    data = sp.recommendations(
        limit=45,
        seed_genres=seed_genres,
        min_popularity=25,
        **criteria
        )
    if not data: 
        raise SpotifyException(msg="Coudn't get recommendations data from Spotify ")

    recommended_tracks = data['tracks']
    print(f'We got {len(recommended_tracks)} tracks for you')

    if len(recommended_tracks) != 0:
        random.shuffle(recommended_tracks)

        # Search for tracks that have "{WEATHER}" in their names
        word_search = sp.search(q=STATUS, type='track', limit=5)
        word_search_results = word_search['tracks']['items']

        # Combine recommended tracks and tracks from word search
        final_list = recommended_tracks + word_search_results
        random.shuffle(final_list)
        #Grab a list of track ID's
        items_id = [item['id'] for item in final_list]
        return items_id
    else:
        raise SpotifyException("Couldn't any tracks that match the criterea")

    






    if WEATHER in rainy:  
        max_dancebility=0.3,
        max_loudness=0.5,
        max_energy=0.5, 
        max_valence=0.3
    elif WEATHER in cloudy:
        max_dancebility=0.5,
        max_loudness=0.7,
        max_energy=0.6, 
        max_valence=0.5
    elif WEATHER in sunny:
        max_dancebility=0.99,
        max_loudness=0.99,
        max_energy=0.99, 
        max_valence=0.99
    elif WEATHER in snowy_or_rest:
        max_dancebility=0.5,
        max_loudness=0.7,
        max_energy=0.7, 
        max_valence=0.6

    seed_genres = get_genres_for_playlist()
    if seed_genres:
        #Get recommended tracks
        try: 
            data_recomm = sp.recommendations(
            limit=45,
            seed_genres=seed_genres,
            max_dancebility=max_dancebility,
            max_loudness=max_loudness,
            max_energy=max_energy, 
            max_valence=max_valence,
            min_popularity=25
        )
        except SpotifyException as e:
            print('Error occured {e}')
    else: SpotifyException(msg="Couldn't select genres for the playlist")

    try: 
        recommendation_tracks = data_recomm['tracks']
        print(f'We got {len(recommendation_tracks)} for you')
    except SpotifyException as e:
        print('Error occured {e}')
    
    if len(recommendation_tracks) != 0:
        random.shuffle(recommendation_tracks)
        #Search for tracks that have "{WEATHER}" in their names
        word_search = sp.search(q=WEATHER, type='track', limit=5)
        word_search_results = word_search['tracks']['items']

        #Combine recommended tracks and tracks from word search
        final_list = recommendation_tracks + word_search_results
        random.shuffle(final_list)

    
        print(f"Your current {WEATHER} playlist \nchosen from favorite genres ({','.join(genre for genre in seed_genres)}) and songs that have '{WEATHER}' in their names):\n")

    else:
        print('Could find a match')
    
    return final_list