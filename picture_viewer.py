# Description: This script will show the latest picture taken in a window.
import sys
from camera_utils import show_latest_picture

print("Showing the latest picture taken...")
save_directory = sys.argv[1] # Get the save directory from the command line arguments
selected_pictures = show_latest_picture(save_directory) # Show the latest picture taken in a window
print(selected_pictures) # Print the selected picture