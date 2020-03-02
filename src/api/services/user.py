"""
Application service for user domain
"""
import logging
from schema import Schema, And, Use, SchemaError

from src.api.utils.crypt import encrypt_value, decrypt_value
from src.api.utils import dynamo
from src.api.utils import env


def validate_register_payload(payload):
    register_schema = Schema({
        'email': And(Use(str)),
        'password': And(Use(str)),
        'pin': And(Use(str))
    })
    try:
        register_schema.validate(payload)
        return True
    except SchemaError:
        logging.error(f'validate_register_payload: Payload not valid.')
        return False


def validate_change_password_payload(payload):
    change_password_schema = Schema({
        'email': And(Use(str)),
        'oldPassword': And(Use(str)),
        'newPassword': And(Use(str))
    })
    try:
        change_password_schema.validate(payload)
        return True
    except SchemaError:
        logging.error(f'validate_change_password_payload: Payload not valid.')
        return False


def encrypt_user(payload):
    password_encrypted = encrypt_value(payload['password'])
    pin_encrypted = encrypt_value(payload['pin'])

    logging.info(f'Encrypted user with email {payload["email"]}')
    return dict(
        email=payload['email'],
        password=password_encrypted,
        pin=pin_encrypted
    )


def register_user(user):
    dynamo.add_item(env.DYNAMO_CLIENTS_TABLE, user)
    logging.info(f'New user was registered with email {user["email"]}')
    return user


def get_user_by_email(email):
    logging.info(f'Querying user by email {email}')
    return dynamo.query_table(env.DYNAMO_CLIENTS_TABLE, 'email', email)


def verify_password(password_encrypted, password):
    return decrypt_value(password_encrypted) == password


def decrypt_card_pin(pin_encrypted):
    return decrypt_value(pin_encrypted)


def encrypt_password(password):
    return encrypt_value(password)


def change_password(user):
    dynamo.add_item(env.DYNAMO_CLIENTS_TABLE, user)
    logging.info(f'Password changed successfully for user with email: {user["email"]}')
    return user


def delete_table():
    return dynamo.delete_table(env.DYNAMO_CLIENTS_TABLE)


def create_table():
    key_schema = [
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    }
                ]
    attribute_definitions = [
                               {
                                   'AttributeName': 'email',
                                   'AttributeType': 'S'
                               }
                           ]
    provisioned_throughput = {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }

    return dynamo.create_table(env.DYNAMO_CLIENTS_TABLE, key_schema, attribute_definitions, provisioned_throughput)


