from flask import render_template, request, url_for, redirect, flash
from flask_mail import Message

from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse

from app import app, psqldb, search_handler, arangodb, airlines_data_collection, list_of_airlines, mail, babel
from app.models import User, Flight, Airport
from app.forms import LoginForm, RegistrationForm, SearchForm
from app.dbmanager.saved_flights_manager import SavedFlightsManager
from app.dbmanager.user_activity_manager import UserActivityManager
from app.dbmanager.history_manager import HistoryManager
from app.dbmanager.airlines_manager import AirlinesManager
from app.dbmanager.destinations_stats_manager import DestinationsStatsManager
import subprocess
import json

from flask_babel import _


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['ru', 'en', 'de'])

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('search'))


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():

        usr = User.query.filter_by(username=form.username.data).first()

        print(usr)
        if usr is None or not usr.check_password(form.password.data):
            flash(_("Error occured. Please try again."))
            return redirect(url_for('login'))
        login_user(usr)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('search')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        usr = User(username=form.username.data, password=form.password.data, first_name=form.first_name.data,
                   last_name=form.last_name.data, email=form.email.data)
        try:
            psqldb.session.add(usr)
        except:
            flash(_("Unable to add user to db"))

        try:
            psqldb.session.commit()

        except Exception as e:
            flash("_(Some error accured)")
            print(e)
            return redirect(url_for('signup'))

        msg_subj = "_(Hello), " + str(form.first_name.data) + "!"
        msg = Message(msg_subj, recipients=[form.email.data])
        msg.html = _("<p>welcome to whatafly!</p>" \
                     "<p>we hope you'll find the best deal with our help</p>" \
                     "<img src='https://www.askideas.com/media/06/Dude-I-Am-So-High-Right-Now-Funny-Plane-Meme.jpg'>")

        mail.send(msg)

        user = User.query.filter_by(username=form.username.data).first()
        userActivityManager = UserActivityManager()
        userActivityManager.init_user(user.id)

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/airlines')
def airlinesinfo():
    airlines_info = []

    for current_airline in list_of_airlines:
        current_airline_data = airlines_data_collection.get(current_airline)
        current_airline_info = current_airline_data.get('info')
        current_airline_info['airline'] = current_airline
        airlines_info.append(current_airline_info)

    return render_template('airlines.html', airlines=airlines_info)


