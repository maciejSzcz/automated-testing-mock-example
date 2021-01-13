from pymongo import MongoClient

class WeatherDatabase(object):
    def __init__(self, url, mongo_client = MongoClient):
        self.client = mongo_client(url)
        self.db = self.client.db

    def add(self, weather):
        try:
            result = self.db.insert_one(weather)
        except ValueError:
            print("Couldn't insert into mongodb")
        return result

    def find(self, city_name):
        result = self.db.find_one({"city": city_name})
        return result

    def delete(self, city_name):
        self.db.delete_one({"city": city_name})
