
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect, render
from .rainy_day import generate_rainy_day_playlist
from .forms import PlaylistForm

# Create your views here.

sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            redirect_uri='http://localhost:8080',
            scope ='playlist-modify-public'
        )
    )


def home(request):
    if request.method == 'POST':
        playlist_form = PlaylistForm(request.POST)
        if playlist_form.is_valid():
            # Perform the playlist creation logic
            #Get current user's id and name
            user = sp.me()
            user_id = user['id']
            user_name = user['display_name']

            playlist_name = playlist_form.cleaned_data['playlist_name']

            #Check if a playlist with the desired name already exists
            
            #my_playlists = sp.current_user_playlists()
            #playlist_names = [playlist['name']for playlist in my_playlists['items']]
            #if playlist_name not in playlist_names:

            #Create a playlist and grab its id
            playlist = sp.user_playlist_create(
                            user=user_id,
                            name = playlist_name,
                            description=f"Tracks for {user_name} on a ___ day"
                        )
            playlist_id = playlist['id']

            #Use a __day algorithm to generate tracks for the playlist
            #Should be a choice depending on the weather

            items = generate_rainy_day_playlist()
            items_id = [item['id'] for item in items]
            
            #Add generated tracks to the new playlist
            sp.playlist_add_items(
                playlist_id=playlist_id,
                items = items_id 
            )
            #Get the url of the playlist
            my_playlists = sp.current_user_playlists()
            for playlist in my_playlists['items']:
                if playlist['name'] == playlist_name:
                    url = playlist['external_urls']['spotify']
                    return render(
                        request, 'home.html',
                        {'playlist_form': playlist_form},
                        context={
                            'url': url
                        }
                    )

    #If the data hasn't been validated, try to input again
    else:
        playlist_form = PlaylistForm()
    return render(
        request, 'home.html',
        {'playlist_form': playlist_form})  

