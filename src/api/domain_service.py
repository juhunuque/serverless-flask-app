"""
Inspired on Domain Driven Design. This class will contain the business logic,
calling the proper methods from the application services. This is just the software
design implemented for this service, however, it use depends on the requirements.
"""

import logging

from src.api.services import user
from src.api.utils.custom_exceptions import CustomRequestError


def initialize_database(is_offline):
    """
    For local environments, check the database is configure, if not, create the required tables.
    :param is_offline:
    :return: None
    """
    if is_offline:
        logging.info('initialize_database has started')
        user.create_table()


def register_user(payload):
    logging.info('register_user has started')

    # Check if the payload aligns with what is required
    if not user.validate_register_payload(payload):
        logging.debug('Payload: ', payload)
        raise CustomRequestError("Payload not valid, check the data and try again.")

    email = payload['email']
    # Validate if the user already exists
    user_result = user.get_user_by_email(email)
    if user_result and user_result['Count'] > 0:
        logging.debug('Payload: ', payload)
        raise CustomRequestError(f'The email is already registered: {email}')

    user_encrypted = user.encrypt_user(payload)

    return user.register_user(user_encrypted)


def verify_user(email, password):
    logging.info('verify_user has started')

    # Validate if the user exists
    user_result = user.get_user_by_email(email)
    if user_result and user_result['Count'] == 0:
        logging.info(f'The user does not exist: {email}')
        return False

    # Verify the password is correct
    password_encrypted = user_result['Items'][0]['password']

    return user.verify_password(password_encrypted, password)


def retrieve_pin(email):
    if not email:
        raise CustomRequestError(f'The email is invalid.')

    # Validate if the user exists
    user_result = user.get_user_by_email(email)
    if user_result and user_result['Count'] == 0:
        logging.info(f'The user does not exist: {email}')
        raise CustomRequestError(f'The email does not exist: {email}')

    pin_encrypted = user_result['Items'][0]['pin']
    return user.decrypt_card_pin(pin_encrypted)


def change_password(payload):
    logging.info('register_user has started')

    # Check if the payload aligns with what is required
    if not user.validate_change_password_payload(payload):
        logging.debug('Payload: ', payload)
        raise CustomRequestError("Payload not valid, check the data and try again.")

    email = payload['email']
    old_password = payload['oldPassword']
    new_password = payload['newPassword']

    # Validate if the user exists
    user_result = user.get_user_by_email(email)
    if user_result and user_result['Count'] == 0:
        logging.info(f'The user does not exist: {email}')
        raise CustomRequestError(f'The user does not exist with email: {email}')

    # Validate old password
    if not verify_user(email, old_password):
        raise CustomRequestError(f'The old password is not corrrect.')

    user_object = user_result['Items'][0]
    user_object['password'] = user.encrypt_password(new_password)

    return user.change_password(user_object)
