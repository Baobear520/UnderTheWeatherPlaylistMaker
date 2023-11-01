import random
from .weather import weather_type


try: 
    weather, status = weather_type() 
except TypeError:
    print("Couldn't obtain weather data")


def get_all_genres(sp):
    #Getting an array of all available genres
    all_genres = sp.recommendation_genre_seeds()['genres']
    return all_genres


#Get a list of most popular genres from user's top artists list
def get_top_genres_from_artists(sp):

    # Get the user's liked tracks
    top_artists = sp.current_user_top_artists(limit=20, time_range='long_term')
    genres = []
    for artist in top_artists['items']:
        genres.extend(artist['genres'])
    print(f'You have {len(genres)} favorite genres')
    return genres

#Get a sorted list of the most popular genres (occur more than once)
def sort_top_genres(sp,genres):
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

def validate_genres_for_playlist(sp,all_genres,pop_genres_names):
    print(f'total {len(all_genres)} genres available')
    
    #Validate that genres from top artist exist in the list of all the genres
    for g in pop_genres_names:
        if g not in all_genres:
            pop_genres_names.remove(g)
    return pop_genres_names


#Select randomly chosen genres depending on the existing number of top_genres
def add_random_genres(sp,all_genres,top_genres):

    number_of_top_genres = len(top_genres) #how many genres we got from user's info
    print(number_of_top_genres)
    number_of_random_genres = 5 #max number of genre seeds used in .recommendations 

    #If user has no top artist data we populate all genre seeds randomly 
    if number_of_top_genres == 0:
        random_seed_genres = random.choices(population=all_genres,k=number_of_random_genres)
    
    #If user only has 1-2 genres that occur more than once
    elif 0 < number_of_top_genres < 3:
        number_of_random_genres = number_of_random_genres - number_of_top_genres
        print(f'We will need {number_of_random_genres} more genres')

        #Randomly select the rest of the genres 
        #The genres must not be in top_genres
        random_seed_genres = []
        while number_of_random_genres != 0:
            genre = random.choice(seq=all_genres) 
            if genre not in top_genres and genre not in random_seed_genres:
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
            genre = random.choice(seq=all_genres) 
            if genre not in top_genres and genre not in random_seed_genres:
                random_seed_genres.append(genre)
            number_of_random_genres -= 1

    print(f"Randomly selected genres are {','.join(random_seed_genres)}")
    return random_seed_genres


#Combine selected genres
def combined_genres(sp,top_genres,random_seed_genres):
    seed_genres = top_genres[:3] + random_seed_genres
    print(f"{','.join(seed_genres)} been selected for recommendations")
    return seed_genres



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
    
   

    






    