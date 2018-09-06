from app import Mail

class MailSender():

    def send_update(self, flight_id, old_price, new_price):
        msg_subj = "Hello, " + str(form.first_name.data) + "!"
        msg = Message(msg_subj, recipients=[form.email.data])
        msg.html = "<p>welcome to whatafly!</p>" \
                   "<p>we hope you'll find the best deal with our help</p>" \
                   "<img src='https://www.askideas.com/media/06/Dude-I-Am-So-High-Right-Now-Funny-Plane-Meme.jpg'>"

        mail.send(msg)
