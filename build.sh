#!/bin/bash

# Build script for Netlify deployment
echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
npm install --legacy-peer-deps

# Build the application
echo "Building application..."
npm run build

echo "Build completed successfully!"
echo "Build output is in dist/public/"