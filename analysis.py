import subprocess
import json 
import tkinter as tk
from tkinter import ttk
import os

#ffprodbe path for the analysis function to use
ffprobe = r"C:\Users\phillg03\BBC Dropbox\Georgina Phillips\UNI\Year 2.1\Programming\BCUTestData\ffmpeg-9.0.2-full_build\bin\ffprobe.exe"

def run_analysis_video(video_path):
     fSelection = video_path

     command = [
     ffprobe,
     "-v", "quiet",
     "-print_format", "json",
     "-show_format",
     "-show_streams",
     fSelection ]
    
     result = subprocess.run(command, capture_output=True,text=True)
     metadata = json.loads(result.stdout)

     duration = round(float(metadata["format"]["duration"]), 2)
     width = metadata["streams"][0]["width"]
     height = metadata["streams"][0]["height"]
     resolution = f"{width}x{height}"
     frameRate = metadata["streams"][0]["avg_frame_rate"]
     codec = metadata["streams"][0]["codec_name"]
    
     return f"""Video Anaylsis Results:
 Duration: {duration} Sec       Score: MAKE
 Resolution: {resolution} px        Score: MAKE
 Frame rate: {frameRate} fps        Score: MAKE
 Ascept Ratio: MAKE                Score: MAKE
 Codec: {codec}                    Score: MAKE
 Black frame: MAKE                 Score: MAKE
 Frozen frame : MAKE               Score: MAKE
 """ 


def run_analysis_audio(video_path):
     fSelection = video_path

     command = [
     ffprobe,
     "-v", "quiet",
     "-print_format", "json",
     "-show_format",
     "-show_streams",
     fSelection ]
    
     result = subprocess.run(command, capture_output=True,text=True)
     metadata = json.loads(result.stdout)

     sample_rate = metadata["streams"][1]["sample_rate"]
     channels = metadata["streams"][1]["channels"]
     bit_depth = metadata["streams"][1]["bits_per_sample"]
     return f""" Audio Analysis Results:
 Sample Rate: {sample_rate}Hz      Score: MAKE  
 channels: {channels}                 Score: MAKE
 Bit Depth: {bit_depth} bits         Score: MAKE
 Peak Level: MAKE                  Score: MAKE
 Silent Sections: MAKE             Score: MAKE
 Average Loudness: MAKE            Score: MAKE
     """
