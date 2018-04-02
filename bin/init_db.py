#!/usr/bin/env python3


import uuid
import json
import os
from loretrack import model
from datetime import datetime
from loretrack.const import NAME_STR


PLAYER_STR = 'player'
RACE_STR = 'race'
CLASSES_STR = 'classes'
STR_SCORE = 'str'
DEX_SCORE = 'dex'
CON_SCORE = 'con'
INT_SCORE = 'int'
WIS_SCORE = 'wis'
CHA_SCORE = 'cha'

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = os.path.join(FILE_PATH, '../data/')
MONSTERS_FILE = os.path.join(DATA_FOLDER, 'monsters_srd.json')
#MONSTERS_FILE = os.path.join(DATA_FOLDER, 'monsters_srd_full.json')
DATA_FILE = os.path.join(DATA_FOLDER, 'data.json')


def get_tables():
    return [model.Campaign(), model.Character(), model.Monster(), model.Encounter()]


def create_tables():
    for table in get_tables():
        table.create_table()
        print('Table "{}" created.'.format(table.Meta.table_name))


def delete_tables():
    for table in get_tables():
        if table.exists():
            table.delete_table()
            print('Table "{}" deleted.'.format(table.Meta.table_name))


def remove_empty_values(data):
    if isinstance(data, list):
        for item in data:
            remove_empty_values(item)
    elif isinstance(data, dict):
        copy = dict(data)
        for key, value in copy.items():
            if not value:
                data.pop(key, None)
            else:
                remove_empty_values(value)


def add_monsters(time):
    with open(MONSTERS_FILE, 'r') as f:
        data = json.load(f)

    total = len(data)

    for index, monster in enumerate(data):
        details = monster.get('Type', None)
        size = details.split(',')[0].split(' ')[0]
        type = ' '.join(''.join(details.split(',')[0:-1]).split(' ')[1:]).capitalize()
        alignment = details.split(',')[-1].strip().capitalize()
        speed = ', '.join(monster.get('Speed', None))

        damage_vulnerabilities = '{}.'.format(', '.join(monster.get('DamageVulnerabilities', None)).capitalize())
        damage_resistances = '{}.'.format(', '.join(monster.get('DamageResistances', None)).replace(', and', ' and').capitalize())
        damage_immunities = '{}.'.format(', '.join(monster.get('DamageImmunities', None)).replace(', and', ' and').capitalize())
        condition_immunities = '{}.'.format(', '.join(monster.get('ConditionImmunities', None)).capitalize())
        senses = ', '.join(monster.get('Senses', None)).capitalize()
        languages = '{}.'.format(', '.join(monster.get('Languages', None)).capitalize()).replace('..', '.')

        if len(damage_vulnerabilities) <= 1:
            damage_vulnerabilities = None

        if len(damage_resistances) <= 1:
            damage_resistances = None

        if len(damage_immunities) <= 1:
            damage_immunities = None

        if len(condition_immunities) <= 1:
            condition_immunities = None

        if len(senses) <= 1:
            senses = None

        if len(languages) <= 1:
            languages = None

        #PynamoDB doesn't like empty fields.
        remove_empty_values(monster)

        monster_item = model.Monster(
            #m_id=str(uuid.uuid4()),
            m_id='a3b596b7-0c45-43ea-bdcd-b374d2ee7b0{}'.format(index),
            name=monster['Name'],
            size=size,
            source=monster.get('Source', None),
            type=type,
            alignment=alignment,
            ac=monster.get('AC', None),
            hp=monster.get('HP', None),
            speed=speed,
            abilities=monster.get('Abilities', None),
            saves=monster.get('Saves', None),
            skills=monster.get('Skills', None),
            damage_vulnerabilities=damage_vulnerabilities,
            damage_resistances=damage_resistances,
            damage_immunities=damage_immunities,
            condition_immunities=condition_immunities,
            senses=senses,
            languages=languages,
            challenge_rating=monster.get('Challenge', None),
            special_abilities=monster.get('Traits', None),
            actions=monster.get('Actions', None),
            reactions=monster.get('Reactions', None),
            legendary_actions=monster.get('LegendaryActions', None),
            update_time=time,
            create_time=time
        )
        print('Adding monster {} out of {}'.format(index + 1, total))
        monster_item.save()

    print('Added monsters to the DB.')


def add_data():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    time = datetime.utcnow()

    for campaign in data[model.Campaign().Meta.table_name]:
        campaign_item = model.Campaign(
            c_id=campaign['c_id'],
            name=campaign[NAME_STR],
            create_time=time
        )
        campaign_item.save()
        print('Added campaign "{}" to the DB.'.format(campaign[NAME_STR]))

    print()

    add_monsters(time)

    print()

    for character in data[model.Character().Meta.table_name]:
        for stat in [STR_SCORE, DEX_SCORE, CON_SCORE, INT_SCORE, WIS_SCORE, CHA_SCORE]:
            if stat not in character['stats']:
                character['stats'][stat] = None

        character_item = model.Character(
            pc_id=character['pc_id'],
            c_id=character['c_id'],
            name=character[NAME_STR],
            player=character[PLAYER_STR],
            race=character[RACE_STR],
            _class=character[CLASSES_STR],
            str=model.Ability(character['stats'][STR_SCORE]),
            dex=model.Ability(character['stats'][DEX_SCORE]),
            con=model.Ability(character['stats'][CON_SCORE]),
            int=model.Ability(character['stats'][INT_SCORE]),
            wis=model.Ability(character['stats'][WIS_SCORE]),
            cha=model.Ability(character['stats'][CHA_SCORE]),
            update_time=time,
            create_time=time
        )
        character_item.save()
        print('Added char "{}" to the DB.'.format(character[NAME_STR]))


def main():
    delete_tables()
    print('\n{}\n'.format('*' * 50))
    create_tables()
    print('\n{}\n'.format('*' * 50))
    add_data()


if __name__ == "__main__":
    main()
