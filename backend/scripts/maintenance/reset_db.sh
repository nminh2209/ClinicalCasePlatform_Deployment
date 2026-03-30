#!/bin/bash
cd "$(dirname "$0")/../.."
# Quick Database Reset Script for Linux/Mac
# This script resets the database and repopulates it with test data

echo "========================================"
echo "Clinical Case Platform - Database Reset"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please create a virtual environment first:"
    echo "  python -m venv venv"
    echo
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run reset script
echo
echo "Running database reset script..."
echo
python reset_database.py

# Check if successful
if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "Database reset completed successfully!"
    echo "========================================"
    echo
    echo "You can now login with:"
    echo "  Admin: admin@test.com / minh1234minh"
    echo "  Instructor: instructor@test.com / testpass123"
    echo "  Student: student@test.com / testpass123"
    echo
else
    echo
    echo "========================================"
    echo "Error occurred during database reset!"
    echo "========================================"
    echo
fi
