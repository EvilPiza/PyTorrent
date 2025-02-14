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
