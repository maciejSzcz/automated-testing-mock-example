from pymongo import MongoClient

class WeatherDatabase(object):
    def __init__(self, url, mongo_client = MongoClient):
        self.client = mongo_client(url)
        self.db = self.client.db

    def add(self, weather):
        result = self.db.insert_one(weather)
        return result

    def find(self, city_name):
        result = self.db.find_one({"city": city_name})
        return result

    def delete(self, city_name):
        result = self.db.delete_one({"city": city_name})
        return result
