from app import app
from flask import render_template

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')
