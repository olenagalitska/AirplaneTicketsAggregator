import requests
import json


class WizzairInfoRobber:
    @staticmethod
    def get_flights(results, depart, arrive, date, adults, children, infants):
        data = {"isFlightChange": 'false', "isSeniorOrStudent": 'false',
                "flightList": [{"departureStation": depart, "arrivalStation": arrive, "departureDate": date}],
                "adultCount": adults, "childCount": children, "infantCount": infants, "wdc": 'true'}
        r = requests.post(url="https://be.wizzair.com/8.3.0/Api/search/search",
                          json=data,
                          headers={"content-type": 'application/json;charset=UTF-8'})
        print(" wizzair status code = ", r.status_code)
        if r.status_code == 200:
            json_response = json.loads(r.text)
            flights = json_response['outboundFlights']
            for flight in flights:
                json_flight = {
                    'airportA': depart,
                    'airportB': arrive,
                    'airline': 'Wizzair',
                    'dateDeparture': flight['departureDateTime'].split('T')[0],
                    'dateArrival': flight['arrivalDateTime'].split('T')[0],
                    'timeDeparture': flight['departureDateTime'].split('T')[1],
                    'timeArrival': flight['arrivalDateTime'].split('T')[1]
                }
                fares = flight['fares']
                json_fares = []
                json_types = []
                for fare in fares:
                    if not fare['wdc']:
                        json_types.append(fare['bundle'])
                        json_fares.append(fare['fullBasePrice'])

                json_flight['fares'] = json_fares
                json_flight['types'] = json_types
                res_url = 'https://wizzair.com/#/booking/select-flight/' + depart \
                          + '/' + arrive + '/' + date + '/null/' + adults + \
                          '/' + children + '/' + infants + '/0/null'
                json_flight['url'] = res_url
                results.append(json_flight)
            return True
        return False
