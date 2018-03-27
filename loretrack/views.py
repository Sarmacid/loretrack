from .loretrack import app
from . import db, config
from flask import render_template, jsonify, request, abort
from .const import NAME_STR, C_ID_STR, M_ID_STR


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/campaign/api/v1.0/get_all', methods=['GET'])
def get_all_campaigns():
    c_list = [c.attribute_values for c in db.get_all_campaigns()]
    return jsonify(c_list)


@app.route('/encounter/api/v1.0/save', methods=['POST'])
def save_encounter():
    if not request.json:
        abort(400)
    elif request.json[NAME_STR] == '':
        return jsonify({'Response': 'The encounter must have a name.'}), 404

    if db.create_encounter(request.json):
        return jsonify({'Response': 'Encounter "{}" saved.'.format(request.json[NAME_STR])}), 201
    else:
        return jsonify({'Response': 'An encounter with that name already exists.'}), 404


@app.route('/encounter/api/v1.0/get_all', methods=['POST'])
def get_all_encounters():
    """
    if not request.json or E_ID_STR not in request.json or C_ID_STR not in request.json:
        abort(400)
    """
    c_id = config.get_option('CAMPAIGN_ID')
    result = {
        'Response': 'Success',
        'Data': [c.attribute_values for c in db.get_all_encounters(c_id)]
    }

    return jsonify(result)


@app.route('/character/api/v1.0/get_all', methods=['POST'])
def get_all_characters():
    if not request.json or C_ID_STR not in request.json:
        abort(400)

    result = {
        'Response': 'Success',
        'Data': [c.to_dict() for c in db.get_all_characters(request.json[C_ID_STR])]
    }

    return jsonify(result)


@app.route('/monster/api/v1.0/get_all', methods=['GET'])
def get_all_monsters():
    # Filter out attributes to return.
    data = [{key: m.attribute_values[key] for key in [M_ID_STR, NAME_STR]} for m in db.get_all_monsters()]
    result = {
        'Response': 'Success',
        'Data': data
    }

    return jsonify(result)


@app.route('/monster/api/v1.0/get', methods=['POST'])
def get_monster():

    if not request.json:
        abort(400)
    elif request.json[M_ID_STR] == '':
        return jsonify({'Response': '"m_id" missing'}), 404

    monster = db.get_monster(request.json[M_ID_STR])

    result = {
        'Response': 'Success',
        'Data': monster.attribute_values
    }

    return jsonify(result)

    if db.create_encounter(request.json):
        return jsonify({'Response': 'Encounter "{}" saved.'.format(request.json[NAME_STR])}), 201
    else:
        return jsonify({'Response': 'An encounter with that name already exists.'}), 404


@app.route('/character/<pc_id>')
def view_character(pc_id):
    c_id = config.get_option('CAMPAIGN_ID')
    character = db.get_single_character(c_id, pc_id)
    return jsonify(character.to_dict())


@app.route('/monster/<m_id>')
def view_monster(m_id):
    monster = db.get_single_monster(m_id)
    return jsonify(monster.to_dict())


@app.errorhandler(404)
def page_not_found(e):
    return "Error."
