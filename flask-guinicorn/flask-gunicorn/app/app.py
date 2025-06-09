from flask import Flask, jsonify, request
import time

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({
        'message': 'Hello from Flask with Gunicorn!',
        'status': 'success'
    })

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({
        'received_data': data,
        'status': 'success'
    })

@app.route('/api/params', methods=['GET'])
def get_params():
    # Get query parameters
    name = request.args.get('name', 'World')
    age = request.args.get('age', '0')
    
    return jsonify({
        'name': name,
        'age': age,
        'status': 'success'
    })

# New async endpoints without async/await
@app.route('/api/async/hello', methods=['GET'])
def async_hello():
    # Simulate some operation
    time.sleep(1)
    return jsonify({
        'message': 'Hello from async Flask with Gunicorn!',
        'status': 'success'
    })

@app.route('/api/async/delayed', methods=['GET'])
def async_delayed():
    delay = int(request.args.get('delay', '2'))
    start_time = time.time()
    
    # Simulate multiple operations
    time.sleep(delay)
    time.sleep(1)  # Additional operation
    
    end_time = time.time()
    return jsonify({
        'message': f'Async operation completed after {delay} seconds',
        'total_time': round(end_time - start_time, 2),
        'status': 'success'
    })

@app.route('/api/async/parallel', methods=['GET'])
def async_parallel():
    def mock_task(delay):
        time.sleep(delay)
        return f'Task completed in {delay} seconds'

    # Run multiple tasks sequentially (simulate parallel)
    results = [
        mock_task(1),
        mock_task(2),
        mock_task(3)
    ]
    
    return jsonify({
        'results': results,
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)