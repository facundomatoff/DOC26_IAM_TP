#
# To run this task on Windows using Visual Studio Code, you will use the official Ultralytics YOLO library.
# The script will use the pre-trained YOLOv8x (extra-large) or YOLOv8m model. 
# Since standard YOLO models detect general classes like person (ID 0) and bottle (ID 39), 
# the script scans each frame to ensure both a person and a beverage container are present in the same image before moving it.
#
# your_project_folder/
# │
# ├── identify_bottles.py   <-- (The new script)
# ├── frames/
# │   ├── animation1/
# │   │   ├── frame_001.png
# │   │   └── frame_002.png
# │   └── animation2/
# │       ├── frame_001.png
# │       └── frame_002.png
# └── dataset/            <-- (Matching images will be moved here)
#
# Critical Script Notes
# * Action Type (shutil.copy): This script copies the files instead of moving (shutil.move) them. 
#   This ensures your original frames directory structure is safe if you want to re-run your logic or tweak thresholds.
# * Preventing File Overwrites: Because multiple subfolders might contain files named frame_001.png, 
#   the script flattens the names in the destination folder to subfoldername_framename.png (e.g., animation1_frame_001.png).
# * Class Mapping: Pre-trained object detection models like YOLO do not natively differentiate between "Coke" and "Water"—
#   they classify both broadly as a bottle or a cup (which captures cans). This rule ensures that a human and a container 
#   must coexist in the image to trigger a match.

import os
import shutil
from ultralytics import YOLO

def filter_beverage_images():
    # Define folder paths
    source_folder = "frames"
    destination_folder = "dataset"
    
    # Target COCO dataset class IDs for YOLO
    # 0: person, 39: bottle, 43: cup (often detects cans/cups/glasses)
    TARGET_CLASSES = {0, 39, 43}
    
    if not os.path.exists(source_folder):
        print(f"Error: The source folder '{source_folder}' does not exist.")
        return
        
    os.makedirs(destination_folder, exist_ok=True)

    # Load pre-trained YOLOv8 medium model (auto-downloads on first run)
    print("Loading YOLOv8 model...")
    model = YOLO("yolov8m.pt") 
    
    print("Scanning folders for frames...")
    
    # Recursively find all images in 'frames' and its subfolders
    valid_extensions = (".png", ".jpg", ".jpeg")
    images_to_process = []
    
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(valid_extensions):
                images_to_process.append(os.path.join(root, file))
                
    if not images_to_process:
        print("No image files found in the 'frames' directory.")
        return
        
    print(f"Found {len(images_to_process)} images. Starting detection...\n")
    matched_count = 0

    # Iterate through each image frame
    for img_path in images_to_process:
        # Run YOLO inference with a confidence threshold of 40%
        results = model(img_path, verbose=False, conf=0.40)
        
        # Extract detected class IDs from the first result object
        detected_classes = set(results[0].boxes.cls.int().tolist())
        
        # Check if a person AND at least one beverage container (bottle/cup) is present
        has_person = 0 in detected_classes
        has_beverage = (39 in detected_classes) or (43 in detected_classes)
        
        if has_person and has_beverage:
            # Generate a clean destination filename to prevent overwriting files with the same name
            parent_subfolder = os.path.basename(os.path.dirname(img_path))
            file_name = os.path.basename(img_path)
            new_file_name = f"{parent_subfolder}_{file_name}"
            dest_path = os.path.join(destination_folder, new_file_name)
            
            # Copy file to the 'dataset' folder (using copy so your original frame remains intact)
            shutil.copy(img_path, dest_path)
            matched_count += 1
            print(f"[MATCH] Person with beverage found in: {parent_subfolder}/{file_name} -> Moved to 'dataset/'")

    print(f"\nProcessing finished! Successfully found and moved {matched_count} matching frames.")

if __name__ == "__main__":
    filter_beverage_images()