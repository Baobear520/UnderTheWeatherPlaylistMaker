import logging
from spotipy.exceptions import SpotifyException


logger = logging.getLogger(__name__)


def create_new_playlist(sp,user_id,user_name,playlist_name,weather):
    #Create a playlist and grab its id and url
    try:
        
        playlist = sp.user_playlist_create(
                    user=user_id,
                    name = playlist_name,
                    description=f"Tracks for {user_name} on a {weather} day"
                )
        logger.info(f"Playlist '{playlist_name}' has been created. ")
        return playlist
    except SpotifyException(reason="Couldn't create a new playlist") as e:
        logger.error(f"Couldn't create a new playlist. Try reloading the page again: {e}")
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        return None


def add_tracks_to_playlist(sp,playlist_id,items_id):
    #Add generated tracks to the new playlist
    try:
        new_playlist = sp.playlist_add_items(
            playlist_id=playlist_id,
            items = items_id 
        )
        logger.info(f"Playlist with id '{playlist_id}' has been populated with {len(items_id)} tracks.")
        return new_playlist
    except SpotifyException(reason="Couldn't add tracks to the playlist") as e:
        logger.error(f"Couldn't add tracks to the playlist. Try reloading the page again: {e}")
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        return None