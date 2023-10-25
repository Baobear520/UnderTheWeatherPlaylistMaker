
from pyowm.owm import OWM
from credentials import ow_credentials
from location import my_IP_location

owm = ow_credentials()
mng = owm.weather_manager()

lat,lon = my_IP_location()
observation = mng.weather_at_coords(lat=lat,lon=lon)
weather = observation.weather
weather = weather.status

print(weather)
