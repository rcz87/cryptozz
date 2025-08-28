import os
import time
from collections import defaultdict, deque
from functools import wraps

from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# Rate limiting storage
rate_limit_storage = defaultdict(lambda: deque())
API_KEYS = {
    os.environ.get('INTERNAL_API_KEY', 'default-key-12345'): 'internal',
    'gpts-api-key': 'gpts',
    'telegram-api-key': 'telegram'
}

# Security middleware
def rate_limit(max_requests=100, per_seconds=60):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            current_time = time.time()
            
            # Clean old requests
            client_requests = rate_limit_storage[client_ip]
            while client_requests and client_requests[0] < current_time - per_seconds:
                client_requests.popleft()
            
            # Check rate limit
            if len(client_requests) >= max_requests:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {max_requests} requests per {per_seconds} seconds'
                }), 429
            
            # Add current request
            client_requests.append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_api_key(f):
    """API key authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for API key in headers
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'message': 'Please provide X-API-Key header or api_key parameter'
            }), 401
        
        if api_key not in API_KEYS:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 403
        
        # Store user type in request context
        g.api_key_type = API_KEYS[api_key]
        
        return f(*args, **kwargs)
    return decorated_function

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # needed for url_for to generate with https

# Add security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    
    db.create_all()
    
# Import routes after app is created
import routes  # noqa: F401