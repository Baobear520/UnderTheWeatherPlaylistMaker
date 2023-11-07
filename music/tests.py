import os
from django.test import TestCase 
from unittest.mock import patch
from pyowm.commons.exceptions import UnauthorizedError
from .scripts import location, credentials

# Create your tests here.
class LocationTests(TestCase):
    @patch('geocoder.ip')
    def test_my_IP_location_success(self, mock_ip):
        # Mock the geocoder.ip function to return expected values
        mock_ip.return_value.latlng = [12.345, 67.890]

        lat, lon = location.my_IP_location()

        self.assertEqual(lat, 12.345)
        self.assertEqual(lon, 67.890)

    @patch('geocoder.ip')
    def test_my_IP_location_failure(self, mock_ip):
        # Mock the geocoder.ip function to raise an exception
        mock_ip.side_effect = Exception("Test exception")

        lat, lon = location.my_IP_location()

        self.assertIsNone(lat)
        self.assertIsNone(lon)

class WeatherTestCase(TestCase):

    @patch('pyowm.owm.OWM')
    def test_ow_credentials_success(self, mock_owm):
        # Mock the OWM constructor to return an OWM object
        mock_mng = mock_owm.return_value.weather_manager.return_value
        mng = credentials.ow_credentials('mmm')

        self.assertEqual(mng, mock_mng)
        mock_owm.assert_called_once_with('kkk')

    @patch('pyowm.owm.OWM')
    def test_ow_credentials_unauthorized_error(self, mock_owm):
        # Mock the OWM constructor to raise UnauthorizedError
        mock_owm.side_effect = UnauthorizedError("Unauthorized")

        mng = credentials.ow_credentials('fvfvfv')

        self.assertIsNone(mng)

    @patch('pyowm.owm.OWM')
    def test_ow_credentials_general_exception(self, mock_owm):
        # Mock the OWM constructor to raise a general exception
        mock_owm.side_effect = Exception("Test exception")

        mng = credentials.ow_credentials('vfvfvf')

        self.assertIsNone(mng)

