# Flask Gunicorn POC

A production-ready Flask application with comprehensive JSON logging and multiple RESTful endpoints, designed to run with Gunicorn.

## Features

- **JSON Logging**: Structured logging in JSON format for easy parsing and analysis
- **Multiple Endpoints**: RESTful API with user and post management
- **Request/Response Logging**: Automatic logging of all requests with timing and metadata
- **Error Handling**: Comprehensive error handling with detailed logging
- **Health Checks**: Built-in health check endpoint
- **Gunicorn Ready**: Optimized configuration for production deployment

## Endpoints

### Core Endpoints

- `GET /` - API information and available endpoints
- `GET /health` - Health check endpoint
- `GET /stats` - Application statistics

### User Management

- `GET /users` - Get all users
- `GET /users/<id>` - Get user by ID
- `POST /users` - Create new user
- `PUT /users/<id>` - Update user
- `DELETE /users/<id>` - Delete user

### Post Management

- `GET /posts` - Get all posts
- `GET /posts/<id>` - Get post by ID
- `POST /posts` - Create new post

### Utility Endpoints

- `POST /echo` - Echo endpoint for testing
- `GET /error-test` - Test error logging

## JSON Logging

The application uses structured JSON logging with the following fields:

- `timestamp`: ISO format timestamp
- `level`: Log level (INFO, WARNING, ERROR)
- `logger`: Logger name
- `message`: Log message
- `module`: Module name
- `function`: Function name
- `line`: Line number
- `request_id`: Request ID (if available)
- `endpoint`: Flask endpoint
- `method`: HTTP method
- `status_code`: HTTP status code
- `response_time`: Response time in seconds

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flask-gunicorn-poc
```

2. Run the startup script:
```bash
./start.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with Flask (development)
python app.py

# Run with Gunicorn (production)
gunicorn -c gunicorn.conf.py app:app
```

## Usage Examples

### Get all users
```bash
curl http://localhost:8000/users
```

### Create a new user
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "email": "alice@example.com", "age": 28}'
```

### Get user by ID
```bash
curl http://localhost:8000/users/1
```

### Create a new post
```bash
curl -X POST http://localhost:8000/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello World!", "author_id": 1}'
```

### Health check
```bash
curl http://localhost:8000/health
```

### Echo endpoint
```bash
curl -X POST http://localhost:8000/echo \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## Configuration

### Gunicorn Configuration

The `gunicorn.conf.py` file contains optimized settings for production:

- **Workers**: Automatically calculated based on CPU cores
- **Port**: 8000 (configurable)
- **Logging**: Structured access and error logs
- **Performance**: Optimized for high throughput

### Environment Variables

You can customize the application behavior with environment variables:

- `FLASK_ENV`: Set to `production` for production mode
- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

## Logging Examples

### Request Log
```json
{
  "timestamp": "2024-01-15T10:30:00.123456",
  "level": "INFO",
  "logger": "__main__",
  "message": "Request started: GET /users",
  "module": "app",
  "function": "log_request",
  "line": 75,
  "request_id": "unknown",
  "endpoint": "get_users",
  "method": "GET",
  "path": "/users",
  "remote_addr": "127.0.0.1",
  "user_agent": "curl/7.68.0"
}
```

### Response Log
```json
{
  "timestamp": "2024-01-15T10:30:00.456789",
  "level": "INFO",
  "logger": "__main__",
  "message": "Request completed: GET /users - 200",
  "module": "app",
  "function": "log_response",
  "line": 85,
  "request_id": "unknown",
  "endpoint": "get_users",
  "method": "GET",
  "status_code": 200,
  "response_time": 0.123
}
```

### Error Log
```json
{
  "timestamp": "2024-01-15T10:30:00.789012",
  "level": "ERROR",
  "logger": "__main__",
  "message": "Unhandled exception: User not found",
  "module": "app",
  "function": "handle_exception",
  "line": 95,
  "request_id": "unknown",
  "endpoint": "get_user",
  "method": "GET",
  "exception_type": "ValueError",
  "exception_message": "User not found"
}
```

## Development

### Running in Development Mode

```bash
python app.py
```

This will start the Flask development server on `http://localhost:5000`

### Running in Production Mode

```bash
gunicorn -c gunicorn.conf.py app:app
```

This will start the Gunicorn production server on `http://localhost:8000`

## Monitoring and Observability

The application provides comprehensive logging for monitoring:

1. **Request Tracking**: Every request is logged with timing and metadata
2. **Error Tracking**: All errors are logged with stack traces
3. **Performance Metrics**: Response times are automatically logged
4. **Health Monitoring**: Built-in health check endpoint

## Dependencies

- Flask 3.1.1
- Gunicorn 23.0.0
- Werkzeug 3.1.3
- Other dependencies listed in `requirements.txt`

## License

This project is open source and available under the MIT License.
