import tkinter as tk
from tkinter import filedialog
import os

def select_folder():
    folder_path = filedialog.askdirectory()
    
    if folder_path:
        print(f"Selected folder: {folder_path}")
        return folder_path
    else:
        print("No folder selected")
    # return os.path.abspath(os.curdir) # Potential optimization :)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    select_folder()
    root.quit()

