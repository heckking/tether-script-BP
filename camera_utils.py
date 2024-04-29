import subprocess
import os
import time
import cv2
import shutil

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
        return subprocess.check_output(['gphoto2', '--list-cameras']).decode().split('\n')[1:-1]
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

def save_tethered_picture(save_path): # Save a picture from the connected camera
    """
    Captures and saves a picture from the connected camera using the 'gphoto2 --capture-image-and-download' command.
    Returns True if successful, otherwise returns False.
    """
    try:
         subprocess.check_output(['gphoto2', '--capture-image-and-download', '--filename', save_path])
         return True
    except subprocess.CalledProcessError:
         return False
     
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
                        print("Model:", camera["model"])
                        print("Serial Number:", camera["serial_number"])
                        print("Firmware Version:", camera["firmware_version"])
                        print("Battery Level:", camera["battery_level"])
                        print("Storage Capacity:", camera["storage_capacity"])
                        print("Remaining Storage:", camera["remaining_storage"])

def list_available_usb_ports(): # List the available USB ports
    """
    Lists the available USB ports.
    """
    try:
        output = subprocess.check_output(['lsusb']).decode()
        usb_ports = output.split('\n')
        for port in usb_ports:
            print(port)
    except subprocess.CalledProcessError:
        print("Failed to list available USB ports.")
        
def capture_and_save_picture(save_directory, filename): # Capture and save a picture
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
            file_extension = os.path.splitext(filename)[1]
            file_name = f"{timestamp}{file_extension}"
            save_path = os.path.join(save_directory, file_name)

            # Capture and save the picture
            if save_tethered_picture(save_path):
                print("Picture captured and saved successfully.")
            else:
                print("Failed to capture and save the picture.")
        
def show_latest_picture(save_directory, filename): # Show the latest picture taken in window
    """
    Shows the latest taken picture continuously with the given save directory.
    It accepts all photo file types.
    """
    # Get the list of files in the save directory
    file_list = os.listdir(save_directory)

    # Filter the file list to only include photo file types
    images = [file for file in file_list if file.endswith(('.nef', '.cr2', '.arw', '.jpg', '.jpeg', '.png'))]

    # Sort the photo file list by modification time in descending order
    images.sort(key=lambda x: os.path.getmtime(os.path.join(save_directory, x)), reverse=True)

    if images:
        # Get the path of the latest photo file
        
        latest_file_path = os.path.join(save_directory, images[0])

        # Create a video capture object
        #cap = cv2.VideoCapture(latest_file_path)

        while True:
            # Calculate the available disk space in MB
            available_space_mb = os.statvfs(save_directory).f_bavail * os.statvfs(save_directory).f_frsize / (1024 * 1024)

            images.sort(key=lambda file: os.path.getmtime(os.path.join(save_directory, file))) # Sort the images by modification time

            latest_image = images[-1] # Get the latest image

            frame = cv2.imread(os.path.join(save_directory, latest_image)) # Read the latest image

            # Display the frame in a window
            cv2.namedWindow("Latest Picture Viewer", cv2.WINDOW_NORMAL) # Create a named window
            cv2.setWindowProperty("Latest Picture Viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Set the window to fullscreen
            cv2.imshow("Latest Picture Viewer", frame) # Show the frame

            # Check if the 'Esc' key is pressed
            if cv2.waitKey(0):
                break

        # Release the video capture object and close the window

        cv2.destroyAllWindows()
    else:
        print("No photos found in the specified directory.")

def copy_captured_pictures(session_directory, destination_directory): # Copy the captured pictures
    """
    Copies all captured pictures in the session directory to the desired destination directory.
    """
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

    # Copy each photo file to the destination directory
    for photo_file in photo_file_list:
        source_path = os.path.join(session_directory, photo_file)
        destination_path = os.path.join(destination_directory, photo_file)
        try:
            shutil.copy2(source_path, destination_path)
            print(f"Successfully copied {photo_file} to {destination_directory}.")
        except shutil.Error as e:
            print(f"Failed to copy {photo_file}: {e}")
        except IOError as e:
            print(f"Failed to copy {photo_file}: {e}")
#TO DO list
# continuous photo viewer add some kind of exit option xxx
# add single photo viewer
# add a way to save the photos x
