#!/bin/bash

# Function to display a separator line
separator() {
    echo "========================================"
}

# Clear any previous jobs (optional, but good practice for background processes)
# jobs -p | xargs kill 2>/dev/null

separator
echo " Clinical Case Platform - Startup"
separator
echo ""
echo "Starting Backend and Frontend servers..."
echo ""
echo "Backend will run on: http://localhost:8000"
echo "Frontend will run on: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all servers (this might not kill background servers automatically on all setups)"
separator
echo ""

# Ensure pid dir exists and stop older instances (if our stopper exists, use it)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_DIR="$SCRIPT_DIR/.pids"
mkdir -p "$PID_DIR"

if [ -f "$SCRIPT_DIR/stop_all.sh" ]; then
    echo "Stopping any previously running servers via stop_all.sh..."
    # call via bash so the stop script doesn't need exec bit
    bash "$SCRIPT_DIR/stop_all.sh" || true
fi

# --- Start Backend ---
echo "Starting Django Backend..."
( cd "$SCRIPT_DIR/backend" && python manage.py runserver ) &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$PID_DIR/backend.pid" || true
echo "Backend PID: $BACKEND_PID"

# Wait 3 seconds for backend to start
echo "Waiting 3 seconds for backend to initialize..."
sleep 3

# --- Start Frontend ---
echo "Starting Vue Frontend..."
( cd "$SCRIPT_DIR/frontend" && npm run dev ) &
FRONTEND_PID=$!
echo "$FRONTEND_PID" > "$PID_DIR/frontend.pid" || true
echo "Frontend PID: $FRONTEND_PID"

echo ""
separator
echo " Both servers are starting..."
separator
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""

# Wait for Ctrl+C
echo "The servers are running in the background. Press [Enter] to exit this script's terminal."
echo "Note: The servers will continue to run in the background after this terminal is closed."
echo "To stop them, run: bash \"$SCRIPT_DIR/stop_all.sh\""
separator
echo ""