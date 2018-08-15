from app import app
from flask import render_template, request, url_for, redirect
from app.forms import LoginForm, RegistrationForm
import datetime

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('profile/<>'))
    return render_template('login.html', form=form)

@app.route('/signup')
def signup():
    form = RegistrationForm()
    return render_template('signup.html', form=form)

@app.route('/airlines')
def airlinesinfo():
    airlines = [
        {
            "name" : "Wizzair",
            "since" : "2003",
            "origin": "Hungary",
            "info" : "To represent user posts I'm using a list, where each element is a dictionary that has author and body fields. When I get to implement users and blog posts for real I'm going to try to preserve these field names as much as possible, so that all the work I'm doing to design and test the home page template using these fake objects will continue to be valid when I introduce real users and posts."
        },
        {
            "name": "Ryanair",
            "since": "2008",
            "origin" : "Sweden",
            "info": "To represent user posts I'm using a list, where each element is a dictionary that has author and body fields. When I get to implement users and blog posts for real I'm going to try to preserve these field names as much as possible, so that all the work I'm doing to design and test the home page template using these fake objects will continue to be valid when I introduce real users and posts."
        }
    ]
    return render_template('airlines.html', airlines=airlines)

@app.route('/search')
def search():
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
            "airport": "ARN"
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
        }
    ]
    return render_template('search.html', airports=airports)


@app.route('/results', methods=['POST', 'GET'])
def results():
    results = [
        {
            "airportA": "KBP",
            "airportB": "FRA",
            "airline": "Ryan Air",
            "date": datetime.datetime(2018, 9, 1, 20, 34),
            "duration": "3:00",
            "price": "43"
        },
        {
            "airportA": "KBP",
            "airportB": "FRA",
            "airline": "Ukrainian International Airlines",
            "date": datetime.datetime(2018, 9, 1, 14, 20),
            "duration": "2:30",
            "price": "70"
        },
        {
            "airportA": "KBP",
            "airportB": "FRA",
            "airline": "Wizz Air",
            "date": datetime.datetime(2018, 9, 1, 11, 15),
            "duration": "2:45",
            "price": "50"
        } ]
    if request.method == 'POST':
        return render_template('results.html', results=results)


@app.route('/profile/<user_id>')
def profile(user_id):
    user = {
        "user_id": user_id,
        "username": "tsmith",
        "firstName": "Tom",
        "lastName": "Smith",
        "birthDate": datetime.date(1985, 3, 25),
        "eMail": "tsmith@gmail.com"
    }
    return render_template('profile.html', user=user)


@app.route('/profile/<user_id>/saved', methods=['POST'])
def saved(user_id):
    user = {
        "user_id": user_id,
        "username": "tsmith",
        "firstName": "Tom",
        "lastName": "Smith",
        "birthDate": datetime.date(1985, 3, 25),
        "eMail": "tsmith@gmail.com"
    }
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


@app.route('/profile/<user_id>/history', methods=['POST'])
def history(user_id):
    user = {
        "user_id": user_id,
        "username": "tsmith",
        "firstName": "Tom",
        "lastName": "Smith",
        "birthDate": datetime.date(1985, 3, 25),
        "eMail": "tsmith@gmail.com"
    }
    routes = [
        {
            "cityA": "Kyiv",
            "cityB": "Frankfurt",
            "date": datetime.date(2018, 9, 1)
        #     this object should contain all configuration parameters to start new search
        }
    ]
    return render_template('history.html', routes=routes)