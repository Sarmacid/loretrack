from . import app
from flask import render_template
import db
import models


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
    Locations = models.Models().Locations()
    location = db.get_record(Locations, location_name)
    print location
    return render_template('location.html', location=location)


@app.errorhandler(404)
def page_not_found(e):
    return "Error."
