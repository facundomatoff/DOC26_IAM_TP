#
# To preserve these files for later review rather than deleting them, the script can be updated to isolate them into an empty folder.
# This version creates an organized subdirectory structure under dataset/empty/ 
# (separating the images and labels to mirror your main dataset format) and uses shutil.move to instantly route empty 
# coordinate files and their matching image frames there.
#
# After running this script, any frame without bottle or can coordinate tags will automatically be relocated out of the active 
# training pool and organized into the following structure:
#
# dataset/
# ├── images/            <-- Contains only populated, train-ready PNGs
# ├── labels/            <-- Contains only populated, train-ready .txt coordinates
# └── empty/
#     ├── images/        <-- Isolated frames containing people but NO datasetd items
#     └── labels/        <-- Isolated blank .txt records for verification
#

import os
import shutil
from collections import Counter

def isolate_empty_labels_and_images():
    # Primary dataset tracks
    labels_folder = os.path.join("dataset", "labels")
    images_folder = os.path.join("dataset", "images")
    
    # Destination tracks for review
    empty_base_folder = os.path.join("dataset", "empty")
    empty_labels_dest = os.path.join(empty_base_folder, "labels")
    empty_images_dest = os.path.join(empty_base_folder, "images")
    
    CLASS_MAPPING = {
        39: "Bottle (ID 39)",
        43: "Cup / Can (ID 43)"
    }
    
    if not os.path.exists(labels_folder) or not os.path.exists(images_folder):
        print("Error: Missing 'dataset/labels' or 'dataset/images' directories.")
        return

    all_label_files = [f for f in os.listdir(labels_folder) if f.lower().endswith('.txt')]
    
    valid_images_count = 0
    empty_label_files = []
    instance_counter = Counter()
    
    print(f"Scanning {len(all_label_files)} annotation records for missing contents...\n")
    
    # Fast memory scan
    for file_name in all_label_files:
        label_path = os.path.join(labels_folder, file_name)
        
        # Kernel-level size assessment (Instant 0-byte detection)
        if os.path.getsize(label_path) == 0:
            empty_label_files.append(file_name)
            continue
            
        has_content = False
        try:
            with open(label_path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        class_id = int(parts[0])
                        instance_counter[class_id] += 1
                        has_content = True
        except (ValueError, IndexError):
            continue
            
        if not has_content:
            empty_label_files.append(file_name)
        else:
            valid_images_count += 1

    # --- Print Analysis Summary ---
    print("=" * 50)
    print("            DATASET ISOLATION REPORT            ")
    print("=" * 50)
    print(f"Valid Active Images (Ready for Training): {valid_images_count}")
    print(f"Unlabelled/Empty Frames Detected:         {len(empty_label_files)}")
    print("-" * 50)
    print("Object breakdown in active training pool:")
    
    for class_id, count in instance_counter.items():
        name = CLASS_MAPPING.get(class_id, f"Unknown ID {class_id}")
        print(f" └─ {name}: {count} objects")
    print("=" * 50)

    # --- Quarantine / Move Execution ---
    if empty_label_files:
        print(f"\n[FOUND] {len(empty_label_files)} frames with empty configurations.")
        response = input("Move these empty label text files and matching PNGs to 'dataset/empty/'? (y/n): ")
        
        if response.lower() == 'y':
            # Dynamically build destination architecture
            os.makedirs(empty_labels_dest, exist_ok=True)
            os.makedirs(empty_images_dest, exist_ok=True)
            
            moved_count = 0
            for label_name in empty_label_files:
                base_name = os.path.splitext(label_name)[0]
                img_name = f"{base_name}.png"
                
                # Source references
                src_label = os.path.join(labels_folder, label_name)
                src_image = os.path.join(images_folder, img_name)
                
                # Target destinations
                dst_label = os.path.join(empty_labels_dest, label_name)
                dst_image = os.path.join(empty_images_dest, img_name)
                
                # Safe step-wise filesystem translocation
                if os.path.exists(src_label):
                    shutil.move(src_label, dst_label)
                if os.path.exists(src_image):
                    shutil.move(src_image, dst_image)
                    moved_count += 1
                    
            print(f"\nSuccess! Transferred {moved_count} image/text file pairs out of the training stream.")
            print(f"You can review them anytime inside: '{empty_base_folder}'")
        else:
            print("\nAction deferred. Dataset left in current state.")
    else:
        print("\nClean slate! Your current image dataset contains no empty tracking files.")

if __name__ == "__main__":
    isolate_empty_labels_and_images()
    