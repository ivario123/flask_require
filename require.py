"""
A simple decorator that allows you to automatically return
an error if the user does not post the required fields.
"""
from functools import wraps
from flask import session, request
from json import loads, dumps
import inspect


def response(name, description="", code=200):
    return dumps({
        "status": code,
        "name": name,
        "description": description
    })


def fields(request):
    """
    Wraps the decorated function in a super function that will
    check that the required fields are present in the request
    before calling the function and passing those fields to it.

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get JSON data from request, if not pressent return 400
            try:
                data = loads(request.data)
            except:
                try:
                    data = request.json
                except:
                    return response("Invalid JSON", description="The request body is not valid JSON", code=400)
            # Get the required fields from the function signature
            if data == None:
                return response("Invalid JSON", description="The request body is not valid JSON", code=400)
            fields = inspect.getfullargspec(func).args
            args = []
            for field in fields:
                if field in data.keys():
                    args.append(data[field])
                else:
                    return response("Missing field", description=f"Missing field '{field}'", code=400)

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
                    return response("unauthorized", description="You are not an admin", code=403)
        return wrapper
    return decorator
