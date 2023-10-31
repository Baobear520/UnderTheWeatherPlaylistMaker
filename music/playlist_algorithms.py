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

try: 
    WEATHER, STATUS = weather_type() 
except TypeError:
    print("Couldn't obtain weather data")




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
    #Get a sorted list of tuples (genre, number of occurences)
    sorted_genres_by_occurances = sorted(
        popular_genres.items(),
        key=lambda x:x[1],
        reverse=True)
    #Get a sorted list of genres only that occur more than once
    popular_genres_names = []
    for data in sorted_genres_by_occurances:
        if data[1] > 1:
            popular_genres_names.append(data[0])
    return popular_genres_names

def get_genres_for_playlist():
    #Getting an array of all available genres
    genres = sp.recommendation_genre_seeds()['genres']
    print(f'total {len(genres)} genres available')
    
    #Retrieve a list of top genres
    top_genres = get_top_genres()
    
    #Verify that genres from top artist exist in the list of all the genres
    for g in top_genres:
        if g not in genres:
            top_genres.remove(g)
    
    #Add randomly chosen genres depending on the existing number of top_genres
    number_of_top_genres = len(top_genres) #how many genres we got from user's info
    number_of_random_genres = 5 #max number of genre seeds used in .recommendations 

    #If user has no top artist data we populate all genre seeds randomly 
    if number_of_top_genres == 0:
        random_seed_genres = random.choices(population=genres,k=number_of_random_genres)
    
    #If user only has 1-2 genres that occur more than once
    elif 0 < number_of_top_genres < 3:
        number_of_random_genres = number_of_random_genres - number_of_top_genres
        print(f'We will need {number_of_random_genres} more genres')
        #Randomly select the rest of the genres 
        #The genres must not be in top_genres
        random_seed_genres = []
        while number_of_random_genres != 0:
            genre = random.choice(seq=genres) 
            if genre not in top_genres:
                random_seed_genres.append(genre)
                print(f'Adding {genre} to the list')
            else:
                print(f'{genre} is already in top_genres')
            number_of_random_genres -= 1

    else:
        #We decide to choose top-3 from top_genres
        top_genres = top_genres[:3]
        #Randomly select the rest of the genres 
        #The genres must not be in top_genres
        number_of_random_genres = 2
        random_seed_genres = []
        while number_of_random_genres != 0:
            genre = random.choice(seq=genres) 
            if genre not in top_genres:
                random_seed_genres.append(genre)
            number_of_random_genres -= 1

    print(f"Randomly selected genres are {','.join(random_seed_genres)}")
    
    #Combine selected genres
    seed_genres = top_genres + random_seed_genres
    print(f"{','.join(seed_genres)} been selected for recommendations")
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
        raise Exception(msg="Coudn't get recommendations data from Spotify ")

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
        raise Exception("Couldn't any tracks that match the criterea")

    






    