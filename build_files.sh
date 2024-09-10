#!/bin/bash

# Echo a message indicating the start of the build process
echo "Starting build process with Python 3.9..."

# Ensure pip is installed
echo "Ensuring pip is installed..."
python3.9 -m ensurepip --upgrade || { echo 'Failed to install pip'; exit 1; }
python3.9 -m pip install --upgrade pip || { echo 'Failed to upgrade pip'; exit 1; }

# Step 1: Install Python dependencies
echo "Installing dependencies using Python 3.9..."
python3.9 -m pip install -r requirements.txt || { echo 'Failed to install requirements'; exit 1; }

# Step 2: Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput || { echo 'Collectstatic failed'; exit 1; }

# Step 3: Apply database migrations
echo "Applying database migrations..."
python3.9 manage.py migrate || { echo 'Migrations failed'; exit 1; }

# Echo a message indicating the completion of the build process
echo "Build process completed successfully using Python 3.9!"
