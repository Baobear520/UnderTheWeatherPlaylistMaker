import os
from spotipy import Spotify
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth,SpotifyOauthError
from django.http import Http404, HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render
from .user_data import get_user_info
from .create_populate_playlist import *
from .playlist_algorithms import generate_playlist
from .forms import PlaylistForm
from .weather import city_ID,weather_type


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

    #Authorize requests to OpenWeather widget
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    city_id = city_ID()

    #Obtain weather data
    weather, status = weather_type()

    #Obtain Spotufy access token
    access_token = request.session.get('access_token')
    if not access_token:
        return render(request,'error.html',status=401)
    sp = Spotify(auth=access_token['access_token'])
    
    
    if request.method == 'POST':
        #Instatniate a PlaylistForm class with data from user's input
        form = PlaylistForm(request.POST)
        if form.is_valid(): #If user's input is valid, grab the value
            playlist_name = form.cleaned_data['playlist_name']
            #Passing the playlist name into sessions
            request.session['playlist_name'] = playlist_name

            #Grab user ID and user_name
            user_id, user_name = get_user_info(sp)
            if not user_id or not user_name:
                return render(request,'error.html',status=500)

            #Generate recommended tracks according to the weather and user's taste
            items_id = generate_playlist(sp,weather,status)
            if not items_id:
                return render(request,'error.html',status=500)
            
            #Create a new empty playlist
            playlist = create_new_playlist(sp,user_id,user_name,playlist_name,weather)
            
            if not playlist:
                return render(request,'error.html',status=500)
        
            playlist_id = playlist['id']
            playlist_url = playlist['external_urls']['spotify']

            #Passing the url into sessions
            request.session['spotify_link'] = playlist_url
            
            #Adding generated tracks into the new playlist
            new_playlist = add_tracks_to_playlist(sp,playlist_id,items_id)
            if not new_playlist:
                return render(request,'error.html',status=500)
            #If successfully populated, redirect to /create-playlist/success url
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
    #If the form is not valid, render the same page and re-instatniate the form
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

    #Grab these variables to pass into the template
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