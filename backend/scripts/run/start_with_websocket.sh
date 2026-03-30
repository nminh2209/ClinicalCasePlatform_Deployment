#!/bin/bash
cd "$(dirname "$0")/../.."
# Start Django server with Daphne (ASGI for WebSocket support)
# Make sure Redis is running: redis-server

# Navigate to the script's directory
cd "$(dirname "$0")"

echo "Starting Clinical Case Platform with WebSocket support..."
echo "Make sure Redis is running on localhost:6379"
echo

daphne -b 0.0.0.0 -p 8000 clinical_case_platform.asgi:application
