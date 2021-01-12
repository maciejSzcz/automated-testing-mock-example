from pymongo import MongoClient

class WeatherDatabase(object):
    def __init__(self, url, mongo_client = MongoClient):
        self.client = mongo_client(url)
        self.db = self.client.db

    def add(self, weather):
        result = self.db.insert_one(weather)
        return result
