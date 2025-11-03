import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

# This class is responsible for talking to the Google Sheet.
class DataManager:
    def __init__(self):
        self.sheety_url = "https://api.sheety.co/1bc31422f630e2d688c55d4e83d46e6a/flightDeals/prices"
        self._user = os.getenv("SHEETY_USERNAME")
        self._password = os.getenv("SHEETY_PASSWORD")
        self._authorization = HTTPBasicAuth(self._user, self._password)

    def get_data(self):
        sheety_response = requests.get(url=self.sheety_url, auth=self._authorization)
        sheety_response.raise_for_status()
        sheety_data = sheety_response.json()["prices"]
        return  sheety_data

    def update_data(self, id, iata_code):
        row_sheety_url = f"{self.sheety_url}/{id}"
        body = {
            "price": {
                "iataCode": iata_code
            }
        }
        sheety_response = requests.put(url=row_sheety_url, json=body, auth=self._authorization)
        sheety_response.raise_for_status()

