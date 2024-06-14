# Description: This script will show the latest picture taken in a window.
import sys
from camera_utils import show_latest_picture
import json

"""
this function is called by the main program to show the latest picture taken.
It will show the latest picture taken in a window.
it will return the selected pictures and dump them to a JSON file.
"""
print("Showing the latest picture taken...")
save_directory = sys.argv[1] # Get the save directory from the command line arguments
selected_pictures = sys.argv[2]
if isinstance(selected_pictures, str) or selected_pictures is None:
    selected_pictures = json.loads(selected_pictures)
    
selected_pictures = show_latest_picture(save_directory, selected_pictures) # Show the latest picture taken in a window

if selected_pictures == 0:
    selected_pictures = None

# Save the file names to a JSON file
with open(save_directory + '/selected_pictures.json', 'w') as f:
    json.dump(selected_pictures, f)
    
    
