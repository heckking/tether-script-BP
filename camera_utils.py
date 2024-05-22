import subprocess
import os
import time
import cv2
import sys
import shutil
from app_utils import calculate_mb_left, choose_save_directory, clear_terminal, wait_for_keypress
import re
import time
import numpy as np
import rawpy
import concurrent.futures # For threading

def is_camera_connected(): # Check if a camera is connected
    """
    Checks if a camera is connected by running the 'gphoto2 --auto-detect' command.
    Returns the output of the command if successful, otherwise returns False.
    """
    try:
        return subprocess.check_output(['gphoto2', '--auto-detect'])
    except subprocess.CalledProcessError:
        return False

def disconnect_camera(): # Disconnect the camera
    print("Disconnecting camera...")
    subprocess.run(["gphoto2", "--auto-detect"])
    subprocess.run(["gphoto2", "--port", "usb:", "--camera", "usb:", "--summary"])
    subprocess.run(["gphoto2", "--port", "usb:", "--camera", "usb:", "--exit"])
    print("Camera disconnected.")

def list_available_cameras(): # List the available cameras
    """
    Lists the available cameras by running the 'gphoto2 --auto-detect' command.
    Returns a list of available cameras if successful, otherwise returns an empty list.
    """
    try:
        return subprocess.check_output(['gphoto2', '--auto-detect']).decode().split('\n')[2:-1]
    except subprocess.CalledProcessError:
        return []

def list_supported_cameras(): # List the supported cameras
    """
    Lists the supported cameras by running the 'gphoto2 --list-cameras' command.
    Returns a list of supported cameras if successful, otherwise returns an empty list.
    """
    try:
        return subprocess.check_output(['gphoto2', '--list-cameras']).decode()
    except subprocess.CalledProcessError:
        return []

def get_connected_camera_model(): # Get the model of the connected camera
    """
    Gets the model of the connected camera by running the 'gphoto2 --auto-detect' command.
    
    Returns:
        str: The model of the connected camera if successful, otherwise returns None.
    """
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
  
def get_camera_info(info): # Get the camera information
    """
    Gets information about the connected camera using the 'gphoto2 --summary' command.
    Returns the camera information if successful, otherwise returns None.
    """
    try:
        output = subprocess.check_output(['gphoto2', '--summary']).decode()
        return output
    except subprocess.CalledProcessError:
        return None

def get_connected_camera_serial_number(): # Get the serial number of the connected camera
    try:
        # Run the gphoto2 command to get the serial number
        result = subprocess.run(['gphoto2', '--get-config', 'serialnumber'], capture_output=True, text=True)

        # Parse the output to get the serial number
        lines = result.stdout.split('\n')
        for line in lines:
            if line.startswith('Current:'):
                return line.split('Current: ')[1]

        # If we didn't find the serial number, raise an exception
        raise Exception('Could not find serial number')

    except Exception as e:
        print(f'Error getting serial number: {e}')
        return None

def get_camera_firmware_version():
    """
    Gets the firmware version of the connected camera by running the 'gphoto2 --get-config firmwareversion' command.
    
    Returns:
        str: The firmware version of the connected camera if successful, otherwise returns None.
    """
    try:
        # Run the gphoto2 command to get the serial number
        result = subprocess.run(['gphoto2', '--get-config', 'deviceversion'], capture_output=True, text=True)

        # Parse the output to get the serial number
        lines = result.stdout.split('\n')
        for line in lines:
            if line.startswith('Current:'):
                return line.split('Current: ')[1]

        # If we didn't find the serial number, raise an exception
        raise Exception('Could not find firmware version')

    except Exception as e:
        print(f'Error getting firmware version: {e}')
        return None

def get_camera_battery_level():
    """
    Gets the battery level of the connected camera by running the 'gphoto2 --get-config batterylevel' command.
    
    Returns:
        str: The battery level of the connected camera if successful, otherwise returns None.
    """
    try:
        # Run the gphoto2 command to get the serial number
        result = subprocess.run(['gphoto2', '--get-config', 'batterylevel'], capture_output=True, text=True)

        # Parse the output to get the serial number
        lines = result.stdout.split('\n')
        for line in lines:
            if line.startswith('Current:'):
                return line.split('Current: ')[1]

        # If we didn't find the serial number, raise an exception
        raise Exception('Could not find battery level')

    except Exception as e:
        print(f'Error getting battery level: {e}')
        return None

def show_camera_info(camera_model, serial_number, firmware_version, battery_level, remaining_storage): # Show the camera information
    """
    Displays the information of the connected camera.
    """
    try:
        print("\033[92mModel:", camera_model, "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")

    try:
        output = subprocess.check_output(['gphoto2', '--abilities']).decode()
        if '--capture-tethered' in output:
            print("\033[92mThe connected camera supports tethered capture.\033[0m")
        else:
            print("\033[91mThe connected camera does not support tethered capture.\033[0m")
    except subprocess.CalledProcessError:
        print("\033[91m\nAn error occurred while trying to get the camera abilities.\n\033[0m")

    try:
        print("\033[92mSerial Number:", serial_number, "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")

    try:
        print("\033[92mFirmware Version:", firmware_version, "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")

    try:
        print("\033[92mBattery Level:", battery_level, "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")
        
    try:
        print("\033[92mRemaining Storage:", remaining_storage, "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")

