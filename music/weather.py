from .credentials import ow_credentials
from .location import my_IP_location

#Authorization
owm = ow_credentials()


def weather_type():
    # Obtaining weather manager object
    mng = owm.weather_manager()

    # Importing IP address coordinates and passing them further
    lat, lon = my_IP_location()

    if lat is not None and lon is not None:
        try:
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
            elif weather in snowy_or_athmosphere:
                return 'Snowy/Athmosphere', observation.weather.detailed_status
        except Exception as e:
            print(f'An error occurred while fetching weather data: {e}')
    else:
        print('Location coordinates are unavailable.')
        return None


def city_ID():
    # Obtaining weather manager object
    # Importing IP address coordinates and passing them further
    lat, lon = my_IP_location()

    if lat is not None and lon is not None:
        try:
            mng = owm.weather_manager()
            # Search for the nearest city based on coordinates
            observation = mng.weather_at_coords(lat, lon)
            location = observation.location
            city_id = location.id
            return city_id
        except Exception as e:
            print(f'An error occurred while fetching city data: {e}')
    else:
        print('Location coordinates are unavailable.')
        return None
