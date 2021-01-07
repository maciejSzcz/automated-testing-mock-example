# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

from unittest import TestCase, main
from unittest.mock import Mock, patch
import unittest

from src.weather.weather import WeatherApp


class TestWeatherApp(TestCase):
    def setUp(self):
        self.temp = WeatherApp()

    @patch('src.weather.weather.requests.get')
    def test_get_weather_by_city_name_succesful(self, mock_get):
        weather_warsaw = {
            "status": 200,
            "data": {
                "city": "warsaw",
                "weather": "rainy",
                "temperature": "2C"
            }
        }

        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = weather_warsaw

        response = self.temp.get_weather_by_city_name("warsaw")

        self.assertEqual(response.json(), weather_warsaw)

    @patch('src.weather.weather.requests.get')
    def test_get_weather_by_city_name_nonexistent_city(self, mock_get):
        weather_warsaww = {
            "status": 400,
            "message": "Invalid city"
        }

        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = weather_warsaww

        response = self.temp.get_weather_by_city_name("warsaww")

        self.assertEqual(response, None)

    @patch('src.weather.weather.requests.get')
    def test_get_weather_by_city_name_requests_get_should_be_called(self, mock_get):
        weather_warsaw = {
            "status": 200,
            "data": {
                "city": "warsaw",
                "weather": "rainy",
                "temperature": "2C"
            }
        }

        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = weather_warsaw

        self.temp.get_weather_by_city_name("warsaw")

        mock_get.assert_called_once()

    def tearDown(self):
        self.temp = None

if __name__ == '__main__':
    main()
