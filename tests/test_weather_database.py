from unittest import TestCase, main
from unittest.mock import Mock, patch, MagicMock
import unittest
import mongomock

from src.weather_database.weather_database import WeatherDatabase


class TestWeatherApp(TestCase):
    def setUp(self):
        self.temp = WeatherDatabase("mongodb://mongodb.example.com:27017", mongomock.MongoClient)

    
    def test_add_calls_mongo_insert_one(self):
        self.temp.client.db.insert_one = Mock()

        self.temp.add({
                "city": "Warsaw",
                "weather": "Rainy",
                "temperature": "2C",
                "wind_dir": "NE",
                "wind_speed": "21km/h",
                "date": "2021-01-10"
        })

        self.temp.client.db.insert_one.assert_called_once()

    def test_add_inserts_weather_to_mongo_db(self):
        self.temp.client.db.insert_one = Mock()
        self.temp.find = Mock()

        data = {
            "city": "Warsaw",
            "weather": "Rainy",
            "temperature": "2C",
            "wind_dir": "NE",
            "wind_speed": "21km/h",
            "date": "2021-01-10"
        }

        self.temp.find.return_value = data

        self.temp.add(data)

        self.assertDictEqual(data, self.temp.find("Warsaw"))

    def test_add_returns_error_message_when_error_raised(self):
        self.temp.client.db.insert_one = Mock()
        self.temp.client.db.insert_one.side_effect = ConnectionError("error connecting to mongodb")

        data = {
            "city": "Warsaw",
            "weather": "Rainy",
            "temperature": "2C",
            "wind_dir": "NE",
            "wind_speed": "21km/h",
            "date": "2021-01-10"
        }


        self.assertEquals(self.temp.add("data"), "Couldn't insert into mongodb")

    def test_add_doesnt_returns_data_when_error_raised(self):
        self.temp.client.db.insert_one = Mock()
        self.temp.client.db.insert_one.side_effect = ConnectionError("error connecting to mongodb")

        data = {
            "city": "Warsaw",
            "weather": "Rainy",
            "temperature": "2C",
            "wind_dir": "NE",
            "wind_speed": "21km/h",
            "date": "2021-01-10"
        }

        self.temp.add(data)

        self.assertNotEqual(self.temp.add("data"), data)

    def test_find_calls_mongo_find_one(self):
        self.temp.client.db.find_one = Mock()

        self.temp.find("Warsaw")

        self.temp.client.db.find_one.assert_called_once()

    def test_find_returns_weather_from_mongo_db(self):
        self.temp.client.db.find_one = Mock()
        self.temp.add = Mock()

        data = {
            "city": "Warsaw",
            "weather": "Rainy",
            "temperature": "2C",
            "wind_dir": "NE",
            "wind_speed": "21km/h",
            "date": "2021-01-10"
        }

        self.temp.add(data)
        self.temp.client.db.find_one.return_value = data

        self.temp.find("Warsaw")


        self.temp.add(data)

        
        self.assertDictEqual(data, self.temp.find("Warsaw"))

    def test_find_returns_error_message_when_error_raised(self):
        self.temp.client.db.find_one = MagicMock()
        self.temp.client.db.find_one.side_effect = ConnectionError("error connecting to mongodb")

        self.temp.find({
            "city": "Warsaw"
        })

        self.assertEquals(self.temp.find("Warsaw"), "Couldn't insert into mongodb")

    def test_delete_calls_mongo_delete_one(self):
        self.temp.client.db.delete_one = Mock()

        self.temp.delete({
            "city": "Warsaw"
        })

        self.temp.client.db.delete_one.assert_called_once()

    def tearDown(self):
        self.temp = None
