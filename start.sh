#!/bin/bash

echo "🚀 Starting Job Aggregator..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "📦 Installing dependencies..."
cd backend
pip3 install -r requirements.txt --break-system-packages --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your internet connection."
    exit 1
fi

echo "✅ Dependencies installed!"
echo ""

# Create data directory if it doesn't exist
mkdir -p ../data

echo "🌐 Starting backend server on http://localhost:8000"
echo "📱 Open frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 main.py
