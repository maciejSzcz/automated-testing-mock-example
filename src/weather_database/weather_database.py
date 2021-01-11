from pymongo import MongoClient

class WeatherDatabase(object):
    def __init__(self, url):
        self.client = MongoClient(url)
        self.db = self.client.weather

    def add(self, weather):
        result = self.db.insert_one(weather)
        return result

    def find(self, city_name):
        result = self.db.find({"city": city_name})
        return result

    def delete(self, city_name):
        result = self.db.delete_one({"city": city_name})
        return result
