import logging
from pyowm.owm import OWM
from pyowm.commons import exceptions 

logger = logging.getLogger(__name__)


def ow_credentials(api_key):
    #Authorization
    try:
        owm = OWM(api_key)
        #Obtain the manager object
        mng = owm.weather_manager()
        logger.info('OpenWeather manager object has been obtained')
        return mng
    except exceptions.UnauthorizedError as e:
        logger.error(f"Coudn't get access to OpenWeather. Please check your internet connection or your api_key validity: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None
