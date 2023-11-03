import logging
from .credentials import ow_credentials
from .location import my_IP_location

logger = logging.getLogger(__name__)

def weather_type(mng,lat,lon):
    
    observation = mng.weather_at_coords(lat=lat, lon=lon)
    # Grabbing current weather status
    weather = observation.weather.status
    #Define lists of similar weather types
    rainy = ['Thunderstorm','Drizzle','Rain']
    cloudy = ['Clouds']
    sunny = ['Clear']
    snowy_or_athmosphere = ['Snow','Atmosphere']
    if weather in rainy:
        return 'Rainy', weather
    elif weather in cloudy:
        return 'Cloudy', weather
    elif weather in sunny:
        return 'Sunny', weather
    else:
        return 'Snowy/Athmosphere', observation.weather.detailed_status
        

def city_ID(mng,lat,lon):
    
    # Search for the nearest city based on coordinates
    observation = mng.weather_at_coords(lat, lon)
    location = observation.location
    city_id = location.id
    return city_id
       
