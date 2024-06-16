#!/bin/bash

# Change the working directory to the directory of the script
cd "$(dirname "$0")"

# Update the package manager and install Python 3 if it is not already installed
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    apt-get update
    apt-get install -y python3
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew update
    brew install python3
else
    echo "Unsupported operating system."
    exit
fi

# Create a virtual environment if it doesn't already exist
if [ ! -d "python_env" ]; then
    python3 -m venv python_env
fi

# Activate the virtual environment
source "$(dirname "$0")/python_env/bin/activate"

# Install the required Python packages if they are not already installed
if ! python3 -m pip show -r libraries.txt &> /dev/null; then
    python3 -m pip install -r libraries.txt
fi
# Run the program with sudo
sudo python3 main.py

# Deactivate the virtual environment
deactivate

# Exit the script
exit