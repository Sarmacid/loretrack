from .loretrack import app
from . import db
from flask import render_template
#import db
#import models


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/locations')
def locations():
    locations = db.scan_table('Locations')
    #print locations
    return render_template('locations.html', locations=locations)


@app.route('/location/<location_name>')
def location(location_name):
    Locations = models.Models().Locations()
    location = db.get_record(Locations, location_name)
    return render_template('location.html', location=location)


@app.route('/combat')
def combat():
    c_id = 'c3b596b7-0c45-43ea-bdcd-b374d2ee7b0e'
    characters = db.get_characters(c_id)
    return render_template('combat.html', title='Combat', characters=characters)


@app.errorhandler(404)
def page_not_found(e):
    return "Error."
