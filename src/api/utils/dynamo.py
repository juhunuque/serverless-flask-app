"""
Some utils to interact with the database agnostically.
This class is intended to be implemented for an application service.
Do not include business logic here!
"""
import boto3
import logging
import json
import decimal
from src.api.utils import env
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import datetime


def __init():
    """
    Returns the dynamoDBSession created.
    :return: dynamoDBSession - dynamoResource
    """
    if env.IS_OFFLINE:
        dynamo_session = boto3.resource(
            'dynamodb',
            region_name='localhost',
            endpoint_url=env.DYNAMO_LOCAL_URL
        )
    else:
        dynamo_session = boto3.resource('dynamodb')

    return dynamo_session


def read_table_item(table_name, pk_name, pk_value):
    """
      Retrieves an item of a table using its primary key.
      :param table_name: Table Name
      :param pk_name: PrimaryKey
      :param pk_value: PrimaryKeyValue
      :return: response - item
    """
    dynamo_session = __init()
    table = dynamo_session.Table(table_name)
    response = table.get_item(Key={pk_name: pk_value})

    return response


def add_item(table_name, item):
    """
    Adds an item to a specific table.
    :param table_name: Table Name
    :param item: Dictionary {col:value}
    :return: response - item
    """
    dynamo_session = __init()
    table = dynamo_session.Table(table_name)
    response = table.put_item(Item=item)

    return response


def delete_item(table_name, pk_name, pk_value):
    """
    Deletes an item of the table using its primaryKey
    :param table_name: Table Name
    :param pk_name: primaryKey
    :param pk_value: primaryKeyValue
    :return: response - item
    """
    dynamo_session = __init()
    table = dynamo_session.Table(table_name)
    response = table.delete_item(Key={pk_name: pk_value})

    return response


def scan_table(table_name, filter_key=None, filter_value=None):
    """
    Perform a scan on the specify table, data can also be filter using
    a filter_key (col name) and its value.
    :param table_name: Table Name
    :param filter_key: column name
    :param filter_value: column value
    :return: response - item
    """
    dynamo_session = __init()
    table = dynamo_session.Table(table_name)
    ttl_filter = Key('ttl').gt(int(datetime.datetime.now().timestamp()))

    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp & ttl_filter)
    else:
        response = table.scan()
    return response


def query_table(table_name, filter_key=None, filter_value=None, index_name=None):
    """
    Perform a query on the specify table,data can also be filter using
     a filter_key (col name) and its value.
     :param table_name: Table Name
     :param filter_key: column name
     :param filter_value: column value
     :return: response - item
    """
    dynamo_session = __init()
    table = dynamo_session.Table(table_name)

    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        if index_name:
            response = table.query(IndexName=index_name,
                                   KeyConditionExpression=filtering_exp)
        else:
            response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()

    return response


def create_table(table_name, key_schema, attribute_definitions, provisioned_throughput):
    """
     Creates a table using the data received by parameter
     :param table_name: Table Name
     :param key_schema: Schema Definition
     :param attribute_definitions: Attribute definitions
     :param provisioned_throughput: Provisioned Throughput
     :return: table - Table Object
    """

    client = __init()
    dynamo_existing_tables = [table.name for table in client.tables.all()]

    if table_name not in dynamo_existing_tables:

        table = client.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput=provisioned_throughput
        )

    else:
        logging.info("Table %(table_name)s already exists", {table_name})
        table = client.Table(table_name)

    return table


def delete_table(table_name):
    """
         Delete a table using the data received by parameter
         :param table_name: Table Name
         :return: boolean - Result of the process
        """
    client = __init()
    try:
        dynamo_existing_tables = [table.name for table in client.tables.all()]

        if table_name in dynamo_existing_tables:
            table = client.Table(table_name)
            logging.info(f'Removing the table {table_name}.')
            table.delete()
            table.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)
            logging.info(f'Removed the table {table_name}.')
        else:
            logging.info("Table %(table_name)s already exists", {table_name})
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            logging.info(f'Table {table_name} not exists.')


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)