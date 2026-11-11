import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import json
import os

root = tk.Tk()
root.title("Broadcast Compliance Checker") # creates and names the GUI window 

filename = fd.askopenfilename()  # drag and drop popup 
ffprobe = r"C:\Users\phillg03\BBC Dropbox\Georgina Phillips\UNI\Year 2.1\Programming\BCUTestData\ffmpeg-9.0.2-full_build\bin\ffprobe.exe"
path = filename
#path = r"C:\Users\phillg03\BBC Dropbox\Georgina Phillips\UNI\Year 2.1\Programming\BCUTestData\BCUTestData\BBC_Videos"

def getData():
    selection =filename.get()
    fSelection = os.path.join(path, selection)

    command = [
    ffprobe,
    "-v", "quiet",
    "-print_format", "json",
    "-show_format",
    "-show_streams",
    fSelection ]
    
    result = subprocess.run(command, capture_output=True,text=True)
    metadata = json.loads(result.stdout)

    duration = metadata["format"]["duration"]
    width = metadata["streams"][0]["width"]
    height = metadata["streams"][0]["height"]
    resolution = f"{width}x{height}"
    frameRate = metadata["streams"][0]["avg_frame_rate"]
    
    text_widget.delete("1.0",tk.END )
    text_widget.insert("1.0" , f"""Video selected: {selection}
It is {duration} seconds long
The resolution is {resolution}
The Frame rate is {frameRate}
""")