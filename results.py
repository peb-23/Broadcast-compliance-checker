import json
with open("ofcom.json", "r") as file: # Load Ofcom compliance standards from JSON file
    ofcom = json.load(file)

def status(result): #function to return pass or fail based on boolean result
    return "PASS" if result else "FAIL"

# VIDEO CHECKS
def check_resolution(actual): # Compare detected resolution against Ofcom requirements
    return actual == ofcom["video"]["resolution"]

def check_frame_rate(actual): # Compare detected frame rate against Ofcom requirements
    return actual == ofcom["video"]["frame_rate"]

def check_aspect_ratio(actual): # Compare detected aspect ratio against Ofcom requirements
    return actual == ofcom["video"]["aspect_ratio"]

def check_codec(actual): # Compare detected codec against Ofcom requirements
    return actual == ofcom["video"]["codec"]

def check_black_frames(found): # gives pass if no black frames are detected
    return not found

def check_frozen_frames(found): # gives pass if no frozen frames are detected
    return not found

def all_video_results(video_data, extra_data): # presents the video results with a pass/fail and formatted for the GUI
    return f"""Duration: {video_data["duration"]} sec
[{status(check_resolution(video_data["resolution"]))}] Resolution: {video_data["resolution"]}
[{status(check_frame_rate(video_data["frame_rate"]))}] Frame Rate: {video_data["frame_rate"]}
[{status(check_aspect_ratio(video_data["aspect_ratio"]))}] Aspect Ratio: {video_data["aspect_ratio"]}
[{status(check_codec(video_data["codec"]))}] Codec: {video_data["codec"]}
[{status(check_black_frames(extra_data["black_frames"]))}] Black Frames
[{status(check_frozen_frames(extra_data["frozen_frames"]))}] Frozen Frames
"""

# AUDIO CHECKS
def check_sample_rate(actual): # Compare detected sample rate against Ofcom requirements
    return str(actual) == ofcom["audio"]["sample_rate"]

def check_bit_depth(actual): # Compare detected bit depth against Ofcom requirements
    if actual == "Unknown":
        return False
    if actual == "Not Available-AAC":  # AAC files do not provide reliable bit-depth information
        return True
    return str(actual) == ofcom["audio"]["bit_depth"]

def check_channels(actual): # Compare detected audio channels against Ofcom requirements
    if str(actual) == "2":
        actual = "stereo"   # returns stereo instead of 2 as its clearer to read
    return actual.lower() == ofcom["audio"]["channels"].lower()

def check_loudness(actual): # Check if measured loudness is within acceptable tolerance of Ofcom standards 
    if actual == "Unknown":
        return False 
    target = ofcom["audio"]["loudness"]
    return abs(float(actual) - float(target)) <= 1.0

def check_true_peak(actual): # Checks if true peak level exceeds Ofcom limit
    if actual == "Unknown":
        return False
    limit = ofcom["audio"]["true_peak_limit"]
    return float(actual) <= float(limit)

def check_silence(found): # gives pass if no silence sections were detected
    return not found

def all_audio_results(audio_data):# presents the audio results with a pass/fail and formatted for the GUI
    if not audio_data["has_audio"]:

        return "Video contains no audio track." # If video doesnt have audio return this message 
    channels = audio_data["channels"]

    if str(channels) == "2": # returns data if video has audio 
        channels = "Stereo"
    return f"""[{status(check_sample_rate(audio_data["sample_rate"]))}] Sample Rate: {audio_data["sample_rate"]}
[{status(check_channels(audio_data["channels"]))}] Channels: {channels}
[{status(check_bit_depth(audio_data["bit_depth"]))}] Bit Depth: {audio_data["bit_depth"]}
[{status(check_loudness(audio_data["loudness"]))}] Loudness: {audio_data["loudness"]} LUFS
[{status(check_true_peak(audio_data["true_peak"]))}] True Peak: {audio_data["true_peak"]} dBTP
[{status(check_silence(audio_data["silence_detected"]))}] Silence Detection
"""

def run_ofcom_check( # Calculates overall compliance score using all completed checks
        video_data, audio_data, extra_data):
    
    if audio_data["has_audio"]:  # Includes audio checks only when an audio is present
        checks = [
            check_resolution(video_data["resolution"]),
            check_frame_rate(video_data["frame_rate"]),
            check_aspect_ratio(video_data["aspect_ratio"]),
            check_codec(video_data["codec"]),
            check_black_frames(extra_data["black_frames"]),
            check_frozen_frames(extra_data["frozen_frames"]),
            check_sample_rate(audio_data["sample_rate"]),
            check_bit_depth(audio_data["bit_depth"]),
            check_channels(audio_data["channels"]), 
            check_loudness(audio_data["loudness"]),
            check_true_peak(audio_data["true_peak"]),
            check_silence(audio_data["silence_detected"]) ]
    else:
        checks = [ # excludes audio checks if no audio is there
            check_resolution(video_data["resolution"]),
            check_frame_rate(video_data["frame_rate"]),
            check_aspect_ratio(video_data["aspect_ratio"]),
            check_codec(video_data["codec"]),
            check_black_frames(extra_data["black_frames"]),
            check_frozen_frames(extra_data["frozen_frames"]) ]

    passed = sum(checks)   # Calculate compliance statistics
    total = len(checks)
    score = round((passed / total) * 100)

    if score >= 90:   # Determine overall compliance status
        overall = "PASS"
    elif score >= 70:
        overall = "WARNING"
    else:
        overall = "FAIL"

    return { # Return results to the GUI and graphing functions
    "overall": overall,
    "score": score,
    "passed": passed,
    "failed": total - passed,
    "total": total }