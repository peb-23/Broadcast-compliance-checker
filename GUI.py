import tkinter as tk # importing package to build the gui from
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os # import operating sysstem commands 
from analysis import run_analysis_video # import data from anaylsis.py
from analysis import run_analysis_audio  
from analysis import run_analysis_videoExtra
from results import run_ofcom_check #import data from results.py
from results import all_video_results
from results import all_audio_results 
from matplotlib.figure import Figure # import matplotlib to make graphs from
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
  
#creating the GUI window
root = tk.Tk()
root.title("Broadcast Compliance Checker")
root.geometry('650x530')

selectedVideo = None #set up variable for video path file 

def selectFile(): # user selects a file

    global selectedVideo  # make the variable as global to modify it

    fileTypes = ( #restricts the file types that can be selected to video files
        ('Video files', '*.mp4 *.avi *.mov'),
        ('All files', '*.*'))

    filename = fd.askopenfilename( # user selects a file popup
        title='Open a video file',
        initialdir='/',
        filetypes=fileTypes)
    
    if not filename: #if no file is selected, return to file selection
        return
    
    #if wrong file type is selected, show error message and return to file selection
    validExtensions = ('.mp4', '.avi', '.mov')
    if not filename.lower().endswith(validExtensions):
        showinfo(
            title='Invalid File',
            message='Please select a supported video file.')
        return
    
    # update & store the selected video path
    selectedVideo = filename  

    # Update label with just the selected file name, not the whole path name
    selected_file_label.config(
        text=f"Selected file: {os.path.basename(filename)}")

# select a video button
open_button = ttk.Button(
    root, text='Select a Video', command=selectFile )
open_button.pack(pady=20)

# Label underneath button to display what file is selected
selected_file_label = ttk.Label(
    root, text="No file selected", wraplength=450 )
selected_file_label.pack(pady=10)

def run_check(): #function which gets the data from the imports to put into text box/graphs 
    if selectedVideo is None:
        texto_widget.insert(tk.END, "Please select a video first.\n")
        return              # if no video is selected, return error message 
    
    video_data = run_analysis_video(selectedVideo)  #bring functions from anaylsis.sheet to gui
    audio_data = run_analysis_audio(selectedVideo)
    extra_data = run_analysis_videoExtra(selectedVideo)

    compliance_data = run_ofcom_check(video_data, audio_data, extra_data) # bring function from results.py to gui 

    video_results_text = all_video_results(video_data,extra_data) #merge both video anaylsis results 
    audio_results_text = all_audio_results(audio_data)
    
    texto_widget.delete("1.0", tk.END) # clears the compliance results text box before adding new text 
    texto_widget.insert(tk.END,f"""Overall Compliance Status: {compliance_data["overall"]}
Compliance Score: {compliance_data["score"]}%
Checks Passed: {compliance_data["passed"]}/{compliance_data["total"]}
""")
    #Making the compliance summary graph 
    for widget in graph_frame.winfo_children(): # clears the graph before adding a new graph
        widget.destroy()

    fig = Figure(figsize=(2, 2))                             # create figure and control the size of graph 
    ax = fig.add_subplot(111)                                # graph - make the plotting area/axis' of the graph  
    ax.set_yticks(range(0, compliance_data["total"] + 2, 2)) #graph - creat the y axis scale based on number of checks  
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)       # graph - add grid lines 

    ax.bar( # creates a bar chart, with 2 columns, pass or fail
        ["PASS", "FAIL"],
        [compliance_data["passed"], #what data goes into each column 
        compliance_data["failed"]],
    color=["green", "red"])
    ax.set_title("Checks") # add a graph title 

    canvas = FigureCanvasTkAgg(fig,master=graph_frame) # embeds the graph into the gui 
    canvas.draw()                                      # draws/displays graph in gui 
    canvas.get_tk_widget().pack()

    textV_widget.delete("1.0", tk.END) #clears video results box 
    textV_widget.insert(               #adds the video results data to box 
    tk.END,f"""{video_results_text}
""")

    textA_widget.delete("1.0", tk.END) #clears audio results box
    textA_widget.insert(               #adds the audio results data to box 
    tk.END,f"""{audio_results_text}
""")

# creating the Run Check button
button = tk.Button(root, text="Run Check", width=25, command=run_check)
button.pack(pady=(0, 20))

# Overall Compliance Frame
overall_frame = tk.Frame(root)
overall_frame.pack(pady=(0, 20))

# Left top frame - Compliance results Text
overall_text_frame = tk.Frame(overall_frame)
overall_text_frame.pack(side=tk.LEFT, padx=10)

texto_widget = tk.Text(overall_text_frame, height=4, width=40)
texto_widget.pack() # compliance results text box 

# Right top frame - Compliance results Graph
graph_frame = tk.Frame(overall_frame)
graph_frame.pack(side=tk.LEFT, padx=10)

#BOTTOM text boxes for video and audio results 
results_frame = tk.Frame(root) # Frame to hold both video and audio text boxes
results_frame.pack(pady=10) 

# Video results text box 
video_frame = tk.Frame(results_frame)
video_frame.pack(side=tk.LEFT, padx=10) # Video Frame
    
video_label = tk.Label(video_frame,text="Video Analysis", font=("Arial", 10, "bold"))
video_label.pack() #Video Label
    
textV_widget = tk.Text(video_frame, height=8, width=40)
textV_widget.pack() #Video text box

# Audio results text box 
audio_frame = tk.Frame(results_frame)  # Audio frame
audio_frame.pack(side=tk.LEFT, padx=10)
    
audio_label = tk.Label(audio_frame,text="Audio Analysis",font=("Arial", 10, "bold"))
audio_label.pack() # Audio Label
    
textA_widget = tk.Text(audio_frame, height=8, width=40)
textA_widget.pack() #Audio text box

# Run application
root.mainloop()