# This script extracts frames from GIF files located in the "gifs" folder and saves them as PNG images in a structured manner.
# Each GIF will have its own subfolder inside the "frames" folder, named after the GIF file (without the .gif extension). 
# The frames will be saved as "frame_001.png", "frame_002.png", etc.
# It reads every .gif file inside the gifs folder, creates a dedicated subfolder for each GIF inside frames, and extracts the images.
#
# your_project_folder/
# │
# ├── your_script.py
# ├── gifs/
# │   ├── animation1.gif
# │   ├── animation2.gif
# │   └── animation3.gif
# └── frames/          <-- (The script will automatically create this if missing)

import os
import glob
from PIL import Image, ImageSequence

def extract_frames_from_folder():
    # Define input and output folders relative to where the script is run
    input_folder = "gifs"
    output_base_folder = "frames"
    
    # Check if the 'gifs' folder exists
    if not os.path.exists(input_folder):
        print(f"Error: The local folder '{input_folder}' does not exist.")
        print("Please create it and place your GIF files inside.")
        return

    # Find all .gif files in the folder (case-insensitive search)
    gif_files = glob.glob(os.path.join(input_folder, "*.[gG][iI][fF]"))
    
    if not gif_files:
        print(f"No GIF files found inside the '{input_folder}' folder.")
        return

    print(f"Found {len(gif_files)} GIF file(s). Starting extraction...\n")

    # Process each GIF found
    for gif_path in gif_files:
        # Get the file name without the extension (e.g., 'animation1')
        gif_name = os.path.splitext(os.path.basename(gif_path))[0]
        
        # Create a unique subfolder for this specific GIF's frames
        gif_output_folder = os.path.join(output_base_folder, gif_name)
        os.makedirs(gif_output_folder, exist_ok=True)
        
        print(f"Processing: {os.path.basename(gif_path)}")
        
        # Open the GIF file
        with Image.open(gif_path) as im:
            # Iterate through every frame in the GIF
            for index, frame in enumerate(ImageSequence.Iterator(im)):
                # Convert to RGBA to cleanly preserve transparency on Windows
                frame_rgba = frame.convert("RGBA")
                
                # Format file name: frame_001.png, frame_002.png, etc.
                frame_name = f"frame_{index + 1:03d}.png"
                frame_save_path = os.path.join(gif_output_folder, frame_name)
                
                # Save the frame as a high-quality PNG
                frame_rgba.save(frame_save_path, "PNG")
                
            print(f"-> Successfully saved {im.n_frames} frames to '{gif_output_folder}'\n")

    print("All tasks completed successfully!")

if __name__ == "__main__":
    extract_frames_from_folder()