#!/usr/bin/env python3
import subprocess
from camera_utils import is_camera_connected, list_available_cameras, get_connected_camera_model, get_camera_info, save_tethered_picture, list_available_usb_ports, show_latest_picture
import time
import tkinter as tk
from app_utils import choose_save_directory, calculate_mb_left

# Check if a camera is connected
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

cameras = []  # Define the "cameras" variable as an empty list

save_directory = choose_save_directory() # Choose the save directory
print("Save directory:", save_directory)
if not save_directory:
    print("No save directory chosen. Please choose a save directory.")
    save_directory = choose_save_directory()
    print("Save directory:", save_directory)
else:
    print("Save directory already chosen:", save_directory)

for camera in cameras:
    print(camera)
    
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
		4.3 Go Back
  
    5. Start new session
    
	6. Reconnect camera
 
	7. Disconnect camera
 
	8. Exit

    """

    while True:
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
        print("3. Transfer all captured pictures in this session")  # Added option to list available USB ports
        print("4. Camera info")
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
            
            choice = input("Enter your choice (1-3): ")
            if choice == "1": # Start Capture
                print("Save Folder:", save_directory, "(", calculate_mb_left(save_directory), "MB left)")
                time.sleep(2)  # Simulating delay before capturing picture
                print("Starting capturing picture...")
                show_latest_picture(save_directory)
                
            elif choice == "2": # Change the save folder
                choice = input("Do you want to change the save folder? (y/n): ")
                if choice.lower() == "y":
                    save_directory = choose_save_directory()
                    print("Save directory:", save_directory)
                else:
                    print("Save directory remains:", save_directory)
                    
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
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1": # Open save folder
                subprocess.Popen(["explorer", save_directory])
            elif choice == "2": # Choose save folder
                save_directory = choose_save_directory()
                print("Save directory:", save_directory)
            elif choice == "3": # Filename change
                filename = input("Enter the custom filename: ")
            elif choice == "4": # Go back
                break
            else:
                print("Invalid choice. Please try again.")
        
        elif choice == "3":
            usb_ports = list_available_usb_ports()  # Function to list available USB ports
            print("Available USB ports:")
            for port in usb_ports:
                print(port)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again. Maybe")
 
print("Exiting camera application.")