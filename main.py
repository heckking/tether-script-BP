#!/usr/bin/env python3
from camera_utils import is_camera_connected, list_available_cameras, get_camera_info, save_tethered_picture, list_available_usb_ports, show_latest_picture, copy_captured_pictures, disconnect_camera, copy_confirm, show_camera_info, get_camera_abilities, get_connected_camera_model, get_connected_camera_serial_number, get_camera_firmware_version, get_camera_battery_level, get_camera_abilities, get_camera_free_space
from app_utils import choose_save_directory, calculate_mb_left, wait_for_keypress, clear_terminal
#import msvcrt   # Windows-specific module for keyboard input
import keyboard # Cross-platform module for keyboard input
import time # Module for time-related functions
import tkinter as tk # Cross-platform module for GUI
import subprocess # Module for running shell commands
import os # Module for interacting with the operating system
import sys # Module for system-specific parameters and functions
import json # Module for working with JSON data
"""Menu layout prototype.
    
    Menu:
Connected Camera: „Nikon D750“
Save Folder: „usr/pictures“ (None) / xx.xxMB left

	1. Start Capture
		Warning: „Save folder not setup“ -> bude se ukazovat přímo z kamery
		Warning „Low on storage“ -> bude pokud disk, kde jsou uložený je méně než 5 GB
		1.1. Setup a save folder
		1.2. Go back

	2. Save Folder settings
		2.1. Open save folder
		2.2. Choose save folder
		2.3. Filename charge („Default - přímo z kamery“)
		2.4. Go back

	3. Transfer all captured pictures in this session

	4. Camera info
		4.1. My Camera info
		4.2. All Supported Cameras
		4.3  Go Back
  
    5. Start new session
    
	6. Reconnect camera
 
	7. Disconnect camera
 
	8. Exit

    """
new_session_check = True # Set starting value of the new session check variable to True
selected_pictures = [] # Define the "selected_pictures" variable as an empty list


wait_for_keypress()

