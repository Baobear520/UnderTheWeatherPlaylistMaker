import os
from django.test import TestCase 
from unittest.mock import Mock, patch
from pyowm.commons.exceptions import UnauthorizedError
from .scripts import location
from .scripts.weather import *
# Create your tests here.
class LocationTests(TestCase):

    """Class for testing location data """

    def setUp(self):
        self.coordinates = (31.470242909455024, 103.28136676508652)

    @patch('geocoder.ip')
    def test_my_IP_location_success(self, mock_ip):
        # Mock the geocoder.ip function to return expected values
        mock_ip.return_value.latlng = self.coordinates

        lat, lon = location.my_IP_location()

        self.assertEqual(lat, self.coordinates[0])
        self.assertEqual(lon, self.coordinates[1])

    @patch('geocoder.ip')
    def test_my_IP_location_failure(self, mock_ip):
        # Mock the geocoder.ip function to raise an exception
        mock_ip.side_effect = Exception("Test exception")

        lat, lon = location.my_IP_location()

        self.assertIsNone(lat)
        self.assertIsNone(lon)

class WeatherStatusTestCase(TestCase):

    """Class for testing weather status"""


    def setUp(self):
        self.coordinates = (31.470242909455024, 103.28136676508652)

    @patch('music.scripts.weather.get_owm_mng')
    def test_weather_type_status_rain(self, mock_owm_mng):
        observation = Mock()
        observation.weather.status = 'Rain'
        mock_owm_mng.weather_at_coords.return_value = observation
        condition = weather_type(mock_owm_mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Rainy')

    @patch('music.scripts.weather.get_owm_mng')
    def test_weather_type_status_drizzle(self, mock_owm_mng):
        observation = Mock()
        observation.weather.status = 'Drizzle'
        mock_owm_mng.weather_at_coords.return_value = observation
        condition = weather_type(mock_owm_mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Rainy')

    @patch('music.scripts.weather.get_owm_mng')
    def test_weather_type_status_thunderstorm(self, mock_owm_mng):
        observation = Mock()
        observation.weather.status = 'Thunderstorm'
        mock_owm_mng.weather_at_coords.return_value = observation
        condition = weather_type(mock_owm_mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Rainy')

    @patch('music.scripts.weather.get_owm_mng')
    def test_weather_type_status_clouds(self, mock_owm_mng):
        # Mock the OWM library to return a cloudy condition
        observation = Mock()
        mock_owm_mng.weather_at_coords.return_value = observation
        observation.weather.status = 'Clouds'
        condition = weather_type(mock_owm_mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Cloudy')

    @patch('music.scripts.weather.get_owm_mng')
    def test_weather_type_status_clear(self, mock_owm_mng):
        # Mock the OWM library to return a sunny condition
        observation = Mock()
        mock_owm_mng.weather_at_coords.return_value = observation
        observation.weather.status = 'Clear'
        condition = weather_type(mock_owm_mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Sunny')

    @patch('music.scripts.weather.get_owm_mng')
    def test_weather_type_status_snow(self, mock_owm_mng):
        # Mock the OWM library to return a snowy condition
        observation = Mock()
        mock_owm_mng.weather_at_coords.return_value = observation
        observation.weather.status = 'Snow'
        condition = weather_type(mock_owm_mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Snowy/Atmosphere')

    @patch('music.scripts.weather.get_owm_mng')
    def test_weather_type_status_atmosphere(self, mock_owm_mng):
        # Mock the OWM library to return a snowy condition
        observation = Mock()
        mock_owm_mng.weather_at_coords.return_value = observation
        observation.weather.status = 'Atmosphere'
        condition = weather_type(mock_owm_mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Snowy/Atmosphere')

    @patch('music.scripts.weather.get_owm_mng')
    def test_weather_type_status_unknown(self, mock_owm_mng):
        # Mock the OWM library to return an unknown condition
        observation = Mock()
        mock_owm_mng.weather_at_coords.return_value = observation
        observation.weather.status = 'UnknownCondition'
        condition = weather_type(mock_owm_mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Unknown')

    @patch('music.scripts.weather.get_owm_mng')
    def test_weather_type_parse_error(self, mock_owm_mng):
        # Mock the OWM library to raise a ParseAPIResponseError
        mock_owm_mng.side_effect = ow_exceptions.ParseAPIResponseError("Test error")

        # Call the weather_type function 
        
        condition, description = weather_type(mock_owm_mng, *self.coordinates)

        # Assert that the function returned (None, None)
        self.assertIsNone(condition)
        self.assertIsNone(description)

        
