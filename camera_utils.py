import subprocess
import os
import time
import cv2
import shutil
from app_utils import calculate_mb_left, choose_save_directory, clear_terminal

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
        output = subprocess.check_output(['gphoto2', '--auto-detect']).decode().split('\n')[2:-1]
        if output:
            return output[0].split()[1]
        else:
            return None
    except subprocess.CalledProcessError:
        return None
  
def get_camera_info(): # Get the camera information
    """
    Gets information about the connected camera using the 'gphoto2 --summary' command.
    Returns the camera information if successful, otherwise returns None.
    """
    try:
        output = subprocess.check_output(['gphoto2', '--summary']).decode()
        return output
    except subprocess.CalledProcessError:
        return None

def show_camera_info(camera): # Show the camera information
    """
    Displays the information of the connected camera.
    """
    try:
        print("\033[92mModel:", camera["model"], "\033[0m")
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
        print("\033[92mSerial Number:", camera["serial_number"], "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")

    try:
        print("\033[92mFirmware Version:", camera["firmware_version"], "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")

    try:
        print("\033[92mBattery Level:", camera["battery_level"], "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")

    try:
        print("\033[92mStorage Capacity:", camera["storage_capacity"], "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")

    try:
        print("\033[92mRemaining Storage:", camera["remaining_storage"], "\033[0m")
    except KeyError as e:
        print("\033[91mError: Missing key", e, "in camera info.\033[0m")

def get_camera_abilities():
    try:
        # Run the 'gphoto2 --abilities' command
        camera_model = get_connected_camera_model()
        if camera_model:
            output = subprocess.check_output(['gphoto2', '--abilities', camera_model]).decode()
        else:
            output = "No camera connected."

        # Return the output of the command
        return output
    except subprocess.CalledProcessError:
        return "An error occurred while trying to get the camera abilities."

def list_available_usb_ports(): # List the available USB ports
    """
    Lists the available USB ports.
    """
    try:
        output = subprocess.check_output(['lsusb']).decode()
        usb_ports = output.split('\n')
        return usb_ports
    except subprocess.CalledProcessError:
        print("Failed to list available USB ports.")

"""
These functions below capture and save a picture from the connected camera and then show it.
"""

def save_tethered_picture(save_path): # Save a picture from the connected camera
    """
    Captures and saves a picture from the connected camera using the 'gphoto2 --capture-image-and-download' command.
    Returns True if successful, otherwise returns False.
    """
    try:
         subprocess.check_output(['gphoto2','--capture-tethered=1','--capture-image-and-download', '--filename', save_path])
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
            if save_tethered_picture(save_path):
                print("Picture captured and saved successfully.")
            else:
                print("Failed to capture and save the picture.")
        
def show_latest_picture(save_directory, filename, camera_model): # Show the latest picture taken in window
    """
    Shows the latest taken picture continuously with the given save directory.
    It accepts all photo file types.
    
    functions used for photo capture and save:
    show_latest_picture <- capture_and_save_picture <- save_tethered_capture
    """
    index = -1    

    while True:
        # Get the list of files in the save directory
        capture_and_save_picture(save_directory, filename, camera_model) # Capture and save a picture
        
        file_list = os.listdir(save_directory)

        # Filter the file list to only include photo file types
        images = [file for file in file_list if file.endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png'))]

        # Sort the photo file list by modification time in descending order
        images.sort(key=lambda x: os.path.getmtime(os.path.join(save_directory, x)), reverse=True)

        if images:
            # Get the path of the latest photo file
            #latest_file_path = os.path.join(save_directory, images[0])
            #calculate_mb_left(save_directory)
            images.sort(key=lambda file: os.path.getmtime(os.path.join(save_directory, file))) # Sort the images by modification time

            latest_image = images[index] # Get the latest image

            frame = cv2.imread(os.path.join(save_directory, latest_image)) # Read the latest image

            # Display the frame in a window
            cv2.namedWindow("Latest Picture Viewer", cv2.WINDOW_NORMAL) # Create a named window
            cv2.setWindowProperty("Latest Picture Viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Set the window to fullscreen
            cv2.imshow("Latest Picture Viewer", frame) # Show the frame
            # Add instructions at the bottom of the window
            # instructions = "Press 'Esc' to exit, 'Left' arrow key to view previous picture, 'Right' arrow key to view next picture"
            # Check if the 'Esc' key is pressed
            key = cv2.waitKey(0)
                
            if key == 27:  # 'Esc' key
                cv2.destroyAllWindows() # Close all windows
                break
            elif key == 81:  # 'Left' arrow key
                index = max(index - 1, -len(images))
            elif key == 83:  # 'Right' arrow key
                index = min(index + 1,- 1)

            
        else:
            print("No photos found in the specified directory.")
            time.sleep(2)

def copy_captured_pictures(session_directory, destination_directory): # Copy the captured pictures
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

    # Filter the file list to only include photo files
    photo_file_list = [file for file in file_list if file.endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png'))]
    
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