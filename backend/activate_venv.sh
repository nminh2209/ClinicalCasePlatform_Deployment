#!/bin/bash
# Activation script for the Python virtual environment

echo "Activating Python virtual environment..."
source venv/bin/activate

echo "Virtual environment activated!"
echo "Python version: $(venv/bin/python --version)"
echo "Django version: $(venv/bin/python -c 'import django; print(django.get_version())')"

echo ""
echo "To deactivate the virtual environment, type: deactivate"
echo "To use the exact venv python, use: venv/bin/python"
echo "To use the exact venv pip, use: venv/bin/pip"

