import requests
from pluralizer import Pluralizer


class Sheety:
    def __init__(self, sheet_name: str, url: str, token: str):
        self.url = url
        self.headers = dict(Authorization=token)
        self.sheet_name = sheet_name
        self.sheet_data = self.get_sheet()
        self.col_names = list(self.sheet_data[0].keys())
        pluralizer = Pluralizer()
        self.row_entry = pluralizer.singular(sheet_name.lower())

    def get_sheet(self) -> list:
        response = requests.get(url=self.url, headers=self.headers).json()[
            self.sheet_name
        ]
        return response

    def edit_row(self, row_id: int, row_params: dict) -> requests.Response:
        body = {self.row_entry: row_params}
        self.edit_row_response = requests.put(
            url=f"{self.url}/{row_id}", json=body, headers=self.headers
        )
        return self.edit_row_response

    def post_row(self, row_params: dict) -> requests.Response:
        body = {self.row_entry: row_params}
        self.post_row_response = requests.post(
            url=self.url, json=body, headers=self.headers
        )
        return self.post_row_response

    def delete_row(self, row_id: int) -> requests.Response:
        self.delete_row_response = requests.delete(
            url=f"{self.url}/{row_id}", headers=self.headers
        )
        return self.delete_row_response

    def edit_value(self, row_id: int, col_name: str, value):
        row_id -= 2
        row_params = self.sheet_data[row_id]
        row_params[col_name] = value
        return self.edit_row(row_id + 2, row_params)

    def edit_column(self, col_name: str, values: list):
        i = 0
        for e in self.sheet_data:
            e[col_name] = values[i]
            e.pop("id")
            self.edit_row(row_id=i + 2, row_params=e)
            i += 1

    def get_column(self, col_name: str) -> list:
        self.col_items = []
        for e in self.sheet_data:
            self.col_items.append(e[col_name])
        return self.col_items

    def get_row(self, row_index) -> dict:
        return self.sheet_data[row_index]
