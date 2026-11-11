import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import json
import os

root = tk.Tk()
root.title("Broadcast Compliance Checker") # creates and names the GUI window 

filename = fd.askopenfilename()
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


def select(event):
    selected_item = filename.get()
    #selected_item = combo_box.get()
    label.config(text="Selected Video: " + selected_item)

label = tk.Label(root, text="Selected Video:")
label.grid(pady=10)

#combo_box = ttk.Combobox(
#    root,
 #   values=[r"1980_TV&Radio_Swapshop.mp4",
#     r"1980_TV&Radio_TheComputerProgramme.mp4",
#     r"1980_TV&Radio_TomorrowsWorld.mp4",
#     r"1990_Events_ConstructionCanaryWharf.mp4",
#     r"1990_Leisure_Shopping.mp4",
#     r"1990_Leisure_SummerFun.mp4",
#     r"1990_People_ElectronicsFactory.mp4",
#     r"1990_TV&Radio_SixOClockNews.mp4",
#     r"2000_Leisure_ClimbingWall.mp4",
#     r"19880223_People_CockleWorkers.mp4",
#     r"19890220_Events_GlobalWarming.mp4",
#     r"19900101_Leisure_Canoeing.mp4"],
#    state="readonly",
#    width=43
#)
#combo_box.grid(pady=40)
#combo_box.set("Select a Video")
#combo_box.bind("<<ComboboxSelected>>", select)       


#button set up
button = tk.Button(root, text="Check Compliance", width=25, command=getData)
button.grid()          


#text box set up 
text_widget = tk.Text(root, height=6, width=55)
text_widget.grid()

root.mainloop()