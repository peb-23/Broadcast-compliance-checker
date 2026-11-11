import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os

#creating the GUI window
root = tk.Tk()
root.title("Broadcast Compliance Checker")
#root.resizable(False, False)
root.geometry('500x300')

#set up variable for video path file 
selected_video = None

# user selects a file
def select_file():

    #only allows user to upload the correct file types
    filetypes = (
        ('Video files', '*.mp4 *.avi *.mov'),
        ('All files', '*.*')
    )

    # user selects a file popup
    filename = fd.askopenfilename(
        title='Open a video file',
        initialdir='/',
        filetypes=filetypes
    )
    #if no file is selected, return to file selection
    if not filename:
        return
    
    #if wrong file type is selected, show error message and return to file selection
    valid_extensions = ('.mp4', '.avi', '.mov')

    if not filename.lower().endswith(valid_extensions):
        showinfo(
            title='Invalid File',
            message='Please select a supported video file.'
        )
        return

    # Update label with selected file name
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

# Run Check button
button = tk.Button(root, text="Run Check", width=25, command=root)
button.pack(pady=(0, 20))
button.pack()

#text box 
text_widget = tk.Text(root, height=6, width=55)
text_widget.pack()

# Run application
root.mainloop()