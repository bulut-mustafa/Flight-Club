import requests
import datetime as dt
from dateutil.relativedelta import relativedelta 
from flight_data import FlightData
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "YOUR TEQUILA KEY"
HEADERS = {
    "apikey" : TEQUILA_API_KEY
}

class FlightSearch:

    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        query = {
            "term" : city_name,
            "location_types": "city"
        }
        respond = requests.get(url=location_endpoint, params=query, headers=HEADERS)
        result = respond.json()["locations"]
        code = result[0]["code"]
        return code
    
    def get_cheapest_flight(self, origin_city_code, destination_city_code):
        
        tomorrows_date = dt.datetime.now()
        tomorrow_string = tomorrows_date.strftime("%d/%m/%Y")
        six_months = tomorrows_date + relativedelta(months=+6)
        six_string = six_months.strftime("%d/%m/%Y")
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        query = {
        "fly_from": origin_city_code,
        "fly_to": destination_city_code,
        "date_from": tomorrow_string,
        "date_to": six_string,
        "flight_type": "round",
        "one_for_city": 1,
        "max_stopovers": 2,
        "nights_in_dst_from": 10,
        "nights_in_dst_to":30,
        "curr": "USD",
        "adult_hold_bag": "1"
        }
        
        response = requests.get(url=search_endpoint, params=query, headers=HEADERS)
        
        try:
            result = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None
        
        
        if len(result["route"]) == 2:
            flight_data = FlightData(
                price=result["price"],
                origin_city=result["cityFrom"],
                origin_airport=result["flyFrom"],
                destination_city=result["cityTo"],
                destination_airport=result["flyTo"],
                out_date= result["route"][0]["local_departure"].split("T")[0],
                return_date= result["route"][1]["local_departure"].split("T")[0],
                route= f"{result['route'][0]['flyFrom']}-{result['route'][0]['flyTo']}-{result['route'][1]['flyFrom']}-{result['route'][1]['flyTo']}",
                stepover= 0
            )
        elif len(result["route"]) == 4:
            flight_data = FlightData(
                price=result["price"],
                origin_city=result["cityFrom"],
                origin_airport=result["flyFrom"],
                destination_city=result["cityTo"],
                destination_airport=result["flyTo"],
                out_date= result["route"][0]["local_departure"].split("T")[0],
                return_date= result["route"][1]["local_departure"].split("T")[0],
                route = f"""{result['route'][0]['flyFrom']}-{result['route'][0]['flyTo']}-{result['route'][1]['flyFrom']}-{result['route'][1]['flyTo']}-
                            {result['route'][2]['flyFrom']}-{result['route'][2]['flyTo']}-{result['route'][3]['flyFrom']}-{result['route'][3]['flyTo']}""",
                stepover=1
            )
        
            
        
        print(f"{flight_data.destination_city}: ${flight_data.price} -- Route: {flight_data.route}")
        return flight_data
        