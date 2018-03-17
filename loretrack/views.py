from .loretrack import app
from . import db, config
from flask import render_template, jsonify
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
    c_id = config.get_option('CAMPAIGN_ID')
    characters = db.get_characters(c_id)
    monsters = db.get_monsters()

    return render_template('combat.html', title='Combat', characters=characters, monsters=monsters)


@app.route('/character/<pc_id>')
def view_character(pc_id):
    c_id = config.get_option('CAMPAIGN_ID')
    character = db.get_single_character(c_id, pc_id)
    return jsonify(character.to_dict())

@app.errorhandler(404)
def page_not_found(e):
    return "Error."
