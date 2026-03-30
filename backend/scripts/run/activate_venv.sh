#!/bin/bash
# Activation script for the Python virtual environment

echo "Activating Python virtual environment..."
VENV_PATH="$(dirname "${BASH_SOURCE[0]}")/../../venv"
source "$VENV_PATH/bin/activate"

echo "Virtual environment activated!"
echo "Python version: $($VENV_PATH/bin/python --version)"
echo "Django version: $($VENV_PATH/bin/python -c 'import django; print(django.get_version())')"

echo ""
echo "To deactivate the virtual environment, type: deactivate"
echo "To use the exact venv python, use: $VENV_PATH/bin/python"
echo "To use the exact venv pip, use: $VENV_PATH/bin/pip"
