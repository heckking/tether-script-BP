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
import gphoto2 as gp

"""
This module provides utility functions for interacting with cameras using the gphoto2 library.

Libraries used:
- subprocess: Provides a way to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
- os: Provides a way to interact with the operating system, such as accessing environment variables and file operations.
- time: Provides various time-related functions, such as getting the current time and delaying execution.
- cv2: OpenCV library for image processing and computer vision tasks.
- sys: Provides access to some variables used or maintained by the interpreter and to functions that interact with the interpreter.
- shutil: Provides high-level file operations, such as copying and moving files.
- re: Provides regular expression matching operations.
- numpy: Library for numerical computing with Python.
- rawpy: Library for reading RAW image files.
- gphoto2: Python bindings for the gphoto2 library, which allows communication with digital cameras.

"""

def is_camera_connected(): # Check if a camera is connected
    """
    Checks if a camera is connected by running the 'gphoto2 --auto-detect' command.
    Returns the output of the command if successful, otherwise returns False.
    """
    try:
        return subprocess.check_output(['gphoto2', '--auto-detect'])
    except subprocess.CalledProcessError:
        return False

def disconnect_camera():
    """
    Disconnects the camera by running a series of gphoto2 commands.
    """
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
    """
    Gets the serial number of the connected camera by running the 'gphoto2 --get-config serialnumber' command.

    Raises:
        Exception: If the serial number could not be found.
    Returns:
        The serial number of the connected camera if successful, otherwise returns None.
    """    
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

def show_camera_info(camera_model, serial_number, firmware_version, battery_level, remaining_storage):
    """
    Displays the information of the connected camera.

    Parameters:
    - camera_model (str): The model of the connected camera.
    - serial_number (str): The serial number of the connected camera.
    - firmware_version (str): The firmware version of the connected camera.
    - battery_level (float): The battery level of the connected camera.
    - remaining_storage (float): The remaining storage of the connected camera.

    Returns:
    None

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
    """
    Retrieves the abilities of the camera using the 'gphoto2 --abilities' command.

    Returns:
        str: The output of the 'gphoto2 --abilities' command.
        
    Raises:
        CalledProcessError: If an error occurs while trying to get the camera abilities.
    """    
    try:
        # Run the 'gphoto2 --abilities' command
        output = subprocess.check_output(['gphoto2', '--abilities']).decode()
        # Return the output of the command
        return output
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("An error occurred while trying to get the camera abilities.")

def list_available_usb_ports():
    """
    Lists the available USB ports.

    This function uses system commands to retrieve information about the available USB ports.
    On macOS, it uses the `system_profiler` command with the `SPUSBDataType` argument.
    On other platforms, it uses the `lsusb` command.
    
    Returns:
        A list of strings, where each string represents an available USB port.

    Raises:
        subprocess.CalledProcessError: If the system command fails to execute.

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

def wait_for_camera_connection():
    """
    Waits for a camera connection.

    This function continuously checks for the presence of a camera by using the `autodetect` method from the `gp.Camera` class.
    It waits until a camera is detected and then breaks out of the loop or until a timeout occurs.

    Returns:
        None
    """
    context = gp.Context()
    timer = 21 
    while True:
        cameras = gp.Camera.autodetect(context)
        if cameras:
            clear_terminal()
            print("\033[1;32mCamera connected successfully.\033[0m")
            time.sleep(2)
            return True
        else:
            clear_terminal()
            timer -= 1
            print(f"Waiting for camera connection... \n{timer} seconds remaining...")
            if timer == 0:
                clear_terminal()
                print("\033[1;31mTimeout: No camera detected.\033[0m")
                time.sleep(2)
                return False
            time.sleep(1)
