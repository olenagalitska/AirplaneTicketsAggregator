from app import mail, arangodb
from app.models import Users, Flight
from flask_mail import Message


class MailSender():

    def send_update(self, flight_id, old_price):
        saved_flights = arangodb.collection('saved_flights')
        users = saved_flights['users']

        recipients = []
        for user_id in users:
            user = Users.query.get(user_id)
            recipients.push(user.email)

        flight = Flight.query.get(flight_id)
        msg_subj = "Price for your flight has changed!"
        msg = Message(msg_subj, recipients=recipients)
        msg.html = "<p>" + flight.departure + "---->" + flight.arrival + "</p>" \
                "<p>" + flight.airline + "</p>" \
                "<p>" + flight.departureTime + " - " + flight.arrivalTime + "</p>" \
                 "<p> Old price: " + old_price + "</p>" \
                 "<p> New price: " + flight.price + "</p>"

        mail.send(msg)
