def get_KeySchema(hash_key, range_key=None):
    keys = [
        {
            # Partition key
            'AttributeName': hash_key,
            'KeyType': 'HASH'
        }
    ]
    if range_key:
        keys.append(
            {
                # Sort key
                'AttributeName': range_key,
                'KeyType': 'RANGE'
            }
        )
    return keys


def get_AttributeDefinitions(fields):
    result = []
    for field in fields:
        result.append(
            {
                'AttributeName': field,
                'AttributeType': fields[field]
            }
        )
    return result


def string():
    return 'S'


def schema(table):
    schema = dict(vars(table))
    del schema['fields']
    return schema


class Models():
    class Locations():
        def __init__(self):
            self.TableName = 'Locations'
            self.KeySchema = get_KeySchema('location_name')
            self.fields = {
                'location_name': string(),
                'location_type': string()
            }
            self.AttributeDefinitions = get_AttributeDefinitions(self.fields)
            self.ProvisionedThroughput = {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