"""
These functions below capture and save a picture from the connected camera and then show it.
"""
def save_tethered_picture(save_directory, filename):
    """
    function is not used in the main program
    
    Captures and saves a picture from the connected camera using the 'gphoto2 --capture-tethered' command.
    
    Args:
        save_directory (str): The directory where the picture will be saved.
        filename (str): The name of the file to be saved. If None, a default name will be used.
    
    Returns:
        bool: True if the picture was successfully captured and saved, False otherwise.
    """
    command = ['gphoto2', '--capture-tethered', '--filename', os.path.join(save_directory, f"%f.%C")]

    print("Capturing and saving a picture...")
    wait_for_keypress()
    subprocess.run(command)
    wait_for_keypress()
    subprocess.run(['gphoto2', '--capture-tethered', '--filename', os.path.join(save_directory, f"%f.%C")], shell=True)
    try:
        if filename is None:
            subprocess.run(['gphoto2', '--capture-tethered', '--filename', os.path.join(save_directory, f"%f.%C")], shell=True)
        else:
            subprocess.run(['gphoto2', '--capture-tethered', '--filename', os.path.join(save_directory, f"{filename}-%f.%C")], shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def capture_and_save_picture(save_directory, filename, camera_model):
    """
    function is not used in the main program
    
    Captures and saves a picture from the connected camera into the chosen directory.

    Args:
        save_directory (str): The directory where the picture will be saved.
        filename (str): The name of the picture file. If not provided, the camera model will be used as the filename.
        camera_model (str): The model of the connected camera.

    Returns:
        None

    Raises:
        None

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

def show_latest_picture(save_directory, selected_pictures): # Show the latest picture taken in window
    """
    This function continuously displays the latest picture taken from the specified save directory. It accepts all photo file types.
    The function starts by checking if there are any selected pictures provided. If there are, they are added to the `selected_photos` list.
    The function then enters a loop where it continuously checks for new photo files in the save directory. It filters the file list to only include photo file types and sorts them by modification time in descending order.
    If a new photo file is found, it checks if it is different from the previous newest image. If it is, it updates the `newest_image` variable and resets the index and tag_preview flags.
    The function then checks the file type of the latest image. If it is a RAW image (e.g., .nef, .cr2, .arw), it uses the `rawpy` library to extract the embedded JPEG preview. If a JPEG preview is found, it decodes the JPEG data and displays the image. Otherwise, it postprocesses the RAW data and displays the image. If there is an error reading the RAW image, it prints an error message and waits for 2 seconds before continuing to the next image.
    If the latest image is not a RAW image, it simply reads and displays the image using OpenCV.
    If the latest image is in the `selected_photos` list, it adds a green border to the image. Otherwise, it adds a black border.
    The function creates a named window called "Latest Picture Viewer" and sets it to fullscreen windowed mode. It then displays the image in the window.    
    The function listens for keyboard events. Pressing the 'Esc' key closes the window and returns the `selected_photos` list if it is not empty. Pressing the 'a' key or left arrow key moves to the previous image. Pressing the 'd' key or right arrow key moves to the next image. Pressing the 'Space' key selects or deselects the current image and updates the `selected_photos` list accordingly.
    If no photos are found in the specified directory, it prints a message and waits for 2 seconds before checking again.
    
    Args:
        save_directory (str): The directory where the pictures are saved.
        selected_pictures (list): A list of selected pictures.

    Returns:
        list or int: If the 'Esc' key is pressed, the function returns an empty list if no pictures are selected, otherwise it returns the list of selected pictures.
    
    functions used for photo capture and save:
    show_latest_picture <- capture_and_save_picture
    """
    index = 0
    latest_image = None
    newest_image = None
    prev_image = None
    selected_photos = []

    if selected_pictures is not None or selected_pictures != [] or selected_pictures != "0" or selected_pictures != "" or selected_pictures != "[]" or selected_pictures != "None":
        selected_photos.extend(selected_pictures)
        
    tag_preview = False
    file_list = os.listdir(save_directory)
    
    if not file_list:
        cv2.namedWindow("Latest Picture Viewer", cv2.WINDOW_NORMAL) # Create a named window
        cv2.setWindowProperty("Latest Picture Viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Set the window to fullscreen windowed mode
            
    while True:
        # Get the list of files in the save directory
        file_list = os.listdir(save_directory)

        # Filter the file list to only include photo file types
        images = [file for file in file_list if file.lower().endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png', '.tif', '.tiff'))]

        # Wait until there is a supported photo file in the directory
        while not images:
            time.sleep(1)
            file_list = os.listdir(save_directory)
            images = [file for file in file_list if file.lower().endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png', '.tif', '.tiff'))]

        # Sort the photo file list by modification time in descending order
        images.sort(key=lambda x: os.path.getmtime(os.path.join(save_directory, x)), reverse=True)
        if images[0] != newest_image: # Check if the newest image is different from the previous newest image
            newest_image = images[0] if images else None
            index = 0
            tag_preview = False
            
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
            key = cv2.waitKey(200) # Wait for 1 second before checking for new pictures            
            if key == 27:  # 'Esc' key
                cv2.destroyAllWindows() # Close all windows
                if selected_photos == []:
                    return 0
                else:
                    return selected_photos

            elif key == ord('a'):  # 'a' key or left arrow key
                index = max(index - 1, -len(images)) if index > 0 else index
                tag_preview = False
            elif key == ord('d'):  # 'd' key or right arrow key
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

def copy_captured_pictures(session_directory, destination_directory, selected_pictures, trf_all): # Copy the captured pictures
    """
    Copies all captured pictures in the session directory to the desired destination directory.

    This function takes the path to the session directory where the captured pictures are located,
    the path to the destination directory where the pictures will be copied,
    a list of selected pictures to be copied (if empty, all pictures will be copied),
    and a flag indicating whether to copy all pictures or only selected pictures.

    The function first checks if the session directory and the destination directory exist.
    If either directory does not exist, an error message is printed and the function returns.

    Next, the function gets the list of files in the session directory and filters the file list
    based on the selected_pictures and trf_all parameters. If trf_all is True, all photo files in
    the session directory are copied. If trf_all is False and selected_pictures is not empty, only
    the selected pictures are copied. If trf_all is False and selected_pictures is empty, an error
    message is printed and the function returns.

    After filtering the file list, the function checks if there are any photo files to be copied.
    If there are no photo files, an error message is printed and the function returns.

    Finally, the function iterates over each photo file in the filtered list and copies it to the
    destination directory. If the destination file already exists, the user is prompted to choose
    whether to overwrite, rename, or skip the file. If the file is successfully copied, a success
    message is printed. If an error occurs during the copying process, an error message is printed.

    Args:
        session_directory (str): The path to the session directory where the captured pictures are located.
        destination_directory (str): The path to the destination directory where the pictures will be copied.
        selected_pictures (list): A list of selected pictures to be copied. If empty, all pictures will be copied.
        trf_all (bool): A flag indicating whether to copy all pictures or only selected pictures.

    Returns:
        None
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

    if trf_all:
        # Copy all photo files
        photo_file_list = [file for file in file_list if file.lower().endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png', '.tif', '.tiff'))]
    else:
        if selected_pictures:
            # Copy only selected pictures
            photo_file_list = [file for file in selected_pictures if file.lower().endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png', '.tif', '.tiff'))]
        else:
            print("No selected pictures found.")
            return

    clear_terminal()

    if not photo_file_list: # Check if there are no photo files in the session directory
        print("No photo files found in the session directory.")
        return
    # Copy each photo file to the destination directory
    for photo_file in photo_file_list:
        source_path = os.path.join(session_directory, photo_file)
        destination_path = os.path.join(destination_directory, photo_file)
        try:
            if os.path.exists(destination_path):
                choice = input(f"{photo_file} already exists in {destination_directory}.\nDo you want to (r)ewrite, (n)rename, or (s)kip?: ")
                if choice.lower() == "r":
                    shutil.copy2(source_path, destination_path)
                    print(f"\nSuccessfully overwritten {photo_file} in {destination_directory}.\n")
                elif choice.lower() == "n":
                    # Generate a new filename with a number suffix
                    n = 1
                    new_filename = os.path.splitext(photo_file)[0] + "_" + str(n) + os.path.splitext(photo_file)[1]
                    new_destination_path = os.path.join(destination_directory, new_filename)
                    while os.path.exists(new_destination_path):
                        n += 1
                        new_filename = os.path.splitext(photo_file)[0] + "_" + str(n) + os.path.splitext(photo_file)[1]
                        new_destination_path = os.path.join(destination_directory, new_filename)

                    shutil.copy2(source_path, new_destination_path)
                    print(f"\nSuccessfully renamed and copied {photo_file} to {new_destination_path}.\n")
                else:
                    print(f"\nSkipping {photo_file}.\n")
            else:
                shutil.copy2(source_path, destination_path)
                print(f"\nSuccessfully copied {photo_file} to {destination_directory}.\n")
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

def copy_confirm(save_directory, destination_directory, selected_pictures): # Copy the selected pictures
    """
    Prompt the user for transfer options and perform the selected picture transfer.

    This function allows the user to choose between different transfer options and performs the selected picture transfer.
    The function uses the `copy_captured_pictures` function to copy the pictures.

    Args:
        save_directory (str): The directory where the captured pictures are saved.
        destination_directory (str): The directory where the selected pictures will be copied.
        selected_pictures (list): A list of selected pictures to be copied.

    Returns:
        int: 0 if the transfer is cancelled.
    """    
    while True: # Check if the transfer is not cancelled
        clear_terminal()
        print("1. Copy all captured pictures")
        print("2. Copy all selected pictures")
        print("3. Show list of selected pictures")
        print("4. Cancel")
        trf_all = None
        transfer_choice = input("Enter your choice (1-4): ")

        if transfer_choice == "1": # Copy all captured pictures
            print("Copying all captured pictures to the destination directory...")
            trf_all = True
            copy_captured_pictures(save_directory, destination_directory, selected_pictures, trf_all) # Copy all captured pictures to the destination directory
            print("\nPicture copy done.\n")
            break

        elif transfer_choice == "2": # Copy only selected pictures
            print("Copying selected pictures to the destination directory...")
            trf_all = False
            copy_captured_pictures(save_directory, destination_directory, selected_pictures, trf_all) # Copy selected pictures to the destination directory
            print("\nPicture copy done.\n")
            break

        elif transfer_choice == "3": # Show list of selected pictures
            print("Selected pictures:")
            if not selected_pictures:
                print("No selected pictures.")
            else:
                for picture in selected_pictures:
                    print(picture)
            wait_for_keypress()

        elif transfer_choice == "4": # Go back
            print("Picture transfer cancelled.")
            wait_for_keypress()
            return 0

        else:
            print("\033[91mInvalid choice. Please try again.\033[0m")
            time.sleep(1)  # Simulating delay before showing the menu again
#TO DO list
# continuous photo viewer add some kind of exit option xxx
# add a way that the user is warnend if the copied file already exists x
# add a way that the user is asked if he wants to overwrite the file x
# add a way that warns the user if the copied session folder memory is too much memory for the destination folder and ask they want to proceed
# add a way to save the photos x
# repair photo viewer border x