import requests
import json


class RyanairInfoRobber:
    @staticmethod
    def get_flights(results, depart, arrive, date, adults, children, infants, teens):
        data = {
            'ADT': adults,
            'TEEN': teens,
            'CHD': children,
            'INF': infants,
            'DateOut': date,
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
        print(r.status_code)
        print(r.text)
        if r.status_code == 200:
            date = date + "T00:00:00.000"
            json_response = json.loads(r.text)
            trips = json_response['trips']
            for trip in trips:
                dates = trip['dates']
                for dat in dates:
                    if dat['dateOut'] == date:
                        flights = dat['flights']
                        if len(flights) > 0:
                            for flight in flights:
                                fares = flight['regularFare']
                                fares = fares['fares']
                                time_depart = flight['time'][0]
                                time_arrive = flight['time'][1]
                                json_flight = {
                                    'airportA': depart,
                                    'airportB': arrive,
                                    'airline': 'Ryanair',
                                    'dateDeparture':time_depart.split('T')[0],
                                    'dateArrival': time_arrive.split('T')[0],
                                    'timeDeparture':time_depart.split('T')[1],
                                    'timeArrival': time_arrive.split('T')[1]
                                }
                                json_fares = []
                                json_types = []
                                for fare in fares:
                                    fare_and_curr = {}
                                    fare_and_curr['amount'] = fare['amount']
                                    fare_and_curr['currencyCode'] = 'EUR'
                                    json_fares.append(fare_and_curr)
                                    json_types.append(fare['type'])

                                json_flight['types'] = json_types
                                json_flight['fares'] = json_fares
                                results.append(json_flight)
            # flights = json_response['flights']
            # print(flights)

            return True
        return None
