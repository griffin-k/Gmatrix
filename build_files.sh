#!/bin/bash

# Echo a message indicating the start of the build process
echo "Starting build process with Python 3.9..."

# Step 1: Install Python dependencies
echo "Installing dependencies using Python 3.9..."
python3.9 -m pip install -r requirements.txt

# Step 2: Collect static files
echo "Collecting static files..."
python3.9 -m manage collectstatic --noinput

# Step 3: Apply database migrations
echo "Applying database migrations..."
python3.9 -m manage migrate

# Echo a message indicating the completion of the build process
echo "Build process completed successfully using Python 3.9!"
