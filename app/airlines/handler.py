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

    def handle_form(self, search_data, airlines):
        results = []

        for airline in airlines:

            if airline == 'wizzair':
                print("coming for wizz")
                self.wizzair_info_robber.get_flights(
                    results=results,
                    depart=search_data['departure'],
                    arrive=search_data['arrival'],
                    date=search_data['date'],
                    adults=str(int(search_data['adults']) + int(search_data['seniors']) + int(search_data['teens'])),
                    children=str(search_data['children']),
                    infants=str(search_data['infants'])
                )

            if airline == 'ryanair':
                print("coming for ryan")
                self.ryanair_info_robber.get_flights(
                    results=results,
                    depart=search_data['departure'],
                    arrive=search_data['arrival'],
                    date=search_data['date'],
                    adults=str(int(search_data['adults']) + int(search_data['seniors'])),
                    children=str(search_data['children']),
                    infants=str(search_data['infants']),
                    teens=str(search_data['teens'])
                )

        print(results)
        return results

    def handle(self, search_data, airlines):
        results = []

        if "wizzair" in airlines:
            print("coming for wizz")
            self.wizzair_info_robber.get_flights(
                results=results,
                depart=search_data.departure,
                arrive=search_data.arrival,
                date=search_data.date,
                adults=str(
                    int(search_data.adults) + int(search_data.seniors) + int(search_data.teens)),
                children=str(search_data.children),
                infants=str(search_data.infants)
            )
        if "ryanair" in airlines:
            print("coming for ryan")
            print(search_data)

            self.ryanair_info_robber.get_flights(
                results=results,
                depart=search_data.departure,
                arrive=search_data.arrival,
                date=search_data.date,
                adults=str(int(search_data.adults) + int(search_data.seniors)),
                children=str(search_data.children),
                infants=str(search_data.infants),
                teens=str(search_data.teens)
            )

        print(results)
        return results