def get_camera_free_space():
    """
    Gets the free space of the connected camera by running the 'gphoto2 --storage-info' command.
    Returns the free space in MiB or GiB if successful, otherwise returns None.
    """
    try:
        # Run the gphoto2 command to get the storage info
        result = subprocess.run(['gphoto2', '--storage-info'], capture_output=True, text=True)

        # Use a regular expression to find the free space
        match = re.search(r'free=(\d+)', result.stdout)
        if match:
            free_space_kb = int(match.group(1))
            free_space_mib = free_space_kb / 1024
            if free_space_mib >= 1024:
                free_space_gib = free_space_mib / 1024
                return f'{free_space_gib:.2f} GiB'
            else:
                return f'{free_space_mib:.2f} MiB'

        # If we didn't find the free space, raise an exception
        raise Exception('Could not find free space')

    except Exception as e:
        print(f'Error getting free space: {e}')
        return None

def get_camera_abilities():
    try:
        # Run the 'gphoto2 --abilities' command
        output = subprocess.check_output(['gphoto2', '--abilities']).decode()
        # Return the output of the command
        return output
    except subprocess.CalledProcessError:
        return "An error occurred while trying to get the camera abilities."

def list_available_usb_ports(): # List the available USB ports
    """
    Lists the available USB ports.
    """
    try:
        if sys.platform == 'darwin':
            output = subprocess.check_output(['system_profiler', 'SPUSBDataType']).decode()
        else:
            output = subprocess.check_output(['lsusb']).decode()
        usb_ports = output.split('\n')
        return usb_ports
    except subprocess.CalledProcessError:
        print("Failed to list available USB ports.")

"""
These functions below capture and save a picture from the connected camera and then show it.
"""

def save_tethered_picture(save_directory, filename): # Save a picture from the connected camera
    """
    Captures and saves a picture from the connected camera using the 'gphoto2 --capture-tethered' command.
    Returns True if successful, otherwise returns False.
    """
    try:
         subprocess.check_output(['gphoto2','--capture-tethered', '--filename', filename, '--folder', save_directory])
         return True
    except subprocess.CalledProcessError:
         return False
           
def capture_and_save_picture(save_directory, filename, camera_model): # Capture and save a picture
            """
            Captures and saves a picture from the connected camera into the chosen directory.
            """
            # Check if a camera is connected
            if not is_camera_connected():
                print("No camera connected.")
                return

            # Check if the save directory exists
            if not os.path.exists(save_directory):
                print("Save directory does not exist.")
                return

            # Check if the save directory is writable
            if not os.access(save_directory, os.W_OK):
                print("Save directory is not writable.")
                return

            # Generate a unique file name for the captured picture
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            if not filename:
                filename = camera_model
            file_extension = os.path.splitext(filename)[1]
            file_name = f"{timestamp}{file_extension}"
            save_path = os.path.join(save_directory, file_name)

            # Capture and save the picture
            if save_tethered_picture(save_path, file_name, save_directory):
                print("Picture captured and saved successfully.")
            else:
                print("Failed to capture and save the picture.")
        
