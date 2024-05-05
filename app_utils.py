import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import keyboard
import time

def choose_save_directory(): # Choose the save directory for capture
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    root.destroy()
    return directory

def calculate_mb_left(directory): # Calculate the available space of the disc where the directory is located
    total_size = 0
    statvfs = os.statvfs(directory)
    total_size = statvfs.f_frsize * statvfs.f_bavail # Available space in bytes
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