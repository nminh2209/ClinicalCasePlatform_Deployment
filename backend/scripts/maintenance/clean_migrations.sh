#!/bin/bash
cd "$(dirname "$0")/../.."
# Clean Migration Reset Script
# This script resets migrations by keeping models but recreating migration history

echo "========================================"
echo "MIGRATION CLEANUP SCRIPT"
echo "========================================"
echo
echo "WARNING: This will reset migration history!"
echo "Make sure you have a backup of your database."
echo
read -p "Type 'yes' to continue: " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo
echo "Step 1: Recording current database state..."
python manage.py migrate --fake

echo
echo "Step 2: Deleting all migration files (keeping __init__.py)..."

# Delete migration files but keep __init__.py
# List of apps to clean
APPS=("accounts" "cases" "comments" "exports" "feedback" "grades" "repositories" "templates")

for app in "${APPS[@]}"; do
    if [ -d "$app/migrations" ]; then
        echo "Cleaning $app migrations..."
        # Find and delete all .py files in migrations folder, excluding __init__.py
        find "$app/migrations" -maxdepth 1 -name "*.py" ! -name "__init__.py" -delete
        
        # Remove __pycache__ if it exists
        if [ -d "$app/migrations/__pycache__" ]; then
            rm -rf "$app/migrations/__pycache__"
        fi
    fi
done

echo
echo "Step 3: Creating fresh migrations..."
python manage.py makemigrations

echo
echo "Step 4: Marking new migrations as applied (fake)..."
python manage.py migrate --fake

echo
echo "========================================"
echo "MIGRATION CLEANUP COMPLETE!"
echo "========================================"
echo
echo "All apps now have single, clean initial migrations."
echo "Database unchanged, but migration history is clean."
echo
read -p "Press any key to continue..."
