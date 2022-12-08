import requests


class FlightSearch:
    def __init__(self, url, api_key):
        self.url = url
        self.headers = dict(apikey=api_key)

    def get_city_codes(self, city_names: list) -> list:
        city_names = [dict(term=city) for city in city_names]
        city_codes = []
        for city in city_names:
            response = requests.get(url=self.url, params=city, headers=self.headers)
            city_codes.append(response.json()["locations"][0]["code"])
        return city_codes

    def get_city_code(self, city_name: str) -> list:
        if not city_name:
            return "CCU"
        city_names = [dict(term=city) for city in city_names]
        response = requests.get(url=self.url, params=city_name, headers=self.headers)
        city_code = response.json()["locations"][0]["code"]
        return city_code

    def get_flight_deals(self, params: dict):
        response = requests.get(url=self.url, params=params, headers=self.headers)
        return response.json()
