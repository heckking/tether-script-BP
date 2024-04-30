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
    return directory

def calculate_mb_left(directory): # Calculate the available space of the disc where the directory is located
    total_size = 0
    statvfs = os.statvfs(directory)
    total_size = statvfs.f_frsize * statvfs.f_bavail
    mb_left = total_size / (1024 * 1024)
    if mb_left > 1024:
        gb_left = mb_left / 1024
        return f"{gb_left:.2f} GB left"
    else:
        return f"{mb_left:.2f} MB left"

def wait_for_keypress(): # Wait for a key press to continue
    
    """
    print("Press any key to continue...")
    while not keyboard.is_pressed():  # if key is pressed 
        time.sleep(0.1)  # wait for 0.1 seconds    
    """    
    input("Press Enter to continue...")

def clear_terminal(): # Clear the text from the terminal
    if os.name == 'nt': 
        # For Windows
        _ = os.system('cls')
    else: 
        # For Linux and Mac
        _ = os.system('clear')