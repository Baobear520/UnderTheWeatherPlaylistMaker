from django.test import TestCase
from unittest.mock import Mock, patch
from ..scripts import location




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