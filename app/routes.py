from app import app
from flask import render_template
from app.forms import LoginForm, RegistrationForm

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/login')
def login():
    form = LoginForm()
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