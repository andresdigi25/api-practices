import json
import logging
import time
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

# Configure JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add request-specific information if available
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'endpoint'):
            log_entry['endpoint'] = record.endpoint
        if hasattr(record, 'method'):
            log_entry['method'] = record.method
        if hasattr(record, 'status_code'):
            log_entry['status_code'] = record.status_code
        if hasattr(record, 'response_time'):
            log_entry['response_time'] = record.response_time
            
        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)

# Sample data store
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 25},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "age": 35}
]

posts = [
    {"id": 1, "title": "First Post", "content": "Hello World!", "author_id": 1},
    {"id": 2, "title": "Second Post", "content": "Another post", "author_id": 2}
]

# Request logging middleware
@app.before_request
def log_request():
    request.start_time = time.time()
    logger.info(
        f"Request started: {request.method} {request.path}",
        extra={
            'request_id': request.headers.get('X-Request-ID', 'unknown'),
            'endpoint': request.endpoint,
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'unknown')
        }
    )

@app.after_request
def log_response(response):
    if hasattr(request, 'start_time'):
        response_time = time.time() - request.start_time
        logger.info(
            f"Request completed: {request.method} {request.path} - {response.status_code}",
            extra={
                'request_id': request.headers.get('X-Request-ID', 'unknown'),
                'endpoint': request.endpoint,
                'method': request.method,
                'status_code': response.status_code,
                'response_time': round(response_time, 3)
            }
        )
    return response

# Error handler
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(
        f"Unhandled exception: {str(e)}",
        extra={
            'request_id': request.headers.get('X-Request-ID', 'unknown'),
            'endpoint': request.endpoint,
            'method': request.method,
            'exception_type': type(e).__name__,
            'exception_message': str(e)
        }
    )
    
    if isinstance(e, HTTPException):
        return jsonify({
            'error': e.description,
            'status_code': e.code
        }), e.code
    
    return jsonify({
        'error': 'Internal Server Error',
        'status_code': 500
    }), 500

@app.route('/')
def index():
    logger.info("Homepage accessed")
    return jsonify({
        'message': 'Welcome to Flask Gunicorn POC API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'users': '/users',
            'user_by_id': '/users/<id>',
            'posts': '/posts',
            'post_by_id': '/posts/<id>',
            'stats': '/stats',
            'echo': '/echo'
        }
    })

@app.route('/health')
def health_check():
    logger.info("Health check requested")
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'flask-gunicorn-poc'
    })

@app.route('/users', methods=['GET'])
def get_users():
    logger.info(f"Retrieved {len(users)} users")
    return jsonify({
        'users': users,
        'count': len(users)
    })

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        logger.info(f"Retrieved user with ID: {user_id}")
        return jsonify(user)
    else:
        logger.warning(f"User not found with ID: {user_id}")
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        logger.warning("Invalid user data provided")
        return jsonify({'error': 'Name and email are required'}), 400
    
    new_id = max(u['id'] for u in users) + 1 if users else 1
    new_user = {
        'id': new_id,
        'name': data['name'],
        'email': data['email'],
        'age': data.get('age', None)
    }
    users.append(new_user)
    
    logger.info(f"Created new user with ID: {new_id}")
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        logger.warning(f"User not found for update with ID: {user_id}")
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if data:
        user.update(data)
        logger.info(f"Updated user with ID: {user_id}")
        return jsonify(user)
    
    logger.warning("No data provided for user update")
    return jsonify({'error': 'No data provided'}), 400

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        logger.warning(f"User not found for deletion with ID: {user_id}")
        return jsonify({'error': 'User not found'}), 404
    
    users.remove(user)
    logger.info(f"Deleted user with ID: {user_id}")
    return jsonify({'message': 'User deleted successfully'})

@app.route('/posts', methods=['GET'])
def get_posts():
    logger.info(f"Retrieved {len(posts)} posts")
    return jsonify({
        'posts': posts,
        'count': len(posts)
    })

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        logger.info(f"Retrieved post with ID: {post_id}")
        return jsonify(post)
    else:
        logger.warning(f"Post not found with ID: {post_id}")
        return jsonify({'error': 'Post not found'}), 404

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        logger.warning("Invalid post data provided")
        return jsonify({'error': 'Title and content are required'}), 400
    
    new_id = max(p['id'] for p in posts) + 1 if posts else 1
    new_post = {
        'id': new_id,
        'title': data['title'],
        'content': data['content'],
        'author_id': data.get('author_id', None)
    }
    posts.append(new_post)
    
    logger.info(f"Created new post with ID: {new_id}")
    return jsonify(new_post), 201

@app.route('/stats')
def get_stats():
    logger.info("Statistics requested")
    return jsonify({
        'total_users': len(users),
        'total_posts': len(posts),
        'timestamp': datetime.utcnow().isoformat(),
        'uptime': 'running'
    })

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    logger.info("Echo endpoint called", extra={'echo_data': data})
    return jsonify({
        'message': 'Echo response',
        'received_data': data,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/error-test')
def error_test():
    logger.error("This is a test error")
    raise ValueError("This is a test error for logging purposes")

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True, host='0.0.0.0', port=5000)

