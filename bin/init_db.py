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


def add_monsters(time):
    with open(MONSTERS_FILE, 'r') as f:
        data = json.load(f)[:-1]

    total = len(data)
    fields = []

    for index, monster in enumerate(data):
        for key in monster:
            if key not in fields:
                fields.append(key)

        monster_item = model.Monster(
            #m_id=str(uuid.uuid4()),
            m_id='a3b596b7-0c45-43ea-bdcd-b374d2ee7b0{}'.format(index),
            name=monster[NAME_STR],
            size=monster.get('size', None),
            type=monster.get('type', None),
            subtype=monster.get('subtype', None),
            alignment=monster.get('alignment', None),
            ac=monster.get('armor_class', None),
            hp=monster.get('hit_points', None),
            hit_dice=monster.get('hit_dice', None),
            speed=monster.get('speed', None),
            str=monster.get('strength', None),
            dex=monster.get('dexterity', None),
            con=monster.get('constitution', None),
            int=monster.get('intelligence', None),
            wis=monster.get('wisdom', None),
            cha=monster.get('charisma', None),
            str_save=monster.get('strength_save', None),
            dex_save=monster.get('dexterity_save', None),
            con_save=monster.get('constitution_save', None),
            int_save=monster.get('intelligence_save', None),
            wis_save=monster.get('wisdom_save', None),
            cha_save=monster.get('charisma_save', None),
            acrobatics=monster.get('acrobatics', None),
            animal_handling=monster.get('animal_handling', None),
            arcana=monster.get('arcana', None),
            athletics=monster.get('athletics', None),
            deception=monster.get('deception', None),
            history=monster.get('history', None),
            insight=monster.get('insight', None),
            intimidation=monster.get('intimidation', None),
            investigation=monster.get('investigation', None),
            medicine=monster.get('medicine', None),
            nature=monster.get('nature', None),
            perception=monster.get('perception', None),
            performance=monster.get('performance', None),
            persuasion=monster.get('persuasion', None),
            religion=monster.get('religion', None),
            sleight_of_hand=monster.get('sleight_of_hand', None),
            stealth=monster.get('stealth', None),
            survival=monster.get('survival', None),
            damage_vulnerabilities=monster.get('damage_vulnerabilities', None),
            damage_resistances=monster.get('damage_resistances', None),
            damage_immunities=monster.get('damage_immunities', None),
            condition_immunities=monster.get('condition_immunities', None),
            senses=monster.get('senses', None),
            languages=monster.get('languages', None),
            challenge_rating=monster.get('challenge_rating', None),
            special_abilities=monster.get('special_abilities', None),
            actions=monster.get('actions', None),
            reactions=monster.get('reactions', None),
            legendary_actions=monster.get('legendary_actions', None),
            update_time=time,
            create_time=time
        )
        print('Adding monster {} out of {}'.format(index + 1, total))
        #print(monster_item.m_id)
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
