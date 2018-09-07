from app import app, psqldb, search_handler, arangodb, airlines_data_collection, list_of_airlines
from flask import render_template, request, url_for, redirect, flash
from app.forms import LoginForm, RegistrationForm, SearchForm
import datetime
from app.models import Users, Flight
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import subprocess
import json


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('search'))


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usr = Users.query.filter_by(username=form.username.data).first()
        print(usr)
        if usr is None or not usr.check_password(form.password.data):
            flash("Error occured. Please try again.")
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
        usr = Users(username=form.username.data, password=form.password.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data)
        try:
            psqldb.session.add(usr)
        except:
            flash("Unable to add user to db")

        try:
            psqldb.session.commit()
        except Exception as e:
            # flash("Duplicate username or email!")
            flash("Some error accured")
            print(e)
            return redirect(url_for('signup'))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/airlines')
def airlinesinfo():
    return render_template('airlines.html')


@app.route('/search', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    print('search')

    airports = [
        {
            "country": "Germany",
            "city": "Frankfurt",
            "airport": "FRA"
        },
        {
            "country": "Switzerland",
            "city": "Zurich",
            "airport": "ZRH"
        },
        {
            "country": "France",
            "city": "Paris",
            "airport": "DDG"
        },
        {
            "country": "Sweden",
            "city": "Stockholm",
            "airport": "NYO"
        },
        {
            "country": "Ireland",
            "city": "Dublin",
            "airport": "DUB"
        },
        {
            "country": "Norway",
            "city": "Oslo",
            "airport": "OSL"
        }, {
            "country": "Ukraine",
            "city": "Kyiv",
            "airport": "KBP"
        }, {
            "country": "Austria",
            "city": "Vienna",
            "airport": "VIE"
        }, {
            "country": "Germany",
            "city": "Berlin (Schonefeld)",
            "airport": "SXF"
        }
    ]
    form.departure.choices = [(airport['airport'], airport['city'] + ", " + airport['airport']) for airport in airports]
    form.arrival.choices = [(airport['airport'], airport['city'] + ", " + airport['airport']) for airport in airports]

    return render_template('search.html', airports=airports, form=form)


@app.route('/results', methods=['POST', 'GET'])
def results():
    form = request.form
    key = form.get('departure') + form.get('arrival') + form.get('date') + form.get('adults') + form.get('teens') + \
          form.get('seniors') + form.get('infants') + form.get('children')

    search = {"departure" : form.get('departure'),
              "arrival" : form.get('arrival'),
              "date" : form.get('date'),
              "adults" : int(form.get('adults')),
              "teens" : int(form.get('teens')),
              "seniors" : int(form.get('seniors')),
              "infants" : int(form.get('infants')),
              "children": int(form.get('children')),
              "airlines" : [],
              "_key" : key
              }
    if not form.get('wizzair') is None:
        search['airlines'].append('wizzair')

    if not form.get('ryanair') is None:
        search['airlines'].append('ryanair')

    if not form.get('uia') is None:
        search['airlines'].append('uia')

    print(search)
    if not current_user.is_anonymous:
        if arangodb.has_collection('history'):
            history = arangodb.collection('history')
        else:
            history = arangodb.create_collection('history')
        search_found = history.get(key)
        if search_found is None:
            history.insert(search)

        if arangodb.has_collection('user_activity'):
            user_activity = arangodb.collection('user_activity')
        else:
            user_activity = arangodb.create_collection('user_activity')

        user_document = user_activity.get(str(current_user.id))
        list_of_searches = user_document['searches']
        list_of_searches.append(key)
        user_document['searches'] = list_of_searches
        user_activity.update(user_document)

    results = search_handler.handle(search)

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
                        airline=flight_json['airline'], number=flight_json['number'])
        flight_check = Flight.query.filter_by(departureTime=flight.departureTime, arrivalTime=flight.arrivalTime,
                                              number=flight.number, airline=flight.airline).first()
        if flight_check is None:
            print("not None")
            try:
                psqldb.session.add(flight)
            except:
                flash("Unable to add user to db")
                return "fail"
            try:
                psqldb.session.commit()
                # to get generted id of just inserted
                flight_check = Flight.query.filter_by(departureTime=flight.departureTime,
                                                      arrivalTime=flight.arrivalTime,
                                                      number=flight.number, airline=flight.airline).first()
            except Exception as e:
                flash("Some error accured")
                print(e)
                return "fail"

        if arangodb.has_collection('user_activity'):
            user_activity = arangodb.collection('user_activity')
        else:
            user_activity = arangodb.create_collection('user_activity')

        if user_activity.get(str(current_user.id)) is None:
            activity = {'_key' : str(current_user.id), 'flights' : [flight_check.id], 'searches': []}
            user_activity.insert(activity)
        else:
            activity = user_activity.get(str(current_user.id))
            list_of_flights = activity['flights']
            list_of_flights.append(flight.id)
            activity['flights'] = list_of_flights
            user_activity.update(activity)

    else:
        return redirect(url_for('login'))

    return "success"



