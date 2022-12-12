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
        # super().__init__(sheet_name, url, token)
        self.date_from = (dt.datetime.now() + relativedelta(days=1)).strftime(
            "%d/%m/%Y"
        )
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
            nights_in_dst_from=7,
            nights_in_dst_to=30,
            flight_type="round",
            max_stopovers=2,
            select_airlines="AI",
            curr="INR",
        )

    def get_details(self, city_codes: list):
        self.lowestPrices_new = []
        self.city_from = []
        self.city_to = []
        self.journey_dates = []
        for city in city_codes:
            params = self.flight_search_params(city)
            try:
                flight_deals = flight_search.get_flight_deals(params)["data"][0]
            except (KeyError, ImportError):
                self.city_from.append("NULL")
                self.city_to.append("NULL")
                self.lowestPrices_new.append("NULL")
                self.journey_dates.append("NULL")
            else:
                self.city_from.append(
                    f"{flight_deals['cityFrom']}-{flight_deals['flyFrom']}"
                )
                self.city_to.append(f"{flight_deals['cityTo']}-{flight_deals['flyTo']}")
                self.lowestPrices_new.append(flight_deals["price"])
                from_ = flight_deals["route"][0]["local_departure"].split("T")[0]
                to_ = flight_deals["route"][-1]["local_arrival"].split("T")[0]
                self.journey_dates.append(f"{from_} to {to_}")

    def start(self):
        city_codes = self.get_column("iataCode")
        self.get_details(city_codes)
        self.lowestPrices_old = self.get_column("lowestPrice")
        i = 0
        for new, old, city_from, city_to, journey_date in zip(
            self.lowestPrices_new,
            self.lowestPrices_old,
            self.city_from,
            self.city_to,
            self.journey_dates,
        ):
            if new != "NULL":
                if new < old:
                    self.edit_value(row_id=i + 2, col_name="lowestPrice", value=new)
                    msg = f"Low price alert! Only ₹{new} to fly from {city_from} to {city_to}, from {journey_date}"
                    mailMan.send_sms(body=msg)
            i += 1

    def test(self):
        params = self.flight_search_params(fly_to="DEL")
        details = flight_search.get_flight_deals(params)
        self.get_details(["DEL"])
        with open("data.json", "w") as f:
            json.dump(details, f)
        print(len(details["data"]), "results found.")
        msg = f"Low price alert! Only ₹{self.lowestPrices_new} to fly from {self.city_from} to {self.city_to}, from {self.journey_dates}"
        print(msg)
