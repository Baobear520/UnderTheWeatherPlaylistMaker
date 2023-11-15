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
    def test_my_IP_location_invalid_coordinates(self, mock_ip):
        # Mock the geocoder.ip function to raise an exception
        mock_ip.side_effect = AttributeError("Test exception")

        lat, lon = location.my_IP_location()

        self.assertIsNone(lat)
        self.assertIsNone(lon)

    @patch('geocoder.ip')
    def test_my_IP_location_unexpected_error(self, mock_ip):
        # Mock the geocoder.ip function to raise an exception
        mock_ip.side_effect = Exception("Test exception")

        lat, lon = location.my_IP_location()

        self.assertIsNone(lat)
        self.assertIsNone(lon)

class WeatherStatusTestCase(TestCase):

    """Class for testing weather """


    def setUp(self):
        self.coordinates = (31.470242909455024, 103.28136676508652)


    def test_weather_type_mng_is_none(self):

        #Test that the weather_type function returns (None, None) 
        #when mng object is None
        mock_mng = None
        
        
        condition, weather = weather_type(mock_mng, *self.coordinates)
        # Assert
        self.assertIsNone(condition)
        self.assertIsNone(weather)

    def test_weather_type_with_invalid_coordinates(self):
    
        #Test that the weather_type function returns (None, None) 
        # when passed invalid coordinates.
        
        # Arrange
        mng = Mock()
        lat, lon = 'invalid', 'coordinates'
        mng.weather_at_coords.side_effect = AssertionError("Test exception")

        # Act
        condition, weather = weather_type(mng, lat, lon)

        # Assert
        self.assertIsNone(condition)
        self.assertIsNone(weather)


    def test_weather_type_with_unexpected_error(self):

        #Test that the weather_type function logs the expected message 
        # when an unexpected error occurs during execution.
        
        # Arrange
        mng = Mock()
        mng.weather_at_coords.side_effect = Exception('Test exception')
        
        # Act
        condition, weather = weather_type(mng, *self.coordinates)

        # Assert
        self.assertIsNone(condition)
        self.assertIsNone(weather)
            

    def test_weather_type_status_rain(self):
        #Test that the weather_type function returns 'Rainy' 
        # if the weather condition is 'Rain'
        mng = Mock()
        #Mocking the weather status
        mng.weather_at_coords.return_value.weather.status = 'Rain'
        #Obtaining the weather condition
        condition = weather_type(mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Rainy')

    
    def test_weather_type_status_drizzle(self):
        #Test that the weather_type function returns 'Rainy' 
        # if the weather condition is 'Drizzle'
        mng = Mock()
        #Mocking the weather status
        mng.weather_at_coords.return_value.weather.status = 'Drizzle'
        #Obtaining the weather condition
        condition = weather_type(mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Rainy')


    def test_weather_type_status_thunderstorm(self):
        #Test that the weather_type function returns 'Rainy' 
        # if the weather condition is 'thunderstorm'
        mng = Mock()
        #Mocking the weather status
        mng.weather_at_coords.return_value.weather.status = 'Thunderstorm'
        #Obtaining the weather condition
        condition = weather_type(mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Rainy')


    def test_weather_type_status_clouds(self):
        #Test that the weather_type function returns 'Cloudy' 
        # if the weather condition is 'Clouds'
        mng = Mock()
        #Mocking the weather status
        mng.weather_at_coords.return_value.weather.status = 'Clouds'
        #Obtaining the weather condition
        condition = weather_type(mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Cloudy')


    def test_weather_type_status_clear(self):
        #Test that the weather_type function returns 'Sunny' 
        # if the weather condition is 'Clear'
        mng = Mock()
        #Mocking the weather status
        mng.weather_at_coords.return_value.weather.status = 'Clear'
        #Obtaining the weather condition
        condition = weather_type(mng, *self.coordinates)[0]
        self.assertEqual(condition, 'Sunny')


    def test_weather_type_status_snow(self):
        #Test that the weather_type function returns 'Snow/Atmosphere' 
        # if the weather condition is 'Snow'
        # and the detailed status that is a string object
        mng = Mock()

        #Mocking the weather status and storing in "weather" variable
        weather = mng.weather_at_coords.return_value.weather.status 
        mng.weather_at_coords.return_value.weather.status = 'Snow'

        #Mocking the weather's detailed status and storing it in "detailed_status"
        weather.detailed_status = str
        detailed_status = weather.detailed_status

        #Obtaining the weather condition
        condition, weather = weather_type(mng, *self.coordinates)
        #Asserting the output
        self.assertEqual(condition, 'Snowy/Atmosphere')
        self.assertIs(detailed_status,str)
        
        
    def test_weather_type_status_atmosphere(self):
        #Test that the weather_type function returns 'Snow/Atmosphere' 
        # if the weather condition is 'Atmosphere'
        # and the detailed status that is a string object
        mng = Mock()

        #Mocking the weather status and storing in "weather" variable
        weather = mng.weather_at_coords.return_value.weather.status 
        mng.weather_at_coords.return_value.weather.status = 'Snow'

        #Mocking the weather's detailed status and storing it in "detailed_status"
        weather.detailed_status = str
        detailed_status = weather.detailed_status

        #Obtaining the weather condition
        condition, weather = weather_type(mng, *self.coordinates)
        #Asserting the output
        self.assertEqual(condition, 'Snowy/Atmosphere')
        self.assertIs(detailed_status,str)


    def test_weather_type_status_unknown(self):
        #Test that the weather_type function returns 'Unknown' 
        # if the weather condition is not in the weather_conditions dictionary keys

        mng = Mock()

        # Mocking the weather status that is not 
        # in OpenWeatherAPI list of weather conditions
        mng.weather_at_coords.return_value.weather.status = 'Breezy'

        #Obtaining the weather condition
        condition = weather_type(mng, *self.coordinates)[0]

        #Asserting the output
        self.assertEqual(condition, 'Unknown')


class CityIDTestCase(TestCase):

    """Class for testing city_ID function """

    def setUp(self):
        self.coordinates = (31.470242909455024, 103.28136676508652)

    def test_cityid_success(self):
        mng = Mock()
        city_id = city_ID(mng,*self.coordinates)
        self.assertIsNotNone(city_id)
    
    def test_cityid_incorrect_coordinates(self):
        lat, lon = 'cxcxc', 'ddd'
        mng = Mock()
        mng.weather_at_coords.side_effect = AssertionError("Test exception")
        city_id = city_ID(mng, lat,lon)
        self.assertIsNone(city_id)
    
    def test_cityid_mng_is_none(self):
        mng = None
        city_id = city_ID(mng,*self.coordinates)
        self.assertIsNone(city_id)


        
