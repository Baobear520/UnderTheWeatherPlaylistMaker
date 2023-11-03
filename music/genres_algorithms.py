import random, logging

logger = logging.getLogger(__name__)

def get_all_genres(sp):
    #Getting an array of all available genres
    all_genres = sp.recommendation_genre_seeds()['genres']
    return all_genres


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
    print(f'Pop genres names are {pop_genres_names}')
    #Validate that genres from top artist exist in the list of all the genres
    for g in pop_genres_names:
        if g not in all_genres:
            pop_genres_names.remove(g)
    return pop_genres_names


#Select randomly chosen genres depending on the existing number of top_genres
def add_random_genres(sp,all_genres,top_genres):

    number_of_top_genres = len(top_genres) #how many genres we got from user's info
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