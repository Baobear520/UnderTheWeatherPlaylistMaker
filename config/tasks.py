import os
from celery import Celery,shared_task
import spotipy
from spotipy.oauth2 import SpotifyOAuth


from config.settings.base import OWM_API_KEY
from music.scripts.genres_algorithms import add_random_genres, combined_genres, sort_top_genres, validate_genres_for_playlist
from music.scripts.playlist_algorithms import get_shortlisted_tracks
from music.scripts.weather import city_ID, get_owm_mng, weather_type

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

celery_app = Celery('config.tasks',backend='redis://127.0.0.1:6379/3',broker='redis://127.0.0.1:6379/2')

#celery.config_from_object('config.settings.dev',namespace='CELERY')
celery_app.autodiscover_tasks()


@shared_task
def weather_task(lat,lon):
    #Obtaining API key for OpenWeatherAPI calls
    api_key = OWM_API_KEY
    mng = get_owm_mng(api_key)

    # Obtain weather data for the widget and further use
    weather, status = weather_type(mng, lat, lon)
    city_id = city_ID(mng, lat, lon)

    weather_data = {
        'weather':weather,
        'status':status,
        'city_id':city_id,
        'api_key': api_key
        }
    return weather_data


# @shared_task
# def tracks_task():
#     auth_manager = SpotifyOAuth(
#             scope='user-library-read user-top-read playlist-modify-public')
#     sp = spotipy.Spotify(auth_manager=auth_manager)
    
#     weather = 'Rainy'
#     status = 'Drizzle'
#     #Generating recommended tracks according to the weather and user's taste
#     items_id = get_shortlisted_tracks(sp,weather,status)

#     return items_id
