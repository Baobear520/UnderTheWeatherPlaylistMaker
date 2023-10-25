import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect, render
from .rainy_day import generate_rainy_day_playlist
from .forms import PlaylistForm


#Authorization
sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            redirect_uri='http://localhost:8080',
            scope ='playlist-modify-public'
        )
    )
def login(request):
    return render(request,'practice.html')


def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist_name = form.cleaned_data['playlist_name']

            #Get current user's id and name
            user = sp.me()
            user_id = user['id']
            user_name = user['display_name']

            #Create a playlist and grab its id and url
            playlist = sp.user_playlist_create(
                            user=user_id,
                            name = playlist_name,
                            description=f"Tracks for {user_name} on a ___ day"
                        )
            playlist_id = playlist['id']
            playlist_url = playlist['external_urls']['spotify']

            #Use a __day algorithm to generate tracks for the playlist
            #Should be a choice depending on the weather

            items = generate_rainy_day_playlist()
            items_id = [item['id'] for item in items]
            
            #Add generated tracks to the new playlist
            sp.playlist_add_items(
                playlist_id=playlist_id,
                items = items_id 
            )
            return render(
                request, 
                'create_playlist.html',
                context={
                    'form': form,
                    'spotify_link': playlist_url,
                }
            )
        else:
            return render(request, 'create_playlist.html',{'form': form})

    else:
        form = PlaylistForm()

    return render(request, 'create_playlist.html',{'form': form})
    
    