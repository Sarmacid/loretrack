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


def get_AttributeDefinitions(fields, keys):
    result = []
    for field in fields:
        if field in keys:
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
            self.AttributeDefinitions = get_AttributeDefinitions(self.fields, self.get_keys())
            self.ProvisionedThroughput = {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }

        def get_keys(self):
            return get_keys_(self)

    class Characters():
        def __init__(self):
            self.TableName = 'Characters'
            self.KeySchema = get_KeySchema('character_name')
            self.fields = {
                'character_name': string(),
                'race': string()
            }
            self.AttributeDefinitions = get_AttributeDefinitions(self.fields, self.get_keys())
            self.ProvisionedThroughput = {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }

        def get_keys(self):
            return get_keys_(self)

    class Location_Types():
        def __init__(self):
            self.TableName = 'Location_Types'
            self.KeySchema = get_KeySchema('location_type')
            self.fields = {
                'location_type': string()
            }
            self.AttributeDefinitions = get_AttributeDefinitions(self.fields, self.get_keys())
            self.ProvisionedThroughput = {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }

        def get_keys(self):
            return get_keys_(self)


def get_keys_(obj):
    keys = []
    for key in obj.KeySchema:
        keys.append(key['AttributeName'])
    return keys
