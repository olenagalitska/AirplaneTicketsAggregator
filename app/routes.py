from app import app
from flask import render_template

import datetime


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


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
        },
        {
            "country": "Ukraine",
            "city": "Kyiv",
            "airport": "KBP"
        }
    ]
    return render_template('search.html', airports=airports)


@app.route('/results')
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
        }
    ]
    return render_template('results.html', results=results)


@app.route('/profile/<user>')
def profile(user):
    return render_template('search.html', user=user)
