
import logging
import os
import random
from celery import Celery,shared_task
import spotipy

from config.settings.base import OWM_API_KEY
from music.scripts.playlist_algorithms import generate_tracks
from music.scripts.weather import city_ID, get_owm_mng, weather_type


logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')


celery_app = Celery('config.tasks')


celery_app.config_from_object('config.settings.dev',namespace='CELERY')
celery_app.autodiscover_tasks()


@shared_task
def weather_task(lat,lon):
    try:
        #Obtaining API key for OpenWeatherAPI calls
        api_key = OWM_API_KEY
        mng = get_owm_mng(api_key)
        #lat, lon = (31.470242909455024, 103.28136676508652)
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
    except Exception as e:
        logger.error(f"An error occured while obtaining weather data.")
        return {}


@shared_task
def generate_tracks_task(auth_info,weather,status):
    try:
        sp = spotipy.Spotify(auth=auth_info)
        final_list = generate_tracks(sp,weather,status)
        return final_list
    except Exception as e:
        logger.error(f"An error occured while trying to generate tracks.")
        return []

@shared_task
def get_shortlisted_tracks_task(final_list):
    try:
        number_of_final_tracks = len(final_list)
        print(number_of_final_tracks)
        k = 50 
        if number_of_final_tracks < 50:
            k == number_of_final_tracks
        
        #Shuffling all the tracks to decrease probability of selecting the same tracks again
        random.shuffle(final_list)

        #Shortening the list to 50 tracks
        short_list = final_list[:k]
        logger.info(f'Shortlisted {len(short_list)} randomly selected tracks from the final list')
        
        #Grab a list of track ID's
        items_id = [item['id'] for item in short_list]
        logger.info(f"Extracted {len(items_id)} track id")
        return items_id
    
    except TypeError as e:
        logger.error(f"{e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []
    

