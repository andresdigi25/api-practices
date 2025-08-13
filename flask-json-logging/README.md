# Flask JSON Logging Examples

This repository contains multiple Flask applications demonstrating different approaches to JSON logging implementation. Each application showcases various logging libraries and techniques for structured logging in Flask applications.

## 📁 Project Structure

```
flask-json-logging/
├── app.py          # Basic json-logging library implementation
├── app2.py         # Alternative json-logging setup
├── app3.py         # Custom JSON formatter with comprehensive API
├── app4.py         # ichain_logger v2 implementation
├── app5.py         # ichain_logger v1 implementation
├── venv/           # Virtual environment (ignored by git)
└── README.md       # This file
```

## 🚀 Applications Overview

### 1. `app.py` - Basic JSON Logging
**Port:** 8000  
**Library:** `json-logging`

A simple Flask application demonstrating basic JSON logging with the `json-logging` library.

**Features:**
- JSON-formatted logs
- Request instrumentation
- Correlation ID tracking
- Exception logging
- URL pattern exclusion

**Endpoints:**
- `GET /` - Home page with correlation ID
- `GET /exception` - Test exception logging
- `GET /exclude_from_request_instrumentation` - Excluded from request logging

**Usage:**
```bash
python app.py
```

### 2. `app2.py` - Alternative JSON Logging Setup
**Port:** 8001  
**Library:** `json-logging`

Similar to `app.py` but with a different initialization order and simplified structure.

**Features:**
- JSON-formatted logs
- Request instrumentation
- Correlation ID tracking

**Endpoints:**
- `GET /` - Home page with correlation ID

**Usage:**
```bash
python app2.py
```

### 3. `app3.py` - Custom JSON Formatter with Full API
**Port:** 8001  
**Library:** Custom JSON formatter

A comprehensive Flask API with custom JSON logging implementation and full CRUD operations.

**Features:**
- Custom JSON log formatter
- Request/response logging middleware
- Error handling with logging
- Full CRUD API for users and posts
- Request timing and correlation tracking
- Structured logging with metadata

**Endpoints:**
- `GET /` - API documentation
- `GET /health` - Health check
- `GET /users` - List all users
- `GET /users/<id>` - Get user by ID
- `POST /users` - Create new user
- `PUT /users/<id>` - Update user
- `DELETE /users/<id>` - Delete user
- `GET /posts` - List all posts
- `GET /posts/<id>` - Get post by ID
- `POST /posts` - Create new post
- `GET /stats` - Get API statistics
- `POST /echo` - Echo endpoint
- `GET /error-test` - Test error logging

**Usage:**
```bash
python app3.py
```

### 4. `app4.py` - iChain Logger v2
**Port:** 8001  
**Library:** `ichain_logger.logger_v2`

Flask application using the iChain logger v2 for structured logging.

**Features:**
- iChain logger v2 implementation
- Correlation ID management
- Request metadata logging

**Endpoints:**
- `GET /` - Home page with logging examples

**Usage:**
```bash
python app4.py
```

### 5. `app5.py` - iChain Logger v1
**Port:** 8001  
**Library:** `ichain_logger.logger`

Flask application using the iChain logger v1 for structured logging.

**Features:**
- iChain logger v1 implementation
- Request metadata logging

**Endpoints:**
- `GET /` - Home page with logging examples

**Usage:**
```bash
python app5.py
```

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.7+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd flask-json-logging
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install flask json-logging ichain-logger
   ```

## 📊 Logging Examples

### JSON Logging Library (`app.py`, `app2.py`)
```python
import json_logging

# Initialize JSON logging
json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)

# Log with extra properties
logger.info("test log statement with extra props", 
           extra={'props': {"extra_property": 'extra_value'}})
```

### Custom JSON Formatter (`app3.py`)
```python
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            # ... additional fields
        }
        return json.dumps(log_entry)
```

### iChain Logger (`app4.py`, `app5.py`)
```python
from ichain_logger.logger_v2 import logger

logger.info('API_CALL', extra={
    'request': {
        'method': 'home',
        'url': 'localhost'
    }
})
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV` - Set to `development` for debug mode
- `PORT` - Override default port (8000/8001)

### Logging Configuration
Each application can be configured with different log levels:
- `DEBUG` - Detailed debug information
- `INFO` - General information messages
- `WARNING` - Warning messages
- `ERROR` - Error messages

## 🧪 Testing

### Test the Applications

1. **Start an application:**
   ```bash
   python app3.py
   ```

2. **Test endpoints:**
   ```bash
   # Health check
   curl http://localhost:8001/health
   
   # Get users
   curl http://localhost:8001/users
   
   # Create user
   curl -X POST http://localhost:8001/users \
        -H "Content-Type: application/json" \
        -d '{"name": "Test User", "email": "test@example.com"}'
   ```

3. **Check logs:**
   The applications will output structured JSON logs to stdout.

## 📝 Log Output Examples

### JSON Logging Library Output
```json
{
  "timestamp": "2024-01-01T12:00:00.000Z",
  "level": "INFO",
  "message": "test log statement",
  "correlation_id": "abc123",
  "extra_property": "extra_value"
}
```

### Custom Formatter Output
```json
{
  "timestamp": "2024-01-01T12:00:00.000Z",
  "level": "INFO",
  "logger": "__main__",
  "message": "Request started: GET /users",
  "module": "app3",
  "function": "log_request",
  "line": 65,
  "request_id": "req-123",
  "endpoint": "get_users",
  "method": "GET",
  "status_code": 200,
  "response_time": 0.045
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Dependencies

- **Flask** - Web framework
- **json-logging** - JSON logging library
- **ichain-logger** - iChain logging library
- **Werkzeug** - WSGI utilities (Flask dependency)

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [JSON Logging Library](https://github.com/bobbui/json-logging-python)
- [Python Logging](https://docs.python.org/3/library/logging.html)
