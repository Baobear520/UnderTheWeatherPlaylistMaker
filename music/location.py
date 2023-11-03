import geocoder
import os, logging
from .credentials import ow_credentials

logger = logging.getLogger(__name__)


def my_IP_location():

    my_loc = geocoder.ip('me')
    logger.info('Obtained {my_loc} object')
    lat,lon = my_loc.latlng
    logger.info('Lat is {lat}, lon is {lon}')
    return lat,lon

