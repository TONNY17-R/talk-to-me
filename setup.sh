#!/bin/bash

# Setup script for Talk to Me project

echo "Setting up Talk to Me..."

# Create environment files if they don't exist
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "Created backend/.env"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo "Created frontend/.env"
fi

# Create SSL directory for nginx
mkdir -p ssl

# Install Python dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install Node dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "Setup complete!"
echo "Run 'docker-compose up' to start the application"
