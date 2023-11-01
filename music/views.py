import os
from spotipy import Spotify
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth,SpotifyOauthError
from django.http import Http404, HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render
from .playlist_algorithms import generate_playlist, weather
from .forms import PlaylistForm
from .weather import city_ID


def login(request):
    #Autentication
    sp = Spotify(
        auth_manager=SpotifyOAuth(
            redirect_uri='http://localhost:8080',
            scope='user-library-read user-top-read playlist-modify-public'
        )
    )
    # In your login view, after the user is authenticated
    access_token = sp.auth_manager.get_access_token()
    request.session['access_token'] = access_token

    return redirect('home page')
    
def home_page(request):
    return render(request,'home_page.html')


def create_playlist(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return render(request,'error.html',status=401)
    sp = Spotify(auth=access_token['access_token'])
    
    #Authorize requests to OpenWeather widget
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    city_id = city_ID()

    if request.method == 'POST':
        #Instatniate a PlaylistForm class with data from user's input
        form = PlaylistForm(request.POST)
        if form.is_valid(): #If user's input is valid, grab the value
            playlist_name = form.cleaned_data['playlist_name']
            #Passing the playlist name into sessions
            request.session['playlist_name'] = playlist_name
            #Get current user's id and name
            user = sp.me()
            user_id = user['id']
            user_name = user['display_name']

            #Generate recommended tracks according to the weather and user's taste
            items_id = generate_playlist(sp)
            if not items_id:
                raise SpotifyException(http_status=500,msg='Error occured',code=404,reason="Coudn't find any tracks matching the criterea")
            
            
            #Create a playlist and grab its id and url
            playlist = sp.user_playlist_create(
                           user=user_id,
                            name = playlist_name,
                            description=f"Tracks for {user_name} on a {weather} day"
                        )
            if not playlist:
                return render(request,'error.html',status=500)
        
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
                return render(request,'error.html',status=500)
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
    playlist_name = request.session.get('playlist_name','__')
    return render(
        request,
        'created.html',
        context = {
            'spotify_link':spotify_link,
            'playlist_name':playlist_name
            }
        )