import spotipy, random
from spotipy.oauth2 import SpotifyOAuth 



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        redirect_uri='http://localhost:8080',
        )
    )

all_playlists = sp.current_user_playlists()['items']
for playlist in all_playlists:
    sp.current_user_unfollow_playlist(playlist_id=playlist['id'])

    """
    data = sp.recommendations(
                limit=45,
                seed_genres=['pop'],
                min_popularity=25,
                min_danceability=0.5,
                min_energy=0.5,
            )
    recommended_tracks = data['tracks']
    print(f"Your current day playlist:\n")
    for track in recommended_tracks:
        print(track['name'])
    """

