# Description: This script will show the latest picture taken in a window.
import sys
from camera_utils import show_latest_picture
import json
import os

print("Showing the latest picture taken...")
save_directory = sys.argv[1] # Get the save directory from the command line arguments
selected_pictures = show_latest_picture(save_directory) # Show the latest picture taken in a window
print("Picture viewer output:")
print(selected_pictures) # Print the selected picture
# Extract only the file names without the full path
file_names = [os.path.basename(file) for file in selected_pictures]

# Save the file names to a JSON file
with open(save_directory + '/selected_pictures.json', 'w') as f:
    json.dump(file_names, f)