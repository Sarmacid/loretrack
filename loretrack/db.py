import boto3
#import config
import json
from datetime import datetime
import dateutil.parser
import uuid
from . import model, config


DATA_FILE = config.get_option('DATA_FILE')
#UPDATE_STRING = config.get_option('UPDATE_STRING')
#CREATE_STRING = config.get_option('CREATE_STRING')


def schema():
    schema = [
        {
            'TableName': 'Locations',
            'KeySchema': [
                {
                    'AttributeName': 'location_name',
                    'KeyType': 'HASH'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'location_name',
                    'AttributeType': 'S'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        },
        {
            'TableName': 'Location_Types',
            'KeySchema': [
                {
                    'AttributeName': 'location_type',
                    'KeyType': 'HASH'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'location_type',
                    'AttributeType': 'S'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        },
        {
            'TableName': 'Characters',
            'KeySchema': [
                {
                    'AttributeName': 'name',
                    'KeyType': 'HASH'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        }
    ]
    return schema


def load_data_from_file():
    path = config.join_path(config.LORETRACK_DIR, DATA_FILE)
    with open(path, 'r') as db_file:
        data = json.load(db_file)

    for table_name in data:
        #print 'Inserting ' + str(len(data[table_name])) + ' records in table "' + table_name + '".'
        for record in data[table_name]:
            put_record(table_name, record)


def get_characters(c_id):
    characters = model.Character().query(c_id)
    return characters
