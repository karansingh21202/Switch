#!/bin/bash

# Upgrade essential build tools
pip install --upgrade pip setuptools wheel

# Manually install problematic packages
pip install Pillow==9.3.0 platformdirs==3.9.1 pkginfo==1.10.0

# Install all other dependencies
pip install -r requirements.txt

# Continue with frontend setup...
npm install
npm run build
mkdir -p static
cp -r dist/* static/
uvicorn main:app --host 0.0.0.0 --port 7000
