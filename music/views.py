import logging
from django.shortcuts import redirect, render
from spotipy import Spotify, DjangoSessionCacheHandler
from spotipy.oauth2 import SpotifyOAuth
from pyowm.commons import exceptions as ow_exceptions
from config.settings.base import OWM_API_KEY
from .scripts.user_data import get_user_info
from .scripts.create_populate_playlist import *
from .scripts.playlist_algorithms import get_shortlisted_tracks
from .scripts.weather import city_ID,weather_type,get_owm_mng
from .forms import PlaylistForm



logger = logging.getLogger(__name__)



def login(request):
    # If request.code exists, then we are set and we can authenticate the user
    if request.code:
        cache_handler = DjangoSessionCacheHandler(request)
        auth_manager = SpotifyOAuth(
            scope='user-library-read user-top-read playlist-modify-public',
            cache_handler=cache_handler,
            show_dialog=True,
        )
        auth_manager.get_access_token(request.code)

        return redirect("login-success")

    # Else, redirect them to authenticate
    return redirect("authenticate")

# url to this view is authenticate/
def authenticate(request):
    context = {}
    cache_handler = DjangoSessionCacheHandler(request)
    auth_manager = SpotifyOAuth(
        scope='user-library-read user-top-read playlist-modify-public',
        cache_handler=cache_handler)
    if auth_manager.validate_token(cache_handler.get_cached_token()):
        # If token already exists and is valid, redirect them to the home page
        return redirect("login-success")

    # Make sure your client_id/client_secret/redirect_uri environment variables are set
    auth_manager = SpotifyOAuth(
        scope='user-library-read user-top-read playlist-modify-public',
        cache_handler=cache_handler,
        show_dialog=True,
    )

    # In authenticate page there is a link button with href set to context["auth_url"]
    context["auth_url"] = auth_manager.get_authorize_url()

    return render(request, "login.html", context)

def login_success(request):
    cache_handler = DjangoSessionCacheHandler(request)
    auth_manager = SpotifyOAuth(
            scope='user-library-read user-top-read playlist-modify-public',
            cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('login')
    sp = Spotify(auth_manager=auth_manager)
        
    #Grab user ID and user_name
    user_id, user_name = get_user_info(sp)

    if not user_id and not user_name:
        return render(request, 'error.html', 
                {"error_message": "Couldn't get access to your profile information. Make sure you're connected to Internet."}, 
                status=404)
    request.session['user_name'] = user_name
    return render(request,
        'login_success.html',
        context={'username':user_name,'user_id':user_id})

def about(request):
    return render(request,'about.html')


def contacts(request):
    return render(request,'contacts.html')

def create_playlist(request):
   
    #Authorize requests to OpenWeather widget
    try:
        api_key = OWM_API_KEY
        #Obtain coordinates for the weather API
        lat = float(request.POST.get('lat') or request.GET.get('lat'))
        lon = float(request.POST.get('lon') or request.GET.get('lon'))
        print(lat, lon)
        print(lat,lon)
        mng = get_owm_mng(api_key)
        #Obtain weather data for the widget and further use
        weather, status = weather_type(mng,lat,lon)
        city_id = city_ID(mng,lat,lon)
        
        cache_handler = DjangoSessionCacheHandler(request)
        auth_manager = SpotifyOAuth(
            scope='user-library-read user-top-read playlist-modify-public',
            cache_handler=cache_handler)
        if not auth_manager.validate_token(cache_handler.get_cached_token()):
            return redirect('login')
        
        sp = Spotify(auth_manager=auth_manager)
        user_name = request.session.get('user_name',None)
        user_id = request.session.get('user_id',None)
        if request.method == 'POST':
            #Instantiate a PlaylistForm class with data from user's input
            form = PlaylistForm(request.POST,sp=sp)
            if form.is_valid(): #If user's input is valid, grab the value
                playlist_name = form.cleaned_data['playlist_name']
            
                #Passing the playlist name into sessions
                request.session['playlist_name'] = playlist_name
                #Generate recommended tracks according to the weather and user's taste
                items_id = get_shortlisted_tracks(sp,weather,status)
               
                if items_id == []:
                    return render(request, 'error.html', {"error_message": "Couldn't find any tracks for you. Check your Internet connection or try again later."}, status=404)

                #Create a new empty playlist
                playlist = create_new_playlist(sp,user_id,user_name,playlist_name,weather)
                if not playlist:
                    return render(request, 'error.html', {"error_message": "Couldn't create a new playlist. Make sure you're connected to Internet"}, status=404)
                
                playlist_id = playlist['id']
                playlist_url = playlist['external_urls']['spotify']

                #Passing the url into sessions
                request.session['spotify_link'] = playlist_url
                
                #Adding generated tracks into the new playlist
                new_playlist = add_tracks_to_playlist(sp,playlist_id,items_id)
                if not new_playlist:
                    return render(request, 'error.html', {"error_message": "Couldn't add tracks to {playlist_name} playlist.Make sure you're connected to Internet."}, status=404)
                #If successfully populated, redirect to /create-playlist/success url
                return redirect('created')
            
            #If the form is not valid, render the same page with error message from the form
            else:
                return render(
                    request, 
                    'create_playlist.html',
                    context={
                        'form': form,
                        'api_key': api_key,
                        'username': user_name
                    }
                )
        #If http method is not POST:
        else:
            form = PlaylistForm()
            return render(
                        request, 
                        'create_playlist.html',
                        context={
                            'form': form,
                            'api_key': api_key,
                            'city_id': city_id,
                            'username': user_name,
                            'weather_type': weather,
                        }
                    )
    except SpotifyException as e:
        logger.error(f"Spotify authorization failed: {e}")
        return render(request, 'error.html', {'error_message': 'Spotify authorization failed. Please try again.'}, status=401)

    except ow_exceptions.PyOWMError as e:
        logger.error(f"Weather data retrieval failed: {e}")
        return render(request, 'error.html', {'error_message': 'Weather data retrieval failed. Please try again later.'}, status=500)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return render(request, 'error.html', {'error_message': 'An unexpected error occurred. Please try again later.'}, status=500)
    

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