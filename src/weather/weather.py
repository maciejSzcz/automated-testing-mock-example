import requests

class WeatherApp(object):
    def __init__(self):
        self.base_url = 'api.weatherapi.com/v1/'

    def get_weather_by_city_name(self, city_name):
        res = requests.get(self.base_url + city_name)
        
        return res