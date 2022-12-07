import requests
from pprint import pprint
from auth import tequila_api_key, tequila_location_url


class FlightSearch:
    def __init__(self, city_names: list):
        self.url = tequila_location_url
        self.params = [dict(term=city) for city in city_names]
        self.headers = dict(apikey=tequila_api_key)

    def get_city_codes(self) -> list:
        city_codes = []
        for param in self.params:
            response = requests.get(url=self.url, params=param, headers=self.headers)
            city_codes.append(response.json()["locations"][0]["code"])
        return city_codes
