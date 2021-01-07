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
            "data": {
                "city": "Warsaw",
                "weather": "Rainy",
                "temperature": "2C",
                "wind_dir": "NE"
            }
        }

        mock_get.return_value = Mock(status=200)
        mock_get.return_value.json.return_value = weather_warsaw

        response = self.temp.get_weather_by_city_name("Warsaw")

        self.assertEqual(response.json(), weather_warsaw)

    @patch('src.weather.weather.requests.get')
    def test_get_weather_by_city_name_nonexistent_city(self, mock_get):
        weather_warsaww = {
            "message": "Invalid city"
        }

        mock_get.return_value = Mock(status=404)
        mock_get.return_value.json.return_value = weather_warsaww

        response = self.temp.get_weather_by_city_name("warsaww")

        self.assertEqual(response, None)

    def test_get_weather_by_city_name_city_type_not_str(self):
        self.assertRaises(TypeError, self.temp.get_weather_by_city_name, 123)

    @patch('src.weather.weather.requests.get')
    def test_get_weather_by_city_name_requests_get_should_be_called(self, mock_get):
        weather_warsaw = {
            "data": {
                "city": "Warsaw",
                "weather": "Rainy",
                "temperature": "2C",
                "wind_dir": "NE"
            }
        }

        mock_get.return_value = Mock(status=200)
        mock_get.return_value.json.return_value = weather_warsaw

        self.temp.get_weather_by_city_name("Warsaw")

        mock_get.assert_called_once()

    def test_get_weather_by_geo_coordinates_succesful(self):
        with patch('src.weather.weather.requests.get') as mock_get:
            weather_coordinates = {
                "data": {
                    "city": "Gdansk",
                    "weather": "Broken Clouds",
                    "temperature": "-4C",
                    "wind_dir": "SW"
                }
            }

            mock_get.return_value = Mock(status=200)
            mock_get.return_value.json.return_value = weather_coordinates

            response = self.temp.get_weather_by_geo_coordinates(54.396, 18.574)

            self.assertEqual(response.json(), weather_coordinates)

    def test_get_weather_by_geo_coordinates_latitude_out_of_range(self):
        with self.assertRaisesRegexp(ValueError, "Latitude has to be between -90 and 90"):
            self.temp.get_weather_by_geo_coordinates(110.354, 12.453)

    def test_get_weather_by_geo_coordinates_longitude_out_of_range(self):
        with self.assertRaisesRegexp(ValueError, "Longitude has to be between -180 and 180"):
            self.temp.get_weather_by_geo_coordinates(32.354, -342.532)

    def tearDown(self):
        self.temp = None

if __name__ == '__main__':
    main()
