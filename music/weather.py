import logging
from pyowm.commons import exceptions as ow_exceptions
from .credentials import ow_credentials
from .location import my_IP_location

logger = logging.getLogger(__name__)


def weather_type(mng, lat, lon):
    try:
        observation = mng.weather_at_coords(lat=lat, lon=lon)
        weather = observation.weather.status
        detailed_weather = observation.weather.detailed_status

        #Creating a dictionary of 'condition': conditions_list  like objects
        weather_conditions = {
            'Rainy': ['Thunderstorm', 'Drizzle', 'Rain'],
            'Cloudy': ['Clouds'],
            'Sunny': ['Clear'],
            'Snowy/Athmosphere': ['Snow', 'Atmosphere']
        }

        for condition, conditions_list in weather_conditions.items():
            if weather in conditions_list:
                if condition == 'Snowy/Athmosphere':
                    return condition,  detailed_weather
                return condition, weather

        # If none of the predefined conditions matched
        return 'Unknown', weather

    except ow_exceptions.ParseAPIResponseError as e:
        logger.error(f"Couldn't obtain weather status (weather: {weather}): {e}")
        return None, None
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        return None, None


def city_ID(mng,lat,lon):
    # Search for the nearest city based on coordinates
    try:
        observation = mng.weather_at_coords(lat, lon)
        location = observation.location
        city_id = location.id
        logger.info(f' Obtained city_id value: {city_id}')
        return city_id
    except ow_exceptions.ParseAPIResponseError as e:
        logger.error(f"Couldn't obtain city_id: {e}")
        return None
    except Exception as e:
        logger.error(f'An unexpected error occured: {e}')
        return None
       
