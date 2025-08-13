#!/bin/bash

# Flask Gunicorn POC Startup Script

echo "Starting Flask Gunicorn POC..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the application with Gunicorn
echo "Starting application with Gunicorn..."
gunicorn -c gunicorn.conf.py app:app
