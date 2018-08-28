from app.airlines.wizzair import WizzairInfoRobber
from app.airlines.ryanair import RyanairInfoRobber


class Handler:

    def __init__(self):
        self.wizzair_info_robber = WizzairInfoRobber()
        self.ryanair_info_robber = RyanairInfoRobber()

    # def handle(self, search_data):
    #
    #     results = []
    #
    #     airlines_icao = search_data.get('airlines')
    #     for airline_icao in airlines_icao:
    #         if airline_icao == "WZZ":
    #             self.wizzair_info_robber.getFlights(
    #                 results=results,
    #                 depart=search_data.get('departure'),
    #                 arrive=search_data.get('arrival'),
    #                 date=search_data.get('date')
    #             )
    #         elif airline_icao == "AUI":
    #             pass
    #         elif airline_icao == "RYR":
    #             pass
    #     return results

    def handle(self, search_data):
        results = []

        self.wizzair_info_robber.get_flights(
            results=results,
            depart=search_data.get('departure'),
            arrive=search_data.get('arrival'),
            date=search_data.get('date'),
            adults=str(int(search_data.get('adults')) + int(search_data.get('seniors')) + int(search_data.get('teens'))),
            children=str(search_data.get('children')),
            infants = str(search_data.get('infants'))
        )

        self.ryanair_info_robber.get_flights(
            results=results,
            depart=search_data.get('departure'),
            arrive=search_data.get('arrival'),
            date=search_data.get('date'),
            adults=str(int(search_data.get('adults')) + int(search_data.get('seniors'))),
            children=str(search_data.get('children')),
            infants=str(search_data.get('infants')),
            teens=str(search_data.get('teens'))
        )

        print(results)
        return results
