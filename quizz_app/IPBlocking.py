from functools import wraps
from flask import request, jsonify

BLOCKED_IPS = {'127.0.0.1'}  # Add IPs you want to block

def check_ip(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.remote_addr in BLOCKED_IPS:
            return jsonify({'error': 'blocked'}), 403  # Forbidden response
        return f(*args, **kwargs)
    return wrapper