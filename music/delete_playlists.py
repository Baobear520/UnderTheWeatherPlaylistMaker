import spotipy
from spotipy.oauth2 import SpotifyOAuth 



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        redirect_uri='http://localhost:8080',
        )
    )
"""
all_playlists = sp.current_user_playlists()['items']
for playlist in all_playlists:
    sp.current_user_unfollow_playlist(playlist_id=playlist['id'])
"""

# Get the user's liked tracks
results = sp.current_user_saved_tracks()

popular_genres = {}
# Iterate through the results to access the liked track information
for item in results['items']:
    track = item['track']
    
    # Use the artist's genres as an approximation of the track's genre
    artist_id = track['artists'][0]['id']
    artist_info = sp.artist(artist_id)
    
    genres = artist_info['genres']
    for g in genres:
        if popular_genres.get(g,None) is not None:
            popular_genres[g] = popular_genres[g] + 1
        else:
            popular_genres[g] = 1
sorted_genres_by_occurances = sorted(popular_genres.items(),key=lambda x:x[1],reverse=True)
saved_tracks_popular_genres = [data[0] for data in sorted_genres_by_occurances[:3]]
print(saved_tracks_popular_genres)    

    


    
    






    

    


