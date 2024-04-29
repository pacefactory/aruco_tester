#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---------------------------------------------------------------------------------------------------------------------
#%% Imports

import argparse

import cv2
import numpy as np

from lib.display import DisplayWindow
from lib.video import PlaybackBar, make_video_reader
from lib.ui import SelectionBar
from lib.history import SourceHistory

from lib.aruco_detector import ArucoDetector


# ---------------------------------------------------------------------------------------------------------------------
#%% Script args

# Set script arg defaults (can change these for easier debugging/development work!)
default_video_source = None
default_display_size_px = 1000

# Define script arguments
parser = argparse.ArgumentParser(description="Script for testing ArUco detections on live video")
parser.add_argument("-i", "--video_source", default=default_video_source, type=str,
                    help="Video source (rtsp url, video file, image file or 0 for webcam")
parser.add_argument("-s", "--display_size", default=default_display_size_px, type=int,
                    help=f"Set maximum side length for displayed image (default: {default_display_size_px})")
    
# For convenience
args = parser.parse_args()
arg_video_source = args.video_source
arg_display_size = args.display_size

# Set up video source history loading/saving
history = SourceHistory()
prev_source = history.load()


# ---------------------------------------------------------------------------------------------------------------------
#%% Set up video source

# Ask user for rtsp url, if no other input was selected
video_source = arg_video_source
if video_source is None:
    print("",
          "Please enter a video source",
          "- For webcam use, enter 0 (or 1, 2, etc. if you have multiple webcams)",
          "- For a video file, enter the path to the file",
          "- You can also enter a path to an image",
          "- Or enter an rtsp url, eg. rtsp://user:password@192.168.0.100:554/profile1",
          "", "", sep = "\n", flush=True)
    
    # Provide default (if present)
    have_default = (prev_source is not None)
    if have_default: print(f"   (default): {prev_source}")
    video_source = input("Video source: ").strip()
    if video_source == "" and have_default: video_source = prev_source


# ---------------------------------------------------------------------------------------------------------------------
#%% Video Loop

# Keycodes, for clarity
KEY_UPARROW = 82
KEY_DOWNARROW = 84

# Set up detector (with default settings)
aruco_detector = ArucoDetector()

# Set up control bars
size_select_bar = SelectionBar("4x4", "5x5", "6x6", "7x7", default="4x4")
maxids_select_bar = SelectionBar("50", "100", "250", "1000", default="1000", bg_color=(30,30,30))

# Set up frame reading
video_source = video_source.replace('"', "").replace("'", "")
source_type, vread = make_video_reader(video_source)
history.save(video_source)

# Set up playback control, if needed
playback_bar = PlaybackBar(vread)
playback_bar.enable(source_type == "video")

# Set up display scaling
video_h, video_w, _ = vread.get_shape()
scaled_display_size = arg_display_size
max_video_size = max(video_h, video_w)
scale_factor = scaled_display_size / max_video_size

# Create window & attach selection bar callbacks
window = DisplayWindow("ArUco Detector - q to quit")
window.add_callbacks(size_select_bar, maxids_select_bar, playback_bar)

# Some feedback
print("",
      "Running ArUco detector!",
      "  - Press up/down arrow keys to resize the display",
      "  - Press esc or q to quit",
      sep = "\n", flush=True)
try:
    for frame in vread:
        
        display_frame = cv2.resize(frame, dsize=None, fx=scale_factor, fy=scale_factor)
        
        # Read controls
        aru_marker_size = size_select_bar.read()
        aru_max_ids = maxids_select_bar.read()
        
        # Run detector
        aruco_detector.select_detector(aru_marker_size, aru_max_ids)
        aru_results = aruco_detector.process_frame(display_frame)
        display_frame = aruco_detector.draw_results(aru_results, display_frame)
        
        # Display image with controls
        display_frame = size_select_bar.append_to_frame(display_frame)
        display_frame = maxids_select_bar.append_to_frame(display_frame)
        display_frame = playback_bar.append_to_frame(display_frame)
        req_close, keypress = window.imshow(display_frame)
        if req_close:
            break
        
        # Change display size on keypress
        if keypress == KEY_UPARROW:
            scaled_display_size = min(4000, scaled_display_size + 50)
            scale_factor = scaled_display_size / max_video_size
        if keypress == KEY_DOWNARROW:
            scaled_display_size = max(100, scaled_display_size - 50)
            scale_factor = scaled_display_size / max_video_size
        
        # Control playback of video files
        playback_bar.adjust_playback_on_drag()

except KeyboardInterrupt:
    print("Cancelled by Ctrl+C")

finally:
    # Clean up
    vread.release()
    cv2.destroyAllWindows()
