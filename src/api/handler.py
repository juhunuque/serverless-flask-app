# Only required for deploying
# try:
#   import unzip_requirements
# except ImportError:
#   pass

import logging
import traceback
import sys

from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

from src.api import domain_service
from src.api.utils import env

from src.api.utils.custom_exceptions import CustomError, CustomAPIError, CustomRequestError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

auth = HTTPBasicAuth()
app = Flask(__name__)
domain_service.initialize_database(env.IS_OFFLINE)


@app.route("/")
def index():
    logger.info('--- index triggered ---')
    return success_response({
        'message': 'Service is waiting'
    })


@app.route('/user/register', methods=['POST'])
def register_user():
    logger.info('--- register_user triggered ---')
    request_data = request.get_json()
    user = domain_service.register_user(request_data)
    return success_response({
        'message': 'User was registered!',
        'user': user
    })


@app.route('/user/retrievePin', methods=['GET'])
@auth.login_required
def retrieve_pin():
    logger.info('--- retrieve_pin triggered ---')
    username = request.authorization["username"]
    pin = domain_service.retrieve_pin(username)
    return success_response({
        'pin': pin
    })


@app.route('/user/changePassword', methods=['PUT'])
def change_password():
    logger.info('--- change_password triggered ---')
    request_data = request.get_json()
    result = domain_service.change_password(request_data)
    return success_response({
        'message': 'Password changed successfully.',
        'user': result
    })


@auth.verify_password
def verify_password(username, password):
    return domain_service.verify_user(username, password)


"""
    Response utils
"""


def __general_response(data=None, success=False):
    return {
        'success': success,
        'data': data
    }


def success_response(data):
    return jsonify(__general_response(data, True)), 200


"""
    Error interceptors
"""


@app.errorhandler(CustomAPIError)
@app.errorhandler(CustomRequestError)
def handler_error(error):
    message = [str(x) for x in error.args]
    response = __general_response()
    response.update({
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    })

    return jsonify(response), error.status_code


@app.errorhandler(CustomError)
@app.errorhandler(Exception)
def handle_unexpected_error(error):
    traceback.print_exc(file=sys.stdout)
    response = __general_response()
    response.update({
        'error': {
            'type': 'UnexpectedException',
            'message': 'An unexpected error has occurred.'
        }
    })

    return jsonify(response), 500


if __name__ == "__main__":
    app.run(debug=env.DEBUG)
