import subprocess
import sys
from camera_utils import save_tethered_picture


print("Taking the latest picture taken...")
save_directory = sys.argv[1] # Get the save directory from the command line arguments
filename = sys.argv[2] # Get the filename from the command line arguments

save_tethered_picture(save_directory, filename) # Save the latest picture taken to the 'pictures' directory
