from . import app
from flask import render_template
import db


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/locations')
def locations():
    locations = db.scan_table('Locations')
    print locations
    return render_template('locations.html', locations=locations)


@app.route('/location/<location_name>')
def location(location_name):
    #location = db.scan_table('Location')
    #print locations
    return render_template('location.html', location=location)


@app.errorhandler(404)
def page_not_found(e):
    return "Error."
