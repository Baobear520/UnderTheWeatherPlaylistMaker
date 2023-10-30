import os
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth,SpotifyOauthError
from django.shortcuts import redirect, render
from .playlist_algorithms import generate_playlist, WEATHER
from .forms import PlaylistForm
from .weather import city_ID


#Authorization
sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            redirect_uri='http://localhost:8080',
            scope ='user-library-read user-top-read playlist-modify-public'
        )
    )

def login(request):
    
    return redirect('home page')
    
def home_page(request):
    return render(request,'home_page.html')


def create_playlist(request):
    #Authorize requests to OpenWeather widget
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    city_id = city_ID()
   
    
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist_name = form.cleaned_data['playlist_name']

            #Get current user's id and name
            user = sp.me()
            user_id = user['id']
            user_name = user['display_name']

            #Generate recommended tracks according to the weather and user's taste
            items_id = generate_playlist()
        
            #Create a playlist and grab its id and url
            playlist = sp.user_playlist_create(
                            user=user_id,
                            name = playlist_name,
                            description=f"Tracks for {user_name} on a {WEATHER} day"
                        )
            if not playlist:
                raise SpotifyException(msg='Error occured while creating a playlist')
            playlist_id = playlist['id']
            playlist_url = playlist['external_urls']['spotify']

            #Passing the url into sessions
            request.session['spotify_link'] = playlist_url
            
            #Add generated tracks to the new playlist
            new_playlist = sp.playlist_add_items(
                playlist_id=playlist_id,
                items = items_id 
            )
            if not new_playlist:
                raise SpotifyException(msg="Couldn't add tracks to the playlist")
            return redirect('created')
                  
        else:
            return render(
                request, 
                'create_playlist.html',
                context={
                    'form': form,
                    'api_key': api_key,
                    'city_id': city_id,
                }
            )
    else:
        form = PlaylistForm()

    return render(
                request, 
                'create_playlist.html',
                context={
                    'form': form,
                    'api_key': api_key,
                    'city_id': city_id,
                }
            )
    
def created(request):
    spotify_link = request.session.get('spotify_link','#')
    return render(request,'created.html',{'spotify_link':spotify_link})