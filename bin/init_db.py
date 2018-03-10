#!/usr/bin/env python3


from loretrack import model
from datetime import datetime


NAME_STR = 'name'
PLAYER_STR = 'player'
RACE_STR = 'race'
CLASSES_STR = 'classes'


def get_tables():
    return [model.Campaign(), model.Character(), model.Monster()]


def create_tables():
    for table in get_tables():
        table.create_table()
        print('Table "{}" created.'.format(table.Meta.table_name))


def delete_tables():
    for table in get_tables():
        if table.exists():
            table.delete_table()
            print('Table "{}" deleted.'.format(table.Meta.table_name))


def add_data():
    data = {
        "monster": [
            {
                "m_id": "e3b596b7-0c45-43ea-bdcd-b374d2ee7b0e",
                "name": "Vampire"
            }
        ],
        "character": [
            {
                "pc_id": "d3b596b7-0c45-43ea-bdcd-b374d2ee7b0e",
                "c_id": "c3b596b7-0c45-43ea-bdcd-b374d2ee7b0e",
                "name": "Sarmacid",
                "race": "Elf",
                "classes": {
                    'Paladin': 1
                },
                "player": "Me"
            },
            {
                "pc_id": "b3b596b7-0c45-43ea-bdcd-b374d2ee7b0e",
                "c_id": "c3b596b7-0c45-43ea-bdcd-b374d2ee7b0e",
                "name": "Arkon",
                "race": "Dragonborn",
                "classes": {
                    'Warlock': 1
                },
                "player": "Me"
            }
        ],
        "campaign": [
            {
                "c_id": "c3b596b7-0c45-43ea-bdcd-b374d2ee7b0e",
                "name": "Swords"
            }
        ]
    }
    time = datetime.utcnow()
    for campaign in data[model.Campaign().Meta.table_name]:
        campaign_item = model.Campaign(
            c_id=campaign['c_id'],
            name=campaign[NAME_STR],
            create_time=time
        )
        campaign_item.save()
        print('Added monster "{}" to the DB.'.format(campaign[NAME_STR]))

    for monster in data[model.Monster().Meta.table_name]:
        monster_item = model.Monster(
            m_id=monster['m_id'],
            name=monster[NAME_STR],
            update_time=time,
            create_time=time
        )
        monster_item.save()
        print('Added monster "{}" to the DB.'.format(monster[NAME_STR]))

    for character in data[model.Character().Meta.table_name]:
        character_item = model.Character(
            pc_id=character['pc_id'],
            c_id=character['c_id'],
            name=character[NAME_STR],
            player=character[PLAYER_STR],
            race=character[RACE_STR],
            classes=character[CLASSES_STR],
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
