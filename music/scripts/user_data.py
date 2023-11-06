import logging
from spotipy.exceptions import SpotifyException

logger = logging.getLogger(__name__)


def get_user_info(sp):
    #Get current user's id and name
    try:
        user = sp.me()
        user_id = user['id']
        user_name = user['display_name']
        logger.info(f"Current user - {user_name}, user_id - {user_id}")
        return user_id, user_name
    except SpotifyException(reason="Couldn't obtain user credentials") as e:
        logger.error(f"Couldn't obtain user credentials. Try reloading the page again: {e}")
        return None,None
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        return None, None



#Get a list of all user's playlists
def get_all_playlists_names(sp):
    try:
        all_playlists = sp.current_user_playlists()['items']
        all_playlists_names = [playlist['name'] for playlist in all_playlists]
        logger.info(f"Obtained a list of all the user's playlists")
        return all_playlists_names
    except SpotifyException(reason="Couldn't obtain user's playlists") as e:
        logger.error(f"Couldn't obtain user's playlists. Try reloading the page again: {e}")
        return []
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        return []

#Get a list of most popular genres from user's top artists list
def get_top_genres_from_artists(sp):
    # Get the user's liked tracks
    try:
        top_artists = sp.current_user_top_artists(limit=20,time_range='long_term')
        logger.info(f"Obtained a list of user's top-20 artists")
        genres = []
        for artist in top_artists['items']:
            genres.extend(artist['genres'])
        logger.info(f"Current user has {len(genres)} favorite genres")
        return genres
    except SpotifyException(reason="Couldn't obtain user's top artists data") as e:
        logger.error(f"Couldn't obtain user's top artists data. Try reloading the page again: {e}")
        return []
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        return []
         