#!/bin/bash

# Check if the script is being run with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo."
    exit
fi

# Update the package manager and install Python 3 if it is not already installed
apt-get update
apt-get install -y python3

# Create a virtual environment if it doesn't already exist
if [ ! -d "python_venv" ]; then
    python3 -m venv python_venv
fi

# Activate the virtual environment
source python_venv/bin/activate

# Install the required Python packages if they are not already installed
if ! python3 -m pip show -r knihovny.txt &> /dev/null; then
    python3 -m pip install -r knihovny.txt
fi
# Run the program with sudo
sudo python3 main.py

