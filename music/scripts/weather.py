import logging
from pyowm.owm import OWM
from pyowm.commons import exceptions as ow_exceptions


logger = logging.getLogger(__name__)


def get_owm_mng(api_key):
    try:
        owm = OWM(api_key)
        #Obtain the manager object
        mng = owm.weather_manager()
        logger.info(f'OpenWeather manager object {mng} has been obtained')
        return mng
    except ow_exceptions.UnauthorizedError as e:
        logger.error(f"Coudn't get access to OpenWeather. Please check your internet connection or your api_key validity: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

def weather_type(mng, lat, lon):
    try:
        observation = mng.weather_at_coords(lat=lat, lon=lon)
        weather = observation.weather.status
        detailed_status = observation.weather.detailed_status

        logging.info(f"Current weather - {weather}, detailed status  - {detailed_status}")
        #Creating a dictionary of 'condition': conditions_list  like objects
        weather_conditions = {
            'Rainy': ['Thunderstorm', 'Drizzle', 'Rain'],
            'Cloudy': ['Clouds'],
            'Sunny': ['Clear'],
            'Snowy/Atmosphere': ['Snow', 'Atmosphere']
        }

        for condition, conditions_list in weather_conditions.items():
            if weather in conditions_list:
                if condition == 'Snowy/Atmosphere':
                    return condition,  detailed_status
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
       
