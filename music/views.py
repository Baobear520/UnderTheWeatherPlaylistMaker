import logging
from django.shortcuts import redirect, render
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth,SpotifyOauthError
from pyowm.commons import exceptions as ow_exceptions
from config.credentials import OWM_API_KEY
from .scripts.location import my_IP_location
from .scripts.user_data import get_user_info
from .scripts.create_populate_playlist import *
from .scripts.playlist_algorithms import generate_playlist
from .scripts.weather import city_ID,weather_type,get_owm_mng
from .forms import PlaylistForm


logger = logging.getLogger(__name__)


def login(request):
    #Autentication
    try:
        sp = Spotify(
            auth_manager=SpotifyOAuth(
                redirect_uri='http://localhost:8080',
                scope='user-library-read user-top-read playlist-modify-public'
            )
        )
        logger.info('Spotify user has been authenticated')
        # In your login view, after the user is authenticated
        access_token = sp.auth_manager.get_access_token()
        request.session['access_token'] = access_token
        return redirect('home')
    except SpotifyOauthError as e:
        # Handle the exception, you can log it and provide a user-friendly error message
        logger.error(f"Spotify authentication failed: {e}")
        return render(request, '1/error.html', {'error_message': 'Spotify authentication failed'})

    
def home_page(request):
    return render(request,'1/home.html')

def about(request):
    return render(request,'1/about.html')

def create_playlist(request):

    #Authorize requests to OpenWeather widget
    try:
        api_key = OWM_API_KEY
        #Obtain coordinates for the weather API
        lat, lon = my_IP_location()
        mng = get_owm_mng(api_key)
        #Obtain weather data for the widget and further use
        weather, status = weather_type(mng,lat,lon)
        city_id = city_ID(mng,lat,lon)

        #Obtain Spotify access token
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request,'error.html',status=401)
        #Pass the access token
        sp = Spotify(auth=access_token['access_token'])
        
        if request.method == 'POST':
            #Instantiate a PlaylistForm class with data from user's input
            form = PlaylistForm(request.POST,sp=sp)
            if form.is_valid(): #If user's input is valid, grab the value
                playlist_name = form.cleaned_data['playlist_name']
            
                #Passing the playlist name into sessions
                request.session['playlist_name'] = playlist_name

                #Grab user ID and user_name
                user_id, user_name = get_user_info(sp)
                if not user_id and not user_name:
                    return render(request, '1/error.html', {"error_message": "Couldn't get access to your profile information."}, status=404)

                #Generate recommended tracks according to the weather and user's taste
                items_id = generate_playlist(sp,weather,status)
               
                if items_id == []:
                    return render(request, '1/error.html', {"error_message": "Couldn't find any tracks for you."}, status=404)

                #Create a new empty playlist
                playlist = create_new_playlist(sp,user_id,user_name,playlist_name,weather)
                if not playlist:
                    return render(request, 'error.html', {"error_message": "Couldn't create a new playlist."}, status=404)
                
                playlist_id = playlist['id']
                playlist_url = playlist['external_urls']['spotify']

                #Passing the url into sessions
                request.session['spotify_link'] = playlist_url
                
                #Adding generated tracks into the new playlist
                new_playlist = add_tracks_to_playlist(sp,playlist_id,items_id)
                if not new_playlist:
                    return render(request, '1/error.html', {"error_message": "Couldn't add tracks to {playlist_name} playlist."}, status=404)
                #If successfully populated, redirect to /create-playlist/success url
                return redirect('created')
            
            #If the form is not valid, render the same page with error message from the form
            else:
                return render(
                    request, 
                    '1/create_playlist.html',
                    context={
                        'form': form,
                        'api_key': api_key,
                        'city_id': city_id,
                    }
                )
        #If http method is not POST:
        else:
            form = PlaylistForm()
            return render(
                        request, 
                        '1/create_playlist.html',
                        context={
                            'form': form,
                            'api_key': api_key,
                            'city_id': city_id,
                        }
                    )
    except SpotifyException as e:
        logger.error(f"Spotify authorization failed: {e}")
        return render(request, '1/error.html', {'error_message': 'Spotify authorization failed. Please log in again.'}, status=401)

    except ow_exceptions.PyOWMError as e:
        logger.error(f"Weather data retrieval failed: {e}")
        return render(request, '1/error.html', {'error_message': 'Weather data retrieval failed. Please try again later.'}, status=500)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return render(request, '1/error.html', {'error_message': 'An unexpected error occurred. Please try again later.'}, status=500)


def created(request):

    #Grab these variables to pass into the template
    spotify_link = request.session.get('spotify_link','#')
    playlist_name = request.session.get('playlist_name','__')
    return render(
        request,
        '1/created.html',
        context = {
            'spotify_link':spotify_link,
            'playlist_name':playlist_name
            }
        )