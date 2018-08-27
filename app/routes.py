from app import app, db, arangodb
from flask import render_template, request, url_for, redirect, flash
from app.forms import LoginForm, RegistrationForm, SearchForm
import datetime
from app.models import Users
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import exc
from werkzeug.urls import url_parse
from app.airlines import wizzair
import subprocess
import json, os


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
        if usr is None or not usr.chech_password(form.password.data):
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
        usr = Users(username=form.username.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data, id=form.username.data)
        usr.set_password(form.password.data),
        db.session.add(usr)
        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            # flash("Duplicate username or email!")
            flash(e.code)
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
        }
    ]
    form.departure.choices = [(airport['airport'], airport['city'] + ", " + airport['airport']) for airport in airports]
    form.arrival.choices = [(airport['airport'], airport['city'] + ", " + airport['airport']) for airport in airports]

    return render_template('search.html', airports=airports, form=form)


@app.route('/results', methods=['POST', 'GET'])
def results():
    form = request.form
    wizz_robber = wizzair.WizzairInfoRobber()
    results = wizz_robber.getFlights(form.get('departure'), form.get('arrival'), form.get('date'))

    if request.method == 'POST': ''
    return render_template('results.html', results=results)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/profile/saved', methods=['POST'])
@login_required
def saved():
    flights = [
        {
            "airportA": "KBP",
            "airportB": "FRA",
            "airline": "Ryan Air",
            "date": datetime.datetime(2018, 9, 1, 20, 34),
            "duration": "3:00",
            "price": "43"
        }
    ]
    return render_template('saved.html', saved_flights=flights)


@app.route('/profile/history', methods=['POST'])
@login_required
def history():
    routes = [
        {
            "cityA": "Kyiv",
            "cityB": "Frankfurt",
            "date": datetime.date(2018, 9, 1)
            #     this object should contain all configuration parameters to start new search
        }
    ]
    return render_template('history.html', routes=routes)


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
    filename = 'json/' + airline + '_news.json'

    with open(filename) as data_file:
        json_data = data_file.read()

    arr = json.loads(json_data)

    return render_template("news.html", news=arr)


@app.route('/updatenews')
def update_news():
    airlines = [
        'wizzair',
        'uia',
        'ryanair'
    ]

    for airline in airlines:
        filename = 'json/' + airline + '_news.json'

        os.remove(filename)

        subprocess.check_output(['scrapy', 'crawl', airline + '_news', '-o', filename])

    return render_template('airlines.html')
