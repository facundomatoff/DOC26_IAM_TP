# Instance vs Image Count: This script cleanly extracts two different metrics you need: 
# * Total images found (the length of the file list) and the 
# * sub-quantities of every specific object inside those images (since one single image frame might contain three bottles and two cans).

import os
from collections import Counter

def high_performance_analysis():
    # Path to your local YOLO configurations folder
    labels_folder = os.path.join("dataset", "labels")
    
    # Map the original COCO indices to human-readable names
    CLASS_MAPPING = {
        39: "Bottle (Standard COCO ID 39)",
        43: "Cup / Can (Standard COCO ID 43)"
    }
    
    if not os.path.exists(labels_folder):
        print(f"Error: The target folder '{labels_folder}' does not exist.")
        print("Please run your dataset generator script first.")
        return

    # Fetch all label files in the directory
    label_files = [f for f in os.listdir(labels_folder) if f.lower().endswith('.txt')]
    total_images_recognized = len(label_files)
    
    # Initialize high-performance counter for internal bounding box instances
    instance_counter = Counter()
    
    print(f"Analyzing {total_images_recognized} annotation files...\n")
    
    # Fast loop over files (runs completely in memory cache)
    for file_name in label_files:
        file_path = os.path.join(labels_folder, file_name)
        
        try:
            with open(file_path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        # Extract the first integer (The Class ID)
                        class_id = int(parts[0])
                        instance_counter[class_id] += 1
        except (ValueError, IndexError):
            # Gracefully ignore corrupted lines or empty trailing lines
            continue

    # --- Print Structured Performance Metrics ---
    print("=" * 45)
    print("          DATASET ANALYSIS REPORT          ")
    print("=" * 45)
    print(f"Total Unique Images Recognized: {total_images_recognized}")
    print("-" * 45)
    print("Total Individual Objects Detected Across All Frames:")
    
    total_objects = sum(instance_counter.values())
    
    for class_id, count in instance_counter.items():
        # Resolve class names dynamically
        readable_name = CLASS_MAPPING.get(class_id, f"Unknown Class ID {class_id}")
        percentage = (count / total_objects * 100) if total_objects > 0 else 0
        print(f" └─ {readable_name}: {count} instances ({percentage:.1f}%)")
        
    print("=" * 45)

if __name__ == "__main__":
    high_performance_analysis()
