import requests

class WeatherApp(object):
    def __init__(self):
        self.base_url = 'api.myweatherapi.com/v1/'

    def get_weather_by_city_name(self, city_name):
        if type(city_name) != str:
            raise TypeError("City name must be of string type")

        res = requests.get(self.base_url + "city=" + city_name)
        
        if res.status != 200:
            return None
        else:
            return res

    def get_weather_by_geo_coordinates(self, lat, lon):
        res = requests.get(self.base_url + "lat=" + str(lat) + "&lon=" + str(lon))

        return res
