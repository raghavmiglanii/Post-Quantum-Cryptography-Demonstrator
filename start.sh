#!/bin/bash

# Post-Quantum Cryptography Demo Startup Script

echo "Starting Post-Quantum Cryptography Demo..."
echo "================================================"

# Check if virtual environment exists
if [ ! -d "pqc_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv pqc_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source pqc_env/bin/activate

# Install dependencies if needed
echo "Installing dependencies..."
pip install flask psutil > /dev/null 2>&1

# Run tests first
echo "Running tests..."
python3 test_app.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Starting Flask application..."
    echo "Open your browser to: http://localhost:8080"
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    # Start the Flask application
    python3 app.py
else
    echo "Tests failed. Please check the errors above."
    exit 1
fi 