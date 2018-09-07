from app import app, mail, arangodb
from app.models import User, Flight
from flask_mail import Message


class MailSender():

    def send_update(self, flight_id, old_price):
        saved_flights = arangodb.collection('saved_flights')

        users = []
        for saved_flight in saved_flights:
            if saved_flight['flight_id'] == flight_id:
                users = saved_flight['users']

        recipients = []
        for user_id in users:
            user = User.query.get(user_id)
            recipients.append(user.email)

        flight = Flight.query.get(flight_id)
        msg_subj = "Price for your flight has changed!"
        with app.app_context():
            msg = Message(msg_subj, recipients=recipients)
            msg.html = "<p>" + flight.departure + "---->" + flight.arrival + "</p>" \
                    "<p>" + flight.airline + "</p>" \
                    "<p>" + str(flight.departureTime) + " - " + str(flight.arrivalTime) + "</p>" \
                     "<p> Old price: " + str(old_price) + "</p>" \
                     "<p> New price: " + str(flight.price) + "</p>"

            mail.send(msg)
