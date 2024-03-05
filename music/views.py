from datetime import datetime
import logging
from celery import chain

from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from spotipy import Spotify, DjangoSessionCacheHandler
from spotipy.oauth2 import SpotifyOAuth
from pyowm.commons import exceptions as ow_exceptions

from config.tasks import generate_tracks_task, get_shortlisted_tracks_task, weather_task

from .scripts.user_data import get_user_info
from .scripts.create_populate_playlist import *

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

    
    auth_manager = SpotifyOAuth(
        scope='user-library-read user-top-read playlist-modify-public',
        cache_handler=cache_handler,
        show_dialog=True,
    )

    # In authenticate page there is a link button with href set to context["auth_url"]
    context["auth_url"] = auth_manager.get_authorize_url()

    return render(request, "login.html", context)


@cache_page(60 * 2)
def login_success(request):
    try:
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
        request.session['username'] = user_name
        request.session['user_id'] = user_id
        return render(request,
            'login_success.html',
            context={'username':user_name,'user_id':user_id})
    
    except ConnectionError as e:
        logger.error(f"Couldn't establsh connection to the cache database: {e}")
        return render(request, 'error.html', {"error_message": "There's a problem connecting to the website. Please try again later."}, status=404)

@cache_page(60 * 15)
def about(request):
    return render(request,'about.html')

@cache_page(60 * 15)
def contacts(request):
    return render(request,'contacts.html')


def create_playlist(request):
    try:
        #Obtaining geo coordinates in case of different HTTP requests
        if request.method == 'GET':
            # Obtain coordinates for the weather API
            lat = float(request.GET.get('lat'))
            lon = float(request.GET.get('lon'))
            
            request.session['lat'] = lat
            request.session['lon'] = lon

        elif request.method == 'POST':
            # Obtain coordinates for the weather API from the session
            lat = request.session.get('lat')
            lon = request.session.get('lon')

        
        #Obtaining weather and city_id if it's in cache
        weather_data = cache.get('weather_data')
        #Else making an API call 
        if not weather_data: 
            weather_data = weather_task.delay(lat,lon).get() #Delegating it to a celery task
            cache.set('weather_data',weather_data,timeout=180) #Storing the value in cache
        
        weather = weather_data['weather']
        status = weather_data['status']

        #Obtaining credentials from cache
        cache_handler = DjangoSessionCacheHandler(request)
        auth_manager = SpotifyOAuth(
            scope='user-library-read user-top-read playlist-modify-public',
            cache_handler=cache_handler)

        #Obtaining JSON serializable access token(to further pass into a celery task)
        access_token = cache_handler.get_cached_token()
        auth_info = access_token['access_token']
        
        #If there's no cached token, redirecting back to login url
        if not auth_manager.validate_token(access_token):
            return redirect('login')
        
        #Else we defined an sp - object
        sp = Spotify(auth_manager=auth_manager)

        #Grabbing username and user id from sessions
        user_name = request.session.get('username', None)
        user_id = request.session.get('user_id', None)

        #Generating recommended tracks according to the weather and user's taste
        #If the value is in cache, retrieving
        items_id = cache.get('items_id')

        #Else making all the neccesary API calls and computations
        if not items_id:
            #Calling a Celery chained tasks
            res = chain(generate_tracks_task.s(auth_info,weather,status),get_shortlisted_tracks_task.s())()
            items_id = res.get()
            cache.set('items_id',items_id,timeout=120) #Storing the value in cache
        
        
        if request.method == 'POST':
            #Instantiate a PlaylistForm class with data from user's input
            form = PlaylistForm(request.POST,sp=sp)
            if form.is_valid(): #If user's input is valid, grab the value
                playlist_name = form.cleaned_data['playlist_name']
            
                #Passing the playlist name into sessions for the further use in /login/success url
                request.session['playlist_name'] = playlist_name
                
                #If no tracks are retrieved
                if items_id == []:
                    return render(request, 'error.html', {"error_message": "Couldn't find any tracks for you. Check your Internet connection or try again later."}, status=404)

                #Create a new empty playlist
                playlist = create_new_playlist(sp,user_id,user_name,playlist_name,weather)
                if not playlist:
                    return render(request, 'error.html', {"error_message": "Couldn't create a new playlist. Make sure you're connected to Internet"}, status=404)
                
                #Deleting the tracklist and the old playlist names from cache 
                #in case user wants to immediately create another playlist
                cache.delete('all_playlists_names')
                cache.delete('items_id')
                
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
                print(items_id)
                return render(
                    request, 
                    'create_playlist.html',
                    context={
                        'form': form,
                        'username': user_name,
                        'items_id': items_id,
                        **weather_data
                    }
        
               )
        form = PlaylistForm()
        return render(
                    request, 
                    'create_playlist.html',
                    context={
                        'form': form,
                        'username': user_name,
                        'items_id': items_id,
                        **weather_data
                        
                        
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
#@cache_page(3*60)
def test_page(request):
    return render(request,"test.html")
    
    