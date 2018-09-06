# from app import search_handler, arangodb, psqldb
# import threading
# import time
# from app.models import Flight
# from app.mail_sender import MailSender


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

            for flight_id in saved_flights:
                flight = Flight.query.get(flight_id)
                flights.append(flight)

            for flight in flights:
                search_data = {
                    'departure': flight.departure,
                    'arrival': flight.arrival,
                    'date': flight.departureTime.date,
                    'adults': '1',
                    'wizzair': False,
                    'ryanair': False,
                    'uia': False
                }
                if flight.airline == 'wizzair':
                    search_data.wizzair = True
                else:
                    if flight.airline == 'ryanair':
                        search_data.ryanair = True
                    if flight.airline == 'uia':
                        search_data.uia = True
                result = search_handler.handle_form(search_data)[0]

                if result.fares.ADT != flight.price:
                    print("Update Found!")
                    old_price = flight.price
                    flight.price = result.fares.ADT
                    psqldb.session.commit()

                    MailSender.send_update(flight.id, old_price)

        time.sleep(60 * 60)


def stop(self):
    self.isWorking = False
