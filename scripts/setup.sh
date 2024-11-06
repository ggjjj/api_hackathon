#!/bin/bash

# Ensure script is run with root privileges for apt operations
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or use sudo."
    exit 1
fi

# Update the package list and install python3-venv if it's not installed
echo "Updating package list and installing jq and python3-venv..."
sudo apt update
sudo apt install jq
sudo apt install -y python3-venv

# Create a new virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install required Python packages
echo "Installing required Python packages..."
pip install fastapi uvicorn
pip install SQLAlchemy
pip install python-decouple
pip install psycopg2
pip install python-dotenv
pip install pytest httpx pytest-asyncio

# Confirm installation
echo "All required packages have been installed successfully!"
