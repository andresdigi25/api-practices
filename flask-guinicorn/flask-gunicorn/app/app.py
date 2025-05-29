from flask import Flask, jsonify, request
import asyncio
import time
from asgiref.sync import async_to_sync

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

# New async endpoints using async_to_sync
@app.route('/api/async/hello', methods=['GET'])
@async_to_sync
async def async_hello():
    # Simulate some async operation
    await asyncio.sleep(1)
    return jsonify({
        'message': 'Hello from async Flask with Gunicorn!',
        'status': 'success'
    })

@app.route('/api/async/delayed', methods=['GET'])
@async_to_sync
async def async_delayed():
    delay = int(request.args.get('delay', '2'))
    start_time = time.time()
    
    # Simulate multiple async operations
    await asyncio.sleep(delay)
    await asyncio.sleep(1)  # Additional async operation
    
    end_time = time.time()
    return jsonify({
        'message': f'Async operation completed after {delay} seconds',
        'total_time': round(end_time - start_time, 2),
        'status': 'success'
    })

@app.route('/api/async/parallel', methods=['GET'])
@async_to_sync
async def async_parallel():
    async def mock_task(delay):
        await asyncio.sleep(delay)
        return f'Task completed in {delay} seconds'

    # Run multiple async tasks in parallel
    tasks = [
        mock_task(1),
        mock_task(2),
        mock_task(3)
    ]
    
    results = await asyncio.gather(*tasks)
    
    return jsonify({
        'results': results,
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 