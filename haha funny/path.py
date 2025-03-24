import tkinter as tk
from tkinter import filedialog
import os

def select_folder():
    return os.path.abspath(os.curdir)   # Auto path
    
    folder_path = filedialog.askdirectory()    # Manual Path
    
    if folder_path:
        print(f"Selected folder: {folder_path}")
        return folder_path
    else:
        print("No folder selected")
        
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    select_folder()
    root.quit()

# This file is so ehhh like Auto Path is just too good, Manual Path could be good for some use cases, like you want the videos to be stored somewhere specific but other than that, Auto is the goat