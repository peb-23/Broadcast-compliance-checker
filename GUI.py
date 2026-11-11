import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title("Broadcast Compliance Checker") # creates and names the GUI window 
root.resizable(False, False)
root.geometry('300x150')

#user drag and drop popup 
def select_file():
    #only allows user to upload the correct file types
    filetypes = (   
        ('Video files', '*.mp4 *.avi *.mov '),
        ('All files', '*.*')
    )

    # user selects a file popup 
    filename = fd.askopenfilename(   
        title = 'Open a video file',
        initialdir = '/',
        filetypes = filetypes
        )

    #if wrong file type is selected, show error message and return to file selection
    if not filename:  
     return
    
    valid_extensions = ('.mp4', '.avi', '.mov')

    if not filename.lower().endswith(valid_extensions):
        showinfo(
            title='Invalid File',
            message='Please select a supported video file.'
        )
        return

   #testing feature:  message box to show the selected file name 
    showinfo(   
        title = 'Selected Video',
        message = filename
    )


# open button
open_button = ttk.Button(   
    root,
    text='Open Video',
    command=select_file
)

open_button.pack(expand=True)


# run the application
root.mainloop()