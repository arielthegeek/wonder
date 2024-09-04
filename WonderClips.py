import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp
import requests
import numpy as np
from PIL import Image
import os

# Monkey-patch PIL.Image in moviepy's resize fx
from moviepy.video.fx import resize

resize.resizer = lambda pic, newsize: np.array(Image.fromarray(pic.astype('uint8')).resize(tuple(map(int, newsize[::-1])), Image.LANCZOS))

# Define the current version
CURRENT_VERSION_BASIC = "v1.0.0"
CURRENT_VERSION_PRO = "v1.0.0"

def check_for_updates():
    try:
        response = requests.get("https://arielthegeek.github.io/wonder/wonder.json")
        response.raise_for_status()
        version_data = response.json()

        latest_version_basic = version_data[0]["basic"]
        latest_version_pro = version_data[0]["pro"]

        if CURRENT_VERSION_BASIC != latest_version_basic:
            alert_new_version("Basic")
        elif CURRENT_VERSION_PRO != latest_version_pro:
            alert_new_version("Pro")

    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")

def alert_new_version(edition):
    print(f"A new version of {edition} Edition is available. Please download it from https://arielthegeek.github.io/wonder.")

def generate_peppers_ghost(input_video_path, output_video_path):
    try:
        # Load the original video
        clip = mp.VideoFileClip(input_video_path)

        # Resize and create the orientations needed for Pepper's Ghost effect
        video_resized = clip.resize(0.5)
        
        # Create different orientations
        video_top = video_resized
        video_bottom = video_resized.fx(mp.vfx.mirror_y)
        video_left = video_resized.rotate(90)
        video_right = video_resized.rotate(-90)

        # Create a final composite layout
        width, height = video_resized.size
        final_width = width * 2
        final_height = height * 2

        # Position the videos in the correct cross layout (not 2x2 grid)
        final_video = mp.CompositeVideoClip([
            video_top.set_position((width // 2, 0)),      # Top
            video_bottom.set_position((width // 2, height)),  # Bottom
            video_left.set_position((0, height // 2)),    # Left
            video_right.set_position((width, height // 2)) # Right
        ], size=(final_width, final_height))

        # Write the final output to a file
        final_video.write_videofile(output_video_path, codec='libx264')
        print(f"Pepper's Ghost video created successfully: {output_video_path}")

    except Exception as e:
        print(f"Error processing video: {e}")

def select_file(prompt, save=False):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    if save:
        file_path = filedialog.asksaveasfilename(title=prompt, defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    else:
        file_path = filedialog.askopenfilename(title=prompt, filetypes=[("Video Files", "*.mp4 *.mov *.avi")])
    
    root.destroy()  # Destroy the root window
    return file_path

if __name__ == "__main__":
    # Check for updates
    check_for_updates()

    # Prompt for input and output file paths using file dialogs
    input_video_path = select_file("Select the input video file:")
    
    if not input_video_path:
        print("Error: No input video file selected.")
        exit(1)

    output_video_path = select_file("Select the output video file location:", save=True)
    
    if not output_video_path:
        print("Error: No output file location selected.")
        exit(1)

    generate_peppers_ghost(input_video_path, output_video_path)