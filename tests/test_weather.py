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
    def test_get_weather_by_city_name(self, mock_get):
        weather_warsaw = {
            "status": 200,
            "data": {
                "city": "warsaw",
                "weather": "not great tbh"
            }
        }

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = weather_warsaw

        response = self.temp.get_weather_by_city_name("warsaw")
        print(mock_get)
        self.assertEqual(response.json(), weather_warsaw)


if __name__ == '__main__':
    main()
