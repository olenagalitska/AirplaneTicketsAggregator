import threading
import time
import datetime

from app import app, arangodb, psqldb, search_handler
from app.models import Flight
from app.mail_sender import MailSender
from app.search_req import SearchRequest

from app.dbmanager.flights_stats_manager import FlightsStatsManager


class FlightsUpdater(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.name = name
        self.isWorking = True

    def needs_update(self, fares_in_db, current_fares):
        result = False
        for i in range(0, len(current_fares)):
            if current_fares[i]['amount'] != fares_in_db[i]['amount']:
                result = True
                break

        return result

    def run(self):
        print('Flights Updater started')
        while self.isWorking:
            saved_flights = arangodb.collection('saved_flights')
            flights = []
            print(saved_flights)

            for saved_flight in saved_flights:
                flight = Flight.query.get(saved_flight["flight_id"])
                flights.append(flight)

            print(flights)

            for flight in flights:

                # with app.test_request_context():
                search_data = SearchRequest(flight.departure, flight.arrival, str(flight.departureTime.date()),
                                            1, 0, 0, 0, 0)

                airlines = []
                if flight.airline == 'Ryanair':
                    airlines.append = 'ryanair'
                else:
                    if flight.airline == 'Wizzair':
                        airlines.append = 'wizzair'
                    # if flight.airline == 'UIA':
                    #     airlines.append = 'uia'

                search_results = search_handler.handle(search_data, airlines)
                if len(search_results) > 0:
                    result = search_results[0]
                    current_fares = result.get("fares")

                    in_db = FlightsStatsManager.get_stats_for(flight.id)

                    print(in_db['fares'])
                    print(current_fares)
                    if self.needs_update(in_db['fares'], current_fares):
                        FlightsStatsManager.update_stats(flight.id,
                                                         {'date': str(datetime.date.today()), 'fares': current_fares})
                        print("Update Found!")

                        MailSender.send_update(flight_id=flight.id, fares=current_fares)

            time.sleep(60 * 60)

    def stop(self):
        self.isWorking = False
