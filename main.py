#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
import datetime as dt

data_manager = DataManager()
flight_search = FlightSearch()

sheet_data = data_manager.get_data()

dates = []
for number in range(1,181):
    new_departure_date = dt.datetime.now() + dt.timedelta(days=number)
    new_return_date = new_departure_date + dt.timedelta(days=14)
    formatted_new_departure_date = new_departure_date.strftime("%Y-%m-%d")
    formatted_new_return_date = new_return_date.strftime("%Y-%m-%d")
    dates.append((formatted_new_departure_date, formatted_new_return_date))

for row in sheet_data:
    # if row["iataCode"] == '':
    #     data_manager.update_data(
    #         id=row["id"],
    #         iata_code=flight_search.get_iata_code(city=row["city"]),
    #     )

    current_destination = row["iataCode"]
    lowest_price = row["lowestPrice"]
    flights = []
    for date in dates[:3]:
        departure_date = date[0]
        return_date = date[1]
        # print(f"Getting price for {row["city"]}")
        flights.append(flight_search.get_flight_offers(origin_location_code="CVG",
                                        destination_location_code=current_destination,
                                        departure_date=departure_date,
                                        return_date=return_date,
                                        adults=1,
                                        currency_code="USD",
                                        max_price=lowest_price))

    best_flight: FlightData = FlightData(price="9999",
                                         out_date="1999-01-01", return_date="1999-01-01",
                                         origin_airport="CVG", destination_airport="CVG",
                                         )
    for flight in flights:
        if float(flight.price) < float(best_flight.price):
            best_flight = flight

    print(f"Low price alert! Only ${best_flight.price} to fly from {best_flight.origin_airport} to "
          f"{best_flight.destination_airport} on {departure_date} until {return_date}.")


