from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, MapAttribute
)
from pynamodb.models import Model


class Campaign(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "campaign"
        host = "http://localhost:8000"

    c_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    create_time = UTCDateTimeAttribute()


class Character(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "character"
        host = "http://localhost:8000"

    pc_id = UnicodeAttribute(range_key=True)
    c_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    player = UnicodeAttribute()
    race = UnicodeAttribute()
    classes = MapAttribute()
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
