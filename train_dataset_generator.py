#
# To adjust your dataset generation strategy, this updated script isolation logic checks for only bottles or cups/cans, 
# regardless of whether human hands or other background noise overlap them. 
# The script leverages Ultralytics YOLO engine configurations to auto-generate standardized .txt bounding box annotation files. 
# These labels use normalized configurations (class_id center_x center_y width height) so you can feed them directly back into 
# custom dataset pipelines later to train a new model variant (e.g., teaching it to distinguish Coke from water).
#
# The script copies matching frames into an organized layout inside the dataset folder. 
# Both the image file and its text coordinate configuration asset share matching file names inside paired directories:
#
# your_project_folder/
# │
# ├── train_dataset_generator.py
# ├── frames/ (your current frames data)
# └── dataset/
#     ├── images/      <-- (Matching frame PNGs are copied here)
#     └── labels/      <-- (Matching YOLO .txt configurations are saved here)
#


import os
import shutil
from ultralytics import YOLO

def generate_custom_training_dataset():
    # Define folder structures matching official YOLO training formats
    source_folder = "frames"
    dest_images_folder = os.path.join("dataset", "images")
    dest_labels_folder = os.path.join("dataset", "labels")
    
    # Target COCO dataset indices for standard YOLO models
    # Class ID 39: bottle, Class ID 43: cup (frequently maps to cans/glasses)
    TARGET_CONTAINERS = {39, 43}
    
    if not os.path.exists(source_folder):
        print(f"Error: The source folder '{source_folder}' does not exist.")
        return
        
    # Build out directory trees
    os.makedirs(dest_images_folder, exist_ok=True)
    os.makedirs(dest_labels_folder, exist_ok=True)

    # Load pre-trained model (Using YOLOv8m for balanced accuracy and speed)
    print("Loading YOLOv8 object detector...")
    model = YOLO("yolov8m.pt") 
    
    # Gather image assets recursively
    valid_extensions = (".png", ".jpg", ".jpeg")
    images_to_process = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(valid_extensions):
                images_to_process.append(os.path.join(root, file))
                
    if not images_to_process:
        print("No image frames detected to filter.")
        return
        
    print(f"Scanning {len(images_to_process)} images for bottles or cans...\n")
    matched_count = 0

    for img_path in images_to_process:
        # Run inference using a 35% confidence limit to maximize capture rate
        results = model(img_path, verbose=False, conf=0.35)[0]
        
        # Parse all detected bounding box records 
        boxes = results.boxes
        if len(boxes) == 0:
            continue
            
        detected_classes = boxes.cls.int().tolist()
        
        # Evaluate if the frame contains at least one bottle (39) or can/cup (43)
        contains_target = any(cls in TARGET_CONTAINERS for cls in detected_classes)
        
        if contains_target:
            # Generate uncollided descriptive names via subfolders
            parent_subfolder = os.path.basename(os.path.dirname(img_path))
            file_base_name = os.path.splitext(os.path.basename(img_path))[0]
            unique_prefix = f"{parent_subfolder}_{file_base_name}"
            
            # Form destination paths
            img_dest_path = os.path.join(dest_images_folder, f"{unique_prefix}.png")
            label_dest_path = os.path.join(dest_labels_folder, f"{unique_prefix}.txt")
            
            # Copy original frame to training image pool
            shutil.copy(img_path, img_dest_path)
            
            # Generate the YOLO custom annotation training configuration txt file
            # Format requirement: [class_id x_center y_center width height] normalized 0 to 1
            with open(label_dest_path, "w") as label_file:
                for box in boxes:
                    cls_id = int(box.cls[0])
                    
                    # Log only targets (ignore people/hands bounding vectors)
                    if cls_id in TARGET_CONTAINERS:
                        # Fetch coordinates normalized by image size automatically via .xywhn
                        xywhn = box.xywhn[0].tolist()
                        x_center, y_center, width, height = xywhn
                        
                        # NOTE: For your custom model downstream training:
                        # You can later open these .txt records and re-index '39' or '43' 
                        # into finer sub-classes like 0=Water, 1=Coke, 2=Can via labeling tools.
                        line = f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
                        label_file.write(line)
            
            matched_count += 1
            print(f"[EXTRACTED] Target container found in: {parent_subfolder}/{file_base_name}")

    print(f"\nCompleted! Generated {matched_count} images & coordinate text files inside 'dataset/'.")

if __name__ == "__main__":
    generate_custom_training_dataset()

