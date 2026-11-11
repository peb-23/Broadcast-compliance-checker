import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
from analysis import run_analysis

  
#creating the GUI window
root = tk.Tk()
root.title("Broadcast Compliance Checker")
root.geometry('500x300')

selected_video = None #set up variable for video path file 

def select_file(): # user selects a file

    global selected_video  # Declare the variable as global to modify it

    filetypes = ( #restricts the file types that can be selected to video files
        ('Video files', '*.mp4 *.avi *.mov'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename( # user selects a file popup
        title='Open a video file',
        initialdir='/',
        filetypes=filetypes
    )
    
    if not filename: #if no file is selected, return to file selection
        return
    
    #if wrong file type is selected, show error message and return to file selection
    valid_extensions = ('.mp4', '.avi', '.mov')

    if not filename.lower().endswith(valid_extensions):
        showinfo(
            title='Invalid File',
            message='Please select a supported video file.'
        )
        return
    
    # update & store the selected video path
    selected_video = filename  

    # Update label with just the selected file name
    selected_file_label.config(
        text=f"Selected file: {os.path.basename(filename)}"
    )

# select a video button
open_button = ttk.Button(
    root,
    text='Select a Video',
    command=select_file
)
open_button.pack(pady=20)

# Label underneath button to display what file is selected
selected_file_label = ttk.Label(
    root,
    text="No file selected",
    wraplength=450
)
selected_file_label.pack(pady=10)



#text box 
text_widget = tk.Text(root, height=6, width=55)
text_widget.pack()

def run_check():

    if selected_video is None:
        text_widget.insert(tk.END, "Please select a video first.\n")
        return

    results = run_analysis(selected_video)
    print(results) 

    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, results)

# Run Check button
button = tk.Button(root, text="Run Check", width=25, command=run_check)
button.pack(pady=(0, 20))

# Run application
root.mainloop()