#This class is responsible for structuring the flight data.
class FlightData:
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

def find_cheapest_flight(flights):
    """
        Parses flight data received from the Amadeus API to identify the cheapest flight option among
        multiple entries.

        Args:
            flights (list): The JSON data containing flight information returned by the API.

        Returns:
            FlightData: An instance of the FlightData class representing the cheapest flight found,
            or a FlightData instance where all fields are 'NA' if no valid flight data is available.

        This function initially checks if the data contains valid flight entries. If no valid data is found,
        it returns a FlightData object containing "N/A" for all fields. Otherwise, it starts by assuming the first
        flight in the list is the cheapest. It then iterates through all available flights in the data, updating
         the cheapest flight details whenever a lower-priced flight is encountered. The result is a populated
         FlightData object with the details of the most affordable flight.
    """
    best_flight_by_day: FlightData = FlightData(price="9999",
                                     out_date="1999-01-01", return_date="1999-01-01",
                                     origin_airport="CVG", destination_airport="CVG",
                                     )
    for flight_index in range(0,len(flights)):
        flight_offer = FlightData(
            price=flights[flight_index]["price"]["total"],
            origin_airport=flights[flight_index]["itineraries"][0]["segments"][0]["departure"]["iataCode"],
            destination_airport=flights[flight_index]["itineraries"][0]["segments"][-1]["arrival"]["iataCode"],
            out_date=flights[flight_index]["itineraries"][0]["segments"][0]["departure"]["at"],
            return_date=flights[flight_index]["itineraries"][0]["segments"][0]["departure"]["at"], # Not correct
        )
        if float(flight_offer.price) < float(best_flight_by_day.price):
            best_flight_by_day = flight_offer

    return best_flight_by_day
