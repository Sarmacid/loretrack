import boto3
import config
import json

DATA_FILE = 'db.json'


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
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'name',
                    'KeyType': 'RANGE'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                },
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

    resource = get_resource()

    for table_name in data:
        table = resource.Table(table_name)
        for record in data[table_name]:
            table.put_item(Item=record)


def scan_table(table_name):
    client = get_client()
    response = client.scan(TableName=table_name)
    print 'Found ' + str(response['Count']) + ' records.'
    data = []
    for item in response['Items']:
        data.append(dynamodb_to_dict(item))
    #print data
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