def show_latest_picture(save_directory): # Show the latest picture taken in window
    """
    Shows the latest taken picture continuously with the given save directory.
    It accepts all photo file types.
    
    functions used for photo capture and save:
    show_latest_picture <- capture_and_save_picture
    """
    index = 0
    latest_image = None
    newest_image = None
    prev_image = None
    selected_photos = []
    tag_preview = False

    while True:
        # Get the list of files in the save directory
        file_list = os.listdir(save_directory)

        # Filter the file list to only include photo file types
        images = [file for file in file_list if file.lower().endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png', '.tif', '.tiff'))]

        # Sort the photo file list by modification time in descending order
        images.sort(key=lambda x: os.path.getmtime(os.path.join(save_directory, x)), reverse=True)
        if images[0] != newest_image: # Check if the newest image is different from the previous newest image
            newest_image = images[0] if images else None
            
        if images:
            # Get the path of the latest photo file
            latest_file_path = os.path.join(save_directory, images[index])
            if latest_image != latest_file_path: # Check if the latest image is different from the previous latest image
                latest_image = latest_file_path
                print("Latest image path:", latest_image)


            """
            if latest_file_path != latest_image:
                latest_image = latest_file_path
            """    
            if tag_preview:
                pass
            else:
                if latest_image.lower().endswith(('.nef', '.cr2', '.arw', '.tif', '.tiff')):                
                    try:
                        with rawpy.imread(latest_image) as raw:
                            
                            # Extract the embedded JPEG preview
                            jpeg_data = raw.extract_thumb()

                            # Check if a JPEG preview was found
                            if jpeg_data.format == rawpy.ThumbFormat.JPEG:
                                # Decode the JPEG data
                                jpeg_array = np.frombuffer(jpeg_data.data, dtype=np.uint8)
                                frame = cv2.imdecode(jpeg_array, cv2.IMREAD_COLOR)
                            else:
                                # If no JPEG preview was found, postprocess the RAW data (this will be slower)
                                rgb = raw.postprocess()
                                frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
                    except rawpy.LibRawNonFatalError:
                        print("Failed to read the RAW image.")
                        time.sleep(2)
                        if key == ord('a'):  # 'a' key
                            index = max(index - 1, 0)
                        elif key == ord('d'):  # 'd' key
                            index = min(index + 1, len(images) - 1)
                        else:
                            index = max(index, 0)
                        continue
                else:
                    frame = cv2.imread(latest_image)
                # Check if the latest image is in the selected photos list
                if latest_image in selected_photos:
                    frame = cv2.copyMakeBorder(frame, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 255, 0))  # Green border
                else:
                    frame = cv2.copyMakeBorder(frame, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))  # Black border
                    
            cv2.namedWindow("Latest Picture Viewer", cv2.WINDOW_NORMAL) # Create a named window
            cv2.setWindowProperty("Latest Picture Viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Set the window to fullscreen windowed mode
           
            if latest_image != prev_image: #check prev image
                cv2.imshow("Latest Picture Viewer", frame) # Show the frame
                prev_image = latest_image
                print("Image framed: " + latest_image)
            
            tag_preview = True
            # Check if the 'Esc' key is pressed
            key = cv2.waitKey(300) # Wait for 1 second before checking for new pictures            
            if key == 27:  # 'Esc' key
                cv2.destroyAllWindows() # Close all windows
                if selected_photos == []:
                    return 0
                else:
                    return selected_photos

            elif key == ord('a'):  # 'a' key
                index = max(index - 1, -len(images)) if index > 0 else index
                tag_preview = False
            elif key == ord('d'):  # 'd' key
                index = min(index + 1, len(images) - 1) if index < len(images) - 1 else index
                tag_preview = False
            elif key == 32:  # 'Space' key
                selected_photo = latest_image
                prev_image = None
                if selected_photo in selected_photos:
                    selected_photos.remove(selected_photo)
                    #border_applied.remove(selected_photo)
                    tag_preview = False
                else:
                    # Add the selected photo to the list
                    selected_photos.append(selected_photo)
                    #border_applied.remove(selected_photo)
                    tag_preview = False
        else:
            print("No photos found in the specified directory.")
            time.sleep(2)
def copy_captured_pictures(session_directory, destination_directory, selected_pictures): # Copy the captured pictures
    """
    Copies all captured pictures in the session directory to the desired destination directory.
    """
    num_errors = 0
    # Check if the session directory exists
    if not os.path.exists(session_directory):
        print("Session directory does not exist.")
        return

    # Check if the destination directory exists
    if not os.path.exists(destination_directory):
        print("Destination directory does not exist.")
        return

    # Get the list of files in the session directory
    file_list = os.listdir(session_directory)

    # Filter the file list based on selected_pictures
    # Ask the user if they want to copy only selected pictures or all pictures
    clear_terminal()
    print("file list:", file_list)
    print("selected_pictures: ", selected_pictures)
    copy_option = input("Do you want to copy only selected pictures? (y/n): ")

    if copy_option.lower() == "y":
        if selected_pictures:
            photo_file_list = [file for file in selected_pictures if file.lower().endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png', '.tif', '.tiff'))]
        else:
            print("No selected pictures found.")
            return
    else:
        # Filter the file list to only include photo files
        photo_file_list = [file for file in file_list if file.lower().endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png', '.tif', '.tiff'))]
    
    print(photo_file_list)
    wait_for_keypress()
    clear_terminal()
    
    if not photo_file_list: # Check if there are no photo files in the session directory
        print("No photo files found in the session directory.")
        return
    # Copy each photo file to the destination directory
    for photo_file in photo_file_list:
        source_path = os.path.join(session_directory, photo_file)
        destination_path = os.path.join(destination_directory, photo_file)
        try:
            shutil.copy2(source_path, destination_path)
            print(f"\nSuccessfully copied {photo_file} to {destination_directory}.")
        except shutil.Error as e:
            print(f"Failed to copy {photo_file}: {e}")
            num_errors += 1
        except IOError as e:
            print(f"Failed to copy {photo_file}: {e}")
            num_errors += 1
            
    if num_errors == 0:
        print("\nAll photo files copied successfully.")
    else:
        print(f"Failed to copy {num_errors} photo files.")

#TO DO list
# continuous photo viewer add some kind of exit option xxx
# add a way that the user is warnend if the copied file already exists
# add a way that the user is asked if he wants to overwrite the file
# add a way that warns the user if the copied session folder memory is too much memory for the destination folder and ask they want to proceed
# add a way to save the photos x
# repair photo viewer border x


