import logging
import traceback
import sys

from flask import Flask, request, jsonify

from src.api.utils import env

from src.api.utils.custom_exceptions import CustomError, CustomAPIError, CustomRequestError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)


@app.route("/")
def index():
    logger.info('--- index triggered ---')
    return success_response({
        'message': 'Service is waiting'
    })

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
