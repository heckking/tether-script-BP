#!/bin/bash

# Check if libgphoto2 is installed
if [ -x "$(command -v gphoto2)" ]; then
    # Update libgphoto2
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux-based systems
        if [ -x "$(command -v apt-get)" ]; then
            # Update libgphoto2 on Debian-based systems
            sudo apt-get update
            sudo apt-get upgrade -y libgphoto2-6 libgphoto2-port12 gphoto2
        elif [ -x "$(command -v yum)" ]; then
            # Update libgphoto2 on Red Hat-based systems
            sudo yum update -y libgphoto2-6 libgphoto2-port12 gphoto2
        elif [ -x "$(command -v pacman)" ]; then
            # Update libgphoto2 on Arch Linux
            sudo pacman -Syu --noconfirm libgphoto2 gphoto2
        else
            echo "Unsupported Linux distribution. Please update libgphoto2 manually."
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if [ -x "$(command -v brew)" ]; then
            # Update libgphoto2 on macOS
            brew update
            brew upgrade gphoto2
        else
            echo "Homebrew not found. Please update libgphoto2 manually."
        fi
    else
        echo "Unsupported operating system. Please update libgphoto2 manually."
    fi
else
    # Rest of the script
    echo "libgphoto2 is not installed. Continuing with the rest of the script..."
    # Add your code here
fi

# Exit the script
exit