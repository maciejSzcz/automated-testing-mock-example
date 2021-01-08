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

    def get_weather_for_cities_by_name(self, *city_names):
        cities_str = ','.join(city_names)

        res = requests.get(self.base_url + "cities=" + cities_str)

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
        res = requests.get(self.base_url + "zip=" + zip_code)

        if res.status != 200:
            return None
        else:
            return res
