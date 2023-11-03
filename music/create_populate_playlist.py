import logging

logger = logging.getLogger(__name__)

def create_new_playlist(sp,user_id,user_name,playlist_name,weather):
#Create a playlist and grab its id and url
    playlist = sp.user_playlist_create(
                    user=user_id,
                    name = playlist_name,
                    description=f"Tracks for {user_name} on a {weather} day"
                        )
    return playlist


def add_tracks_to_playlist(sp,playlist_id,items_id):

    #Add generated tracks to the new playlist
    new_playlist = sp.playlist_add_items(
        playlist_id=playlist_id,
        items = items_id 
    )
    return new_playlist