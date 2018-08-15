from app import app
from flask import render_template


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


@app.route('/profile/<user>')
def profile(user):
    return render_template('search.html', user=user)
