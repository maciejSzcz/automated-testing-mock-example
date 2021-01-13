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

    def test_find_calls_mongo_find_one(self):
        self.temp.client.db.find_one = Mock()

        self.temp.find({
            "city": "Warsaw"
        })

        self.temp.client.db.find_one.assert_called_once()

    def tearDown(self):
        self.temp = None
