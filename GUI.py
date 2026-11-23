import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
from analysis import run_analysis_video
from analysis import run_analysis_audio  
from results import run_ofcom_check

  
#creating the GUI window
root = tk.Tk()
root.title("Broadcast Compliance Checker")
root.geometry('650x450')

selectedVideo = None #set up variable for video path file 

def selectFile(): # user selects a file

    global selectedVideo  # Declare the variable as global to modify it

    fileTypes = ( #restricts the file types that can be selected to video files
        ('Video files', '*.mp4 *.avi *.mov'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename( # user selects a file popup
        title='Open a video file',
        initialdir='/',
        filetypes=fileTypes
    )
    
    if not filename: #if no file is selected, return to file selection
        return
    
    #if wrong file type is selected, show error message and return to file selection
    validExtensions = ('.mp4', '.avi', '.mov')

    if not filename.lower().endswith(validExtensions):
        showinfo(
            title='Invalid File',
            message='Please select a supported video file.'
        )
        return
    
    # update & store the selected video path
    selectedVideo = filename  

    # Update label with just the selected file name
    selected_file_label.config(
        text=f"Selected file: {os.path.basename(filename)}"
    )

# select a video button
open_button = ttk.Button(
    root,
    text='Select a Video',
    command=selectFile
)
open_button.pack(pady=20)

# Label underneath button to display what file is selected
selected_file_label = ttk.Label(
    root,
    text="No file selected",
    wraplength=450
)
selected_file_label.pack(pady=10)


def run_check():

    if selectedVideo is None:
        texto_widget.insert(tk.END, "Please select a video first.\n")
        return
    
    results_Ofcom = run_ofcom_check(selectedVideo)
    results_video = run_analysis_video(selectedVideo)
    results_audio = run_analysis_audio(selectedVideo)
    
    texto_widget.delete("1.0", tk.END)
    texto_widget.insert(tk.END, results_Ofcom)

    textV_widget.delete("1.0", tk.END)
    textV_widget.insert(tk.END, results_video)

    textA_widget.delete("1.0", tk.END)
    textA_widget.insert(tk.END, results_audio)

# Run Check button
button = tk.Button(root, text="Run Check", width=25, command=run_check)
button.pack(pady=(0, 20))

#text box -pass/fail
texto_widget = tk.Text(root, height=4, width=70)
texto_widget.pack(pady=(0, 20))

# Frame to hold both text boxes
results_frame = tk.Frame(root)
results_frame.pack(pady=10)

# Video section
video_frame = tk.Frame(results_frame)
video_frame.pack(side=tk.LEFT, padx=10)

video_label = tk.Label(
    video_frame,
    text="Video Analysis",
    font=("Arial", 10, "bold")
)
video_label.pack()

textV_widget = tk.Text(
    video_frame,
    height=10,
    width=40
)
textV_widget.pack()

# Audio section
audio_frame = tk.Frame(results_frame)
audio_frame.pack(side=tk.LEFT, padx=10)

audio_label = tk.Label(
    audio_frame,
    text="Audio Analysis",
    font=("Arial", 10, "bold")
)
audio_label.pack()

textA_widget = tk.Text(
    audio_frame,
    height=10,
    width=40
)
textA_widget.pack()

# Run application
root.mainloop()