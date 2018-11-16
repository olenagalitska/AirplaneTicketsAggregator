from app import logger
from app.airlines.wizzair import WizzairInfoRobber
from app.airlines.ryanair import RyanairInfoRobber
from app.airlines.klm import KLMInfoRobber


class Handler:

    def __init__(self):
        logger.info('try to init WizzairInfoRobber()')
        self.wizzair_info_robber = WizzairInfoRobber()
        logger.info('succeeded')

        logger.info('try to init RyanairInfoRobber()')
        self.ryanair_info_robber = RyanairInfoRobber()
        logger.info('succeeded')

        logger.info('try to init KLMInfoRobber()')
        self.klm_info_robber = KLMInfoRobber()
        logger.info('succeeded')

    def handle(self, search_data, airlines):
        results = []

        logger.info('search_data: ' +
                    str(search_data.departure) +
                    str(search_data.arrival) +
                    str(search_data.date) +
                    str(search_data.adults) +
                    str(search_data.seniors) +
                    str(search_data.teens) +
                    str(search_data.children) +
                    str(search_data.infants))

        logger.info('airlines: ' + str(airlines))

        if "wizzair" in airlines:
            logger.info('try to get flights from wizzair')

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
            logger.info('try to get flights from ryanair')

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

        # if "klm" in airlines:
        logger.info('try to get flights from klm')

        self.klm_info_robber.get_flights(
            results=results,
            depart=search_data.departure,
            arrive=search_data.arrival,
            date=search_data.date,
            adults=str(int(search_data.adults) + int(search_data.seniors)),
            children=str(search_data.children + search_data.teens),
            infants=str(search_data.infants)
        )



        logger.info('results:' + str(results))
        return results
