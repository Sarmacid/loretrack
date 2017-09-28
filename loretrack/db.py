import boto3
import config
import json
from datetime import datetime
import dateutil.parser
import uuid


DATA_FILE = config.get_option('DATA_FILE')
UPDATE_STRING = config.get_option('UPDATE_STRING')
CREATE_STRING = config.get_option('CREATE_STRING')


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


def get_client():
    dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    return dynamodb


def get_resource():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    return dynamodb


def list_tables():
    client = get_client()
    table_names = client.list_tables()['TableNames']
    return table_names


def delete_table(tablename):
    client = get_client()
    response = client.delete_table(TableName=tablename)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print 'Deleted table "' + tablename + '"'
        return True
    else:
        print 'Could not delete table "' + tablename + '"'
        return False


def delete_all_tables():
    table_names = list_tables()
    for table_name in table_names:
        delete_table(table_name)


def create_table(table_schema):
    client = get_client()
    try:
        client.create_table(
            TableName=table_schema['TableName'],
            KeySchema=table_schema['KeySchema'],
            AttributeDefinitions=table_schema['AttributeDefinitions'],
            ProvisionedThroughput=table_schema['ProvisionedThroughput']
        )
        print 'Created table "' + table_schema['TableName'] + '"'
        return True
    except client.exceptions.ResourceInUseException:
        print 'Table "' + table_schema['TableName'] + '" already exists.'
        return False


def create_all_tables():
    for table_name in schema():
        create_table(table_name)


def init_db():
    delete_all_tables()
    create_all_tables()
    load_data_from_file()


def load_data_from_file():
    path = config.join_path(config.LORETRACK_DIR, DATA_FILE)
    with open(path, 'r') as db_file:
        data = json.load(db_file)

    for table_name in data:
        print 'Inserting ' + str(len(data[table_name])) + ' records in table "' + table_name + '".'
        for record in data[table_name]:
            put_record(table_name, record)


def put_record(table_name, record):
    time = datetime.now().isoformat()
    timestamps = {
        CREATE_STRING: time,
        UPDATE_STRING: time
    }
    my_uuid = str(uuid.uuid4())
    if 'info' not in record:
        record['info'] = timestamps
        record['info']['uuid'] = my_uuid
    else:
        if CREATE_STRING not in record['info']:
            record['info'].update(timestamps)
        else:
            record['info'][UPDATE_STRING] = timestamps[UPDATE_STRING]
        if 'guid' not in record['info']:
            record['info']['uuid'] = my_uuid

    resource = get_resource()
    table = resource.Table(table_name)
    table.put_item(Item=record)


def get_record(table_name, string):
    client = get_client()
    key = schema()[0]['AttributeDefinitions'][0]
    response = client.get_item(TableName=table_name, Key={key['AttributeName']: {key['AttributeType']: string}})
    print json.dumps(response, indent=4)


def scan_table(table_name):
    client = get_client()
    response = client.scan(TableName=table_name)
    print 'Found ' + str(response['Count']) + ' records.'
    data = []
    for item in response['Items']:
        #print item
        data.append(dynamodb_to_dict(item))
    return data


def dynamodb_to_dict(item):
    item_dict = {}
    if isinstance(item, unicode):
        return item
    for key, value in item.iteritems():
        if key == 'S':
            return str(value)
        elif key == 'N':
            return int(value)
        elif key == 'M':
            value_dict = {}
            for k, v in value.iteritems():
                if k == UPDATE_STRING or k == CREATE_STRING:
                    value_dict[str(k)] = dateutil.parser.parse(dynamodb_to_dict(v))
                else:
                    value_dict[str(k)] = dynamodb_to_dict(v)
            return value_dict
        elif key == 'L':
            value_list = []
            for i in value:
                value_list.append(dynamodb_to_dict(i))
            return value_list
        elif key == 'NULL':
            if value is True:
                return None
        else:
            value = dynamodb_to_dict(value)
        item_dict[str(key)] = value
    return item_dict


def describe_table(table_name):
    client = get_client()
    response = client.describe_table(TableName=table_name)
    return response
