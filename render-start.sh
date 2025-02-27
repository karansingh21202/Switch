#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install

# Build the frontend
npm run build

# Move built frontend files to backend static folder
mkdir -p static
cp -r dist/* static/

# Start FastAPI backend
uvicorn main:app --host 0.0.0.0 --port 7000
