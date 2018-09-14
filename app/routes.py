import requests
from flask import render_template, request, url_for, redirect, flash, Markup
from flask_mail import Message

from flask_login import current_user, login_user, logout_user, login_required
from markupsafe import Markup

from werkzeug.urls import url_parse

from app import app, psqldb, search_handler, arangodb, airlines_data_collection, list_of_airlines, mail, babel
from app.models import User, Flight, Airport
from app.forms import LoginForm, RegistrationForm, SearchForm
from app.dbmanager.saved_flights_manager import SavedFlightsManager
from app.dbmanager.user_activity_manager import UserActivityManager
from app.dbmanager.history_manager import HistoryManager
from app.dbmanager.airlines_manager import AirlinesManager
from app.dbmanager.destinations_stats_manager import DestinationsStatsManager
from app.dbmanager.flights_stats_manager import FlightsStatsManager
from app.search_req import SearchRequest
from app.graph_maker import GraphMaker
import subprocess
import json
import datetime

from flask_babel import _
from plotly.offline import plot
from plotly.graph_objs import Scatter, Histogram, Figure, Layout, Pie



@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['ru', 'en', 'de'])
    # return 'ru'


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
        print(current_airline_data)
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

    dest_airport = Airport.query.filter_by(code=form.get('arrival')).first()
    if dest_airport is not None:
        print(dest_airport.city)
        destination_stats_manager = DestinationsStatsManager()
        destination_stats_manager.increase_counter(dest_airport, form.get('date'))

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

    # if request.method == 'POST': ''
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
                        airline=flight_json['airline'], number=flight_json['number'])
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
        user_activity_manager = UserActivityManager()
        user_activity_manager.insert_flight(flight_check.id, current_user.id, flight_json['fares'])

        saved_flight_manager = SavedFlightsManager()
        saved_flight_manager.add_saved_flight(flight_check.id, current_user.id, flight_json['fares'])

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


# TODO: add progressbar here
@app.route('/show_results', methods=['POST', 'GET'])
def show_results():
    key = request.form["key"]
    historyManager = HistoryManager()
    document = historyManager.get_history(key)

    search_data = SearchRequest(str(document['departure']), str(document['arrival']), str(document['date']),
                                int(document['adults']), int(document['seniors']), int(document['teens']),
                                int(document['children']), int(document['infants']), True, True, True)

    results = search_handler.handle(search_data, list_of_airlines)
    return 'ok'

@app.route('/airlines_stats/<stat_year>', methods=['GET'])
def airlines_stats(stat_year):
    airlineManager = AirlinesManager()
    results = airlineManager.get_airline_stats()
    x = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    all_years = []
    for i in range(2018, datetime.datetime.now().year + 2):
        all_years.append(i)
    for result in results:
        data1 = []
        if result['year'] == int(stat_year):
            sums = []
            airlines = result['airlines']
            for i in range (0, len(result['counters'])):
                trace = Scatter(y=(result['counters'])[i], x=x, name=result['airlines'][i])
                sums.append(sum(result['counters'][i]))
                data1.append(trace)

            month_plot_div = plot(data1, output_type='div')
            print(airlines)
            print(sums)
            year_plot_div=plot([Pie(labels=airlines, values=sums)], output_type='div')

            return render_template('airlines_stats.html',
                                   stats_div=Markup(month_plot_div),
                                   whole_year_stats=Markup(year_plot_div),
                                   years=all_years, current_year=stat_year
                                   )
    return render_template('airlines_stats.html', stats_div="No data available", whole_year_stats="No data available",
                           years=all_years)

@app.route('/price_graph/<flight_id>', methods=["POST", "GET"])
def price_graph(flight_id):
    prices = FlightsStatsManager.get_all_stats_for(flight_id)
    flight = Flight.query.filter_by(id=flight_id).first()

    dates = []
    fares = []

    for price in prices:
        dates.append(price['date'])
        fares.append(price['fares'])

    # print(dates)
    print(fares)
    my_plot_div = GraphMaker.get_price_graph(dates, fares)
    return render_template('price_graph.html', prices=prices, flight=flight, div_placeholder=Markup(my_plot_div))


# ---------------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


