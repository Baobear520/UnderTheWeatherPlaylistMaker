import random
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth
from .weather import weather_type



#Autentication
sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            redirect_uri='http://localhost:8080',
            scope='user-library-read'
        )
    )

WEATHER = weather_type()


def saved_tracks_genres():
    # Get the user's liked tracks
    results = sp.current_user_saved_tracks(limit=50)

    popular_genres = {}
    # Iterate through the results to access the liked track information
    for item in results['items']:
        track = item['track']
        
        # Use the artist's genres as an approximation of the track's genre
        artist_id = track['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        
        genres = artist_info['genres']

        for g in genres:
            if popular_genres.get(g) is not None:
                popular_genres[g] = popular_genres[g] + 1
            else:
                popular_genres[g] = 1
    sorted_genres_by_occurances = sorted(
        popular_genres.items(),
        key=lambda x:x[1],
        reverse=True)
    saved_tracks_popular_genres = [data[0] for data in sorted_genres_by_occurances]
    return saved_tracks_popular_genres

def get_genres_for_playlist():
    #Getting an array of all available genres
    genres = sp.recommendation_genre_seeds()
    genres = genres['genres']
    print(f'total {len(genres)} genres available')
    
    #Grab 3 most popular genres amongst user's saved tracks
    pop_genres = saved_tracks_genres()
    print(f'There are {len(pop_genres)} most popular genres in your library')

    #Verify that genres from saved track exist in the list of all the genres
    for g in pop_genres:
        if g not in genres:
            pop_genres.remove(g)
            print(f'{g} is not valid genres name. Removed')

    top_pop_genres = pop_genres[:3]

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

    #Define lists of similar weather types
    rainy = ['Thunderstorm','Drizzle','Rain']
    cloudy = ['Clouds']
    sunny = ['Clear']
    snowy_or_rest = ['Snow','Atmosphere']

    #Define critereas for songs that would suit the playlist

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
        
    recommendation_tracks = data_recomm['tracks']
    print(f'We got {len(recommendation_tracks)} for you')
    
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