from collections import OrderedDict

class Error:
    PROGRAMMING_ERROR = OrderedDict([
        ("errno", 1),
        ("errmsg", "Programming failure")
    ])

    INVALID_USER = OrderedDict([
        ("errno", 2),
        ("errmsg", "Credentials are not valid or user is not active")
    ])

    REQUIRED_ARGUMENTS = OrderedDict([
        ("errno", 3),
        ("errmsg", "The following arguments are required: {}")
    ])

    TOKEN_GENERATION_ERROR = OrderedDict([
        ("errno", 4),
        ("errmsg", "Token generation failed, please try again or contact the administrator")
    ])

    INVALID_REQUEST_BODY = OrderedDict([
        ("errno", 5),
        ("errmsg", "The request body must be a valid JSON object")
    ])

    EXPIRED_TOKEN = OrderedDict([
        ("errno", 6),
        ("errmsg", "Token expired. Please log in again")
    ])

    INVALID_TOKEN = OrderedDict([
        ("errno", 7),
        ("errmsg", "Invalid token. Please try again")
    ])

    TOKEN_NOT_FOUND = OrderedDict([
        ("errno", 8),
        ("errmsg", "Token was not found in request headers")
    ])

    CLIENT_NOT_FOUND = OrderedDict([
        ("errno", 8),
        ("errmsg", "Client was not found. Please try again")
    ])  

    USER_CREATION_ERROR = OrderedDict([
        ("errno", 9),
        ("errmsg", "An error has occurred during user creation")
    ])