"""
A simple decorator that allows you to automatically return
an error if the user does not post the required fields.
"""
from functools import wraps
from flask import session, request, make_response
from json import loads, dumps
import inspect


def response(name, description="", code=200):
    return make_response(dumps({"status": code, "name": name, "description": description}), code)


def fields(request, response_formatter=None, error_formatter=response):
    """
    Wraps the decorated function in a super function that will
    check that the required fields are present in the request
    before calling the function and passing those fields to it.

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get JSON data from request, if not present return 400
            default_error_response = {
                "name": "Invalid JSON",
                "description": "The request body is not valid JSON",
                "code": 400,
            }
            try:
                data = loads(request.data)
            except:
                try:
                    data = request.json
                except:
                    return error_formatter(**default_error_response)
            if data == None:
                return error_formatter(**default_error_response)

            spec = inspect.getfullargspec(func)
            annotations = spec.annotations
            fields = spec.args
            args = []
            for field in fields:
                if field in data.keys():
                    actual_type = type(data[field])
                    expected_type = annotations.get(field, actual_type)
                    if actual_type != expected_type:
                        incorrect_field_type_response = {
                            "name": "Incorrect field type",
                            "description": f"Expected '{field}' to be of type {expected_type} got type {actual_type}",
                            "code": 400,
                        }
                        return error_formatter(**incorrect_field_type_response)
                    args.append(data[field])
                else:
                    missing_filed_response = {
                        "name": "Missing field",
                        "description": f"Missing field '{field}'",
                        "code": 400,
                    }
                    return error_formatter(**missing_filed_response)
            if response_formatter:
                return response_formatter(**func(*args, **kwargs))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def admin(callback=None):
    """
    Wraps the decorated function in a super function that will
    check that the user is an admin before calling the function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session.get("admin", False):
                return func(*args, **kwargs)
            else:
                if callback:
                    return callback()
                else:
                    return response(
                        "unauthorized", description="You are not an admin", code=403
                    )

        return wrapper

    return decorator
