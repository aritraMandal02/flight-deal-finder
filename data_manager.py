from sheety import Sheety
import datetime as dt
from dateutil.relativedelta import relativedelta
from flight_search import FlightSearch
from auth import sheety_url, TOKEN
from auth import tequila_search_url, tequila_api_key, account_sid, auth_token
from msg_sender import MailMan
import json

flight_search = FlightSearch(url=tequila_search_url, api_key=tequila_api_key)
mailMan = MailMan(account_sid, auth_token)

sheet_name = "prices"
url = sheety_url
token = TOKEN


class Manager(Sheety):
    def __init__(self):
        super().__init__(sheet_name, url, token)
        self.date_from = dt.datetime.now().strftime("%d/%m/%Y")
        self.date_to = (dt.datetime.now() + relativedelta(months=6)).strftime(
            "%d/%m/%Y"
        )
        self.fly_from = flight_search.get_city_code(input("Enter departure city: "))

    def flight_search_params(self, fly_to: str) -> dict:
        return dict(
            fly_from=self.fly_from,
            fly_to=fly_to,
            date_from=self.date_from,
            date_to=self.date_to,
            curr="INR",
        )

    def get_details(self, city_codes: list):
        self.lowestPrices_new = []
        for city in city_codes:
            params = self.flight_search_params(city)
            flight_deals = flight_search.get_flight_deals(params)["data"][0]
            price = flight_deals["price"]
            self.city_from = f"{flight_deals['cityFrom']}-{flight_deals['flyFrom']}"
            self.city_to = f"{flight_deals['cityTo']}-{flight_deals['flyTo']}"
            self.lowestPrices_new.append(price)

    def start(self):
        city_codes = self.get_column("iataCode")
        self.get_details(city_codes)
        self.lowestPrices_old = self.get_column("lowestPrice")
        i = 0
        for new, old in zip(self.lowestPrices_new, self.lowestPrices_old):
            if new < old:
                self.edit_value(row_id=i + 2, col_name="lowestPrice", value=new)
                msg = f"Only ₹{new} to fly from {self.city_from} to {self.city_to}, from {self.date_from} to {self.date_to}"
                mailMan.send_sms(body=msg)
                print("change", i)
            i += 1

    def test(self):
        params = self.flight_search_params(fly_to="PAR")
        details = flight_search.get_flight_deals(params)
        with open("data.json", "w") as f:
            json.dump(details, f)
        print(details)
