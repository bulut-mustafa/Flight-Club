
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
data_manager = DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_destination_data()
notification_manager = NotificationManager()

ORIGIN_CITY_CODE = "NYC"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()
    

for destination in sheet_data:
    cheapest_flight = flight_search.get_cheapest_flight(ORIGIN_CITY_CODE, destination["iataCode"])
    
    if cheapest_flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! Only £{cheapest_flight.price} to fly from {cheapest_flight.origin_city}-{cheapest_flight.origin_airport} to {cheapest_flight.destination_city}-{cheapest_flight.destination_airport}, from {cheapest_flight.out_date} to {cheapest_flight.return_date}."
        )


