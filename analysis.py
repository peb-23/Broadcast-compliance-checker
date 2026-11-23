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
 [P/F] Duration: {duration} Sec 
 [P/F] Resolution: {resolution} px
 [P/F] Frame rate: {frameRate} fps 
 [P/F] Ascept Ratio: MAKE 
 [P/F]  Codec: {codec} 
 [P/F]  Black frame: MAKE 
 [P/F] Frozen frame : MAKE 
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

     sampleRate = metadata["streams"][1]["sample_rate"]
     channels = metadata["streams"][1]["channels"]
     bitDepth = metadata["streams"][1]["bits_per_sample"]
    # peakLimit = metadata["streams"][1]["max_bit_rate"]
    # loudness = metadata["streams"][1]["tags"]["loudness"]
    # silence = metadata["streams"][1]["tags"]["silence_start"] 

     return f""" Audio Analysis Results:
 [P/F] Sample Rate: {sampleRate}Hz  
 [P/F] channels: {channels} 
 [P/F] Bit Depth: {bitDepth} bits 
 [P/F] Peak Limit: peakLimit
 [P/F] Silent Sections: silence
 [P/F] Loudness: loudness
     """
