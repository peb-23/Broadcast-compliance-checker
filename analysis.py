import subprocess        # run ffmpeg & ffprode commands
import json              # read metadata
from math import gcd     # import math to calc ascept ratio from resolution values 
import re                # regular expression - easier to search ffmpeg 

#ffprodbe path for the analysis function to use
ffprobe = r"C:\Users\phillg03\BBC Dropbox\Georgina Phillips\UNI\Year 2.1\Programming\BCUTestData\ffmpeg-9.0.2-full_build\bin\ffprobe.exe"
# ffmpeg path for the analysis function to use
ffmpeg = r"C:\Users\phillg03\BBC Dropbox\Georgina Phillips\UNI\Year 2.1\Programming\BCUTestData\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"

def run_analysis_videoExtra(video_path): # function anaylses the chosens video for black and frozen frames using ffmpeg
     fSelection = video_path

     command = [
          ffmpeg,
          "-i", fSelection,
          "-vf", "blackdetect=d=1:pix_th=0.10,freezedetect=n=-60dB:d=2",
          "-f", "null",
          "-"]

     result = subprocess.run(command, capture_output=True, text=True) # stores output for anaysis
     output = result.stderr 

     return {
        "black_frames": "black_start" in output,
        "frozen_frames": "freeze_start" in output} #returns if issues were detected or not 

def run_analysis_video(video_path):  # function anaylses the chosen videos video metadata using ffprobe 
     fSelection = video_path

     command = [ #ffprobe command to extract video metadata
     ffprobe,
     "-v", "quiet",
     "-print_format", "json",
     "-show_format",
     "-show_streams",
     fSelection ]
    
     result = subprocess.run(command, capture_output=True,text=True) # stores ffprobe output and converts json data into a dictonary 
     metadata = json.loads(result.stdout)

     duration = round(float(metadata["format"]["duration"]), 2)  # extracts and calulates video properties from metadata
     width = metadata["streams"][0]["width"]
     height = metadata["streams"][0]["height"]
     resolution = f"{width}x{height}"
     frameRate = metadata["streams"][0]["avg_frame_rate"]
     aspectRatio = f"{width // gcd(width, height)}:{height // gcd(width, height)}"
     codec = metadata["streams"][0]["codec_name"]
    
     return {                 # returns the video properties 
        "duration": duration,
        "resolution": resolution,
        "frame_rate": frameRate,
        "aspect_ratio": aspectRatio,
        "codec": codec }

def run_analysis_audio(video_path):  #function anaylses the chosens videos audio metadata using ffprobe 
     fSelection = video_path

     command = [ #ffprobe command to extract audio metadata
     ffprobe,
     "-v", "quiet",
     "-print_format", "json",
     "-show_format",
     "-show_streams",
     fSelection ]

     result = subprocess.run(command, capture_output=True,text=True) # stores ffprobe output and converts json data into a dictonary
     metadata = json.loads(result.stdout)

     audio_stream = next((  # finds the first available audio stream in the file 
        stream
        for stream in metadata["streams"]
        if stream["codec_type"] == "audio"),None)
     
     if audio_stream is None:  #if there is no audio, return boolean 
          return {
               "has_audio": False }

     sampleRate = audio_stream["sample_rate"]   #extracts audio properties 
     channels = audio_stream["channels"]
     bitDepth = audio_stream.get("bits_per_raw_sample")
     if not bitDepth:
          bitDepth = audio_stream.get("bits_per_sample")

     codecName = audio_stream["codec_name"]
     if codecName == "aac":
          bitDepth = "Not Available-AAC"  # AAC audio does not report a reliable bit depth
     elif not bitDepth or bitDepth == 0:
          bitDepth = "Unknown"

     loudnessCommand = [ #  measure loudness/true peak values using ffmpeg loudnorm filter
       ffmpeg,
       "-i", fSelection,
       "-af", "loudnorm=print_format=json",
       "-f", "null",
        "-" ]
     
     loudnessResult = subprocess.run(loudnessCommand, capture_output=True,text=True ) #stored loudness output
     loudnessOutput = loudnessResult.stderr
     loudness = "Unknown" #creates values used if loudness cannot be extracted
     truePeak = "Unknown"

     match = re.search(r"\{[\s\S]*?output_tp[\s\S]*?\}",loudnessOutput) # Search FFmpeg output for loudness stats

     if match:
          loudnessData = json.loads(
               match.group())
          loudness = loudnessData["input_i"] #updates variables 
          truePeak = loudnessData["input_tp"]

     silenceCommand = [ # ffmpeg command to detect silences longer than 2 seconds
      ffmpeg,
      "-i", fSelection,
      "-af", "silencedetect=n=-50dB:d=2",
      "-f", "null",
      "-" ]

     silenceResult = subprocess.run(silenceCommand, capture_output=True,text=True )
     silenceDetected =  False
     if "silence_start" in silenceResult.stderr: #checks and stores if any siilences were detected 
          silenceDetected = True

     return {                  # Returns all the extracted audio analysis results
    "has_audio": True,
    "sample_rate": sampleRate,
    "channels": channels,
    "bit_depth": bitDepth,
    "loudness": loudness,
    "true_peak": truePeak,
    "silence_detected": silenceDetected }