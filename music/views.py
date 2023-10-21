from django.forms import ValidationError
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.http import HttpResponse, JsonResponse

from django.template.response import TemplateResponse
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
    if request.method == "POST":
        my_form = PlaylistForm(request.POST)
        if my_form.is_valid():
            return render(request,'practice.html')
        else:
            return render(request,'home_page.html',{'form': my_form})
    my_form = PlaylistForm()
    return render(request,'home_page.html',{'form': my_form})


def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist_name = form.cleaned_data['playlist_name']

            #Validate that the playlist name is unique
            all_playlists = sp.current_user_playlists()['items']
            all_playlists_names = [playlist['name'] for playlist in all_playlists]
            #if the playlist name is unique, proceed
            if playlist_name not in all_playlists_names:
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
                        'all_playlists_names': all_playlists_names
                    }
                )
            else:
                #Add an error message to the form
                form.add_error(error=ValidationError('Playlist name must be unique.'),field='playlist_name')
                form.clean()
    else:
        form = PlaylistForm()
    return render(request, 'create_playlist.html',{'form': form})
    