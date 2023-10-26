
from pyowm.owm import OWM
from .credentials import ow_credentials
from .location import my_IP_location

#Authorization
owm = ow_credentials()


def all_weather_types():
    pass

def weather_type():
    #Obtaining weather manager object
    mng = owm.weather_manager()

    #Importing IP address coordinates and passing them further
    lat,lon = my_IP_location()
    observation = mng.weather_at_coords(lat=lat,lon=lon)
    #Grabbing current weather status
    weather = observation.weather
    return weather.status



def city_ID():

    #Obtaining weather manager object
    #Importing IP address coordinates and passing them further
    lat,lon = my_IP_location()
    try:
        mng = owm.weather_manager()
        # Search for the nearest city based on coordinates
        observation = mng.weather_at_coords(lat, lon)
        location = observation.location
        city_id = location.id
        return city_id
    except ValueError as e:
        print(f'An error occurred: {e}')
