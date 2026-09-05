from flask import redirect, session
from functools import wraps

def require_role(role):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "role" not in session or session["role"] != role:
                return "Unauthorized: You do not have permission to access this page."
            return func(*args, **kwargs)
        return wrapper
    return inner