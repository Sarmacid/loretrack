import uuid
from datetime import datetime
from . import model
from .const import C_ID_STR, E_ID_STR, NAME_STR, UPDATE_TIME_STR, CREATE_TIME_STR


def get_characters(c_id):
    return model.Character().query(c_id)


def get_single_character(c_id, pc_id):
    return model.Character().get(c_id, pc_id)


def get_all_monsters():
    return model.Monster().scan()


def get_monster(m_id):
    return model.Monster().get(m_id)


def get_encounter(c_id, name):
    try:
        return model.Encounter().get(c_id, name)
    except model.Encounter.DoesNotExist:
        return False


def create_encounter(data):
    if get_encounter(data[C_ID_STR], data[NAME_STR]):
        return False

    time = datetime.utcnow()
    data[E_ID_STR] = str(uuid.uuid4())
    data[CREATE_TIME_STR] = time
    data[UPDATE_TIME_STR] = time
    encounter_item = model.Encounter(**data)
    encounter_item.save()

    return data[E_ID_STR]


def get_all_encounters(c_id):
    return model.Encounter().query(c_id)


def get_all_characters(c_id):
    return model.Character().query(c_id)


def get_all_campaigns():
    return model.Campaign().scan()
