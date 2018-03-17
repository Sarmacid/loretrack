from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, MapAttribute, Attribute
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
    Sorcery
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
            #print(key)
            #print(value)
            #print(type(value))

            if isinstance(value, MapAttribute):
                d[key] = value.as_dict()
            elif isinstance(value, Ability):
                d['ability'][key] = value.value
            else:
                d[key] = value
        return d

    pc_id = UnicodeAttribute(range_key=True)
    c_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    player = UnicodeAttribute()
    race = UnicodeAttribute()
    classes = MapAttribute()
    str = PickleAttribute()
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

    m_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    update_time = UTCDateTimeAttribute()
    create_time = UTCDateTimeAttribute()
