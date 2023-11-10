import logging
import geocoder

logger = logging.getLogger(__name__)


def my_IP_location():
    #Obtaining geolocation coordinates
    try: 
        my_loc = geocoder.ip('me')
        lat,lon = my_loc.latlng
        logger.info('Obtained lat and lon are {lat}, {lon} ')
        return lat,lon
    except AttributeError as e:
        logger.error(f"Invalid coordinates: {e}")
        return None, None
    except Exception as e:
        logger.error(f"An unexpected error occured: {e}")
        return None,None
    

