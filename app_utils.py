import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def choose_save_directory(): # Choose the save directory for capture
    root = tk.Tk()
    root.withdraw()
    save_directory = filedialog.askdirectory()
    return save_directory

def choose_destination_directory(): # Choose the destination directory for transfer
    root = tk.Tk()
    root.withdraw()
    destination_directory = filedialog.askdirectory()
    return destination_directory

def calculate_mb_left(directory): # Calculate the available space in MB
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    mb_left = (1024 * 1024) - (total_size / (1024 * 1024))
    return mb_left