@app.route('/search', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    print('search')

    airports = Airport.query.order_by("country").all()
    print(airports)
    form.departure.choices = [(airport.code, airport.city + " - " + airport.code + " (" + airport.country + ")") for
                              airport in airports]
    form.arrival.choices = [(airport.code, airport.city + " - " + airport.code + " (" + airport.country + ")") for
                            airport in airports]

    return render_template('search.html', airports=airports, form=form)


@app.route('/results', methods=['POST', 'GET'])
def results():
    form = request.form
    key = form.get('departure') + form.get('arrival') + form.get('date') + form.get('adults') + form.get('teens') + \
          form.get('seniors') + form.get('infants') + form.get('children')

    search = {"departure": form.get('departure'),
              "arrival": form.get('arrival'),
              "date": form.get('date'),
              "adults": int(form.get('adults')),
              "teens": int(form.get('teens')),
              "seniors": int(form.get('seniors')),
              "infants": int(form.get('infants')),
              "children": int(form.get('children')),
              "_key": key
              }

    # TODO: fix this
    airports = Airport.query.order_by("code").all()

    dest_airport_code = form.get('arrival')
    date = form.get('date')

    print(dest_airport_code)
    print(date)

    for airport in airports:
        if airport.code == dest_airport_code:
            dest_airport = airport
            break

    if dest_airport is not None:
        print(dest_airport.city)
        destination_stats_manager = DestinationsStatsManager()
        # destination_stats_manager.increase_counter(dest_airport, date)

    airlines = []
    if not form.get('wizzair') is None:
        airlines.append('wizzair')

    if not form.get('ryanair') is None:
        airlines.append('ryanair')

    if not form.get('uia') is None:
        airlines.append('uia')

    if not current_user.is_anonymous:
        historyManager = HistoryManager()
        historyManager.insert_history(key, search)

        userActivityManager = UserActivityManager()
        userActivityManager.insert_search(key, current_user.id)

    results = search_handler.handle_form(search, airlines)

    if request.method == 'POST': ''
    return render_template('results.html', results=results)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/save', methods=['POST'])
def save():
    if not current_user.is_anonymous:
        flight_json = request.form["flight_info"]
        flight_json = json.loads(flight_json)
        flight = Flight(departure=flight_json['airportA'], arrival=flight_json['airportB'],
                        departureTime=flight_json['dateDeparture'] + 'T' + flight_json['timeDeparture'],
                        arrivalTime=flight_json['dateArrival'] + 'T' + flight_json['timeArrival'],
                        airline=flight_json['airline'], number=flight_json['number'],
                        price=((flight_json['fares'])[0])['amount'])
        flight_check = Flight.query.filter_by(departureTime=flight.departureTime, arrivalTime=flight.arrivalTime,
                                              number=flight.number, airline=flight.airline).first()

        airlinesManager = AirlinesManager()
        airlinesManager.increase_count(flight_json['airline'], flight_json['dateArrival'])
        if flight_check is None:
            try:
                psqldb.session.add(flight)
            except:
                flash(_("Unable to add user to db"))
                return "fail"
            try:
                psqldb.session.commit()
                # to get generted id of just inserted
                flight_check = Flight.query.filter_by(departureTime=flight.departureTime,
                                                      arrivalTime=flight.arrivalTime,
                                                      number=flight.number, airline=flight.airline).first()
                # init saved_flights table for newly added flight
                saved_flight_manager = SavedFlightsManager()
                saved_flight_manager.init_flight(flight_check.id, current_user.id)

            except Exception as e:
                flash(_("Some error accured"))
                print(e)
                return "fail"

        # add flight id to user saved flights
        userActivityManager = UserActivityManager()
        userActivityManager.insert_flight(flight_check.id, current_user.id)

    else:
        return redirect(url_for('login'))

    return "success"


@app.route('/profile/saved', methods=['POST', 'GET'])
@login_required
def saved():
    userActivityManager = UserActivityManager()
    list_of_flights = userActivityManager.get_saved_flights(current_user.id)

    return render_template('saved.html', saved_flights=list_of_flights)


@app.route('/profile/history', methods=['POST', 'GET'])
@login_required
def history():
    userActivityManager = UserActivityManager()
    list_of_searches = userActivityManager.get_user_history(current_user.id)
    return render_template('history.html', routes=list_of_searches)


@app.route('/news/<airline>')
def news_airline(airline):
    # get airlines from DB and check if there is such airline
    # if airline in airlines

    if airline not in list_of_airlines:
        # TODO: show error page
        # pass
        return redirect(url_for('airlinesinfo'))
    else:

        airline_data = airlines_data_collection.get(airline)

        airline_news_data = airline_data['news_data']

        news = (airline_news_data['news'])['v.' + str(airline_news_data['latest_version'])]

        print('data from db:')
        print(news)
        return render_template("news.html", news=news, airline=airline)


@app.route('/updateairlinesnews')
def update_airlines_news():
    subprocess.check_output(['scrapy', 'crawl', 'airlines_news_spider'])

    return redirect(url_for('airlinesinfo'))


@app.route('/updateairlinesinfo')
def update_airlines_info():
    subprocess.check_output(['scrapy', 'crawl', 'airlines_info_spider'])
    return redirect(url_for('airlinesinfo'))


@app.route('/remove_history', methods=['POST', 'GET'])
def remove_history():
    key = request.form["key_to_remove"]
    historyManager = HistoryManager()
    historyManager.remove_history(key, current_user.id)
    return "ok"

# ---------------------------------------------------------------------------------


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

    # TODO remove from history if everyone removes ?
