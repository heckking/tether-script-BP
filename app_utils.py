import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import keyboard
import time
import json

def choose_save_directory():
    """
    Opens a dialog box to choose the save directory for capture.

    Returns:
        str: The selected directory path.
    """
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    root.destroy()
    return directory

def calculate_mb_left(directory):
    """
    Calculate the available space in megabytes (MB) of the disk where the specified directory is located.

    Args:
        directory (str): The path to the directory.

    Returns:
        str: A string indicating the amount of available space in either gigabytes (GB) or megabytes (MB),
             with color-coded formatting:
             - If the available space is greater than 1024 MB, it returns the amount in GB with green color.
             - If the available space is less than or equal to 1024 MB, it returns the amount in GB with green color.
             - If the available space is greater than 512 MB, it returns the amount in MB with orange color.
             - If the available space is less than or equal to 512 MB, it returns the amount in MB with red color.
    """
    total_size = 0
    statvfs = os.statvfs(directory)
    total_size = statvfs.f_frsize * statvfs.f_bavail  # Available space in bytes
    mb_left = total_size / (1024 * 1024)
    if mb_left > 1024:
        gb_left = mb_left / 1024
        return f"\033[38;5;46m{gb_left:.2f} GiB left\033[0m"  # Green color
    else:
        if mb_left <= 1024:
            gb_left = mb_left / 1024
            return f"\033[38;5;46m{gb_left:.2f} GiB left\033[0m"  # Green color
        elif mb_left > 512:
            return f"\033[38;5;202m{mb_left:.2f} MiB left\033[0m"  # Orange color
        else:
            return f"\033[38;5;196m{mb_left:.2f} MiB left\033[0m"  # Red color

def wait_for_keypress(): # Wait for a key press to continue
    
    """
    print("Press any key to continue...")
    while not keyboard.is_pressed():  # if key is pressed 
        time.sleep(0.1)  # wait for 0.1 seconds    
    """    
    input("\033[38;5;226mPress Enter to continue...\033[0m") # Yellow color

def clear_terminal(): # Clear the text from the terminal
    if os.name == 'nt': 
        # For Windows
        _ = os.system('cls')
    else: 
        # For Linux and Mac
        _ = os.system('clear')
        
def change_save_directory(save_directory, selected_pictures):
    """
    Change the save directory for capture.

    This function allows the user to change the save directory for captured pictures. It prompts the user to choose a new save directory and updates the `save_directory` variable accordingly. 
    If there is an active session in the new save folder, it prompts the user to confirm whether they want to continue with the session or not. If the user chooses not to continue, the `selected_pictures.json` file in the save directory will be deleted. 
    If the user chooses to continue, the `selected_pictures.json` file will be loaded.

    Args:
        save_directory (str): The current save directory.
        selected_pictures (list): The list of selected pictures.

    Returns:
        tuple: A tuple containing the updated `save_directory` and `selected_pictures`.

    """
    clear_terminal()
    choice_folder = input("Do you want to change the save folder? (y/n): ")
    if choice_folder.lower() == "y":
        print("Please choose a save directory.")
        time.sleep(2)  # Simulating delay before choosing the save directory
        new_save_directory = choose_save_directory()
        print("New save directory:", new_save_directory)
        print("Old save directory:", save_directory)
        wait_for_keypress()
        try:
            if new_save_directory or not new_save_directory == save_directory: # Check if a new save directory is chosen
                save_directory = new_save_directory
                print("Save directory changed to:", save_directory)
                if os.path.exists(save_directory + '/selected_pictures.json'): # Check if there is an active session in the folder
                    print("\033[93mWarning: There is an active session in this new save folder.\033[0m")
                    response = input("Do you want to continue with the session? (y/n): ")
                    while response.lower() != 'y' and response.lower() != 'n':
                        print("Invalid input. Please enter 'y' or 'n'.")
                        response = input("Do you want to continue with the session? (y/n): ")
                    """
                    if the response is 'n', the selected_pictures.json file will be deleted. If the file does not exist, it will print that the file does not exist. 
                    If the response is 'y', the selected_pictures.json file will be loaded.
                    """            
                    if response.lower() == 'n':
                        # Delete the selected_pictures.json file
                        if os.path.exists(save_directory + '/selected_pictures.json'):
                            os.remove(save_directory + '/selected_pictures.json')
                            print("selected_pictures.json file deleted.")
                            selected_pictures = []
                        else:
                            print("selected_pictures.json file does not exist.")
                            selected_pictures = []
                    else:
                        selected_pictures = []
                        with open(save_directory + '/selected_pictures.json', 'r') as f:
                            selected_pictures = json.load(f)
                            print(selected_pictures)
                    wait_for_keypress()
                else:
                    print("Save directory changed to:", save_directory)
                    selected_pictures = []
                
                time.sleep(2)  # Simulating delay before showing the menu again
                clear_terminal()
                print("Save directory: \033[94m{}\033[0m".format(save_directory))
                print("Remaining storage:", calculate_mb_left(save_directory))
            else:
                clear_terminal()
                print("Save directory remains: \033[94m{}\033[0m".format(save_directory))
                print("Remaining storage:", calculate_mb_left(save_directory))
            wait_for_keypress()
        except:
            print("Invalid save directory. Please choose a valid save directory.")
            time.sleep(1)
    else:
        clear_terminal()
        print("Save directory remains: \033[94m{}\033[0m".format(save_directory))
        print("Remaining storage:", calculate_mb_left(save_directory))
        wait_for_keypress()
    
    return save_directory, selected_pictures