import concurrent.futures
import cv2
from camera_utils import is_camera_connected, choose_save_directory, save_tethered_picture, copy_captured_pictures
from app_utils import wait_for_keypress
import subprocess
import tempfile
import json
import os

filename = 'testing'
save_directory = choose_save_directory()
if os.path.exists(save_directory + '/selected_pictures.json'):
    os.remove(save_directory + '/selected_pictures.json')

is_camera_connected()

def get_camera_model():
    try:
        result = subprocess.run(['gphoto2', '--auto-detect'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        lines = output.split('\n')
        for line in lines:
            if 'usb:' in line:
                model = line.split('usb:')[0].strip()
                return model
    except subprocess.CalledProcessError:
        return None

model = get_camera_model()
print(model)   
"""
print(get_connected_camera_model())
print(get_connected_camera_serial_number())
#print(get_camera_firmware_version())
print(get_camera_battery_level())

print(get_camera_free_space())
    
print(get_camera_abilities())
"""
wait_for_keypress()

p1 = subprocess.Popen(['python3', 'picture_viewer.py', save_directory])
#p2 = subprocess.Popen(['python3', 'tether_program.py', save_directory, filename])

p1.wait()

print("p1 is done")
# Read selected_pictures.txt and put them in the selected photos list
with open(save_directory + '/selected_pictures.json', 'r') as f:
    selected_pictures = json.load(f)
    selected_pictures = [os.path.basename(file) for file in selected_pictures]
# Print the output
print(selected_pictures)
wait_for_keypress()
print("Waiting for the processes to finish...")
session_directory = save_directory
destination_directory = choose_save_directory()
copy_captured_pictures(session_directory, destination_directory, selected_pictures)
#p2.send_signal(subprocess.signal.SIGINT)
#p2.terminate()
print("p2 is done")
# Clear the selected_pictures.json file
os.remove(save_directory + '/selected_pictures.json')

wait_for_keypress()
