#!/usr/bin/env python3
from camera_utils import is_camera_connected, list_available_cameras, get_connected_camera_model, get_camera_info, save_tethered_picture, list_available_usb_ports, show_latest_picture, copy_captured_pictures, disconnect_camera, show_camera_info
from app_utils import choose_save_directory, calculate_mb_left
#import msvcrt   # Windows-specific module for keyboard input
import keyboard # Cross-platform module for keyboard input
import time # Module for time-related functions
import tkinter as tk # Cross-platform module for GUI
import subprocess # Module for running shell commands

# Check if a camera is connected
"""
while not is_camera_connected():
    print("No camera is connected.")
    time.sleep(2)  # Simulating delay before checking again

print("Camera is connected.")
print("Updating status bar...")
time.sleep(2)  # Simulating delay for updating status bar
print("Status bar updated: Camera is connected.")
print("Camera model:", get_connected_camera_model())

camera_info = get_camera_info()  # Get the information of the connected camera
camera = {
    "model": camera_info
}
"""
cameras = []  # Define the "cameras" variable as an empty list

save_directory = choose_save_directory() # Choose the save directory
print("Save directory:", save_directory)
if not save_directory:
    print("No save directory chosen. Please choose a save directory.")
    save_directory = choose_save_directory()
    print("Save directory:", save_directory)
else:
    print("Save directory already chosen:", save_directory)

    if cameras:
        for camera in cameras:
            print(camera)
    else:
        print("No camera available.")
    
    class FakeCamera:
        def __init__(self, model):
            self.model = model

    # Create a fake camera object for testing
    fake_camera = FakeCamera("Nikon D750")
    camera = {
        "model": fake_camera.model
    }

    filename = ""
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

    while True: # Main menu loop
        if not is_camera_connected():
            print("Camera is disconnected.")
            print("Please connect the camera.")
            while not is_camera_connected():
                time.sleep(2)  # Simulating delay before checking again
            print("Camera is connected.")
            
        print("Menu:")
        if is_camera_connected():
            print("Camera is connected.")
        else:
            print("No camera is connected.")
            
        print("Connected Camera:", camera["model"])
        print("Save Folder:", save_directory, "(", calculate_mb_left(save_directory), "MB left)")

        print("1. Capture")
        print("2. Save Folder settings")
        print("3. Transfer all captured pictures in this session") 
        print("4. Camera and system info")
        print("5. Start new session")
        print("6. Reconnet camera")
        print("7. Disconnect camera")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == "1": # Start Capture
            print("Connected Camera:", camera["model"])
            print("Save Folder:", save_directory, "(", calculate_mb_left(save_directory), "MB left)")
            
            print("1. Start Capture session")
            print("2. Change the save folder")
            print("3. Go back")
            
            while True:
                choice = input("Enter your choice (1-3): ")
                if choice == "1": # Start Capture
                    print("Save Folder:", save_directory, "(", calculate_mb_left(save_directory), "MB left)")
                    time.sleep(2)  # Simulating delay before capturing picture
                    print("Starting capturing picture...")
                    show_latest_picture(save_directory, filename)
                    
                elif choice == "2": # Change the save folder
                    choice = input("Do you want to change the save folder? (y/n): ")
                    if choice.lower() == "y":
                        save_directory = choose_save_directory()
                        print("Save directory:", save_directory)
                        print("Remaining storage:", calculate_mb_left(save_directory), "MB left")
                    else:
                        print("Save directory remains:", save_directory)
                        print("Remaining storage:", calculate_mb_left(save_directory), "MB left")
                elif choice == "3": # Go back
                    break
                else:
                    print("Invalid choice. Please try again.")
                      
        elif choice == "2": # Save Folder settings
            print("Connected Camera:", camera["model"])
            print("Save Folder:", save_directory, "(", calculate_mb_left(save_directory), "MB left)")
            
            print("1. Open save folder")
            print("2. Change save folder")
            print("3. Change filename")
            print("4. Go back")
            
            while True:
                print("1. Open save folder")
                print("2. Change save folder")
                print("3. Change filename")
                print("4. Go back")
                choice = input("Enter your choice (1-4): ")
                
                if choice == "1": # Open save folder
                    #subprocess.Popen(["explorer", save_directory])
                    subprocess.Popen(["nautilus", save_directory])
                elif choice == "2": # Choose save folder
                    save_directory = choose_save_directory()
                    print("Save directory:", save_directory)
                elif choice == "3": # Filename change
                    filename = input("Enter the custom filename: ")
                elif choice == "4": # Go back
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
        elif choice == "3": # Transfer all captured pictures in this session
                destination_directory = choose_save_directory()  # Choose the destination directory
                print("Destination directory:", destination_directory)
                if not destination_directory: # Check if a destination directory is chosen
                    print("No destination directory chosen. Please choose a destination directory.")
                    destination_directory = choose_save_directory()
                    print("Destination directory:", destination_directory)
                else:
                    print("Destination directory already chosen:", destination_directory)
                
                if not save_directory: # Check if a save directory is chosen
                    print("No save directory chosen. Please choose a save directory.")
                    break
                
                # Copy captured pictures to the destination directory
                print("Copying captured pictures to the destination directory...")
                
                copy_captured_pictures(save_directory, destination_directory)
                print("Pictures copied successfully.")
                time.wait(4)  # Simulating delay before going back to the main menu
                # Go back to the main menu
                break

        elif choice == "4": # Camera info
            print("1. My Camera info")
            print("2. All connected cameras")
            print("3. All supported cameras")
            print("4. All available USB ports")
            print("5. Go back")
            
            choice = input("Enter your choice (1-5): ")
            while True:
                if choice == "1": # My Camera info
                    print("Camera Information:")
                    show_camera_info(camera) # Show the camera information
                    print("Press any key to continue...")
                    keyboard.read_key()
                        
                elif choice == "2": # All connected cameras
                    print("All Connected Cameras:")
                    for camera in cameras:
                        print(camera)
                    print("Press any key to continue...")
                    keyboard.read_key()
                    
                elif choice == "3":
                    print("All Supported Cameras:")
                    supported_cameras = list_available_cameras()
                    for camera in supported_cameras:
                        print(camera)
                    keyboard.read_key()
                    
                elif choice == "4":
                    print("All Available USB Ports:")
                    usb_ports = list_available_usb_ports()
                    for port in usb_ports:
                        print(port)
                    keyboard.read_key()
                    
                elif choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")
                choice = input("Enter your choice (1-5): ")
                
        elif choice == "5": # Start new session
            confirm = input("Are you sure you want to start a new session? (y/n): ")
            if confirm.lower() == "y":
                cameras = []
                save_directory = None
                destination_directory = None
                camera = {}
                break
            else:
                print("Session not restarted.")
                
        elif choice == "6": # Reconnect camera
            print("Reconnecting camera...")
            confirm = input("Are you sure you want to reconnect the camera? (y/n): ")
            if confirm.lower() == "y":
                while not is_camera_connected():
                    time.sleep(2)  # Simulating delay before checking again
                print("Camera reconnected.")
            else:
                print("Camera not reconnected.")
                
        elif choice == "7": # Disconnect camera
            confirm = input("Are you sure you want to disconnect the camera? (y/n): ")
            if confirm.lower() == "y":
                disconnect_camera()
                print("Camera disconnected.")
            else:
                print("Camera not disconnected.")
        
        elif choice == "8": # Exit
            break
        else:
            print("Invalid choice. Please try again.")
 
print("Exiting camera application.")