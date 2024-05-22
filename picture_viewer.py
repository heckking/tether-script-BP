# Description: This script will show the latest picture taken in a window.
import sys
from camera_utils import show_latest_picture
from app_utils import wait_for_keypress
import json
import os

print("Showing the latest picture taken...")
save_directory = sys.argv[1] # Get the save directory from the command line arguments
selected_pictures = json.loads(sys.argv[2])
selected_pictures = show_latest_picture(save_directory, selected_pictures) # Show the latest picture taken in a window
"""
print("Picture viewer output:")
print(selected_pictures) # Print the selected picture

file_names = [os.path.basename(file) for file in selected_pictures]

"""

# Save the file names to a JSON file
with open(save_directory + '/selected_pictures.json', 'w') as f:
    json.dump(selected_pictures, f)