@app.route('/profile/saved', methods=['POST'])
@login_required
def saved():
    if arangodb.has_collection('user_activity'):
        user_activity = arangodb.collection('user_activity')
        user_document = user_activity.get(str(current_user.id))
        flights_ids = user_document['flights']
        list_of_flights = []
        for id in flights_ids:
            flight = Flight.query.filter_by(id=id).first()
            list_of_flights.append(flight)
    return render_template('saved.html', saved_flights=list_of_flights)


@app.route('/profile/history', methods=['POST'])
@login_required
def history():
    if arangodb.has_collection('user_activity'):
        user_activity = arangodb.collection('user_activity')
        history_flights = arangodb.collection('history')
        user_document = user_activity.get(str(current_user.id))
        search_ids = user_document['searches']
        list_of_searches = []
        for id in search_ids:
            search = history_flights.get(id)
            list_of_searches.append(search)
    return render_template('history.html', routes=list_of_searches)


@app.route('/arango')
def arango_test():
    if arangodb.has_collection('user_activity'):
        user_activity = arangodb.collection('user_activity')
    else:
        user_activity = arangodb.create_collection('user_activity')

    # Add a hash index to the collection.
    user_activity.add_hash_index(fields=['name'], unique=False)
    # Truncate the collection.
    user_activity.truncate()

    # Insert new documents into the collection.
    user_activity.insert({'name': 'jane', 'age': 19})
    user_activity.insert({'name': 'josh', 'age': 18})
    user_activity.insert({'name': 'jake', 'age': 21})

    # Execute an AQL query. This returns a result cursor.
    cursor = arangodb.aql.execute('FOR doc IN user_activity RETURN doc')

    # Iterate through the cursor to retrieve the documents.
    student_names = [document['name'] for document in cursor]

    return len(student_names)


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

        airline_news_data = airline_data['news']

        news = airline_news_data['v.' + str(airline_news_data['latest_version'])]

        print('news:')
        print(news)

        filename = 'json/' + airline + '_news.json'

        with open(filename) as data_file:
            json_data = data_file.read()

        arr = json.loads(json_data)

        print('arr:')
        print(arr)

        return render_template("news.html", news=arr, airline=airline)


@app.route('/updateairlinesnews')
def update_airlines_news():
    # for airline in airlines:
    #     filename = 'json/' + airline + '_news.json'
    #
    #     if os.path.exists(filename):
    #         os.remove(filename)

    subprocess.check_output(['scrapy', 'crawl', 'airlines_news_spider'])

    return redirect(url_for('airlinesinfo'))


@app.route('/updateairlinesinfo')
def update_airlines_info():
    subprocess.check_output(['scrapy', 'crawl', 'airlines_info_spider'])
    return redirect(url_for('airlinesinfo'))

# @app.route('/arango')
# def index():
#     arangodb.db.collection('user_activity').insert_many([
#         {'_key': 'Abby', 'age': 22},
#         {'_key': 'John', 'age': 18},
#         {'_key': 'Mary', 'age': 21}
#     ])
#
#     # Execute the query
#     cursor = arangodb.aql.execute(
#         'FOR s IN students FILTER s.age < @value RETURN s',
#         bind_vars={'value': 19}
#     )
#
#     # Iterate through the result cursor
#     # [student['_key'] for student in cursor]
#     return render_template('search.html')


# @app.route('/init_sql')
# def trypsql():
#     psqldb.create_all()
#     psqldb.session.commit()
#
#     user1 = Users('user1', 'password', 'user1@example.com', 'user1FName', 'user1LName')
#     user2 = Users('user2', 'password', 'user2@example.com', 'user2FName', 'user2LName')
#     psqldb.session.add(user1)
#     psqldb.session.add(user2)
#     psqldb.session.commit()
#     users = psqldb.session.query(Users).all()
#     return render_template('list_of_users.html', users=users)


# @app.route('/test_arangodb')
# def test_arangodb():
#     # python-arango
#     routes_stats = arangodb.collection('routes_stats')
#
#     # routes_stats.add_hash_index(fields=['route_id'], unique=True)
#     routes_stats.insert({'route_id': '2', 'data': "25:08:2018"})


# pyArango
#
# from pyArango.connection import *
#
#
# routes_stats = arangodb["routes_stats"]
#
# #  cannot find good docs, ide does not see methods of objects while working with pyArango


# ArangoPy
#
# required additional packages and some problems occurs

#
#
#
# return redirect(url_for('login'))


# @app.route('/test_update_arango')
# def test_update_arango():
#     ryanair_news = airlines_data_collection.get('ryanair')
#     updated_version = int(ryanair_news.get('updated_version'))
#     print(updated_version)
#
#     updated_version += 1
#
#     print(ryanair_news)
#
#     ryanair_news['updated_version'] = str(updated_version)
#
#     airlines_data_collection.update(ryanair_news)
#
#     return redirect(url_for('search'))
