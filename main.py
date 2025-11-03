#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os

import flight_data
from notification_manager import NotificationManager
from data_manager import DataManager
from flight_search import FlightSearch
import datetime as dt

# ==================== Set up the Flight Search ====================

notification_manager = NotificationManager()
flight_search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_data()

# Set your origin airport
ORIGIN_CITY_IATA = "CVG"

# ==================== Search for Flights and Send Notifications ====================

# Creates a list of date tuples (departure_date, return_date) 2 week durations from today to +180 days
dates = []
for number in range(1,181):
    new_departure_date = dt.datetime.now() + dt.timedelta(days=number)
    new_return_date = new_departure_date + dt.timedelta(days=14)
    formatted_new_departure_date = new_departure_date.strftime("%Y-%m-%d")
    formatted_new_return_date = new_return_date.strftime("%Y-%m-%d")
    dates.append((formatted_new_departure_date, formatted_new_return_date))

for row in sheet_data:
    current_destination = row["iataCode"]
    lowest_price = row["lowestPrice"]
    flights = []
    for date in dates[:3]:
        departure_date = date[0]
        return_date = date[1]
        flights.append(
            flight_data.find_cheapest_flight(
                flights=flight_search.get_flight_offers(
                    origin_location_code=ORIGIN_CITY_IATA,
                    destination_location_code=current_destination,
                    departure_date=departure_date,
                    return_date=return_date,
                    adults=1,
                    currency_code="USD",
                    max_price=lowest_price,
                )
            )
        )

    best_flight = flights[0]

    for flight in flights:
        if float(flight.price) < float(best_flight.price):
            best_flight = flight

    notification_manager.send_smtp_message(
        phone_number=os.getenv("MY_PHONE_NUMBER"),
        message=f"Low price alert! Only ${best_flight.price} to fly from {best_flight.origin_airport} to "
                f"{best_flight.destination_airport} on {departure_date} until {return_date}.")


