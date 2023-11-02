import geocoder
import os
from .credentials import ow_credentials

def my_IP_location():
    my_loc = geocoder.ip('me')
    lat,lon = my_loc.latlng
    #lat, lon = None, None
    if lat is None or lon is None:
        raise ConnectionError('Cannot obtain coordinates')
    return lat,lon

