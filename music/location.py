import geocoder
import os
from .credentials import ow_credentials

def my_IP_location():
    my_loc = geocoder.ip('me')
    lat,long = my_loc.latlng
    return lat,long

