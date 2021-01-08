from unittest import TestCase, main
from unittest.mock import Mock, patch, MagicMock
import unittest

from src.weather.weather import WeatherApp


class TestWeatherApp(TestCase):
    def setUp(self):
        self.temp = WeatherApp()

    @patch('src.weather.weather.requests.get')
    def test_get_weather_by_city_name_succesful(self, mock_get):
        weather_warsaw = {
            "data": [
                {
                    "city": "Warsaw",
                    "weather": "Rainy",
                    "temperature": "2C",
                    "wind_dir": "NE"
                }
            ]
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
            "data": [
                {
                    "city": "Warsaw",
                    "weather": "Rainy",
                    "temperature": "2C",
                    "wind_dir": "NE"
                }
            ]
        }

        mock_get.return_value = Mock(status=200)
        mock_get.return_value.json.return_value = weather_warsaw

        self.temp.get_weather_by_city_name("Warsaw")

        mock_get.assert_called_once()

    @patch('src.weather.weather.requests.get')
    def test_get_weather_for_cities_by_name_succesful(self, mock_get):
        weather_cities = {
            "data": [
                {
                    "city": "Warsaw",
                    "weather": "Rainy",
                    "temperature": "2C",
                    "wind_dir": "NE"
                },
                {
                    "city": "Wroclaw",
                    "weather": "Clear sky",
                    "temperature": "4C",
                    "wind_dir": "SW"
                },
                {
                    "city": "Gdansk",
                    "weather": "Snow storm",
                    "temperature": "-3C",
                    "wind_dir": "NE"
                }
            ]
        }

        mock_get.return_value = Mock(status=200)
        mock_get.return_value.json.return_value = weather_cities

        response = self.temp.get_weather_for_cities_by_name("Warsaw", "Wroclaw", "Gdansk")

        self.assertEqual(response.json(), weather_cities)

    def test_get_weather_by_geo_coordinates_succesful(self):
        with patch('src.weather.weather.requests.get') as mock_get:
            weather_coordinates = {
                "data": [
                    {
                        "city": "Gdansk",
                        "weather": "Broken Clouds",
                        "temperature": "-4C",
                        "wind_dir": "SW"
                    }
                ]
            }

            mock_get.return_value = Mock(status=200)
            mock_get.return_value.json.return_value = weather_coordinates

            response = self.temp.get_weather_by_geo_coordinates(54.396, 18.574)

            self.assertEqual(response.json(), weather_coordinates)

    def test_get_weather_by_geo_coordinates_no_data_for_values(self):
        with patch('src.weather.weather.requests.get') as mock_get:
            weather_coordinates = {
                "mesage": "No data found for given coordinates"
            }

            mock_get.return_value = Mock(status=404)
            mock_get.return_value.json.return_value = weather_coordinates

            response = self.temp.get_weather_by_geo_coordinates(48.276, -36.945)

            self.assertEqual(response, None)

    def test_get_weather_by_geo_coordinates_requests_get_should_be_called(self):
        with patch('src.weather.weather.requests.get') as mock_get:
            weather_coordinates = {
                "data": [
                    {
                        "city": "Gdansk",
                        "weather": "Broken Clouds",
                        "temperature": "-4C",
                        "wind_dir": "SW"
                    }
                ]
            }

            mock_get.return_value = Mock(status=200)
            mock_get.return_value.json.return_value = weather_coordinates

            self.temp.get_weather_by_geo_coordinates(54.396, 18.574)

            mock_get.assert_called_once_with('api.myweatherapi.com/v1/lat=54.396&lon=18.574')

    def test_get_weather_by_geo_coordinates_latitude_out_of_range(self):
        with self.assertRaisesRegexp(ValueError, "Latitude has to be between -90 and 90"):
            self.temp.get_weather_by_geo_coordinates(110.354, 12.453)

    def test_get_weather_by_geo_coordinates_longitude_out_of_range(self):
        with self.assertRaisesRegexp(ValueError, "Longitude has to be between -180 and 180"):
            self.temp.get_weather_by_geo_coordinates(32.354, -342.532)

    def test_get_weather_by_geo_coordinates_coordinates_type_not_float(self):
        with self.assertRaisesRegexp(TypeError, "Coordinates must be of float type"):
            self.temp.get_weather_by_geo_coordinates(110, "123.432")

    def test_get_weather_by_zip_code_pl_succesful(self):
        with patch('src.weather.weather.requests.get') as mock_get:
            weather_coordinates = {
                "data": [
                    {
                        "city": "Gizycko",
                        "weather": "Sunny",
                        "temperature": "21C",
                        "wind_dir": "SW"
                    }
                ]
            }

            mock_get.return_value = MagicMock(status=200)
            mock_get.return_value.json.return_value.__contains__.return_value = True

            response = self.temp.get_weather_by_zip_code_pl("11-500")

            self.assertTrue(weather_coordinates in response.json())

    def tearDown(self):
        self.temp = None

if __name__ == '__main__':
    main()