while True: # Main menu loop
    if new_session_check: # Check if a new session is started and initialize the variables
        is_camera_connected()
        clear_terminal()
        print("New session started.")
        print("\033[94mChoose a save directory.\033[0m")
        new_session_check = False
        cameras = []  # Define the "cameras" variable as an empty list

        while True:
            save_directory = choose_save_directory() # Choose the save directory
            if not save_directory:
                print("No save directory chosen. Please choose a save directory.")
            else:
                print("Save directory:", save_directory)
                break

        class ConnectedCamera:
            def __init__(self, model, serial_number, firmware_version, battery_level, remaining_storage):
                self.model = model
                self.serial_number = serial_number
                self.firmware_version = firmware_version
                self.battery_level = battery_level
                self.remaining_storage = remaining_storage

        ConnectedCamera.model = get_connected_camera_model()        
        """
        ConnectedCamera.serial_number = get_connected_camera_serial_number()
        ConnectedCamera.firmware_version = get_camera_firmware_version()
        ConnectedCamera.battery_level = get_camera_battery_level()
        ConnectedCamera.remaining_storage = get_camera_free_space()
        """         
        camera_model = ConnectedCamera.model
        """
        serial_number = ConnectedCamera.serial_number
        firmware_version = ConnectedCamera.firmware_version
        battery_level = ConnectedCamera.battery_level
        remaining_storage = ConnectedCamera.remaining_storage
        """
        if camera_model:
            filename = camera_model.replace(" ", "_")
        else:
            filename = "picture"
        
        if os.path.exists(save_directory + '/selected_pictures.json'):
            with open(save_directory + '/selected_pictures.json', 'r') as f:
                selected_pictures = json.load(f)
                if selected_pictures == 0 or selected_pictures is None:
                    os.remove(save_directory + '/selected_pictures.json')
        
        if os.path.exists(save_directory + '/selected_pictures.json'): # Check if there is an active session in the folder
            print("\033[93mWarning: There is still an active session in this folder.\033[0m")
            response = input("Do you want to continue with the session? (y/n): ")
            while response.lower() != 'y' and response.lower() != 'n':
                print("Invalid input. Please enter 'y' or 'n'.")
                response = input("Do you want to continue with the session? (y/n): ")
            
            if response.lower() == 'n':
                # Delete the selected_pictures.json file
                if os.path.exists(save_directory + '/selected_pictures.json'):
                    os.remove(save_directory + '/selected_pictures.json')
                    print("selected_pictures.json file deleted.")
                else:
                    print("selected_pictures.json file does not exist.")
            else:
                with open(save_directory + '/selected_pictures.json', 'r') as f:
                    selected_pictures = json.load(f)
                    print(selected_pictures)
            wait_for_keypress()
    
    if not is_camera_connected():
        print("Camera is disconnected.")
        print("Please connect the camera.")
        while not is_camera_connected():
            time.sleep(2)  # Simulating delay before checking again
        print("Camera is connected.")
        time.sleep(2)  # Simulating delay before showing the main menu
    
    clear_terminal()
    print("Menu:")
    if is_camera_connected():
        print("\033[92mCamera is connected.\033[0m")
    else:
        print("\033[91mNo camera is connected.\033[0m")
        
    print("Connected Camera:", ConnectedCamera.model)
    print("Save Folder: \033[94m{}\033[0m ({})".format(save_directory, calculate_mb_left(save_directory)))

    print("1. Capture")
    print("2. Save Folder settings")
    print("3. Transfer captured pictures in this session") 
    print("4. Camera and system info (Work in progress)")
    print("5. Start new session")
    print("6. Reconnect camera")
    print("7. Disconnect camera")
    print("8. Exit")

    choice = input("Enter your choice (1-8): ")

    if choice == "1": # Start Capture
        #print("Connected Camera:", camera["model"])
        #print("Save Folder:", save_directory, "(", calculate_mb_left(save_directory), ")")
        while True:
            clear_terminal()
            print("Connected Camera:", ConnectedCamera.model)
            print("Save Folder: \033[94m{}\033[0m ({})".format(save_directory, calculate_mb_left(save_directory)))
            print("1. Start Capture session")
            print("2. Change the save folder")
            print("3. View pictures")
            print("4. Go back")
        
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1": # Start Capture
                print("Save Folder: \033[94m{}\033[0m ({})".format(save_directory, calculate_mb_left(save_directory)))
                time.sleep(1)  # Simulating delay before capturing picture
                print("Starting capturing picture...")
                time.sleep(1)  # Simulating delay before capturing picture
                clear_terminal()
                print('Press Esc key to exit the viewer.\nUse "A" and "D" keys to navigate the pictures.\n\nPress (A) key to go back.\nPress (D) key to go forward.\n\nPress spacebar to select and deselect the picture.\n')
                wait_for_keypress()
                time.sleep(1)
                
                print(filename)
                wait_for_keypress()
                if filename == "":
                    command = ['gphoto2', '--capture-tethered', '--filename', os.path.join(save_directory, f"%f.%C")]
                else:
                    command = ['gphoto2', '--capture-tethered', '--filename', os.path.join(save_directory, f"{filename}-%f.%C")]
                
                p1 = subprocess.Popen(['python3', 'picture_viewer.py', save_directory, json.dumps(selected_pictures)])
                p2 = subprocess.Popen(command)

                p1.wait()
                p2.terminate()
                clear_terminal()
                
                with open(save_directory + '/selected_pictures.json', 'r', encoding='utf-8') as f:
                    selected_pictures = json.load(f)
                    #selected_pictures = [os.path.basename(file) for file in selected_pictures]
                print(selected_pictures)
                wait_for_keypress()
                
                while True: # Picture transfer menu loop
                    copy_choice = input("Do you want to copy the captured pictures? (y/n): ")
                    if copy_choice.lower() == "y":
                        print("Choose a destination directory to transfer the captured pictures.\n")
                        wait_for_keypress()
                        destination_directory = choose_save_directory()  # Choose the destination directory
                        print("Destination directory:", destination_directory)
                        time.sleep(1)  # Simulating delay before copying the pictures

                        if not destination_directory:  # Check if a destination directory is chosen
                            clear_terminal()
                            print("No destination directory chosen. Transfer cancelled.")
                            break
                        elif not save_directory:  # Check if a save directory is chosen
                            clear_terminal()
                            print("No save directory chosen. Transfer cancelled.")
                            break
                        elif save_directory == destination_directory:  # Check if the save and destination directories are the same
                            print("Save and destination directories are the same.")
                            print("Please choose a different destination directory.")
                            break
                        else:
                            copy_confirm(save_directory, destination_directory, selected_pictures)
                            break
                            
                    elif copy_choice.lower() == "n":
                        print("Picture copy cancelled.")
                        wait_for_keypress()
                        break
                    else:
                        print("Invalid choice. Please try again.")
        
            elif choice == "2": # Change the save folder
                choice_folder = input("Do you want to change the save folder? (y/n): ")
                if choice_folder.lower() == "y":
                    new_save_directory = choose_save_directory()
                    try:
                        if new_save_directory: # Check if a new save directory is chosen
                            save_directory = new_save_directory
                            print("Save directory: \033[94m{}\033[0m".format(save_directory))
                            print("Remaining storage:", calculate_mb_left(save_directory))
                        else:
                            print("Save directory remains: \033[94m{}\033[0m".format(save_directory))
                            print("Remaining storage:", calculate_mb_left(save_directory))
                        wait_for_keypress()
                    except:
                        print("Invalid save directory. Please choose a valid save directory.")
                        time.sleep(1)
                else:
                    print("Save directory remains: \033[94m{}\033[0m".format(save_directory))
                    print("Remaining storage:", calculate_mb_left(save_directory))
                    wait_for_keypress()
                    
            elif choice == "3": # View pictures
                
                clear_terminal()
                print('Press Esc key to exit the viewer.\nUse "A" and "D" keys to navigate the pictures.\n\nPress (A) key to go back.\nPress (D) key to go forward.\n\nPress spacebar to select and deselect the picture.\n')
                wait_for_keypress()
                time.sleep(1)
                
                p1 = subprocess.Popen(['python3', 'picture_viewer.py', save_directory, json.dumps(selected_pictures)])
                p1.wait()
                with open(save_directory + '/selected_pictures.json', 'r', encoding='utf-8') as f:
                    selected_pictures = json.load(f)
                    
                #clear_terminal()
                wait_for_keypress()
            
            elif choice == "4": # Go back
                break
            else:
                print("\033[91mInvalid choice. Please try again.\033[0m")
                time.sleep(1)  # Simulating delay before showing the menu again
                    
    elif choice == "2": # Save Folder settings
        
        while True:
            clear_terminal()
            print("Connected Camera:", ConnectedCamera.model)
            print("Save Folder: \033[94m{}\033[0m ({})".format(save_directory, calculate_mb_left(save_directory)))
            print("1. Open save folder")
            print("2. Change save folder")
            print("3. Change filename (Current filename:", filename, ")")
            print("4. Go back")
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1": # Open save folder
                #subprocess.Popen(["explorer", save_directory])
                with open(os.devnull, 'w') as devnull: # Suppressing the output of the command
                    try:
                        if sys.platform == "darwin": # Mac
                            subprocess.Popen(['open', save_directory], stderr=devnull)
                        else: # Linux
                            subprocess.Popen(['xdg-open', save_directory], stderr=devnull)
                    except PermissionError:
                        print("Please run the program with sudo privileges to open the save folder.")
                wait_for_keypress()
                
            elif choice == "2": # Choose save folder
                clear_terminal()
                print("Please choose a save directory.")
                time.sleep(2)  # Simulating delay before choosing the save directory
                save_directory = choose_save_directory()
                print("Save directory: \033[94m{}\033[0m".format(save_directory))
                time.sleep(2)  # Simulating delay before showing the menu again
                wait_for_keypress()
                
            elif choice == "3": # Filename change
                previous_filename = filename
                while True: # Filename change menu loop
                    clear_terminal()
                    print("Current filename:", previous_filename)
                    filename = input("Enter the custom filename: ")
                    if not filename or filename.strip() == "":
                        print("Invalid filename. Please enter a valid filename.")
                        filename = previous_filename
                        time.sleep(1)  # Simulating delay before showing the menu again
                    elif any(char in filename for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']):
                        print("Invalid filename. The following characters are not allowed: / \\ : * ? \" < > |")
                        filename = previous_filename
                        time.sleep(1)  # Simulating delay before showing the menu again
                    else:
                        # Continue with the rest of the code
                        print("Filename changed to:", filename)
                        previous_filename = filename
                        time.sleep(0.5)  # Simulating delay before showing the menu again
                        break
                    print("Filename changed to:", filename)
                    previous_filename = filename
                time.sleep(0.5)  # Simulating delay before showing the menu again
                wait_for_keypress()
                
            elif choice == "4": # Go back
                break
            else:
                print("\033[91mInvalid choice. Please try again.\033[0m")
                time.sleep(1)  # Simulating delay before showing the menu again
                
    elif choice == "3": # Transfer captured pictures in this session
        clear_terminal()
        cancel = 0
        print("Choose a destination directory to transfer the captured pictures.\n")
        time.sleep(1)  # Simulating delay before choosing the destination directory
        while True:
            destination_directory = choose_save_directory()  # Choose the destination directory
            print("Destination directory:", destination_directory)
            time.sleep(1)  # Simulating delay before copying the pictures

            if not destination_directory:  # Check if a destination directory is chosen
                clear_terminal()
                print("No destination directory chosen. Transfer cancelled.")
                cancel = 1
                break

            if not save_directory:  # Check if a save directory is chosen
                clear_terminal()
                print("No save directory chosen. Transfer cancelled.")
                cancel = 1
                break

            if save_directory == destination_directory:  # Check if the save and destination directories are the same
                print("Save and destination directories are the same.")
                print("Please choose a different destination directory.")
                continue

            while cancel == 0: # Check if the transfer is not cancelled
                cancel = copy_confirm(save_directory, destination_directory, selected_pictures)               
            if cancel == 1:
                break
            wait_for_keypress()
            
    elif choice == "4": # Camera info (work in progress)
        while True: # Camera info menu loop
            clear_terminal()                
            print("Connected Camera:", ConnectedCamera.model)
            print("Save Folder: \033[94m{}\033[0m ({})".format(save_directory, calculate_mb_left(save_directory)))
            print("\033[91m1. My Camera info: WARNING not reliable\033[0m")
            print("2. All connected cameras")
            print("3. All supported cameras")
            print("4. All available USB ports")
            print("5. Go back")
            choice = input("Enter your choice (1-5): ") 
                            
            if choice == "1": # My Camera info
                clear_terminal()
                #print("All supported abbilities of the connected camera:")
                #print(get_camera_abilities())
                print("\nCamera Information:")
                print("Model:", camera_model)
                #show_camera_info(camera_model, serial_number, firmware_version, battery_level, remaining_storage) # Show the camera information
                wait_for_keypress()
                    
            elif choice == "2": # All connected cameras
                clear_terminal()
                print("All Connected Cameras:")
                print(ConnectedCamera.model)
                wait_for_keypress()
                
            elif choice == "3": # All supported cameras
                clear_terminal()
                print("All Supported Cameras:")
                supported_cameras = list_available_cameras()
                for camera in supported_cameras:
                    print(camera)
                wait_for_keypress()
                
            elif choice == "4": # All available USB ports
                clear_terminal()
                print("All Available USB Ports:")
                usb_ports = list_available_usb_ports()
                for port in usb_ports:
                    print(port)
                wait_for_keypress()
                
            elif choice == "5": # Go back
                break
            else:
                print("\033[91mInvalid choice. Please try again.\033[0m")
                time.sleep(1)  # Simulating delay before showing the menu again
            
    elif choice == "5": # Start new session
        clear_terminal()
        confirm = input("Are you sure you want to start a new session? (y/n): ")
        if confirm.lower() == "y":
            print("New session starting...")

            selected_pictures = []
            cameras = []
            save_directory = None
            destination_directory = None
            camera = {}
            new_session_check = True

            time.sleep(2)  # Simulating delay before showing the main menu
            wait_for_keypress()
        else:
            print("Session not restarted.")
            time.sleep(2) 
                        
    elif choice == "6": # Reconnect camera
        print("Reconnecting camera...")
        confirm = input("Are you sure you want to reconnect the camera? (y/n): ")
        if confirm.lower() == "y":
            while not is_camera_connected():
                time.sleep(2)  # Simulating delay before checking again
            print("Camera reconnected.")
        else:
            print("Camera not reconnected.")
            
        wait_for_keypress()
            
    elif choice == "7": # Disconnect camera
        confirm = input("Are you sure you want to disconnect the camera? (y/n): ")
        if confirm.lower() == "y":
            disconnect_camera()
            print("Camera disconnected.")
        else:
            print("Camera not disconnected.")
        
        wait_for_keypress()
    
    elif choice == "8": # Exit
        break
    else:
        print("\033[91mInvalid choice. Please try again.\033[0m")
        time.sleep(1) # Simulating delay before showing the menu again
 
print("Exiting camera application.")
if os.path.exists(save_directory + '/selected_pictures.json'):
    if selected_pictures == 0 or selected_pictures is None or selected_pictures == [] or selected_pictures == "[]" or selected_pictures == "":
        os.remove(save_directory + '/selected_pictures.json')


#TO DO:
# Look on line 301