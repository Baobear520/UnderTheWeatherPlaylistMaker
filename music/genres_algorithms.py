import random, logging
from spotipy.exceptions import SpotifyException


logger = logging.getLogger(__name__)


def get_all_genres(sp):
    #Getting an array of all available genres
    try:
        all_genres = sp.recommendation_genre_seeds()['genres']
        logger.info(f"Obtained available genres from Spotify")
        return all_genres
    except SpotifyException(reason="Couldn't obtain available genres from Spotify.") as e:
        logger.error(f"Couldn't obtain available genres from Spotify. Try reloading the page: {e}")
        return []
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        return []
    

#Get a sorted list of the most popular genres (occur more than once)
def sort_top_genres(sp, genres):
    try:
        popular_genres = {}
        #Loop through the list of all genres and add the key and value into the dict
        for g in genres:
            if g in popular_genres:
                popular_genres[g] += 1
            else:
                popular_genres[g] = 1

        logger.info("Obtained a sorted list of tuples (genre, number of occurrences)")

        # Get a sorted list of tuples (genre, number of occurrences)
        sorted_genres_by_occurrences = sorted(
            popular_genres.items(),
            key=lambda x: x[1],
            reverse=True
        )
        # Get a sorted list of genres that occur more than once
        popular_genres_names = [data[0] for data in sorted_genres_by_occurrences if data[1] > 1]
        return popular_genres_names
    except ValueError as e:
        logger.error(f"No available genres to sort: {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []


def validate_genres_for_playlist(sp,all_genres,pop_genres_names):
    #Validate that genres from top artist exist in the list of all the genres
    try:
        for g in pop_genres_names:
            if g not in all_genres:
                pop_genres_names.remove(g)
        logger.info(f"Obtained a list of validated most popular genres")
        return pop_genres_names
    except ValueError as e:
        logger.error(f"No data in most popular genres : {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []


#Select randomly chosen genres depending on the existing number of top_genres
def add_random_genres(sp,all_genres,top_genres):
    number_of_top_genres = len(top_genres) #how many genres we got from user's info
    logger.info(f"Number of the most popular genres - {number_of_top_genres}")
    number_of_random_genres = 5 #max number of genre seeds used in sp.recommendations 
    
    try:
        #If user has no top artist data we populate all genre seeds randomly 
        if number_of_top_genres == 0:
            random_seed_genres = random.choices(population=all_genres,k=number_of_random_genres)
        
        #If user only has 1-2 genres that occur more than once
        elif 0 < number_of_top_genres < 3:
            number_of_random_genres = number_of_random_genres - number_of_top_genres

            #Randomly select the rest of the genres 
            #The genres must not be in top_genres
            random_seed_genres = []
            while number_of_random_genres != 0:
                genre = random.choice(seq=all_genres) 
                if genre not in top_genres and genre not in random_seed_genres:
                    random_seed_genres.append(genre)
                    logger.info(f'Adding {genre} to the list')
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
                    logger.info(f'Adding {genre} to the list')
                number_of_random_genres -= 1

        logger(f"Randomly selected genres are {','.join(random_seed_genres)}")
        return random_seed_genres
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []

#Combine selected genres
def combined_genres(sp,top_genres,random_seed_genres):
    try:
        top_genres = top_genres[:3]
        logger.info(f"Top-3 most popular genres are {','.join(top_genres)}")
        seed_genres = top_genres + random_seed_genres
        logger.info(f"{','.join(seed_genres)} been selected for recommendations")
        return seed_genres
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []