#!/bin/bash

# Install Python 3 if it is not already installed
if ! command -v python3 &> /dev/null; then
    sudo apt-get update
    sudo apt-get install python3
fi
# Create a virtual environment if it doesn't already exist
if [ ! -d "python_venv" ]; then
    sudo python3 -m venv python_venv
fi
# Activate the virtual environment
source python_venv/bin/activate
# Install the required Python packages if they are not already installed
if ! python3 -m pip show -r knihovny.txt &> /dev/null; then
    python3 -m pip install -r knihovny.txt
fi
# Run the program with sudo
sudo python3 main.py

