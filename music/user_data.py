
def get_user_info(sp):
#Get current user's id and name
    user = sp.me()
    user_id = user['id']
    user_name = user['display_name']
    return user_id, user_name

#Get a list of most popular genres from user's top artists list
def get_top_genres_from_artists(sp):

    # Get the user's liked tracks
    top_artists = sp.current_user_top_artists(limit=20, time_range='long_term')
    genres = []
    for artist in top_artists['items']:
        genres.extend(artist['genres'])
    print(f'You have {len(genres)} favorite genres')
    return genres