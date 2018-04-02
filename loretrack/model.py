from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, MapAttribute, ListAttribute
)
from pynamodb.models import Model
from math import ceil
import pickle
from pynamodb.attributes import BinaryAttribute


class Campaign(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "campaign"
        host = "http://localhost:8000"

    c_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    create_time = UTCDateTimeAttribute()


class Ability(object):
    def __init__(self, value):
        self.value = value

    def mod(self):
        return ceil((self.value - 10) / 2)


class PickleAttribute(BinaryAttribute):
    """
    Sorcery and magic.
    """
    def serialize(self, value):
        return super(PickleAttribute, self).serialize(pickle.dumps(value))

    def deserialize(self, value):
        return pickle.loads(super(PickleAttribute, self).deserialize(value))


class Character(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "character"
        host = "http://localhost:8000"

    def to_dict(self):
        d = {
            'ability': {}
        }
        for key in self.attribute_values:

            value = self.__getattribute__(key)

            # Returned key will be class instead of _class
            if key.startswith('_'):
                key = key[1:]

            if isinstance(value, MapAttribute):
                d[key] = value.as_dict()
            elif isinstance(value, Ability):
                d['ability'][key] = value.value
            else:
                d[key] = value
        return d

    c_id = UnicodeAttribute(hash_key=True)
    pc_id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    player = UnicodeAttribute()
    race = UnicodeAttribute()
    _class = MapAttribute()
    str = PickleAttribute(null=True)
    dex = PickleAttribute(null=True)
    con = PickleAttribute(null=True)
    int = PickleAttribute(null=True)
    wis = PickleAttribute(null=True)
    cha = PickleAttribute(null=True)
    update_time = UTCDateTimeAttribute()
    create_time = UTCDateTimeAttribute()


class Monster(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "monster"
        host = "http://localhost:8000"

    def to_dict(self):
        d = {}
        for key in self.attribute_values:
            value = self.__getattribute__(key)

            if isinstance(value, MapAttribute):
                d[key] = value.as_dict()
            else:
                d[key] = value
        return d

    m_id = UnicodeAttribute()
    name = UnicodeAttribute(hash_key=True)
    source = UnicodeAttribute(null=True)
    size = UnicodeAttribute(null=True)
    type = UnicodeAttribute(null=True)
    alignment = UnicodeAttribute(null=True)
    ac = MapAttribute(null=True)
    hp = MapAttribute(null=True)
    speed = UnicodeAttribute(null=True)
    abilities = MapAttribute(null=True)
    saves = ListAttribute(null=True)
    skills = ListAttribute(null=True)
    damage_vulnerabilities = UnicodeAttribute(null=True)
    damage_resistances = UnicodeAttribute(null=True)
    damage_immunities = UnicodeAttribute(null=True)
    condition_immunities = UnicodeAttribute(null=True)
    senses = UnicodeAttribute(null=True)
    languages = UnicodeAttribute(null=True)
    challenge_rating = UnicodeAttribute(null=True)
    special_abilities = ListAttribute(null=True)
    actions = ListAttribute(null=True)
    reactions = ListAttribute(null=True)
    legendary_actions = ListAttribute(null=True)
    update_time = UTCDateTimeAttribute()
    create_time = UTCDateTimeAttribute()


class Encounter(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "encounter"
        host = "http://localhost:8000"

    name = UnicodeAttribute(range_key=True)
    c_id = UnicodeAttribute(hash_key=True)
    e_id = UnicodeAttribute()
    pc_ids = ListAttribute(null=True)
    monsters = ListAttribute(null=True)
    update_time = UTCDateTimeAttribute()
    create_time = UTCDateTimeAttribute()
