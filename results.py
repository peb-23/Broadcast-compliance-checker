import json
with open("ofcom.json", "r") as file:
    ofcom = json.load(file)

def status(result): #function to return pass or fail based on boolean result
    return "PASS" if result else "FAIL"

# VIDEO CHECKS
def check_resolution(actual):
    return actual == ofcom["video"]["resolution"]

def check_frame_rate(actual):
    return actual == ofcom["video"]["frame_rate"]

def check_aspect_ratio(actual):
    return actual == ofcom["video"]["aspect_ratio"]

def check_codec(actual):
    return actual == ofcom["video"]["codec"]

def check_black_frames(found):
    return not found

def check_frozen_frames(found):
    return not found

def all_video_results(video_data, extra_data):
    return f"""Duration: {video_data["duration"]} sec
[{status(check_resolution(video_data["resolution"]))}] Resolution: {video_data["resolution"]}
[{status(check_frame_rate(video_data["frame_rate"]))}] Frame Rate: {video_data["frame_rate"]}
[{status(check_aspect_ratio(video_data["aspect_ratio"]))}] Aspect Ratio: {video_data["aspect_ratio"]}
[{status(check_codec(video_data["codec"]))}] Codec: {video_data["codec"]}
[{status(check_black_frames(extra_data["black_frames"]))}] Black Frames
[{status(check_frozen_frames(extra_data["frozen_frames"]))}] Frozen Frames
"""

# AUDIO CHECKS
def check_sample_rate(actual):
    return str(actual) == ofcom["audio"]["sample_rate"]

def check_bit_depth(actual):
    if actual == "Unknown":
        return False
    return str(actual) == ofcom["audio"]["bit_depth"]

def check_channels(actual):
    if str(actual) == "2":
        actual = "stereo"
    return actual.lower() == ofcom["audio"]["channels"].lower()

def check_loudness(actual):
    if actual == "Unknown":
        return False 
    target = ofcom["audio"]["loudness"]
    return abs(float(actual) - float(target)) <= 1.0

def check_true_peak(actual):
    if actual == "Unknown":
        return False
    limit = ofcom["audio"]["true_peak_limit"]
    return float(actual) <= float(limit)

def check_silence(found):
    return not found

def all_audio_results(audio_data):
    if not audio_data["has_audio"]:
        return "Video contains no audio track."
    channels = audio_data["channels"]

    if str(channels) == "2":
        channels = "Stereo"

    return f"""[{status(check_sample_rate(audio_data["sample_rate"]))}] Sample Rate: {audio_data["sample_rate"]}
[{status(check_channels(audio_data["channels"]))}] Channels: {channels}
[{status(check_bit_depth(audio_data["bit_depth"]))}] Bit Depth: {audio_data["bit_depth"]}
[{status(check_loudness(audio_data["loudness"]))}] Loudness: {audio_data["loudness"]} LUFS
[{status(check_true_peak(audio_data["true_peak"]))}] True Peak: {audio_data["true_peak"]} dBTP
[{status(check_silence(audio_data["silence_detected"]))}] Silence Detection
"""

def run_ofcom_check(
        video_data,
        audio_data,
        extra_data):
    if audio_data["has_audio"]:
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

        checks = [
            check_resolution(video_data["resolution"]),
            check_frame_rate(video_data["frame_rate"]),
            check_aspect_ratio(video_data["aspect_ratio"]),
            check_codec(video_data["codec"]),
            check_black_frames(extra_data["black_frames"]),
            check_frozen_frames(extra_data["frozen_frames"])
        ]

    passed = sum(checks)
    total = len(checks)
    score = round((passed / total) * 100)

    if score >= 90:
        overall = "PASS"
    elif score >= 70:
        overall = "WARNING"
    else:
        overall = "FAIL"

    return f"""Overall Compliance Status: {overall}
Compliance Score: {score}%
Checks Passed: {passed}/{total}
"""