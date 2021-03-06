from pymongo import MongoClient

class WeatherDatabase(object):
    def __init__(self, url, mongo_client = MongoClient):
        self.client = mongo_client(url)
        self.db = self.client.db

    def add(self, weather):
        try:
            result = self.db.insert_one(weather)
        except:
            result = "Couldn't insert into mongodb"
        return result

    def find(self, city_name):
        try:
            result = self.db.find_one({"city": city_name})
        except:
            result = "Couldn't query mongodb"
        return result

    def delete(self, city_name):
        try:
            self.db.delete_one({"city": city_name})
            return "Successfully deleted from mongodb"
        except:
            return "Couldn't delete from mongodb"
