from flask import Flask, request, jsonify
import logging
from datetime import datetime
from functools import wraps

class APIMiddleware:
    @staticmethod
    def log_requests():
        def middleware():
            timestamp = datetime.now().isoformat()
            logging.info(f"[{timestamp}] {request.method} {request.path}")
        return middleware
    
    @staticmethod
    def auth_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            token = auth_header.replace('Bearer ', '')
            
            if token != 'valid-token':
                return jsonify({'error': 'Unauthorized'}), 401
            return f(*args, **kwargs)
        return decorated

# Инициализация приложения
app = Flask(__name__)
middleware = APIMiddleware()

app.before_request(middleware.log_requests())

@app.route('/')
def home():
    return jsonify(message="Welcome to the API!")

@app.route('/secure')
@middleware.auth_required
def secure():
    return jsonify(message="Secure data accessed!")

if __name__ == '__main__':
    app.run(debug=True, port=3000)