from unittest import TestCase, main
from unittest.mock import Mock, patch, MagicMock
import unittest

from src.weather.weather import WeatherApp


class TestWeatherApp(TestCase):
    def setUp(self):
        fake_database = Mock()
        self.temp = WeatherApp(fake_database)

    @patch('src.weather.weather.requests.get')
    def test_while_save_weather_single_city_calls_get_weather_by_city_name(self, mock_get):
        self.temp.weather_database.add = Mock()

        self.temp.save_weather_single_city("Warsaw")

        self.temp.weather_database.add.assert_called_once()

    @patch('src.weather.weather.requests.get')
    def test_save_weather_single_city_valueerror_raised_with_404_response(self, mock_get):
        weather_warsaww = {
            "message": "Invalid city"
        }

        mock_get.return_value = Mock(status=404)
        mock_get.return_value.json.return_value = weather_warsaww

        self.temp.weather_database.add = Mock()
        self.temp.weather_database.add.side_effect = ValueError("Value can't be none")

        with self.assertRaisesRegexp(ValueError, "Value can't be none"):
            self.temp.save_weather_single_city("warsaww")

    def test_save_weather_single_city_typerror_raised_with_not_str(self):
        self.temp.weather_database.add = Mock()
        with self.assertRaisesRegexp(TypeError, "City name must be of string type"):
            self.temp.save_weather_single_city(12+3j)


    @patch('src.weather.weather.requests.get')
    def test_get_weather_by_city_name_succesful(self, mock_get):
        weather_warsaw = {
            "data": [
                {
                    "city": "Warsaw",
                    "weather": "Rainy",
                    "temperature": "2C",
                    "wind_dir": "NE",
                    "wind_speed": "21km/h",
                    "date": "2021-01-10"
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
                    "wind_dir": "NE",
                    "wind_speed": "19km/h",
                    "date": "2021-01-09"
                }
            ]
        }

        mock_get.return_value = Mock(status=200)
        mock_get.return_value.json.return_value = weather_warsaw

        self.temp.get_weather_by_city_name("Warsaw")

        mock_get.assert_called_once()

    @patch('src.weather.weather.requests.get')
    def test_while_save_weather_multiple_cities_calls_get_weather_for_cities_by_name(self, mock_get):
        weather_cities = {
            "data": [
                {
                    "city": "Warsaw",
                    "weather": "Rainy",
                    "temperature": "2C",
                    "wind_dir": "NE",
                    "wind_speed": "31km/h",
                    "date": "2021-01-01"
                },
                {
                    "city": "Wroclaw",
                    "weather": "Clear sky",
                    "temperature": "4C",
                    "wind_dir": "SW",
                    "wind_speed": "0km/h",
                    "date": "2021-01-01"
                },
                {
                    "city": "Gdansk",
                    "weather": "Snow storm",
                    "temperature": "-3C",
                    "wind_dir": "NE",
                    "wind_speed": "35km/h",
                    "date": "2021-01-01"
                }
            ]
        }

        mock_get.return_value = Mock(status=200)
        mock_get.return_value.json.return_value = weather_cities

        self.temp.weather_database.add = Mock()

        self.temp.save_weather_multiple_cities("Warsaw", "Wroclaw", "Gdansk")
        
        self.assertEquals(self.temp.weather_database.add.call_count, 3)

    @patch('src.weather.weather.requests.get')
    def test_get_weather_for_cities_by_name_succesful(self, mock_get):
        weather_cities = {
            "data": [
                {
                    "city": "Warsaw",
                    "weather": "Rainy",
                    "temperature": "2C",
                    "wind_dir": "NE",
                    "wind_speed": "31km/h",
                    "date": "2021-01-01"
                },
                {
                    "city": "Wroclaw",
                    "weather": "Clear sky",
                    "temperature": "4C",
                    "wind_dir": "SW",
                    "wind_speed": "0km/h",
                    "date": "2021-01-01"
                },
                {
                    "city": "Gdansk",
                    "weather": "Snow storm",
                    "temperature": "-3C",
                    "wind_dir": "NE",
                    "wind_speed": "35km/h",
                    "date": "2021-01-01"
                }
            ]
        }

        mock_get.return_value = Mock(status=200)
        mock_get.return_value.json.return_value = weather_cities

        response = self.temp.get_weather_for_cities_by_name("Warsaw", "Wroclaw", "Gdansk")

        self.assertEqual(response.json(), weather_cities)

    @patch('src.weather.weather.requests.get')
    def test_get_weather_for_cities_by_name_partial_success(self, mock_get):
        weather_cities = {
            "data": [
                {
                    "city": "Warsaw",
                    "weather": "Rainy",
                    "temperature": "2C",
                    "wind_dir": "NE",
                    "wind_speed": "14km/h",
                    "date": "2021-01-04"
                },
                {
                    "city": "Wroclaw",
                    "weather": "Clear sky",
                    "temperature": "4C",
                    "wind_dir": "SW",
                    "wind_speed": "3km/h",
                    "date": "2021-01-04"
                }
            ]
        }

        mock_get.return_value = Mock(status=206)
        mock_get.return_value.json.return_value = weather_cities

        response = self.temp.get_weather_for_cities_by_name("Warsaw", "Wroclaw", "Gdainsik")

        self.assertEqual(response.json(), weather_cities)

    @patch('src.weather.weather.requests.get')
    def test_while_get_weather_for_cities_by_name_requests_get_is_called(self, spy_get):
        self.temp.get_weather_for_cities_by_name("Warsaw", "Wroclaw", "Gdansk")

        spy_get.assert_called_once_with('api.myweatherapi.com/v1/cities=Warsaw,Wroclaw,Gdansk')


    @patch('src.weather.weather.requests.get')
    def test_get_weather_for_cities_by_name_no_city_valid(self, mock_get):
        weather_cities = {
            "message": "Invalid cities"
        }

        mock_get.return_value = Mock(status=400)
        mock_get.return_value.json.return_value = weather_cities

        response = self.temp.get_weather_for_cities_by_name("Ugabuga", "Na pewno nie miasto", "Podkarpacie")

        self.assertEqual(response, None)

    def test_get_weather_for_cities_by_name_raises_value_error_with_no_args(self):
        with self.assertRaisesRegexp(ValueError, "Cities must be provided"):
            self.temp.get_weather_for_cities_by_name()


    def test_get_weather_by_geo_coordinates_succesful(self):
        with patch('src.weather.weather.requests.get') as mock_get:
            weather_coordinates = {
                "data": [
                    {
                        "city": "Gdansk",
                        "weather": "Broken Clouds",
                        "temperature": "-4C",
                        "wind_dir": "SW",
                        "wind_speed": "5km/h",
                        "date": "2021-01-11"
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
                        "wind_dir": "SW",
                        "wind_speed": "17km/h",
                        "date": "2021-01-03"
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
                        "wind_dir": "SW",
                        "wind_speed": "5km/h",
                        "date": "2021-01-04"
                    }
                ]
            }

            mock_get.return_value = MagicMock(status=200)
            mock_get.return_value.json.return_value.__contains__.return_value = True

            response = self.temp.get_weather_by_zip_code_pl("11-500")

            self.assertTrue(weather_coordinates in response.json())

    def test_get_weather_by_zip_code_pl_no_data_for_zip_code(self):
        with patch('src.weather.weather.requests.get') as mock_get:
            weather_coordinates = {
                "mesage": "No data found for given zip code"
            }

            mock_get.return_value = Mock(status=404)
            mock_get.return_value.json.return_value = weather_coordinates

            response = self.temp.get_weather_by_zip_code_pl("99-999")

            self.assertEqual(response, None)

    def test_get_weather_by_zip_code_pl_raises_value_error_with_wrong_format(self):
        with self.assertRaisesRegexp(ValueError, "Zip code must be formated like XX-XXX"):
            self.temp.get_weather_by_zip_code_pl("1234-39")

    def test_get_weather_by_zip_code_pl_raises_type_error_with_not_string(self):
        with self.assertRaisesRegexp(TypeError, "Zip code must be of string type"):
            self.temp.get_weather_by_zip_code_pl(12345)

    def test_while_get_weather_by_zip_code_pl_requests_get_is_called(self):
        with patch('src.weather.weather.requests.get') as spy_get:
            self.temp.get_weather_by_zip_code_pl("11-500")

            spy_get.assert_called_once_with('api.myweatherapi.com/v1/zip=11-500')

    def tearDown(self):
        self.temp = None

if __name__ == '__main__':
    main()
