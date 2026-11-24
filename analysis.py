import subprocess
import json 
import tkinter as tk
from tkinter import ttk
import os
from math import gcd

#ffprodbe path for the analysis function to use
ffprobe = r"C:\Users\phillg03\BBC Dropbox\Georgina Phillips\UNI\Year 2.1\Programming\BCUTestData\ffmpeg-9.0.2-full_build\bin\ffprobe.exe"
# ffmpeg path for the analysis function to use
ffmpeg = r"C:\Users\phillg03\BBC Dropbox\Georgina Phillips\UNI\Year 2.1\Programming\BCUTestData\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"

def run_analysis_videoExtra(video_path):
     fSelection = video_path

     command = [
          ffmpeg,
          "-i", fSelection,
          "-vf", "blackdetect=d=1:pix_th=0.10,freezedetect=n=-60dB:d=2",
          "-f", "null",
          "-"]

     result = subprocess.run(
          command,
          capture_output=True,
          text=True)

     output = result.stderr
     blackFrame = "Pass - No  Black Frames"
     frozenFrame = "Pass - No Frozen Frames"

     if "black_start" in output:
          blackFrame = "Fail - Black frames detected"

     if "freeze_start" in output:
          frozenFrame = "Fail - Frozen frames detected"

     return {
        "black_frames": "black_start" in output,
        "frozen_frames": "freeze_start" in output
    }

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
     aspectRatio = f"{width // gcd(width, height)}:{height // gcd(width, height)}"
     codec = metadata["streams"][0]["codec_name"]
    
     return {
        "duration": duration,
        "resolution": resolution,
        "frame_rate": frameRate,
        "aspect_ratio": aspectRatio,
        "codec": codec
    }


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
     return {
    "sample_rate": sampleRate,
    "channels": channels,
    "bit_depth": bitDepth
}

#     return f"""[P/F] Sample Rate: {sampleRate}Hz  
# [P/F] channels: {channels} 
 #[P/F] Bit Depth: {bitDepth} bits 
 #[P/F] Peak Limit: 
 #[P/F] Silent Sections:
 #[P/F] Loudness: 
 #    """
