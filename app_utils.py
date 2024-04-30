import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import keyboard

def choose_save_directory(): # Choose the save directory for capture
    root = tk.Tk()
    root.withdraw()
    save_directory = filedialog.askdirectory()
    return save_directory

def calculate_mb_left(directory): # Calculate the available space in MB
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    mb_left = (1024 * 1024) - (total_size / (1024 * 1024))
    return mb_left

def wait_for_keypress():
    print("Press any key to continue...")
    while keyboard.is_pressed():  # if key is pressed 
        pass  # then do nothing
    keyboard.read_key()  # read the key
