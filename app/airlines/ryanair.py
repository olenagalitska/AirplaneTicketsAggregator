import requests
import json


class RyanairInfoRobber:
    @staticmethod
    def get_flights(results, depart, arrive, date):
        data = {
            'ADT': '1',
            'TEEN': '0',
            'CHD': '0',
            'INF': '0',
            'DateOut': '2018 - 10 - 27',
            'Origin': depart,
            'Destination': arrive,
            'FlexDaysOut': '0',         # change to check whole month
            'IncludeConnectingFlights': 'false',
            'RoundTrip': 'false',
            'ToUs': 'AGREED',
            'exists': 'false'
        }
        r = requests.get(url="https://desktopapps.ryanair.com/v4/en-ie/availability",
                         params=data,
                         headers={"content-type": "application/json;charset=UTF-8"})
        if r.status_code == 200:
            json_response = json.loads(r.text)
            trips = json_response['trips']
            print(trips)
            for trip in trips:
                dates = trip['dates']
                print(dates)
            # flights = json_response['flights']
            # print(flights)
            # results = []
            # for flight in flights:
            #     json_flight = {
            #         'airportA': depart,
            #         'airportB': arrive,
            #         'airline': 'Wizzair',
            #         'date': flight['departureDateTime']
            #     }
            #     fares = flight['fares']
            #     for fare in fares:
            #         if fare['bundle'] == 'BASIC' and not fare['wdc']:
            #             full_price = fare['fullBasePrice']
            #             json_flight['price'] = full_price['amount']
            #     results.append(json_flight)
            return True
        return None
