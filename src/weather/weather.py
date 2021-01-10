import requests
import re

class WeatherApp(object):
    def __init__(self, database=None):
        self.__base_url = 'api.myweatherapi.com/v1/'
        self.__weather_database = database

    @property
    def base_url(self):
        return self.__base_url

    @property
    def weather_database(self):
        return self.__weather_database

    def save_weather_single_city(self, city_name):
        city = self.get_weather_by_city_name(city_name)

        self.weather_database.add(city)

    def get_weather_by_city_name(self, city_name):
        if type(city_name) != str:
            raise TypeError("City name must be of string type")

        res = requests.get(self.base_url + "city=" + city_name)
        
        if res.status != 200:
            return None
        else:
            return res

    def get_weather_for_cities_by_name(self, *city_names):
        if len(city_names) == 0:
            raise ValueError("Cities must be provided")

        cities_str = ','.join(city_names)

        res = requests.get(self.base_url + "cities=" + cities_str)

        if res.status != 200 and res.status != 206:
            return None
        else:
            return res

    def get_weather_by_geo_coordinates(self, lat, lon):
        if type(lat) != float or type(lon) != float:
            raise TypeError("Coordinates must be of float type")
        elif lat > 90.000 or lat < -90.000:
            raise ValueError("Latitude has to be between -90 and 90")
        elif lon > 180.000 or lon < -180.000:
            raise ValueError("Longitude has to be between -180 and 180")

        res = requests.get(self.base_url + "lat=" + str(lat) + "&lon=" + str(lon))

        if res.status != 200:
            return None
        else:
            return res

    def get_weather_by_zip_code_pl(self, zip_code):
        format_regexp = re.compile(r"^[0-9]{2}-[0-9]{3}$")

        if type(zip_code) != str:
            raise TypeError("Zip code must be of string type")
        elif not format_regexp.match(zip_code):
            raise ValueError("Zip code must be formated like XX-XXX")

        res = requests.get(self.base_url + "zip=" + zip_code)

        if res.status != 200:
            return None
        else:
            return res

    
