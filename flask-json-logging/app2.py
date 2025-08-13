import logging
import sys
from flask import Flask
import json_logging

app = Flask(__name__)
# init the logger as usual
logger = logging.getLogger("test logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app, exclude_url_patterns=[r'/exclude_from_request_instrumentation'])



@app.route('/')
def home():
    logger.info("test log statement")
    logger.info("test log statement with extra props", extra={'props': {"extra_property": 'extra_value'}})
    logger.info("test log statement with custom correlation id",
                extra={'props': {'correlation_id': 'custom_correlation_id'}})

    correlation_id = json_logging.get_correlation_id()
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(8001), use_reloader=False)