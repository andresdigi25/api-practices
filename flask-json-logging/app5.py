from uuid import uuid4
from flask import Flask
from ichain_logger.logger import logger

app = Flask(__name__)

@app.route('/')
def home():
    logger.info("test log statement")
    logger.info("test log statement with extra props", extra={'props': {"extra_property": 'extra_value'}})
    logger.info("test log statement with custom correlation id",extra={'props': {'correlation_id': 'custom_correlation_id'}})
    logger.info('API_CALL', extra={
            'request': {
                'method': 'home',
                'url': 'localhost'
            }
        })
    
    return "Hello, World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(8001), use_reloader=False)