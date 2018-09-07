from app import search_handler, arangodb, psqldb
import threading
import time
from app.models import Flight
from app.mail_sender import MailSender


class FlightsUpdater(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.name = name
        self.isWorking = True

    def run(self):
        time.sleep(30)
        print('Flights Updater started')
        while self.isWorking:
            saved_flights = arangodb.collection('saved_flights')
            flights = []
            print(saved_flights)

            for saved_flight in saved_flights:
                flight = Flight.query.get(saved_flight["flight_id"])
                flights.append(flight)

            for flight in flights:

                with app.test_request_context():
                    search_data = SearchRequest(flight.departure, flight.arrival, str(flight.departureTime.date()),
                                                1, 0, 0, 0, 0, False, False, False)

                    if flight.airline == 'ryanair':
                        search_data.ryanair = True
                    else:
                        if flight.airline == 'wizzair':
                            search_data.wizzair = True
                        if flight.airline == 'uia':
                            search_data.uia = True

                    # print("r: " + search_data.get('ryanair'))
                    search_results = search_handler.handle(search_data)
                    if len(search_results) > 0:
                        result = search_results[0]
                        result.get("fares")[0].get("amount")

                        print(flight.price)
                        if result.get("fares")[0].get("amount") != flight.price:
                            print("Update Found!")
                            old_price = flight.price
                            flight.price = result.get("fares")[0].get("amount")
                            psqldb.session.commit()

                            mail_sender = MailSender()
                            mail_sender.send_update(flight_id=flight.id, old_price=old_price)

            time.sleep(60 * 60)

    def stop(self):
        self.isWorking = False
