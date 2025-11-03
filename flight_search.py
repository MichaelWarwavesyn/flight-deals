import requests
from dotenv import load_dotenv
import os

load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

#This class is responsible for talking to the Flight Search API.
class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        # Getting a new token every time program is run. Could reuse unexpired tokens as an extension.
        self._token = self._get_new_token()

    def _get_new_token(self):
        amadeus_header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        amadeus_body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        amadeus_response = requests.post(url=TOKEN_ENDPOINT,headers=amadeus_header,data=amadeus_body)

        return amadeus_response.json()['access_token']

    def get_iata_code(self, city):
        amadeus_city_search_query = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS",
        }
        amadeus_header = {"Authorization": f"Bearer {self._token}"}
        amadeus_city_search_response = requests.get(
            url=IATA_ENDPOINT,
            headers=amadeus_header,
            params=amadeus_city_search_query)

        print(f"Status code {amadeus_city_search_response.status_code}. Airport IATA: {amadeus_city_search_response.text}")
        try:
            code = amadeus_city_search_response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"

        return code

    def get_flight_offers(
            self, origin_location_code, destination_location_code,
            departure_date, return_date, adults, currency_code, max_price):
        flight_offers_query = {
            "originLocationCode": origin_location_code,
            "destinationLocationCode": destination_location_code,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": adults,
            "currencyCode": currency_code,
            "maxPrice": max_price,
        }
        flight_offers_header = {"Authorization": f"Bearer {self._token}"}
        flight_offers_response = requests.get(url=FLIGHT_ENDPOINT,headers=flight_offers_header,params=flight_offers_query)
        flight_offers_data = flight_offers_response.json()["data"]

        return flight_offers_data
