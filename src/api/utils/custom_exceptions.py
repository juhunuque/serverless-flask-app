class CustomError(Exception):
    """Base Custom error."""
    status_code = 500


class CustomRequestError(CustomError):
    """Request error."""
    status_code = 400


class CustomAPIError(CustomError):
    """API error."""
    status_code = 400
