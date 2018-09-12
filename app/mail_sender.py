from flask_mail import Message

from app import app, mail, arangodb
from app.models import User, Flight


class MailSender:

    @staticmethod
    def send_update(flight_id, fares):
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
        msg_subj = _("Price for your flight has changed!")
        with app.app_context():
            msg = Message(msg_subj, recipients=recipients)
            msg.html = "<p>" + flight.departure + "---->" + flight.arrival + "</p>" \
                    "<p>" + flight.airline + "</p>" \
                    "<p>" + str(flight.departureTime) + " - " + str(flight.arrivalTime) + "</p>"

            msg.html += _("<p> Current fares:")
            for fare in fares:
                msg.html += str(fare['amount']) + " " + str(fare['currencyCode']) + "</p><p>"
            msg.html += "</p>"

            mail.send(msg)
