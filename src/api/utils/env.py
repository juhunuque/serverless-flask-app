"""
File to capture environment variables and handle them as a variable.
"""
import os

STAGE = os.getenv('STAGE', None)
DEBUG = bool(os.getenv('DEBUG', False))
IS_OFFLINE = os.environ.get('IS_OFFLINE')
DYNAMO_CLIENTS_TABLE = os.environ.get('DYNAMO_CLIENTS_TABLE')
AWS_REGION = os.environ.get('AWS_REGION')
DYNAMO_LOCAL_URL = os.environ.get('DYNAMO_LOCAL_URL')

